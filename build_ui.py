import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 1. ErrorBoundary
error_boundary = '''
import React from 'react';
import { AlertCircle, RefreshCw, Home } from 'lucide-react';
import { Link } from 'react-router-dom';

export class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error("ErrorBoundary caught an error", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-[400px] h-full flex flex-col items-center justify-center p-8 bg-white rounded-2xl border border-gray-100 shadow-sm text-center">
                    <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mb-6">
                        <AlertCircle className="w-8 h-8 text-red-600" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-3">Something went wrong</h2>
                    <p className="text-gray-500 max-w-md mx-auto mb-8">
                        We encountered an unexpected error while trying to render this view. 
                        Please try reloading the page or return to the dashboard.
                    </p>
                    <div className="flex gap-4">
                        <button 
                            onClick={() => window.location.reload()}
                            className="flex items-center gap-2 px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-900 rounded-lg font-medium transition-colors"
                        >
                            <RefreshCw size={18} />
                            Retry
                        </button>
                        <Link 
                            to="/dashboard"
                            className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                        >
                            <Home size={18} />
                            Go to Dashboard
                        </Link>
                    </div>
                </div>
            );
        }
        return this.props.children;
    }
}
'''

# 2. MainLayout.jsx update
main_layout = '''
import { useState, useContext, useEffect } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { AuthContext } from '../context/AuthContext';
import { ErrorBoundary } from '../components/ErrorBoundary';
import { 
    LayoutDashboard, Users, CreditCard, Activity, Building, 
    Briefcase, FileText, ShieldAlert, Settings, LogOut, 
    Menu, X, Search, Bell, Landmark, ChevronDown
} from 'lucide-react';

export default function MainLayout() {
    const { user, logout } = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate();
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [profileOpen, setProfileOpen] = useState(false);

    useEffect(() => {
        setSidebarOpen(false);
        setProfileOpen(false);
    }, [location]);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const navItems = [
        { section: 'OVERVIEW', items: [
            { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] }
        ]},
        { section: 'BANKING', items: [
            { path: '/accounts', label: 'Accounts', icon: CreditCard, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
            { path: '/customers', label: 'Customers', icon: Users, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
            { path: '/transactions', label: 'Transactions', icon: Activity, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] }
        ]},
        { section: 'OPERATIONS', items: [
            { path: '/employees', label: 'Employees', icon: Briefcase, roles: ['ADMIN'] },
            { path: '/branches', label: 'Branches', icon: Building, roles: ['ADMIN'] }
        ]},
        { section: 'INSIGHTS', items: [
            { path: '/reports', label: 'Reports', icon: FileText, roles: ['ADMIN', 'MANAGER'] },
            { path: '/audit-logs', label: 'Audit Logs', icon: ShieldAlert, roles: ['ADMIN'] }
        ]},
        { section: 'SYSTEM', items: [
            { path: '/settings', label: 'Settings', icon: Settings, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] }
        ]}
    ];

    const sidebarClass = 'fixed lg:static inset-y-0 left-0 z-50 w-72 bg-white border-r border-gray-200 flex flex-col transition-transform duration-300 ease-in-out shadow-2xl lg:shadow-none ' + (sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0');

    return (
        <div className="flex h-screen bg-[#F8FAFC] text-slate-800 font-sans overflow-hidden">
            <AnimatePresence>
                {sidebarOpen && (
                    <motion.div 
                        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-slate-900/40 z-40 lg:hidden backdrop-blur-sm"
                        onClick={() => setSidebarOpen(false)}
                    />
                )}
            </AnimatePresence>

            <motion.aside className={sidebarClass}>
                <div className="h-20 flex items-center px-6 border-b border-gray-100 bg-white">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-blue-900 flex items-center justify-center shadow-md">
                            <Landmark className="text-white w-6 h-6" />
                        </div>
                        <div>
                            <h1 className="text-[13px] font-bold text-slate-900 leading-tight tracking-wide">Bank Account</h1>
                            <h1 className="text-[13px] font-bold text-slate-900 leading-tight tracking-wide">Management</h1>
                        </div>
                    </div>
                    <button onClick={() => setSidebarOpen(false)} className="ml-auto lg:hidden text-slate-400 hover:text-slate-900">
                        <X size={20} />
                    </button>
                </div>
                
                <div className="flex-1 overflow-y-auto py-6 px-4 space-y-6 custom-scrollbar bg-white">
                    {navItems.map((group, idx) => {
                        const filtered = group.items.filter(item => item.roles.includes(user?.role));
                        if (filtered.length === 0) return null;
                        
                        return (
                            <div key={idx} className="space-y-1">
                                <p className="px-3 text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-3">{group.section}</p>
                                {filtered.map((item) => {
                                    const isActive = location.pathname.startsWith(item.path);
                                    const activeClass = isActive ? 'bg-blue-50 text-blue-800 shadow-sm' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900';
                                    const iconClass = isActive ? 'text-blue-700' : 'text-slate-400';
                                    return (
                                        <Link 
                                            key={item.path} 
                                            to={item.path}
                                            className={'flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium transition-all duration-200 ' + activeClass}
                                        >
                                            <item.icon size={18} className={iconClass} />
                                            <span className="text-sm">{item.label}</span>
                                        </Link>
                                    )
                                })}
                            </div>
                        )
                    })}
                </div>
            </motion.aside>

            <main className="flex-1 flex flex-col h-screen min-w-0">
                <header className="h-20 bg-white/90 backdrop-blur-md border-b border-gray-200 flex items-center justify-between px-6 z-30 sticky top-0 shadow-sm">
                    <div className="flex items-center gap-4">
                        <button onClick={() => setSidebarOpen(true)} className="lg:hidden text-slate-500 hover:text-slate-900 p-2 rounded-md hover:bg-slate-100">
                            <Menu size={20} />
                        </button>
                        <div className="hidden md:flex items-center gap-2 text-slate-500">
                            <span className="text-sm font-medium">Platform</span>
                            <span className="text-slate-300">/</span>
                            <span className="text-sm font-semibold text-slate-900 capitalize">{location.pathname.split('/')[1] || 'Dashboard'}</span>
                        </div>
                    </div>
                    
                    <div className="flex items-center gap-5">
                        <div className="relative hidden sm:block">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
                            <input 
                                type="text" 
                                placeholder="Search accounts, customers..." 
                                className="w-72 pl-10 pr-4 py-2 bg-slate-100 border-transparent focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-100 rounded-xl text-sm transition-all outline-none text-slate-800 placeholder-slate-400"
                            />
                        </div>
                        
                        <div className="h-6 w-px bg-slate-200 mx-2 hidden sm:block"></div>
                        
                        <button className="relative p-2 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-full transition-colors">
                            <Bell size={20} />
                        </button>
                        
                        <div className="relative">
                            <button 
                                onClick={() => setProfileOpen(!profileOpen)}
                                className="flex items-center gap-3 hover:bg-slate-50 p-1.5 rounded-xl transition-colors border border-transparent hover:border-slate-100"
                            >
                                <div className="text-right hidden md:block">
                                    <p className="text-sm font-bold text-slate-900 leading-tight">{user?.username}</p>
                                    <p className="text-[11px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full mt-0.5 inline-block">{user?.role}</p>
                                </div>
                                <div className="w-9 h-9 rounded-full bg-blue-900 flex items-center justify-center text-white font-bold shadow-sm">
                                    {user?.username?.charAt(0).toUpperCase() || 'U'}
                                </div>
                                <ChevronDown size={16} className="text-slate-400" />
                            </button>
                            
                            <AnimatePresence>
                                {profileOpen && (
                                    <motion.div 
                                        initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 10 }}
                                        className="absolute right-0 mt-2 w-56 bg-white border border-gray-100 rounded-xl shadow-lg py-2 z-50"
                                    >
                                        <div className="px-4 py-3 border-b border-gray-50 md:hidden">
                                            <p className="text-sm font-bold text-slate-900">{user?.username}</p>
                                            <p className="text-xs text-slate-500">{user?.role}</p>
                                        </div>
                                        <Link to="/settings" className="flex items-center gap-2 px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-slate-900">
                                            <Settings size={16} /> My Profile
                                        </Link>
                                        <button 
                                            onClick={handleLogout}
                                            className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 text-left"
                                        >
                                            <LogOut size={16} /> Logout
                                        </button>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </div>
                    </div>
                </header>
                
                <div className="flex-1 overflow-auto p-6 md:p-8 relative z-0">
                    <ErrorBoundary>
                        <AnimatePresence mode="wait">
                            <motion.div
                                key={location.pathname}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                transition={{ duration: 0.2 }}
                                className="h-full max-w-[1600px] mx-auto"
                            >
                                <Outlet />
                            </motion.div>
                        </AnimatePresence>
                    </ErrorBoundary>
                </div>
            </main>
        </div>
    );
}
'''

