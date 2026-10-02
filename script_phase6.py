import os

src_dir = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\src'

files = {
    'styles/theme.css': '''
:root {
  --bg-primary: #f8fafc;
  --bg-secondary: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --accent-electric: #0ea5e9;
  --accent-purple: #8b5cf6;
}
.dark {
  --bg-primary: #0a192f;
  --bg-secondary: #112240;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --accent-electric: #64ffda;
  --accent-purple: #6b46c1;
}
body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
}
''',
    'layouts/MainLayout.jsx': '''import { Outlet, Link } from 'react-router-dom';
import { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { Bell, Search, Moon, Sun, User, Database, Home, Users, CreditCard, Activity, Landmark, ShieldAlert, FileText, Settings, LogOut } from 'lucide-react';

export default function MainLayout() {
    const { user, logout } = useContext(AuthContext);
    const [darkMode, setDarkMode] = useState(true);

    const toggleTheme = () => {
        setDarkMode(!darkMode);
        document.documentElement.classList.toggle('dark');
    };

    return (
        <div className={lex min-h-screen  bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans}>
            {/* Sidebar */}
            <motion.aside initial={{ x: -200 }} animate={{ x: 0 }} className="w-64 bg-[var(--bg-secondary)] border-r border-gray-800 p-5 flex flex-col">
                <div className="flex items-center gap-3 mb-10 text-[var(--accent-electric)]">
                    <Database size={32} />
                    <h1 className="text-2xl font-bold tracking-widest">BANKX</h1>
                </div>
                
                <nav className="flex-1 space-y-6 overflow-y-auto">
                    <div>
                        <p className="text-xs text-gray-500 mb-2 uppercase tracking-wider">Overview</p>
                        <Link to="/dashboard" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 hover:text-[var(--accent-electric)] transition"><Home size={18} /> Dashboard</Link>
                    </div>
                    <div>
                        <p className="text-xs text-gray-500 mb-2 uppercase tracking-wider">Banking</p>
                        <Link to="/customers" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition"><Users size={18} /> Customers</Link>
                        <Link to="/accounts" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition"><CreditCard size={18} /> Accounts</Link>
                        <Link to="/transactions" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition"><Activity size={18} /> Transactions</Link>
                        <Link to="/loans" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition"><Landmark size={18} /> Loans</Link>
                    </div>
                    {(user?.role === 'ADMIN' || user?.role === 'MANAGER') && (
                        <div>
                            <p className="text-xs text-gray-500 mb-2 uppercase tracking-wider">Management</p>
                            <Link to="/branches" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition"><Database size={18} /> Branches</Link>
                            <Link to="/employees" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition"><User size={18} /> Employees</Link>
                        </div>
                    )}
                    <div>
                        <p className="text-xs text-gray-500 mb-2 uppercase tracking-wider">Security</p>
                        <Link to="/database-visualizer" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition"><Database size={18} /> DB Architecture</Link>
                        {user?.role === 'ADMIN' && <Link to="/audit-logs" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition"><ShieldAlert size={18} /> Audit Logs</Link>}
                    </div>
                </nav>
                <div className="pt-5 border-t border-gray-800">
                    <button onClick={logout} className="flex items-center gap-3 p-2 w-full text-left text-red-400 hover:bg-gray-800 rounded transition"><LogOut size={18} /> Logout</button>
                </div>
            </motion.aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col h-screen overflow-hidden">
                {/* Top Nav */}
                <header className="h-16 bg-[var(--bg-secondary)] border-b border-gray-800 flex items-center justify-between px-8">
                    <div className="flex items-center bg-gray-800/50 rounded-lg px-3 py-1.5 w-96 border border-gray-700">
                        <Search size={18} className="text-gray-400 mr-2" />
                        <input type="text" placeholder="Global search..." className="bg-transparent border-none outline-none text-sm w-full" />
                    </div>
                    <div className="flex items-center gap-6">
                        <button onClick={toggleTheme} className="text-gray-400 hover:text-white transition">
                            {darkMode ? <Sun size={20} /> : <Moon size={20} />}
                        </button>
                        <Bell size={20} className="text-gray-400 hover:text-white cursor-pointer transition" />
                        <div className="flex items-center gap-3 border-l border-gray-700 pl-6">
                            <div className="w-8 h-8 rounded-full bg-[var(--accent-purple)] flex items-center justify-center font-bold">
                                {user?.username?.charAt(0).toUpperCase()}
                            </div>
                            <div className="text-sm">
                                <p className="font-semibold">{user?.username}</p>
                                <p className="text-xs text-[var(--accent-electric)]">{user?.role}</p>
                            </div>
                        </div>
                    </div>
                </header>
                <div className="flex-1 overflow-auto p-8 bg-[var(--bg-primary)]">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
''',
    'pages/Dashboard.jsx': '''import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import api from '../services/api';
import { Users, CreditCard, Activity, Landmark, DollarSign } from 'lucide-react';

export default function Dashboard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch real data from API. Mocking fetch logic for demo.
        api.get('/api/health').then(() => {
            setStats({
                customers: 2450, accounts: 3100, balance: 12500000, 
                transactions: 45000, loans: 120,
                trend: [{ name: 'Jan', val: 400 }, { name: 'Feb', val: 600 }, { name: 'Mar', val: 800 }]
            });
            setLoading(false);
        }).catch(() => setLoading(false));
    }, []);

    if (loading) return <div className="animate-pulse flex gap-4"><div className="h-32 w-1/4 bg-gray-800 rounded"></div></div>;

    const cards = [
        { title: 'Total Customers', value: stats?.customers, icon: Users, color: 'text-blue-400' },
        { title: 'Total Accounts', value: stats?.accounts, icon: CreditCard, color: 'text-green-400' },
        { title: 'Total Balance', value: $, icon: DollarSign, color: 'text-[var(--accent-electric)]' },
        { title: 'Transactions', value: stats?.transactions, icon: Activity, color: 'text-purple-400' },
        { title: 'Active Loans', value: stats?.loans, icon: Landmark, color: 'text-orange-400' },
    ];

    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
            <h1 className="text-3xl font-bold tracking-tight">Banking Intelligence Overview</h1>
            
            {/* KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
                {cards.map((c, i) => (
                    <motion.div key={i} whileHover={{ y: -5 }} className="bg-[var(--bg-secondary)] p-6 rounded-xl border border-gray-800 shadow-lg relative overflow-hidden">
                        <div className="flex justify-between items-start mb-4">
                            <p className="text-gray-400 text-sm font-medium">{c.title}</p>
                            <c.icon size={20} className={c.color} />
                        </div>
                        <h3 className="text-2xl font-bold">{c.value}</h3>
                        <div className={bsolute -bottom-4 -right-4 opacity-10}><c.icon size={100} /></div>
                    </motion.div>
                ))}
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-[var(--bg-secondary)] p-6 rounded-xl border border-gray-800 shadow-lg">
                    <h3 className="text-lg font-semibold mb-6">Transaction Trend</h3>
                    <div className="h-72">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={stats?.trend}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                <XAxis dataKey="name" stroke="#9ca3af" />
                                <YAxis stroke="#9ca3af" />
                                <Tooltip contentStyle={{ backgroundColor: '#112240', border: 'none' }} />
                                <Line type="monotone" dataKey="val" stroke="var(--accent-electric)" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
                
                <div className="bg-[var(--bg-secondary)] p-6 rounded-xl border border-gray-800 shadow-lg">
                    <h3 className="text-lg font-semibold mb-6">Database-Driven Insights</h3>
                    <div className="space-y-4">
                        <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700 flex justify-between items-center">
                            <span>High-Value Transactions (Today)</span>
                            <span className="text-[var(--accent-electric)] font-bold">12</span>
                        </div>
                        <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700 flex justify-between items-center">
                            <span>Customers with Multiple Accounts</span>
                            <span className="text-purple-400 font-bold">18%</span>
                        </div>
                        <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700 flex justify-between items-center">
                            <span>Branch with Highest Volume</span>
                            <span className="text-green-400 font-bold">Downtown Main</span>
                        </div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
''',
    'pages/DatabaseVisualizer.jsx': '''import { motion } from 'framer-motion';
import { Database, User, CreditCard, Activity, Landmark, Briefcase } from 'lucide-react';

export default function DatabaseVisualizer() {
    const nodes = [
        { id: 'customer', label: 'CUSTOMER', icon: User, x: 50, y: 50 },
        { id: 'account', label: 'ACCOUNT', icon: CreditCard, x: 250, y: 150 },
        { id: 'transaction', label: 'TRANSACTION', icon: Activity, x: 450, y: 250 },
        { id: 'branch', label: 'BRANCH', icon: Database, x: 250, y: 350 },
        { id: 'employee', label: 'EMPLOYEE', icon: Briefcase, x: 50, y: 350 },
        { id: 'loan', label: 'LOAN', icon: Landmark, x: 50, y: 150 },
    ];

    return (
        <div className="h-full flex flex-col">
            <h1 className="text-3xl font-bold tracking-tight mb-4 text-[var(--accent-electric)]">Database Architecture</h1>
            <p className="text-gray-400 mb-8">Interactive visualization of the BANKX relational database schema.</p>
            
            <div className="flex-1 bg-[var(--bg-secondary)] rounded-xl border border-gray-800 relative overflow-hidden flex items-center justify-center p-10">
                <div className="relative w-[600px] h-[500px]">
                    {/* SVG Lines for Relationships */}
                    <svg className="absolute inset-0 w-full h-full pointer-events-none">
                        <line x1="100" y1="100" x2="250" y2="150" stroke="#374151" strokeWidth="2" strokeDasharray="5,5" />
                        <line x1="300" y1="200" x2="450" y2="250" stroke="#374151" strokeWidth="2" />
                        <line x1="250" y1="350" x2="250" y2="200" stroke="#374151" strokeWidth="2" />
                        <line x1="250" y1="350" x2="100" y2="350" stroke="#374151" strokeWidth="2" />
                        <line x1="100" y1="100" x2="100" y2="150" stroke="#374151" strokeWidth="2" />
                    </svg>
                    
                    {/* Nodes */}
                    {nodes.map(n => (
                        <motion.div 
                            key={n.id} 
                            whileHover={{ scale: 1.1, boxShadow: '0 0 20px rgba(100,255,218,0.3)' }}
                            className="absolute bg-gray-900 border border-[var(--accent-electric)] p-4 rounded-xl flex flex-col items-center justify-center w-32 h-32 cursor-pointer shadow-lg shadow-[var(--accent-electric)]/10"
                            style={{ left: n.x, top: n.y }}
                        >
                            <n.icon size={32} className="text-[var(--accent-purple)] mb-2" />
                            <span className="text-xs font-bold tracking-wider">{n.label}</span>
                        </motion.div>
                    ))}
                </div>
            </div>
        </div>
    );
}
'''
}

for filename, content in files.items():
    filepath = os.path.join(src_dir, filename.replace('/', os.sep))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

print("Phase 6 advanced UI components created.")
