import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 1. Customers
customers_page = '''
import React, { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import { X } from 'lucide-react';

export default function Customers() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    
    // Modal state
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingRecord, setEditingRecord] = useState(null);
    const [formData, setFormData] = useState({
        first_name: '', last_name: '', email: '', phone: '', kyc_status: 'PENDING'
    });
    const [formLoading, setFormLoading] = useState(false);

    const fetchData = async () => {
        try {
            const res = await api.get('/api/customers');
            setData(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleDelete = async (row) => {
        if(window.confirm('Are you sure you want to delete this customer?')) {
            try {
                await api.delete(/api/customers/);
                fetchData();
            } catch (err) {
                alert('Failed to delete. Customer may have active accounts or loans.');
            }
        }
    };
    
    const handleEdit = (row) => {
        setEditingRecord(row);
        setFormData({
            first_name: row.first_name,
            last_name: row.last_name,
            email: row.email,
            phone: row.phone,
            kyc_status: row.kyc_status
        });
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingRecord(null);
        setFormData({ first_name: '', last_name: '', email: '', phone: '', kyc_status: 'PENDING' });
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormLoading(true);
        try {
            if (editingRecord) {
                await api.put(/api/customers/, formData);
            } else {
                await api.post('/api/customers', formData);
            }
            setIsModalOpen(false);
            fetchData();
        } catch (err) {
            alert(err.response?.data?.detail || 'An error occurred saving the customer.');
        } finally {
            setFormLoading(false);
        }
    };

    const columns = [
        { header: "ID", accessor: "customer_id" },
        { header: "First Name", accessor: "first_name" },
        { header: "Last Name", accessor: "last_name" },
        { header: "Email", accessor: "email" },
        { header: "Phone", accessor: "phone" },
        { header: "KYC Status", accessor: "kyc_status", render: (row) => (
            <span className={px-2.5 py-1 rounded-full text-xs font-semibold }>
                {row.kyc_status}
            </span>
        )},
        { header: "Edit", accessor: "edit", render: (row) => (
            <button onClick={() => handleEdit(row)} className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>
        )}
    ];

    const filteredData = data.filter(row => 
        Object.values(row).some(val => 
            String(val).toLowerCase().includes(searchQuery.toLowerCase())
        )
    );

    return (
        <div className="h-full relative">
            <DataTable 
                title="Customers" 
                columns={columns} 
                data={filteredData} 
                loading={loading} 
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                onDelete={handleDelete}
                onAdd={handleAdd}
            />

            {isModalOpen && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden">
                        <div className="flex justify-between items-center p-6 border-b border-slate-100">
                            <h2 className="text-xl font-bold text-slate-900">
                                {editingRecord ? 'Edit Customer' : 'Add New Customer'}
                            </h2>
                            <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                                <X size={20} />
                            </button>
                        </div>
                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">First Name</label>
                                    <input required type="text" value={formData.first_name} onChange={e => setFormData({...formData, first_name: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Last Name</label>
                                    <input required type="text" value={formData.last_name} onChange={e => setFormData({...formData, last_name: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                                <input required type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Phone</label>
                                <input required type="text" value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">KYC Status</label>
                                <select value={formData.kyc_status} onChange={e => setFormData({...formData, kyc_status: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none">
                                    <option value="PENDING">Pending</option>
                                    <option value="VERIFIED">Verified</option>
                                    <option value="REJECTED">Rejected</option>
                                </select>
                            </div>
                            <div className="pt-4 flex justify-end gap-3">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-100 rounded-lg transition-colors">Cancel</button>
                                <button type="submit" disabled={formLoading} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50">
                                    {formLoading ? 'Saving...' : 'Save Customer'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
'''
write_file('frontend/src/pages/Customers.jsx', customers_page)

# 2. Branches
branches_page = '''
import React, { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import { X } from 'lucide-react';

export default function Branches() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingRecord, setEditingRecord] = useState(null);
    const [formData, setFormData] = useState({ branch_code: '', branch_name: '', city: '', phone: '' });
    const [formLoading, setFormLoading] = useState(false);

    const fetchData = async () => {
        try {
            const res = await api.get('/api/branches');
            setData(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };
    useEffect(() => { fetchData(); }, []);

    const handleDelete = async (row) => {
        if(window.confirm('Delete branch?')) {
            try { await api.delete(/api/branches/); fetchData(); }
            catch (err) { alert('Failed to delete. Accounts or employees may be linked.'); }
        }
    };
    
    const handleEdit = (row) => {
        setEditingRecord(row);
        setFormData({ branch_code: row.branch_code, branch_name: row.branch_name, city: row.city || '', phone: row.phone || '' });
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingRecord(null);
        setFormData({ branch_code: '', branch_name: '', city: '', phone: '' });
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormLoading(true);
        try {
            if (editingRecord) await api.put(/api/branches/, formData);
            else await api.post('/api/branches', formData);
            setIsModalOpen(false); fetchData();
        } catch (err) { alert(err.response?.data?.detail || 'Error saving branch'); } 
        finally { setFormLoading(false); }
    };

    const columns = [
        { header: "Code", accessor: "branch_code" },
        { header: "Name", accessor: "branch_name" },
        { header: "City", accessor: "city" },
        { header: "Phone", accessor: "phone" },
        { header: "Edit", accessor: "edit", render: (row) => (
            <button onClick={() => handleEdit(row)} className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>
        )}
    ];

    const filteredData = data.filter(row => Object.values(row).some(val => String(val).toLowerCase().includes(searchQuery.toLowerCase())));

    return (
        <div className="h-full relative">
            <DataTable title="Branches" columns={columns} data={filteredData} loading={loading} searchQuery={searchQuery} setSearchQuery={setSearchQuery} onDelete={handleDelete} onAdd={handleAdd} />
            {isModalOpen && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden">
                        <div className="flex justify-between items-center p-6 border-b border-slate-100">
                            <h2 className="text-xl font-bold">{editingRecord ? 'Edit Branch' : 'Add Branch'}</h2>
                            <button onClick={() => setIsModalOpen(false)}><X size={20} /></button>
                        </div>
                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            <div><label className="block text-sm font-medium mb-1">Branch Code</label><input required value={formData.branch_code} onChange={e=>setFormData({...formData, branch_code: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div><label className="block text-sm font-medium mb-1">Name</label><input required value={formData.branch_name} onChange={e=>setFormData({...formData, branch_name: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div><label className="block text-sm font-medium mb-1">City</label><input value={formData.city} onChange={e=>setFormData({...formData, city: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div><label className="block text-sm font-medium mb-1">Phone</label><input value={formData.phone} onChange={e=>setFormData({...formData, phone: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div className="pt-4 flex justify-end gap-3"><button type="button" onClick={()=>setIsModalOpen(false)} className="px-4 py-2 hover:bg-slate-100 rounded-lg">Cancel</button><button type="submit" disabled={formLoading} className="px-4 py-2 bg-blue-600 text-white rounded-lg">Save</button></div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
'''
write_file('frontend/src/pages/Branches.jsx', branches_page)

