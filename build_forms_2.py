import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 4. Accounts
accounts_page = '''
import React, { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import { X } from 'lucide-react';

export default function Accounts() {
    const [data, setData] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [branches, setBranches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingRecord, setEditingRecord] = useState(null);
    const [formData, setFormData] = useState({ 
        customer_id: '', branch_id: '', account_number: '', 
        account_type: 'SAVINGS', balance: '0.00', opened_date: new Date().toISOString().split('T')[0] 
    });
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
            try { await api.delete(/api/accounts/); fetchData(); }
            catch (err) { alert('Failed to delete account.'); }
        }
    };
    
    const handleEdit = (row) => {
        setEditingRecord(row);
        setFormData({ 
            customer_id: row.customer_id, branch_id: row.branch_id, 
            account_number: row.account_number, account_type: row.account_type, 
            balance: row.balance, opened_date: row.opened_date 
        });
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingRecord(null);
        setFormData({ 
            customer_id: customers[0]?.customer_id || '', branch_id: branches[0]?.branch_id || '', 
            account_number: 'ACC' + Math.floor(Math.random() * 1000000), 
            account_type: 'SAVINGS', balance: '0.00', opened_date: new Date().toISOString().split('T')[0] 
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
            if (editingRecord) await api.put(/api/accounts/, payload);
            else await api.post('/api/accounts', payload);
            setIsModalOpen(false); fetchData();
        } catch (err) { alert(err.response?.data?.detail || 'Error saving account'); } 
        finally { setFormLoading(false); }
    };

    const columns = [
        { header: "Account #", accessor: "account_number" },
        { header: "Type", accessor: "account_type", render: (row) => (
            <span className="font-semibold text-slate-700">{row.account_type}</span>
        )},
        { header: "Balance", accessor: "balance", render: (row) => $ },
        { header: "Status", accessor: "status", render: (row) => (
            <span className={px-2 py-1 rounded-full text-xs font-semibold }>{row.status}</span>
        )},
        { header: "Opened", accessor: "opened_date" },
        { header: "Edit", accessor: "edit", render: (row) => (
            <button onClick={() => handleEdit(row)} className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>
        )}
    ];

    const filteredData = data.filter(row => Object.values(row).some(val => String(val).toLowerCase().includes(searchQuery.toLowerCase())));

    return (
        <div className="h-full relative">
            <DataTable title="Accounts" columns={columns} data={filteredData} loading={loading} searchQuery={searchQuery} setSearchQuery={setSearchQuery} onDelete={handleDelete} onAdd={handleAdd} />
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
                                        {customers.map(c => <option key={c.customer_id} value={c.customer_id}>{c.first_name} {c.last_name}</option>)}
                                    </select>
                                </div>
                                <div><label className="block text-sm font-medium mb-1">Branch</label>
                                    <select required value={formData.branch_id} onChange={e=>setFormData({...formData, branch_id: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500">
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
                            <div><label className="block text-sm font-medium mb-1">Balance</label><input required type="number" step="0.01" value={formData.balance} onChange={e=>setFormData({...formData, balance: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div className="pt-4 flex justify-end gap-3"><button type="button" onClick={()=>setIsModalOpen(false)} className="px-4 py-2 hover:bg-slate-100 rounded-lg">Cancel</button><button type="submit" disabled={formLoading} className="px-4 py-2 bg-blue-600 text-white rounded-lg">Save</button></div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
'''
write_file('frontend/src/pages/Accounts.jsx', accounts_page)

# 5. Reports
reports_page = '''
import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { Loader2 } from 'lucide-react';

export default function Reports() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchReports = async () => {
            try {
                // Using the dashboard summary endpoint for real stats
                const res = await api.get('/api/dashboard/summary');
                setStats(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchReports();
    }, []);

    if (loading) {
        return <div className="flex h-full items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-blue-600" /></div>;
    }

    // Since we don't have a time-series API yet, we map the aggregate counters into a visualization
    const distributionData = [
        { name: 'Accounts', value: stats?.accounts || 0 },
        { name: 'Customers', value: stats?.customers || 0 },
        { name: 'Employees', value: stats?.employees || 0 }
    ];

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-slate-900">System Reports</h1>
                <p className="text-slate-500 mt-1">Analytics and data visualization based on live database records.</p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
                    <h3 className="text-lg font-bold text-slate-900 mb-6">Entity Distribution</h3>
                    <div className="h-72">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={distributionData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#64748b' }} />
                                <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b' }} />
                                <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} barSize={40} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
                
                <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-center items-center text-center">
                    <h3 className="text-lg font-bold text-slate-900 mb-2">Transaction Volume</h3>
                    <div className="text-5xl font-black text-emerald-600 mb-4">{stats?.transactions || 0}</div>
                    <p className="text-slate-500 max-w-sm">Total historical transactions processed by the system. Time-series transaction APIs are required for line charting.</p>
                </div>
            </div>
        </div>
    );
}
'''
write_file('frontend/src/pages/Reports.jsx', reports_page)

print("Additional pages built successfully.")
