import { useState, useEffect, useContext } from 'react';
import { Users, CreditCard, Activity, Briefcase, Plus, TrendingUp, Filter, CheckCircle2, Shield } from 'lucide-react';
import api from '../services/api';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Legend } from 'recharts';

export default function Dashboard() {
    const { user } = useContext(AuthContext);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState(null);
    const [error, setError] = useState(null);

    const fetchData = async () => {
        try {
            const res = await api.get('/api/dashboard/summary');
            setStats(res.data);
            setError(null);
        } catch (err) {
            console.error(err);
            setError("Unable to load dashboard data.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
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

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center h-64 text-center">
                <Shield size={48} className="text-slate-300 mb-4" />
                <h2 className="text-xl font-bold text-slate-700">{error}</h2>
            </div>
        );
    }

    const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
    const formatCurrency = (val) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val);

    const cards = [
        { title: 'Total Accounts', value: stats.accounts, icon: CreditCard, color: 'bg-blue-50 text-blue-600' },
        { title: 'Customers', value: stats.customers, icon: Users, color: 'bg-indigo-50 text-indigo-600' },
        { title: 'Transactions', value: stats.transactions, icon: Activity, color: 'bg-emerald-50 text-emerald-600' },
        { title: 'Total Balance', value: formatCurrency(stats.total_balance), icon: Briefcase, color: 'bg-amber-50 text-amber-600' }
    ];

    // Determine quick actions by role
    const quickActions = [
        { label: 'New Account', path: '/accounts', roles: ['ADMIN', 'MANAGER'] },
        { label: 'New Customer', path: '/customers', roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
        { label: 'New Transaction', path: '/transactions', roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
        { label: 'New Loan', path: '/loans', roles: ['ADMIN', 'MANAGER'] },
        { label: 'Manage Employees', path: '/employees', roles: ['ADMIN'] },
        { label: 'Manage Branches', path: '/branches', roles: ['ADMIN'] }
    ].filter(action => action.roles.includes(user?.role));

    return (
        <div className="space-y-8 pb-10">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h1 className="text-2xl md:text-3xl font-bold text-slate-900">{greeting()}, {user?.username}</h1>
                    <p className="text-slate-500 mt-2">Here's an overview of your banking operations.</p>
                </div>
                <div className="flex items-center gap-2 bg-emerald-50 text-emerald-700 px-4 py-2 rounded-lg font-medium text-sm">
                    <span className="relative flex h-3 w-3">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                    </span>
                    System Online
                </div>
            </div>
            
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {cards.map((card, idx) => (
                    <div key={idx} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-sm font-semibold text-slate-500">{card.title}</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">
                                    {card.value}
                                </h3>
                            </div>
                            <div className={`p-3 rounded-xl ${card.color}`}>
                                <card.icon size={24} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Quick Actions & Banking Summary */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                    <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                        <Plus size={20} className="text-blue-600" /> Quick Actions
                    </h2>
                    <div className="flex flex-wrap gap-3">
                        {quickActions.map((action, idx) => (
                            <Link 
                                key={idx} 
                                to={action.path}
                                className="flex items-center gap-2 px-4 py-2.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl text-slate-700 font-medium transition-colors"
                            >
                                <Plus size={16} />
                                {action.label}
                            </Link>
                        ))}
                    </div>
                </div>

                <div className="bg-gradient-to-br from-slate-900 to-slate-800 p-6 rounded-2xl shadow-sm text-white">
                    <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                        <Briefcase size={20} className="text-blue-400" /> Banking Overview
                    </h2>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center border-b border-slate-700 pb-2">
                            <span className="text-slate-400 text-sm">Total Balance</span>
                            <span className="font-bold">{formatCurrency(stats.total_balance)}</span>
                        </div>
                        <div className="flex justify-between items-center border-b border-slate-700 pb-2">
                            <span className="text-slate-400 text-sm">Average Account Balance</span>
                            <span className="font-bold">{formatCurrency(stats.average_balance)}</span>
                        </div>
                        <div className="flex justify-between items-center border-b border-slate-700 pb-2">
                            <span className="text-slate-400 text-sm">Active Accounts</span>
                            <span className="font-bold text-emerald-400">{stats.active_accounts} / {stats.accounts}</span>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="text-slate-400 text-sm">Total Customers</span>
                            <span className="font-bold">{stats.customers}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
                    <h2 className="text-lg font-bold text-slate-900 mb-6">Account Distribution</h2>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={stats.account_distribution}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {stats.account_distribution.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <RechartsTooltip />
                                <Legend verticalAlign="bottom" height={36}/>
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
                    <h2 className="text-lg font-bold text-slate-900 mb-6">Account Status</h2>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={stats.status_distribution}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {stats.status_distribution.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={
                                            entry.name === 'ACTIVE' ? '#10b981' : 
                                            entry.name === 'CLOSED' ? '#ef4444' : '#f59e0b'
                                        } />
                                    ))}
                                </Pie>
                                <RechartsTooltip />
                                <Legend verticalAlign="bottom" height={36}/>
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
                    <h2 className="text-lg font-bold text-slate-900 mb-6">Transaction Overview</h2>
                    <div className="h-72">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={stats.transaction_distribution} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} />
                                <YAxis axisLine={false} tickLine={false} />
                                <RechartsTooltip cursor={{fill: '#f8fafc'}} />
                                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                                    {stats.transaction_distribution.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.name === 'DEPOSIT' ? '#3b82f6' : '#f59e0b'} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Loans Overview (Compact) */}
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                        <Briefcase size={20} className="text-blue-600" /> Loans Overview
                    </h2>
                    <Link to="/loans" className="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors">
                        View All Loans →
                    </Link>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                        <p className="text-xs font-semibold text-slate-500 uppercase">Total Loans</p>
                        <p className="text-2xl font-bold text-slate-800 mt-1">{stats.total_loans || 0}</p>
                    </div>
                    <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                        <p className="text-xs font-semibold text-slate-500 uppercase">Active</p>
                        <p className="text-2xl font-bold text-emerald-600 mt-1">{stats.active_loans || 0}</p>
                    </div>
                    <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                        <p className="text-xs font-semibold text-slate-500 uppercase">Pending</p>
                        <p className="text-2xl font-bold text-amber-500 mt-1">{stats.pending_loans || 0}</p>
                    </div>
                    <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                        <p className="text-xs font-semibold text-slate-500 uppercase">Total Amount</p>
                        <p className="text-2xl font-bold text-slate-800 mt-1">{formatCurrency(stats.total_loan_amount || 0)}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