# 3. Transactions
transactions_page = '''
import React, { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import { X, ArrowUpRight, ArrowDownLeft, RefreshCcw } from 'lucide-react';

export default function Transactions() {
    const [data, setData] = useState([]);
    const [accounts, setAccounts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState({ account_id: '', transaction_type: 'DEPOSIT', amount: '', description: '' });
    const [formLoading, setFormLoading] = useState(false);

    const fetchData = async () => {
        try {
            const [txnRes, accRes] = await Promise.all([
                api.get('/api/transactions'),
                api.get('/api/accounts')
            ]);
            setData(txnRes.data);
            setAccounts(accRes.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };
    useEffect(() => { fetchData(); }, []);

    const handleAdd = () => {
        setFormData({ account_id: accounts[0]?.account_id || '', transaction_type: 'DEPOSIT', amount: '', description: '' });
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormLoading(true);
        try {
            await api.post('/api/transactions', {
                ...formData,
                account_id: parseInt(formData.account_id),
                amount: parseFloat(formData.amount)
            });
            setIsModalOpen(false); fetchData();
        } catch (err) { alert(err.response?.data?.detail || 'Transaction failed'); } 
        finally { setFormLoading(false); }
    };

    const columns = [
        { header: "Txn ID", accessor: "transaction_id" },
        { header: "Account ID", accessor: "account_id" },
        { header: "Type", accessor: "transaction_type", render: (row) => {
            if (row.transaction_type === 'DEPOSIT') return <span className="flex items-center text-emerald-600"><ArrowDownLeft size={16} className="mr-1"/> Deposit</span>;
            if (row.transaction_type === 'WITHDRAWAL') return <span className="flex items-center text-red-600"><ArrowUpRight size={16} className="mr-1"/> Withdrawal</span>;
            return <span className="flex items-center text-blue-600"><RefreshCcw size={16} className="mr-1"/> Transfer</span>;
        }},
        { header: "Amount", accessor: "amount", render: (row) => $ },
        { header: "Date", accessor: "transaction_date", render: (row) => new Date(row.transaction_date).toLocaleString() },
        { header: "Status", accessor: "status", render: (row) => (
            <span className={px-2 py-1 rounded-full text-xs }>{row.status}</span>
        )}
    ];

    const filteredData = data.filter(row => Object.values(row).some(val => String(val).toLowerCase().includes(searchQuery.toLowerCase())));

    return (
        <div className="h-full relative">
            <DataTable title="Transactions" columns={columns} data={filteredData} loading={loading} searchQuery={searchQuery} setSearchQuery={setSearchQuery} onAdd={handleAdd} addButtonLabel="New Transaction" />
            {isModalOpen && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden">
                        <div className="flex justify-between items-center p-6 border-b border-slate-100">
                            <h2 className="text-xl font-bold">New Transaction</h2>
                            <button onClick={() => setIsModalOpen(false)}><X size={20} /></button>
                        </div>
                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            <div>
                                <label className="block text-sm font-medium mb-1">Target Account</label>
                                <select required value={formData.account_id} onChange={e=>setFormData({...formData, account_id: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500">
                                    {accounts.map(a => <option key={a.account_id} value={a.account_id}>{a.account_number} (Bal: )</option>)}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">Transaction Type</label>
                                <select value={formData.transaction_type} onChange={e=>setFormData({...formData, transaction_type: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500">
                                    <option value="DEPOSIT">Deposit</option>
                                    <option value="WITHDRAWAL">Withdrawal</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">Amount ($)</label>
                                <input required type="number" step="0.01" min="0.01" value={formData.amount} onChange={e=>setFormData({...formData, amount: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">Description (Optional)</label>
                                <input value={formData.description} onChange={e=>setFormData({...formData, description: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" />
                            </div>
                            <div className="pt-4 flex justify-end gap-3"><button type="button" onClick={()=>setIsModalOpen(false)} className="px-4 py-2 hover:bg-slate-100 rounded-lg">Cancel</button><button type="submit" disabled={formLoading} className="px-4 py-2 bg-blue-600 text-white rounded-lg">Execute</button></div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
'''
write_file('frontend/src/pages/Transactions.jsx', transactions_page)

print("Forms built successfully.")
