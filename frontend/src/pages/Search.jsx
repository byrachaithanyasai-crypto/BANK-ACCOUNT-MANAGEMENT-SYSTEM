import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import api from '../services/api';
import { Loader2, Search as SearchIcon, User, CreditCard, Activity } from 'lucide-react';

export default function SearchResults() {
    const location = useLocation();
    const query = new URLSearchParams(location.search).get('q') || '';
    
    const [loading, setLoading] = useState(true);
    const [results, setResults] = useState({ accounts: [], customers: [], transactions: [] });

    useEffect(() => {
        if (!query) {
            setLoading(false);
            return;
        }
        
        const fetchSearch = async () => {
            setLoading(true);
            try {
                // Fetch all data and filter in memory as a simple frontend global search
                const [accRes, custRes, txnRes] = await Promise.all([
                    api.get('/api/accounts'),
                    api.get('/api/customers'),
                    api.get('/api/transactions')
                ]);
                
                const lowerQ = query.toLowerCase();
                
                setResults({
                    accounts: accRes.data.filter(a => 
                        a.account_number.toLowerCase().includes(lowerQ) || 
                        a.account_type.toLowerCase().includes(lowerQ)
                    ),
                    customers: custRes.data.filter(c => 
                        c.first_name.toLowerCase().includes(lowerQ) || 
                        c.last_name.toLowerCase().includes(lowerQ) ||
                        c.email.toLowerCase().includes(lowerQ)
                    ),
                    transactions: txnRes.data.filter(t => 
                        String(t.transaction_id).includes(lowerQ) ||
                        String(t.amount).includes(lowerQ)
                    )
                });
            } catch (err) {
                console.error("Global search failed", err);
            } finally {
                setLoading(false);
            }
        };
        fetchSearch();
    }, [query]);

    if (!query) return <div className="p-8 text-slate-500">Please enter a search query in the header.</div>;

    if (loading) return <div className="flex justify-center p-12"><Loader2 className="w-8 h-8 animate-spin text-blue-600" /></div>;

    const hasResults = results.accounts.length > 0 || results.customers.length > 0 || results.transactions.length > 0;

    return (
        <div className="space-y-6 max-w-5xl">
            <h1 className="text-2xl font-bold text-slate-900">Search Results for "{query}"</h1>
            
            {!hasResults ? (
                <div className="bg-white p-12 rounded-2xl border border-slate-200 text-center text-slate-500 shadow-sm">
                    No results found across Accounts, Customers, or Transactions.
                </div>
            ) : (
                <div className="space-y-6">
                    {results.customers.length > 0 && (
                        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                            <div className="p-4 bg-slate-50 border-b border-slate-100 flex items-center gap-2 font-bold text-slate-700">
                                <User size={18} /> Customers ({results.customers.length})
                            </div>
                            <div className="divide-y divide-slate-100">
                                {results.customers.map(c => (
                                    <div key={c.customer_id} className="p-4 hover:bg-slate-50 flex justify-between items-center">
                                        <div>
                                            <p className="font-medium text-slate-900">{c.first_name} {c.last_name}</p>
                                            <p className="text-sm text-slate-500">{c.email} | {c.phone}</p>
                                        </div>
                                        <Link to="/customers" className="text-sm text-blue-600 hover:underline">View</Link>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                    
                    {results.accounts.length > 0 && (
                        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                            <div className="p-4 bg-slate-50 border-b border-slate-100 flex items-center gap-2 font-bold text-slate-700">
                                <CreditCard size={18} /> Accounts ({results.accounts.length})
                            </div>
                            <div className="divide-y divide-slate-100">
                                {results.accounts.map(a => (
                                    <div key={a.account_id} className="p-4 hover:bg-slate-50 flex justify-between items-center">
                                        <div>
                                            <p className="font-medium text-slate-900">{a.account_number}</p>
                                            <p className="text-sm text-slate-500">{a.account_type} | Balance: ${a.balance}</p>
                                        </div>
                                        <Link to="/accounts" className="text-sm text-blue-600 hover:underline">View</Link>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                    
                    {results.transactions.length > 0 && (
                        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                            <div className="p-4 bg-slate-50 border-b border-slate-100 flex items-center gap-2 font-bold text-slate-700">
                                <Activity size={18} /> Transactions ({results.transactions.length})
                            </div>
                            <div className="divide-y divide-slate-100">
                                {results.transactions.map(t => (
                                    <div key={t.transaction_id} className="p-4 hover:bg-slate-50 flex justify-between items-center">
                                        <div>
                                            <p className="font-medium text-slate-900">Txn #{t.transaction_id} - {t.transaction_type}</p>
                                            <p className="text-sm text-slate-500">Amount: ${t.amount} | Date: {new Date(t.transaction_date).toLocaleDateString()}</p>
                                        </div>
                                        <Link to="/transactions" className="text-sm text-blue-600 hover:underline">View</Link>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
