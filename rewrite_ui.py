import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. MainLayout.jsx
main_layout = '''
import { useState, useContext, useEffect } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { AuthContext } from '../context/AuthContext';
import { 
    LayoutDashboard, Users, CreditCard, Activity, Building, 
    Briefcase, FileText, ShieldAlert, Settings, LogOut, 
    Menu, X, Search, Bell, Landmark 
} from 'lucide-react';

export default function MainLayout() {
    const { user, logout } = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate();
    const [sidebarOpen, setSidebarOpen] = useState(false);

    // Close sidebar on mobile when navigating
    useEffect(() => {
        setSidebarOpen(false);
    }, [location]);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const navItems = [
        { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
        { path: '/accounts', label: 'Accounts', icon: CreditCard, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
        { path: '/customers', label: 'Customers', icon: Users, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
        { path: '/transactions', label: 'Transactions', icon: Activity, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
        { path: '/employees', label: 'Employees', icon: Briefcase, roles: ['ADMIN'] },
        { path: '/branches', label: 'Branches', icon: Building, roles: ['ADMIN'] },
        { path: '/reports', label: 'Reports', icon: FileText, roles: ['ADMIN', 'MANAGER'] },
        { path: '/audit-logs', label: 'Audit Logs', icon: ShieldAlert, roles: ['ADMIN'] },
        { path: '/settings', label: 'Settings', icon: Settings, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
    ];

    const filteredNav = navItems.filter(item => item.roles.includes(user?.role));

    return (
        <div className="flex h-screen bg-[#F3F4F6] text-gray-900 font-sans overflow-hidden">
            {/* Mobile Sidebar Overlay */}
            <AnimatePresence>
                {sidebarOpen && (
                    <motion.div 
                        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-gray-900/50 z-40 lg:hidden backdrop-blur-sm"
                        onClick={() => setSidebarOpen(false)}
                    />
                )}
            </AnimatePresence>

            {/* Sidebar */}
            <motion.aside 
                className={ixed lg:static inset-y-0 left-0 z-50 w-72 bg-white border-r border-gray-200 flex flex-col transition-transform duration-300 ease-in-out shadow-xl lg:shadow-none }
            >
                <div className="h-20 flex items-center px-6 border-b border-gray-100">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
                            <Landmark className="text-white w-6 h-6" />
                        </div>
                        <div>
                            <h1 className="text-sm font-bold text-gray-900 leading-tight">Bank Account</h1>
                            <h1 className="text-sm font-bold text-gray-900 leading-tight">Management</h1>
                        </div>
                    </div>
                    <button onClick={() => setSidebarOpen(false)} className="ml-auto lg:hidden text-gray-500 hover:text-gray-900">
                        <X size={20} />
                    </button>
                </div>
                
                <div className="flex-1 overflow-y-auto py-6 px-4 space-y-1 custom-scrollbar">
                    <p className="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Navigation</p>
                    {filteredNav.map((item) => {
                        const isActive = location.pathname.startsWith(item.path);
                        return (
                            <Link 
                                key={item.path} 
                                to={item.path}
                                className={lex items-center gap-3 px-3 py-2.5 rounded-lg font-medium transition-all duration-200 }
                            >
                                <item.icon size={20} className={isActive ? 'text-blue-600' : 'text-gray-400'} />
                                {item.label}
                            </Link>
                        )
                    })}
                </div>

                <div className="p-4 border-t border-gray-100">
                    <div className="bg-gray-50 rounded-xl p-4 flex flex-col gap-3 border border-gray-100">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold">
                                {user?.username?.charAt(0).toUpperCase() || 'U'}
                            </div>
                            <div className="overflow-hidden">
                                <p className="text-sm font-bold text-gray-900 truncate">{user?.username}</p>
                                <p className="text-xs font-medium text-gray-500 truncate">{user?.role}</p>
                            </div>
                        </div>
                        <button 
                            onClick={handleLogout}
                            className="w-full flex items-center justify-center gap-2 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                        >
                            <LogOut size={16} /> Logout
                        </button>
                    </div>
                </div>
            </motion.aside>

            {/* Main Content Area */}
            <main className="flex-1 flex flex-col h-screen min-w-0">
                {/* Header */}
                <header className="h-20 bg-white/80 backdrop-blur-md border-b border-gray-200 flex items-center justify-between px-6 z-30 sticky top-0">
                    <div className="flex items-center gap-4">
                        <button onClick={() => setSidebarOpen(true)} className="lg:hidden text-gray-500 hover:text-gray-900 p-2 rounded-md hover:bg-gray-100">
                            <Menu size={20} />
                        </button>
                        <div className="hidden md:flex items-center gap-2 text-gray-500">
                            <span className="text-sm font-medium">Platform</span>
                            <span className="text-gray-300">/</span>
                            <span className="text-sm font-semibold text-gray-900 capitalize">{location.pathname.split('/')[1] || 'Dashboard'}</span>
                        </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                        <div className="relative hidden sm:block">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
                            <input 
                                type="text" 
                                placeholder="Search..." 
                                className="w-64 pl-10 pr-4 py-2 bg-gray-100 border-transparent focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 rounded-lg text-sm transition-all outline-none"
                            />
                        </div>
                        <button className="relative p-2 text-gray-500 hover:text-gray-900 hover:bg-gray-100 rounded-full transition-colors">
                            <Bell size={20} />
                            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                        </button>
                    </div>
                </header>
                
                {/* Scrollable Content */}
                <div className="flex-1 overflow-auto p-6 md:p-8 relative z-0">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={location.pathname}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            transition={{ duration: 0.2 }}
                            className="h-full max-w-7xl mx-auto"
                        >
                            <Outlet />
                        </motion.div>
                    </AnimatePresence>
                </div>
            </main>
        </div>
    );
}
'''