# 3. Dashboard.jsx update
dashboard_page = '''
import { useState, useEffect, useContext } from 'react';
import { Users, CreditCard, Activity, Briefcase, FileQuestion } from 'lucide-react';
import api from '../services/api';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function Dashboard() {
    const { user } = useContext(AuthContext);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [stats, setStats] = useState(null);

    const fetchStats = async () => {
        setLoading(true);
        setError(null);
        try {
            // Attempt to fetch real aggregate stats if available.
            // If the backend doesn't support it, we handle the error gracefully.
            const res = await api.get('/api/health'); 
            
            // If the health endpoint exists but doesn't return business data, 
            // we do NOT fabricate it.
            setStats(res.data?.stats || null);
        } catch (err) {
            // Backend endpoint doesn't exist or failed
            setStats(null);
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
                <div className="h-96 bg-slate-200 rounded-2xl"></div>
            </div>
        );
    }

    const cards = [
        { title: 'Total Accounts', value: stats?.accounts, icon: CreditCard, color: 'bg-blue-50 text-blue-600' },
        { title: 'Customers', value: stats?.customers, icon: Users, color: 'bg-indigo-50 text-indigo-600' },
        { title: 'Transactions', value: stats?.transactions, icon: Activity, color: 'bg-emerald-50 text-emerald-600' },
        { title: 'Active Employees', value: stats?.employees, icon: Briefcase, color: 'bg-amber-50 text-amber-600' }
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
            
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {cards.map((card, idx) => (
                    <div key={idx} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-sm font-semibold text-slate-500">{card.title}</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">
                                    {card.value !== undefined && card.value !== null ? card.value.toLocaleString() : '—'}
                                </h3>
                            </div>
                            <div className={p-3 rounded-xl }>
                                <card.icon size={24} />
                            </div>
                        </div>
                        <p className="text-xs text-slate-400 font-medium mt-4">
                            {card.value !== undefined && card.value !== null ? 'Current real-time total' : 'Data unavailable'}
                        </p>
                    </div>
                ))}
            </div>

            {/* Empty Analytics State */}
            <div className="bg-white p-12 rounded-2xl border border-slate-100 shadow-sm text-center flex flex-col items-center">
                <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-6">
                    <Activity className="w-10 h-10 text-slate-300" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">Analytics data is not available yet</h3>
                <p className="text-slate-500 max-w-md mx-auto mb-8">
                    Detailed financial charting and aggregate transaction insights will appear here once the reporting engine is fully connected to the backend.
                </p>
                <div className="flex gap-4 justify-center">
                    <Link to="/accounts" className="px-6 py-2.5 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 rounded-xl font-medium transition-colors">
                        View Accounts
                    </Link>
                    <Link to="/customers" className="px-6 py-2.5 bg-blue-900 text-white hover:bg-blue-800 rounded-xl font-medium transition-colors">
                        Manage Customers
                    </Link>
                </div>
            </div>
        </div>
    );
}
'''

