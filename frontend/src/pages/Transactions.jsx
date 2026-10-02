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
        { header: "Amount", accessor: "amount", render: (row) => `$${parseFloat(row.amount).toFixed(2)}` },
        { header: "Date", accessor: "transaction_date", render: (row) => new Date(row.transaction_date).toLocaleString() },
        { header: "Status", accessor: "status", render: (row) => (
            <span className={`px-2 py-1 rounded-full text-xs ${row.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>{row.status}</span>
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
                                    <option value="">Select an account...</option>
                                    {accounts.map(a => <option key={a.account_id} value={a.account_id}>{a.account_number} (Bal: ${a.balance})</option>)}
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

