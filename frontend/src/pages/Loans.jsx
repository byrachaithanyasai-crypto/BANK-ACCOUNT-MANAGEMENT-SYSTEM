import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Plus, X, CheckCircle, UserPlus } from 'lucide-react';
import DataTable from '../components/DataTable';
import api from '../services/api';

export default function Loans() {
    const { user } = useContext(AuthContext);
    const [data, setData] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isAssignModalOpen, setIsAssignModalOpen] = useState(false);
    
    const [editingRecord, setEditingRecord] = useState(null);
    const [assigningRecord, setAssigningRecord] = useState(null);
    
    const [formData, setFormData] = useState({ 
        customer_id: '', branch_id: 1, loan_type: 'PERSONAL', principal_amount: '', interest_rate: '', term_months: '', start_date: '', outstanding_balance: '', status: 'PENDING', loan_officer_id: ''
    });
    const [formLoading, setFormLoading] = useState(false);

    const fetchData = async () => {
        try {
            const [resLoans, resCust] = await Promise.all([
                api.get('/api/loans'),
                api.get('/api/customers')
            ]);
            setData(resLoans.data);
            setCustomers(resCust.data);
            if (["ADMIN", "MANAGER"].includes(user?.role)) {
                const resEmp = await api.get('/api/employees');
                setEmployees(resEmp.data);
            }
        } catch (err) { console.error(err); }
        finally { setLoading(false); }
    };
    useEffect(() => { fetchData(); }, [user?.role]);

    const handleDelete = async (row) => {
        if(window.confirm('Delete loan?')) {
            try { 
                await api.delete('/api/loans/' + row.loan_id); 
                fetchData(); 
            }
            catch (err) { alert(err.response?.data?.detail || 'Failed to delete loan.'); }
        }
    };

    const handleApprove = async (row) => {
        if(window.confirm('Approve this loan?')) {
            try { 
                await api.put('/api/loans/' + row.loan_id, { status: 'ACTIVE' }); 
                fetchData(); 
            }
            catch (err) { alert(err.response?.data?.detail || 'Failed to approve loan.'); }
        }
    };

    const handleEdit = (row) => {
        setEditingRecord(row);
        setFormData({ 
            customer_id: row.customer_id, branch_id: row.branch_id, loan_type: row.loan_type,
            principal_amount: row.principal_amount, interest_rate: row.interest_rate, 
            term_months: row.term_months, start_date: row.start_date, outstanding_balance: row.outstanding_balance,
            status: row.status, loan_officer_id: row.loan_officer_id || ''
        });
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingRecord(null);
        setFormData({ 
            customer_id: customers.length > 0 ? customers[0].customer_id : '', branch_id: 1, loan_type: 'PERSONAL',
            principal_amount: '', interest_rate: '', term_months: '', start_date: new Date().toISOString().split('T')[0], 
            outstanding_balance: '', status: 'PENDING', loan_officer_id: ''
        });
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault(); setFormLoading(true);
        try {
            const payload = { ...formData };
            if (!payload.loan_officer_id) payload.loan_officer_id = null;
            if (editingRecord) await api.put('/api/loans/' + editingRecord.loan_id, payload);
            else await api.post('/api/loans/', payload);
            setIsModalOpen(false); fetchData();
        } catch (err) { alert(err.response?.data?.detail || 'Error saving loan'); }
        finally { setFormLoading(false); }
    };
    
    const handleAssignSubmit = async (e) => {
        e.preventDefault(); setFormLoading(true);
        try {
            const payload = { loan_officer_id: formData.loan_officer_id || null };
            await api.put('/api/loans/' + assigningRecord.loan_id, payload);
            setIsAssignModalOpen(false); fetchData();
        } catch (err) { alert(err.response?.data?.detail || 'Error assigning loan officer'); }
        finally { setFormLoading(false); }
    };

    const canEdit = ["ADMIN", "MANAGER"].includes(user?.role);
    const canDelete = user?.role === "ADMIN";
    const canCreate = ["ADMIN", "MANAGER"].includes(user?.role);
    const canApprove = ["ADMIN", "MANAGER"].includes(user?.role);
    const canAssign = ["ADMIN", "MANAGER"].includes(user?.role);

    const columns = [
        { header: "Loan ID", accessor: "loan_id" },
        { header: "Customer", accessor: "customer_id", render: (row) => {
            const c = customers.find(c => c.customer_id === row.customer_id);
            return c ? c.first_name + ' ' + c.last_name : row.customer_id;
        }},
        { header: "Type", accessor: "loan_type", render: (row) => <span className="font-semibold text-slate-700">{row.loan_type}</span> },
        { header: "Amount", accessor: "principal_amount", render: (row) => '$' + parseFloat(row.principal_amount).toFixed(2) },
        { header: "Balance", accessor: "outstanding_balance", render: (row) => '$' + parseFloat(row.outstanding_balance).toFixed(2) },
        { header: "EMI (approx)", accessor: "emi", render: (row) => {
            const P = parseFloat(row.principal_amount);
            const R = parseFloat(row.interest_rate) / 12 / 100;
            const N = parseInt(row.term_months);
            if (R === 0) return '$' + (P / N).toFixed(2);
            const emi = P * R * Math.pow(1+R, N) / (Math.pow(1+R, N) - 1);
            return '$' + emi.toFixed(2);
        }},
        { header: "Status", accessor: "status", render: (row) => (
            <span className={'px-2 py-1 rounded-full text-xs font-semibold ' + (row.status === 'ACTIVE' ? 'bg-emerald-100 text-emerald-700' : row.status === 'PENDING' ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-700')}>
                {row.status}
            </span>
        )}
    ];

    if (canEdit || canDelete || canApprove || canAssign) {
        columns.push({
            header: "Actions",
            accessor: "actions",
            render: (row) => (
                <div className="flex items-center gap-3">
                    {canEdit && <button onClick={() => handleEdit(row)} className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>}
                    {canDelete && <button onClick={() => handleDelete(row)} className="text-red-600 hover:text-red-800 font-medium">Delete</button>}
                    {canApprove && row.status === 'PENDING' && <button onClick={() => handleApprove(row)} className="text-emerald-600 hover:text-emerald-800 font-medium flex items-center gap-1"><CheckCircle size={14}/> Approve</button>}
                    {canAssign && <button onClick={() => { setAssigningRecord(row); setFormData({...formData, loan_officer_id: row.loan_officer_id || ''}); setIsAssignModalOpen(true); }} className="text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1"><UserPlus size={14}/> Assign</button>}
                </div>
            )
        });
    }

    const filteredData = data.filter(row => Object.values(row).some(val => String(val).toLowerCase().includes(searchQuery.toLowerCase())));

    return (
                <div className="h-full relative flex flex-col space-y-6 pb-6">
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 mb-2">
                <h1 className="text-2xl font-bold text-slate-900 mb-1">Loans</h1>
                <p className="text-slate-500 mb-6">Manage loan applications, approvals, repayment information and loan officers.</p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Loans</p>
                        <h3 className="text-2xl font-bold text-slate-900 mt-1">{data.length}</h3>
                    </div>
                    <div className="bg-emerald-50 p-4 rounded-xl border border-emerald-100">
                        <p className="text-xs font-semibold text-emerald-600 uppercase tracking-wider">Active Loans</p>
                        <h3 className="text-2xl font-bold text-emerald-700 mt-1">{data.filter(d => d.status === 'ACTIVE').length}</h3>
                    </div>
                    <div className="bg-amber-50 p-4 rounded-xl border border-amber-100">
                        <p className="text-xs font-semibold text-amber-600 uppercase tracking-wider">Pending Loans</p>
                        <h3 className="text-2xl font-bold text-amber-700 mt-1">{data.filter(d => d.status === 'PENDING').length}</h3>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-xl border border-blue-100">
                        <p className="text-xs font-semibold text-blue-600 uppercase tracking-wider">Total Loan Amount</p>
                        <h3 className="text-2xl font-bold text-blue-700 mt-1">
                            {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(
                                data.reduce((acc, d) => acc + parseFloat(d.principal_amount || 0), 0)
                            )}
                        </h3>
                    </div>
                </div>
            </div>
            <DataTable 
                title="Loans" 
                columns={columns} 
                data={filteredData} 
                loading={loading} 
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                onAdd={canCreate ? handleAdd : null}
            />

            {isAssignModalOpen && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold">Assign Loan Officer</h2>
                            <button onClick={() => setIsAssignModalOpen(false)}><X size={20}/></button>
                        </div>
                        <form onSubmit={handleAssignSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium mb-1">Select Officer</label>
                                <select value={formData.loan_officer_id} onChange={e => setFormData({...formData, loan_officer_id: e.target.value})} className="w-full px-3 py-2 border rounded-lg">
                                    <option value="">Unassigned</option>
                                    {employees.map(e => <option key={e.employee_id} value={e.employee_id}>{e.first_name} {e.last_name}</option>)}
                                </select>
                            </div>
                            <div className="flex justify-end gap-3 pt-2">
                                <button type="button" onClick={() => setIsAssignModalOpen(false)} className="px-4 py-2 hover:bg-slate-100 rounded-lg">Cancel</button>
                                <button type="submit" disabled={formLoading} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg">Assign</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {isModalOpen && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4 overflow-y-auto">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl my-8 p-6">
                        <div className="flex justify-between items-center mb-4 border-b pb-4">
                            <h2 className="text-xl font-bold text-slate-900">
                                {editingRecord ? 'Edit Loan' : 'Add New Loan'}
                            </h2>
                            <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                                <X size={20} />
                            </button>
                        </div>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Customer</label>
                                    <select required value={formData.customer_id} onChange={e => setFormData({...formData, customer_id: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none" disabled={editingRecord}>
                                        <option value="">Select Customer</option>
                                        {customers.map(c => <option key={c.customer_id} value={c.customer_id}>{c.first_name} {c.last_name}</option>)}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Loan Type</label>
                                    <select required value={formData.loan_type} onChange={e => setFormData({...formData, loan_type: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none">
                                        <option value="PERSONAL">PERSONAL</option><option value="HOME">HOME</option><option value="AUTO">AUTO</option><option value="BUSINESS">BUSINESS</option>
                                    </select>
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Principal Amount</label><input required type="number" step="0.01" value={formData.principal_amount} onChange={e => setFormData({...formData, principal_amount: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none" /></div>
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Interest Rate (%)</label><input required type="number" step="0.01" value={formData.interest_rate} onChange={e => setFormData({...formData, interest_rate: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none" /></div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Term (Months)</label><input required type="number" value={formData.term_months} onChange={e => setFormData({...formData, term_months: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none" /></div>
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Start Date</label><input required type="date" value={formData.start_date} onChange={e => setFormData({...formData, start_date: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none" /></div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Outstanding Balance</label><input required type="number" step="0.01" value={formData.outstanding_balance} onChange={e => setFormData({...formData, outstanding_balance: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none" /></div>
                                                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Loan Officer</label>
                                    <select value={formData.loan_officer_id} onChange={e => setFormData({...formData, loan_officer_id: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none bg-slate-50" disabled>
                                        <option value="">Unassigned</option>
                                        {employees.map(e => <option key={e.employee_id} value={e.employee_id}>{e.first_name} {e.last_name}</option>)}
                                    </select>
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Status</label>
                                    <select value={formData.status} onChange={e => setFormData({...formData, status: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none">
                                        <option value="PENDING">PENDING</option><option value="ACTIVE">ACTIVE</option><option value="CLOSED">CLOSED</option><option value="DEFAULTED">DEFAULTED</option>
                                    </select>
                                </div>
                            </div>
                            <div className="pt-4 flex justify-end gap-3">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-100 rounded-lg transition-colors">Cancel</button>
                                <button type="submit" disabled={formLoading} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50">{formLoading ? 'Saving...' : 'Save Loan'}</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}


