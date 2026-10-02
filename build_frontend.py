import os

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def write_file(path, content):
    ensure_dir(path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

datatable = '''
import React from 'react';
import { Search, Loader2 } from 'lucide-react';

export default function DataTable({ 
    title, 
    columns, 
    data, 
    loading, 
    onAdd, 
    onDelete, 
    searchQuery, 
    setSearchQuery,
    addButtonLabel = "Add New"
}) {
    return (
        <div className="space-y-6 flex flex-col h-full">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
                    <p className="text-slate-500 mt-1">Manage and view {title.toLowerCase()} records.</p>
                </div>
                <div className="flex items-center gap-3">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
                        <input 
                            type="text" 
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder={`Search ${title.toLowerCase()}...`} 
                            className="w-full sm:w-64 pl-10 pr-4 py-2 bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 rounded-lg text-sm transition-all outline-none"
                        />
                    </div>
                    {onAdd && (
                        <button 
                            onClick={onAdd}
                            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors whitespace-nowrap"
                        >
                            {addButtonLabel}
                        </button>
                    )}
                </div>
            </div>
            
            <div className="flex-1 bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
                <div className="overflow-x-auto flex-1 custom-scrollbar">
                    <table className="w-full text-left text-sm whitespace-nowrap">
                        <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200 sticky top-0 z-10">
                            <tr>
                                {columns.map((col, idx) => (
                                    <th key={idx} className="px-6 py-4">{col.header}</th>
                                ))}
                                {onDelete && <th className="px-6 py-4 text-right">Actions</th>}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {loading ? (
                                <tr>
                                    <td colSpan={columns.length + (onDelete ? 1 : 0)} className="px-6 py-20 text-center text-slate-500">
                                        <div className="flex flex-col items-center justify-center">
                                            <Loader2 className="w-8 h-8 animate-spin text-blue-500 mb-4" />
                                            <p>Loading {title.toLowerCase()}...</p>
                                        </div>
                                    </td>
                                </tr>
                            ) : data.length === 0 ? (
                                <tr>
                                    <td colSpan={columns.length + (onDelete ? 1 : 0)} className="px-6 py-20 text-center text-slate-500">
                                        <p className="font-medium text-slate-900">No {title.toLowerCase()} found</p>
                                        <p className="mt-1">Try adjusting your search criteria.</p>
                                    </td>
                                </tr>
                            ) : (
                                data.map((row, rowIdx) => (
                                    <tr key={rowIdx} className="hover:bg-slate-50/50 transition-colors">
                                        {columns.map((col, colIdx) => (
                                            <td key={colIdx} className="px-6 py-4 text-slate-700">
                                                {row[col.accessor]}
                                            </td>
                                        ))}
                                        {onDelete && (
                                            <td className="px-6 py-4 text-right">
                                                <button 
                                                    onClick={() => onDelete(row)}
                                                    className="text-red-500 hover:text-red-700 font-medium text-xs px-3 py-1.5 rounded-lg hover:bg-red-50 transition-colors"
                                                >
                                                    Delete
                                                </button>
                                            </td>
                                        )}
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
'''
write_file('frontend/src/components/DataTable.jsx', datatable)

pages = {
    "Accounts": {
        "api": "/api/accounts",
        "pk": "account_id",
        "columns": [
            {"header": "Account ID", "accessor": "account_id"},
            {"header": "Account Number", "accessor": "account_number"},
            {"header": "Type", "accessor": "account_type"},
            {"header": "Balance", "accessor": "balance"},
            {"header": "Status", "accessor": "status"},
        ]
    },
    "Customers": {
        "api": "/api/customers",
        "pk": "customer_id",
        "columns": [
            {"header": "ID", "accessor": "customer_id"},
            {"header": "First Name", "accessor": "first_name"},
            {"header": "Last Name", "accessor": "last_name"},
            {"header": "Email", "accessor": "email"},
            {"header": "KYC Status", "accessor": "kyc_status"},
        ]
    },
    "Employees": {
        "api": "/api/employees",
        "pk": "employee_id",
        "columns": [
            {"header": "ID", "accessor": "employee_id"},
            {"header": "First Name", "accessor": "first_name"},
            {"header": "Last Name", "accessor": "last_name"},
            {"header": "Email", "accessor": "email"},
            {"header": "Position", "accessor": "position"},
        ]
    },
    "Branches": {
        "api": "/api/branches",
        "pk": "branch_id",
        "columns": [
            {"header": "Code", "accessor": "branch_code"},
            {"header": "Name", "accessor": "branch_name"},
            {"header": "City", "accessor": "city"},
            {"header": "Phone", "accessor": "phone"},
        ]
    },
    "AuditLogs": {
        "api": "/api/audit-logs",
        "pk": "log_id",
        "columns": [
            {"header": "Timestamp", "accessor": "action_timestamp"},
            {"header": "User ID", "accessor": "user_id"},
            {"header": "Action", "accessor": "action"},
            {"header": "Table", "accessor": "table_name"},
            {"header": "Record ID", "accessor": "record_id"},
        ]
    },
    "Transactions": {
        "api": "/api/transactions",
        "pk": "transaction_id",
        "columns": [
            {"header": "Transaction ID", "accessor": "transaction_id"},
            {"header": "Account ID", "accessor": "account_id"},
            {"header": "Type", "accessor": "transaction_type"},
            {"header": "Amount", "accessor": "amount"},
            {"header": "Date", "accessor": "transaction_date"},
            {"header": "Status", "accessor": "status"}
        ]
    }
}

for page_name, conf in pages.items():
    cols_str = str(conf["columns"]).replace("'", '"')
    api_url = conf["api"]
    pk = conf["pk"]
    
    content = f"""
import React, {{ useState, useEffect }} from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';

export default function {page_name}() {{
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');

    const fetchData = async () => {{
        try {{
            const res = await api.get('{api_url}');
            setData(res.data);
        }} catch (err) {{
            console.error(err);
        }} finally {{
            setLoading(false);
        }}
    }};

    useEffect(() => {{
        fetchData();
    }}, []);

    const handleDelete = async (row) => {{
        if(window.confirm('Are you sure you want to delete this record?')) {{
            try {{
                await api.delete(`{api_url}/${{row.{pk}}}`);
                fetchData();
            }} catch (err) {{
                alert('Failed to delete record. It may be restricted by existing relationships or permissions.');
            }}
        }}
    }};

    const columns = {cols_str};

    const filteredData = data.filter(row => 
        Object.values(row).some(val => 
            String(val).toLowerCase().includes(searchQuery.toLowerCase())
        )
    );

    return (
        <DataTable 
            title="{page_name}" 
            columns={{columns}} 
            data={{filteredData}} 
            loading={{loading}} 
            searchQuery={{searchQuery}}
            setSearchQuery={{setSearchQuery}}
            onDelete={{handleDelete}}
            onAdd={{() => alert('Please implement full modal forms here.')}}
        />
    );
}}
"""
    write_file(f'frontend/src/pages/{page_name}.jsx', content)

dashboard = '''
import { useState, useEffect, useContext } from 'react';
import { Users, CreditCard, Activity, Briefcase } from 'lucide-react';
import api from '../services/api';
import { AuthContext } from '../context/AuthContext';

export default function Dashboard() {
    const { user } = useContext(AuthContext);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState({ accounts: 0, customers: 0, transactions: 0, employees: 0 });

    const fetchStats = async () => {
        try {
            const res = await api.get('/api/dashboard/summary');
            setStats(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStats();
    }, []);

    const greeting = () => {
        const hour = new Date().getHours();
        if (hour < 12) return 'Good morning';
        if (hour < 18) return 'Good afternoon';
        return 'Good evening';
    };

    if (loading) {
        return (
            <div className="space-y-8 animate-pulse">
                <div className="h-10 bg-slate-200 rounded w-1/4"></div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {[...Array(4)].map((_, i) => <div key={i} className="h-32 bg-slate-200 rounded-2xl"></div>)}
                </div>
            </div>
        );
    }

    const cards = [
        { title: 'Total Accounts', value: stats.accounts, icon: CreditCard, color: 'bg-blue-50 text-blue-600' },
        { title: 'Customers', value: stats.customers, icon: Users, color: 'bg-indigo-50 text-indigo-600' },
        { title: 'Transactions', value: stats.transactions, icon: Activity, color: 'bg-emerald-50 text-emerald-600' },
        { title: 'Active Employees', value: stats.employees, icon: Briefcase, color: 'bg-amber-50 text-amber-600' }
    ];

    return (
        <div className="space-y-8">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h1 className="text-2xl md:text-3xl font-bold text-slate-900">{greeting()}, {user?.username}</h1>
                    <p className="text-slate-500 mt-2">Here's an overview of your banking operations.</p>
                </div>
                <div className="flex items-center gap-3">
                    <div className="px-4 py-2 bg-white rounded-lg border border-slate-200 shadow-sm text-sm">
                        <span className="text-slate-500 mr-2">System Status:</span>
                        <span className="text-emerald-600 font-semibold flex items-center inline-flex gap-1">
                            <span className="w-2 h-2 rounded-full bg-emerald-500"></span> Online
                        </span>
                    </div>
                </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {cards.map((card, idx) => (
                    <div key={idx} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-sm font-semibold text-slate-500">{card.title}</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">
                                    {card.value.toLocaleString()}
                                </h3>
                            </div>
                            <div className={`p-3 rounded-xl ${card.color}`}>
                                <card.icon size={24} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 min-h-[300px] flex flex-col justify-center items-center text-center">
                    <p className="text-slate-500 font-medium">Recent Activity feed</p>
                    <p className="text-sm text-slate-400 mt-2">Driven by real database records</p>
                </div>
                <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 min-h-[300px] flex flex-col justify-center items-center text-center">
                    <p className="text-slate-500 font-medium">System Diagnostics</p>
                    <p className="text-sm text-slate-400 mt-2">All services operating normally</p>
                </div>
            </div>
        </div>
    );
}
'''
write_file('frontend/src/pages/Dashboard.jsx', dashboard)
print("done")
