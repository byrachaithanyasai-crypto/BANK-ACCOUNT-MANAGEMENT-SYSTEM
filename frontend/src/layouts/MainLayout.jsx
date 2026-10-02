import React, { useContext, useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';
import { ErrorBoundary } from '../components/ErrorBoundary';
import { 
    LayoutDashboard, 
    Users, 
    CreditCard, 
    Activity, 
    Briefcase, 
    Building2, 
    PieChart, 
    ShieldAlert, 
    Settings, 
    LogOut,
    Menu,
    X,
    Bell,
    Search,
    ChevronDown
} from 'lucide-react';

export default function MainLayout() {
    const { user, logout } = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate();
    const [globalSearch, setGlobalSearch] = useState('');
    const handleGlobalSearch = (e) => { 
        if(e.key === 'Enter' && globalSearch.trim()) navigate('/search?q=' + encodeURIComponent(globalSearch.trim())); 
    };
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [profileOpen, setProfileOpen] = useState(false);

    const handleLogout = () => {
        logout();
    };

    const navItems = [
        {
            section: "Overview",
            items: [
                { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] }
            ]
        },
        {
            section: "Banking",
            items: [
                { path: '/accounts', label: 'Accounts', icon: CreditCard, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
                { path: '/customers', label: 'Customers', icon: Users, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] },
                { path: '/transactions', label: 'Transactions', icon: Activity, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] }
            ]
        },
        {
            section: "Operations",
            items: [
                { path: '/employees', label: 'Employees', icon: Briefcase, roles: ['ADMIN'] },
                { path: '/branches', label: 'Branches', icon: Building2, roles: ['ADMIN'] }
            ]
        },
        {
            section: "Insights",
            items: [
                { path: '/reports', label: 'Reports', icon: PieChart, roles: ['ADMIN', 'MANAGER'] },
                
            ]
        },
        {
            section: "System",
            items: [
                { path: '/settings', label: 'Settings', icon: Settings, roles: ['ADMIN', 'MANAGER', 'EMPLOYEE'] }
            ]
        }
    ];

    return (
        <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
            <AnimatePresence>
                {sidebarOpen && (
                    <motion.div 
                        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-slate-900/50 z-40 lg:hidden backdrop-blur-sm"
                        onClick={() => setSidebarOpen(false)}
                    />
                )}
            </AnimatePresence>

            <motion.aside 
                className={`fixed lg:static inset-y-0 left-0 z-50 w-72 bg-white border-r border-slate-200 flex flex-col transform transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}
            >
                <div className="h-20 flex items-center px-6 border-b border-slate-200 bg-white">
                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
                            <ShieldAlert className="text-white w-5 h-5" />
                        </div>
                        <span className="text-xl font-black text-slate-900 tracking-tight">Bank Account Management System</span>
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
                <header className="h-20 bg-white/90 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-6 z-30 sticky top-0 shadow-sm">
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
                                value={globalSearch}
                                onChange={(e) => setGlobalSearch(e.target.value)}
                                onKeyDown={handleGlobalSearch}
                                placeholder="Search accounts, customers... (Press Enter)" 
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
                                        className="absolute right-0 mt-2 w-56 bg-white border border-slate-100 rounded-xl shadow-lg py-2 z-50"
                                    >
                                        <div className="px-4 py-3 border-b border-slate-50 md:hidden">
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



