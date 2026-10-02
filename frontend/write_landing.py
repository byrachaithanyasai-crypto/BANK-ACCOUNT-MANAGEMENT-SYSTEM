import os

filepath = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\src\pages\Landing.jsx'

landing_jsx = '''import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Database, Shield, Activity, Users, Landmark, FileText, Server, Lock, Network, ChevronRight } from 'lucide-react';

export default function Landing() {
    const features = [
        { icon: Shield, title: 'Secure Banking', desc: 'Robust JWT authentication and RBAC-driven access control.' },
        { icon: Activity, title: 'Transaction Management', desc: 'ACID-compliant operations enforced by MySQL Stored Procedures.' },
        { icon: Users, title: 'Customer 360', desc: 'Comprehensive unified profiles mapping accounts, loans, and history.' },
        { icon: Landmark, title: 'Loan Management', desc: 'Detailed tracking of principals, interest, and EMI analytics.' },
        { icon: Database, title: 'Branch Analytics', desc: 'Aggregated financial oversight and relational branch mapping.' },
        { icon: FileText, title: 'Audit & Alerts', desc: 'Automated database triggers capturing critical system events.' }
    ];

    const nodes = [
        { label: 'CUSTOMER', x: '50%', y: '10%' },
        { label: 'ACCOUNT', x: '90%', y: '35%' },
        { label: 'TRANSACTION', x: '75%', y: '85%' },
        { label: 'LOAN', x: '25%', y: '85%' },
        { label: 'BRANCH', x: '10%', y: '35%' },
    ];

    return (
        <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans overflow-x-hidden relative">
            
            {/* Background Particles */}
            {Array.from({ length: 20 }).map((_, i) => (
                <div key={i} className="particle" style={{
                    width: Math.random() * 4 + 2 + 'px',
                    height: Math.random() * 4 + 2 + 'px',
                    left: Math.random() * 100 + 'vw',
                    top: Math.random() * 100 + 100 + 'vh',
                    animationDuration: Math.random() * 10 + 15 + 's',
                    animationDelay: Math.random() * 5 + 's'
                }} />
            ))}

            {/* Premium Sticky Navbar */}
            <header className="fixed top-0 w-full z-50 glass-panel border-x-0 border-t-0">
                <div className="container mx-auto px-8 py-5 flex justify-between items-center">
                    <div className="flex items-center gap-3 text-white group cursor-pointer">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--accent-electric)] to-[var(--accent-purple)] flex items-center justify-center shadow-lg shadow-[var(--accent-electric)]/20 group-hover:scale-110 transition-transform">
                            <Database size={20} className="text-navy-900" />
                        </div>
                        <div>
                            <span className="text-xl font-extrabold tracking-widest block leading-tight">BANKX</span>
                            <span className="text-[10px] text-[var(--accent-electric)] font-mono uppercase tracking-widest block leading-tight">DBMS Intelligence</span>
                        </div>
                    </div>
                    <nav className="hidden md:flex gap-10 text-sm font-semibold text-gray-400">
                        <a href="#features" className="hover:text-white transition hover:-translate-y-0.5">Core Features</a>
                        <a href="#technology" className="hover:text-white transition hover:-translate-y-0.5">Architecture</a>
                        <a href="#security" className="hover:text-white transition hover:-translate-y-0.5">Security Protocol</a>
                    </nav>
                    <Link to="/login" className="relative group px-6 py-2.5 rounded-full bg-white/5 border border-white/10 hover:border-[var(--accent-electric)] transition-all overflow-hidden">
                        <div className="absolute inset-0 bg-gradient-to-r from-[var(--accent-electric)] to-[var(--accent-purple)] opacity-0 group-hover:opacity-20 transition-opacity"></div>
                        <span className="relative font-bold text-sm text-white group-hover:text-[var(--accent-electric)] flex items-center gap-2">
                            Login to Portal <ChevronRight size={16} />
                        </span>
                    </Link>
                </div>
                <div className="h-[1px] w-full bg-gradient-to-r from-transparent via-[var(--accent-electric)] to-transparent opacity-20"></div>
            </header>

            {/* WOW Hero Section */}
            <section className="relative pt-40 pb-32 px-6 container mx-auto flex flex-col lg:flex-row items-center gap-16 min-h-screen">
                
                {/* Hero Text */}
                <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, ease: "easeOut" }} className="flex-1 space-y-8 z-10 relative">
                    <div className="inline-flex items-center gap-3 px-4 py-2 glass-card rounded-full border border-[var(--accent-electric)]/30 shadow-[0_0_20px_rgba(100,255,218,0.1)]">
                        <span className="w-2 h-2 rounded-full bg-[var(--accent-electric)] animate-pulse"></span>
                        <span className="text-[10px] font-mono text-[var(--accent-electric)] tracking-widest uppercase">Smart Banking • Database Intelligence</span>
                    </div>
                    
                    <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-[1.1]">
                        Banking,<br />
                        <span className="relative">
                            Re-engineered
                            <span className="absolute -bottom-4 left-0 w-full h-2 bg-gradient-to-r from-[var(--accent-electric)] to-transparent rounded-full opacity-50"></span>
                        </span><br />
                        Around <span className="text-gradient">Data.</span>
                    </h1>
                    
                    <p className="text-xl text-gray-400 max-w-2xl leading-relaxed font-light">
                        A secure, database-driven banking management platform combining relational data integrity, robust transaction processing, and real-time intelligence.
                    </p>
                    
                    <div className="flex gap-6 pt-6">
                        <Link to="/login" className="group relative px-8 py-4 bg-[var(--text-primary)] text-[var(--bg-primary)] rounded-xl font-bold overflow-hidden transition-transform hover:scale-105 shadow-xl shadow-white/10">
                            <div className="absolute inset-0 bg-gradient-to-r from-[var(--accent-electric)] to-white opacity-0 group-hover:opacity-100 transition-opacity"></div>
                            <span className="relative flex items-center gap-2">Access Banking System <ChevronRight size={20} className="group-hover:translate-x-1 transition-transform" /></span>
                        </Link>
                    </div>
                </motion.div>
                
                {/* 3D Database Visualization (CSS/Framer Motion) */}
                <div className="flex-1 relative w-full h-[600px] hidden lg:flex items-center justify-center perspective-[1000px]">
                    <motion.div 
                        animate={{ rotateY: 360 }} 
                        transition={{ duration: 40, repeat: Infinity, ease: "linear" }}
                        className="relative w-96 h-96 transform-style-3d"
                    >
                        {/* Central Glowing Core */}
                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 rounded-full bg-[var(--accent-purple)]/20 blur-2xl animate-pulse"></div>
                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 glass-card rounded-full border-2 border-[var(--accent-electric)] flex flex-col items-center justify-center shadow-[0_0_50px_rgba(100,255,218,0.4)] z-50">
                            <Server size={40} className="text-[var(--accent-electric)] mb-2 drop-shadow-[0_0_10px_rgba(100,255,218,0.8)]" />
                            <span className="font-mono text-xs font-bold text-white tracking-widest">BANKX DB</span>
                        </div>
                        
                        {/* Orbiting Nodes */}
                        {nodes.map((node, i) => {
                            const delay = i * -8;
                            return (
                                <motion.div 
                                    key={i}
                                    className="absolute w-full h-full rounded-full border border-gray-700/30"
                                    style={{ transform: otateZ(deg) rotateX(60deg) }}
                                >
                                    <motion.div 
                                        animate={{ rotateZ: -360 }}
                                        transition={{ duration: 20, repeat: Infinity, ease: "linear", delay }}
                                        className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2"
                                    >
                                        <div className="glass-panel px-4 py-2 rounded-lg border border-[var(--accent-electric)]/50 shadow-lg shadow-[var(--accent-purple)]/20 transform rotateX(-60deg) flex items-center gap-2 group hover:border-[var(--accent-electric)] hover:shadow-[0_0_20px_rgba(100,255,218,0.5)] cursor-default transition-all">
                                            <div className="w-2 h-2 rounded-full bg-[var(--accent-electric)] group-hover:animate-ping"></div>
                                            <span className="text-xs font-bold text-white tracking-widest">{node.label}</span>
                                        </div>
                                    </motion.div>
                                </motion.div>
                            )
                        })}
                    </motion.div>

                    {/* Status Panel Overlay */}
                    <motion.div initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 1 }} className="absolute bottom-10 -right-10 glass-panel p-6 rounded-2xl w-64 border-r-4 border-r-[var(--accent-electric)]">
                        <p className="text-[10px] font-mono text-gray-400 tracking-widest mb-4 uppercase">System Architecture</p>
                        <div className="space-y-3">
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-300">Database</span>
                                <span className="font-bold text-white">MySQL 8.0</span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-300">API Gateway</span>
                                <span className="font-bold text-white">FastAPI</span>
                            </div>
                            <div className="flex justify-between items-center text-sm border-t border-gray-800 pt-3">
                                <span className="text-gray-300 flex items-center gap-2"><Lock size={12} className="text-[var(--accent-electric)]"/> Protection</span>
                                <span className="font-bold text-[var(--accent-electric)]">JWT Active</span>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Premium Features Section */}
            <section id="features" className="py-32 relative z-20">
                <div className="container mx-auto px-6">
                    <div className="text-center mb-20">
                        <h2 className="text-4xl md:text-5xl font-black mb-6">Where Banking Meets <br/><span className="text-gradient">Database Intelligence</span></h2>
                        <p className="text-xl text-gray-400 max-w-3xl mx-auto">Relational integrity enforced at the lowest level. BANKX leverages Primary Keys, ACID Transactions, Stored Procedures, and Triggers to guarantee financial data consistency.</p>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {features.map((f, i) => (
                            <motion.div 
                                key={i} 
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: i * 0.1 }}
                                whileHover={{ y: -10, scale: 1.02 }} 
                                className="glass-panel p-8 rounded-2xl group cursor-default relative overflow-hidden"
                            >
                                <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-[var(--accent-electric)]/10 to-transparent rounded-bl-full opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                                <div className="w-14 h-14 bg-gray-900/80 rounded-xl border border-gray-700 flex items-center justify-center mb-8 text-white group-hover:border-[var(--accent-electric)] group-hover:text-[var(--accent-electric)] transition-colors duration-300 shadow-lg">
                                    <f.icon size={28} />
                                </div>
                                <h3 className="text-2xl font-bold mb-4 text-white group-hover:text-[var(--accent-electric)] transition-colors">{f.title}</h3>
                                <p className="text-gray-400 text-base leading-relaxed">{f.desc}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-16 bg-navy-900 border-t border-gray-800 text-center relative z-20">
                <div className="container mx-auto px-6">
                    <Database size={48} className="mx-auto mb-8 text-[var(--accent-electric)] opacity-50" />
                    <h2 className="text-3xl font-black mb-8 text-white">Initiate Secure Session</h2>
                    <Link to="/login" className="inline-block px-10 py-4 bg-[var(--accent-electric)] text-navy-900 rounded-xl font-bold hover:shadow-[0_0_30px_rgba(100,255,218,0.5)] transition-all hover:scale-105">
                        Access Banking Portal
                    </Link>
                    <p className="mt-16 text-sm font-mono text-gray-600 tracking-widest uppercase">2026 BANKX DBMS Capstone. ACID Integrity Enforced.</p>
                </div>
            </footer>
        </div>
    );
}'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(landing_jsx)
print("Landing.jsx updated")