# 2. Dashboard.jsx
dashboard_page = '''
import { useState, useEffect, useContext } from 'react';
import { Users, CreditCard, Activity, TrendingUp, AlertCircle } from 'lucide-react';
import api from '../services/api';
import { AuthContext } from '../context/AuthContext';

export default function Dashboard() {
    const { user } = useContext(AuthContext);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [stats, setStats] = useState(null);

    const fetchStats = async () => {
        setLoading(true);
        setError(null);
        try {
            // Placeholder simulation since specific analytical APIs don't exist yet
            // In a real app, this would be an actual API call.
            await api.get('/api/health'); 
            setStats({
                accounts: 1420,
                customers: 1250,
                transactions: 8430,
                active_branches: 5
            });
        } catch (err) {
            setError('Unable to load dashboard data.');
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
            <div className="space-y-6 animate-pulse">
                <div className="h-8 bg-gray-200 rounded w-1/4"></div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {[...Array(4)].map((_, i) => <div key={i} className="h-32 bg-gray-200 rounded-xl"></div>)}
                </div>
                <div className="h-96 bg-gray-200 rounded-xl"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center h-64 bg-white rounded-xl border border-gray-200">
                <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{error}</h3>
                <button onClick={fetchStats} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">Retry</button>
            </div>
        );
    }

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">{greeting()}, {user?.username}</h1>
                <p className="text-gray-500 mt-1">Here's an overview of your banking operations.</p>
            </div>
            
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-sm font-medium text-gray-500">Total Accounts</p>
                            <h3 className="text-3xl font-bold text-gray-900 mt-2">{stats?.accounts.toLocaleString()}</h3>
                        </div>
                        <div className="p-3 bg-blue-50 text-blue-600 rounded-xl">
                            <CreditCard size={24} />
                        </div>
                    </div>
                    <p className="text-xs text-green-600 font-medium mt-4 flex items-center gap-1"><TrendingUp size={14}/> +12% this month</p>
                </div>
                <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-sm font-medium text-gray-500">Total Customers</p>
                            <h3 className="text-3xl font-bold text-gray-900 mt-2">{stats?.customers.toLocaleString()}</h3>
                        </div>
                        <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
                            <Users size={24} />
                        </div>
                    </div>
                    <p className="text-xs text-green-600 font-medium mt-4 flex items-center gap-1"><TrendingUp size={14}/> +8% this month</p>
                </div>
                <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-sm font-medium text-gray-500">Total Transactions</p>
                            <h3 className="text-3xl font-bold text-gray-900 mt-2">{stats?.transactions.toLocaleString()}</h3>
                        </div>
                        <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
                            <Activity size={24} />
                        </div>
                    </div>
                    <p className="text-xs text-gray-500 font-medium mt-4">Across all active branches</p>
                </div>
                <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-sm font-medium text-gray-500">Active Branches</p>
                            <h3 className="text-3xl font-bold text-gray-900 mt-2">{stats?.active_branches}</h3>
                        </div>
                        <div className="p-3 bg-amber-50 text-amber-600 rounded-xl">
                            <Landmark size={24} />
                        </div>
                    </div>
                    <p className="text-xs text-gray-500 font-medium mt-4">Operational status normal</p>
                </div>
            </div>

            {/* Empty Analytics State */}
            <div className="bg-white p-8 rounded-2xl border border-gray-100 shadow-sm text-center">
                <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Activity className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No analytics data available yet.</h3>
                <p className="text-gray-500 max-w-sm mx-auto">Detailed financial charting will appear here once the reporting engine accumulates sufficient transactional history.</p>
            </div>
        </div>
    );
}
'''

