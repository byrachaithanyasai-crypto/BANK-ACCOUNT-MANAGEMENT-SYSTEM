import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Search, Home, Users, CreditCard, Activity, Landmark, Database, User, ShieldAlert } from 'lucide-react';

export default function CommandPalette({ isOpen, setIsOpen }) {
    const navigate = useNavigate();
    const [query, setQuery] = useState('');

    const commands = [
        { name: 'Go to Dashboard', path: '/dashboard', icon: Home },
        { name: 'Customers', path: '/customers', icon: Users },
        { name: 'Accounts', path: '/accounts', icon: CreditCard },
        { name: 'Transactions', path: '/transactions', icon: Activity },
        { name: 'Loans', path: '/loans', icon: Landmark },
        { name: 'Branches', path: '/branches', icon: Database },
        { name: 'Employees', path: '/employees', icon: User },
        { name: 'Audit Logs', path: '/audit-logs', icon: ShieldAlert },
    ];

    const filtered = commands.filter(c => c.name.toLowerCase().includes(query.toLowerCase()));

    useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                setIsOpen(open => !open);
            }
            if (e.key === 'Escape') setIsOpen(false);
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [setIsOpen]);

    return (
        <AnimatePresence>
            {isOpen && (
                <div className="fixed inset-0 z-[100] flex items-start justify-center pt-[20vh] px-4">
                    <motion.div 
                        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-navy-900/80 backdrop-blur-sm"
                        onClick={() => setIsOpen(false)}
                    />
                    <motion.div 
                        initial={{ opacity: 0, scale: 0.95, y: -20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: -20 }}
                        className="relative w-full max-w-2xl bg-[var(--bg-secondary)] border border-gray-700 rounded-xl shadow-2xl overflow-hidden"
                    >
                        <div className="flex items-center px-4 py-3 border-b border-gray-700">
                            <Search className="text-gray-400 mr-3" size={20} />
                            <input 
                                autoFocus
                                type="text"
                                className="w-full bg-transparent text-white outline-none placeholder-gray-500"
                                placeholder="Search commands, resources, or customers... (Esc to close)"
                                value={query}
                                onChange={e => setQuery(e.target.value)}
                            />
                        </div>
                        <div className="max-h-96 overflow-y-auto p-2">
                            {filtered.length === 0 ? (
                                <div className="p-4 text-center text-gray-500">No results found.</div>
                            ) : (
                                filtered.map((cmd, i) => (
                                    <button 
                                        key={i}
                                        onClick={() => { navigate(cmd.path); setIsOpen(false); }}
                                        className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-[var(--accent-electric)]/10 hover:text-[var(--accent-electric)] transition text-left"
                                    >
                                        <cmd.icon size={18} />
                                        <span>{cmd.name}</span>
                                    </button>
                                ))
                            )}
                        </div>
                    </motion.div>
                </div>
            )}
        </AnimatePresence>
    );
}
