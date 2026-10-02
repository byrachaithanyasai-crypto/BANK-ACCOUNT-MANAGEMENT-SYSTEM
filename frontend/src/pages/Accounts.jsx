import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Plus, X } from 'lucide-react';
import DataTable from '../components/DataTable';
import api from '../services/api';

export default function Accounts() {
    const { user } = useContext(AuthContext);
    const [data, setData] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [branches, setBranches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingRecord, setEditingRecord] = useState(null);
    const [formData, setFormData] = useState({ customer_id: '', branch_id: '', account_number: '', account_type: 'SAVINGS', balance: '0.00', status: 'ACTIVE', opened_date: '' });
    const [formLoading, setFormLoading] = useState(false);

    const fetchData = async () => {
        try {
            const [accRes, custRes, brRes] = await Promise.all([
                api.get('/api/accounts'), api.get('/api/customers'), api.get('/api/branches')
            ]);
            setData(accRes.data); setCustomers(custRes.data); setBranches(brRes.data);
        } catch (err) { console.error(err); } 
        finally { setLoading(false); }
    };
    useEffect(() => { fetchData(); }, []);

    const handleDelete = async (row) => {
        if(window.confirm('Close account?')) {
            try { 
                await api.delete('/api/accounts/' + row.account_id); 
                fetchData(); 
            }
            catch (err) { alert(err.response?.data?.detail || 'Failed to delete account.'); }
        }
    };
    
    const handleEdit = (row) => {
        setEditingRecord(row);
        setFormData({ 
            customer_id: row.customer_id, branch_id: row.branch_id, 
            account_number: row.account_number, account_type: row.account_type, 
            balance: row.balance, status: row.status, opened_date: row.opened_date 
        });
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingRecord(null);
        setFormData({ 
            customer_id: customers[0]?.customer_id || '', branch_id: branches[0]?.branch_id || '', 
            account_number: 'ACC' + Math.floor(Math.random() * 1000000), 
            account_type: 'SAVINGS', balance: '0.00', status: 'ACTIVE', opened_date: new Date().toISOString().split('T')[0] 
        });
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault(); setFormLoading(true);
        try {
            const payload = {
                ...formData,
                customer_id: parseInt(formData.customer_id),
                branch_id: parseInt(formData.branch_id),
                balance: parseFloat(formData.balance)
            };
            if (editingRecord) await api.put('/api/accounts/' + editingRecord.account_id, payload);
            else await api.post('/api/accounts', payload);
            setIsModalOpen(false); fetchData();
        } catch (err) { alert(err.response?.data?.detail || 'Error saving account'); } 
        finally { setFormLoading(false); }
    };

    const canEdit = ["ADMIN", "MANAGER"].includes(user?.role);
    const canDelete = user?.role === "ADMIN";
    const canCreate = ["ADMIN", "MANAGER"].includes(user?.role);

    const columns = [
        { header: "Account #", accessor: "account_number" }, 
        { header: "Customer", accessor: "customer_id", render: (row) => { const c = customers.find(c => c.customer_id === row.customer_id); return c ? c.first_name + " " + c.last_name : row.customer_id; } },
        { header: "Type", accessor: "account_type", render: (row) => (
            <span className="font-semibold text-slate-700">{row.account_type}</span>
        )},
        { header: "Balance", accessor: "balance", render: (row) => '$' + parseFloat(row.balance).toFixed(2) },
        { header: "Status", accessor: "status", render: (row) => (
            <span className={'px-2 py-1 rounded-full text-xs font-semibold ' + (row.status === 'ACTIVE' ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-700')}>{row.status}</span>
        )},
        { header: "Opened", accessor: "opened_date" }
    ];

    if (canEdit || canDelete) {
        columns.push({
            header: "Actions", 
            accessor: "actions", 
            render: (row) => (
                <div className="flex items-center gap-3">
                    {canEdit && <button onClick={() => handleEdit(row)} className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>}
                    {canDelete && <button onClick={() => handleDelete(row)} className="text-red-600 hover:text-red-800 font-medium">Delete</button>}
                </div>
            )
        });
    }

    const filteredData = data.filter(row => Object.values(row).some(val => String(val).toLowerCase().includes(searchQuery.toLowerCase())));

    return (
        <div className="h-full relative">
            <DataTable 
                title="Accounts" 
                columns={columns} 
                data={filteredData} 
                loading={loading} 
                searchQuery={searchQuery} 
                setSearchQuery={setSearchQuery} 
                onAdd={canCreate ? handleAdd : null} 
            />
            {isModalOpen && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden">
                        <div className="flex justify-between items-center p-6 border-b border-slate-100">
                            <h2 className="text-xl font-bold">{editingRecord ? 'Edit Account' : 'Open Account'}</h2>
                            <button onClick={() => setIsModalOpen(false)}><X size={20} /></button>
                        </div>
                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            {!editingRecord && (
                                <>
                                <div><label className="block text-sm font-medium mb-1">Customer</label>
                                    <select required value={formData.customer_id} onChange={e=>setFormData({...formData, customer_id: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500">
                                        <option value="">Select a customer...</option>
                                        {customers.map(c => <option key={c.customer_id} value={c.customer_id}>{c.first_name + ' ' + c.last_name}</option>)}
                                    </select>
                                </div>
                                <div><label className="block text-sm font-medium mb-1">Branch</label>
                                    <select required value={formData.branch_id} onChange={e=>setFormData({...formData, branch_id: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500">
                                        <option value="">Select a branch...</option>
                                        {branches.map(b => <option key={b.branch_id} value={b.branch_id}>{b.branch_name}</option>)}
                                    </select>
                                </div>
                                </>
                            )}
                            <div><label className="block text-sm font-medium mb-1">Account Number (Auto-generated)</label><input required disabled={!!editingRecord} value={formData.account_number} onChange={e=>setFormData({...formData, account_number: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none bg-slate-50" /></div>
                            <div><label className="block text-sm font-medium mb-1">Account Type</label>
                                <select required value={formData.account_type} onChange={e=>setFormData({...formData, account_type: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500">
                                    <option value="SAVINGS">Savings</option><option value="CHECKING">Checking</option><option value="BUSINESS">Business</option>
                                </select>
                            </div>
                            <div><label className="block text-sm font-medium mb-1">Status</label>
                                <select required value={formData.status} onChange={e=>setFormData({...formData, status: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500">
                                    <option value="ACTIVE">Active</option><option value="INACTIVE">Inactive</option><option value="CLOSED">Closed</option>
                                </select>
                            </div>
                            <div><label className="block text-sm font-medium mb-1">Balance</label><input required type="number" step="0.01" value={formData.balance} onChange={e=>setFormData({...formData, balance: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div className="pt-4 flex justify-end gap-3"><button type="button" onClick={()=>setIsModalOpen(false)} className="px-4 py-2 hover:bg-slate-100 rounded-lg">Cancel</button><button type="submit" disabled={formLoading} className="px-4 py-2 bg-blue-600 text-white rounded-lg">Save</button></div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