# 3. Placeholder Page components
placeholder_page = '''
import { FileQuestion } from 'lucide-react';

export default function {name}() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">{name}</h1>
                <p className="text-gray-500 mt-1">Manage and monitor {name.toLowerCase()}.</p>
            </div>
            <div className="bg-white p-12 rounded-2xl border border-gray-100 shadow-sm text-center flex flex-col items-center">
                <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
                    <FileQuestion className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Module Not Configured</h3>
                <p className="text-gray-500 max-w-md">The {name.toLowerCase()} view requires integration with the core backend API endpoints which are currently in development.</p>
            </div>
        </div>
    );
}
'''

# 4. App.jsx (Routing cleanup)
app_jsx = '''
import { Routes, Route, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './context/AuthContext';

import MainLayout from './layouts/MainLayout';
import AuthLayout from './layouts/AuthLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

// Dynamically created Placeholders
import Accounts from './pages/Accounts';
import Customers from './pages/Customers';
import Transactions from './pages/Transactions';
import Employees from './pages/Employees';
import Branches from './pages/Branches';
import Reports from './pages/Reports';
import AuditLogs from './pages/AuditLogs';
import Settings from './pages/Settings';

const ProtectedRoute = ({ children }) => {
    const { user, loading } = useContext(AuthContext);
    
    if (loading) {
        return (
            <div className="h-screen flex flex-col items-center justify-center bg-gray-50">
                <div className="w-12 h-12 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>
                <p className="mt-4 text-gray-500 font-medium text-sm">Verifying Session...</p>
            </div>
        );
    }
    
    return user ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/login" element={<Login />} />
      
      <Route element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/accounts" element={<Accounts />} />
        <Route path="/customers" element={<Customers />} />
        <Route path="/transactions" element={<Transactions />} />
        <Route path="/employees" element={<Employees />} />
        <Route path="/branches" element={<Branches />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/audit-logs" element={<AuditLogs />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

export default App;
'''

# Create files
write_file('frontend/src/layouts/MainLayout.jsx', main_layout)
write_file('frontend/src/pages/Dashboard.jsx', dashboard_page)
write_file('frontend/src/App.jsx', app_jsx)

pages = ['Accounts', 'Customers', 'Transactions', 'Employees', 'Branches', 'Reports', 'AuditLogs', 'Settings']
for page in pages:
    write_file(f'frontend/src/pages/{page}.jsx', placeholder_page.replace('{name}', page))

print("Files generated.")