# 4. Standard Reusable Empty/Placeholder Page
placeholder_page = '''
import { FileQuestion, Search } from 'lucide-react';

export default function {name}() {
    return (
        <div className="space-y-6 h-full flex flex-col">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">{name}</h1>
                    <p className="text-slate-500 mt-1">Manage and monitor {name.toLowerCase()}.</p>
                </div>
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
                    <input 
                        type="text" 
                        placeholder="Search {name.toLowerCase()}..." 
                        className="w-full sm:w-64 pl-10 pr-4 py-2 bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 rounded-lg text-sm transition-all outline-none"
                    />
                </div>
            </div>
            
            <div className="flex-1 bg-white p-12 rounded-2xl border border-slate-100 shadow-sm text-center flex flex-col items-center justify-center min-h-[400px]">
                <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                    <FileQuestion className="w-8 h-8 text-slate-400" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">{name} data is not available</h3>
                <p className="text-slate-500 max-w-md">
                    The {name.toLowerCase()} listing requires integration with the core backend API endpoints which are currently under development.
                </p>
            </div>
        </div>
    );
}
'''

write_file('frontend/src/components/ErrorBoundary.jsx', error_boundary)
write_file('frontend/src/layouts/MainLayout.jsx', main_layout)
write_file('frontend/src/pages/Dashboard.jsx', dashboard_page)

pages = ['Accounts', 'Customers', 'Transactions', 'Employees', 'Branches', 'Reports', 'AuditLogs', 'Settings']
for page in pages:
    write_file(f'frontend/src/pages/{page}.jsx', placeholder_page.replace('{name}', page))

print("Scaffolded new layouts and pages.")
