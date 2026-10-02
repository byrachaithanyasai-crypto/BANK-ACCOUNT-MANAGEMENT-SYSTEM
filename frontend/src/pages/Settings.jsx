import React, { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { User, Shield, Key, Loader2, CheckCircle2 } from 'lucide-react';
import api from '../services/api';

export default function Settings() {
    const { user, logout } = useContext(AuthContext);
    const [activeTab, setActiveTab] = useState('profile');

    const [passwordData, setPasswordData] = useState({ current_password: '', new_password: '', confirm_password: '' });
    const [passwordLoading, setPasswordLoading] = useState(false);
    const [passwordSuccess, setPasswordSuccess] = useState('');
    const [passwordError, setPasswordError] = useState('');

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();
        setPasswordError('');
        setPasswordSuccess('');
        
        if (passwordData.new_password !== passwordData.confirm_password) {
            setPasswordError("New passwords do not match.");
            return;
        }

        setPasswordLoading(true);
        try {
            await api.post('/api/auth/change-password', {
                current_password: passwordData.current_password,
                new_password: passwordData.new_password
            });
            setPasswordSuccess("Password updated successfully.");
            setPasswordData({ current_password: '', new_password: '', confirm_password: '' });
        } catch (err) {
            setPasswordError(err.response?.data?.detail || "Failed to update password.");
        } finally {
            setPasswordLoading(false);
        }
    };

    return (
        <div className="space-y-6 max-w-5xl">
            <div>
                <h1 className="text-2xl font-bold text-slate-900">System Settings</h1>
                <p className="text-slate-500 mt-1">Manage your account profile and application preferences.</p>
            </div>

            <div className="flex flex-col md:flex-row gap-8">
                <div className="w-full md:w-64 space-y-1">
                    <button 
                        onClick={() => setActiveTab('profile')}
                        className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl transition-colors ${activeTab === 'profile' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
                    >
                        <User size={18} /> Profile Overview
                    </button>
                    <button 
                        onClick={() => setActiveTab('security')}
                        className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl transition-colors ${activeTab === 'security' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
                    >
                        <Shield size={18} /> Security & Auth
                    </button>
                </div>

                <div className="flex-1">
                    {activeTab === 'profile' && (
                        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                            <div className="p-6 border-b border-slate-100 bg-slate-50/50">
                                <h2 className="text-lg font-bold text-slate-900">Profile Information</h2>
                            </div>
                            <div className="p-6 space-y-6">
                                <div className="flex items-center gap-6 pb-6 border-b border-slate-100">
                                    <div className="w-20 h-20 bg-blue-900 text-white rounded-2xl flex items-center justify-center text-3xl font-bold shadow-inner">
                                        {user?.username?.charAt(0).toUpperCase()}
                                    </div>
                                    <div>
                                        <h3 className="text-2xl font-bold text-slate-900">{user?.username}</h3>
                                        <span className="inline-block mt-2 px-3 py-1 bg-blue-100 text-blue-800 text-xs font-bold rounded-full uppercase tracking-wider">
                                            {user?.role}
                                        </span>
                                    </div>
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-500 mb-1">Username</label>
                                        <p className="text-slate-900 font-medium">{user?.username}</p>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-500 mb-1">Account Status</label>
                                        <p className="text-emerald-600 font-medium flex items-center gap-2">
                                            <span className="w-2 h-2 rounded-full bg-emerald-500"></span> Active
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'security' && (
                        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                            <div className="p-6 border-b border-slate-100 bg-slate-50/50 flex items-center gap-3">
                                <Key size={20} className="text-slate-400" />
                                <h2 className="text-lg font-bold text-slate-900">Change Password</h2>
                            </div>
                            <form onSubmit={handlePasswordSubmit} className="p-6 space-y-5">
                                {passwordError && (
                                    <div className="p-3 bg-red-50 text-red-700 text-sm font-medium rounded-lg border border-red-100">
                                        {passwordError}
                                    </div>
                                )}
                                {passwordSuccess && (
                                    <div className="p-3 bg-emerald-50 text-emerald-700 text-sm font-medium rounded-lg border border-emerald-100 flex items-center gap-2">
                                        <CheckCircle2 size={16} /> {passwordSuccess}
                                    </div>
                                )}
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Current Password</label>
                                    <input 
                                        required 
                                        type="password" 
                                        value={passwordData.current_password} 
                                        onChange={e => setPasswordData({...passwordData, current_password: e.target.value})}
                                        className="w-full max-w-md px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition-all" 
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">New Password</label>
                                    <input 
                                        required 
                                        type="password" 
                                        value={passwordData.new_password} 
                                        onChange={e => setPasswordData({...passwordData, new_password: e.target.value})}
                                        className="w-full max-w-md px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition-all" 
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Confirm New Password</label>
                                    <input 
                                        required 
                                        type="password" 
                                        value={passwordData.confirm_password} 
                                        onChange={e => setPasswordData({...passwordData, confirm_password: e.target.value})}
                                        className="w-full max-w-md px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition-all" 
                                    />
                                </div>
                                <div className="pt-2">
                                    <button 
                                        type="submit" 
                                        disabled={passwordLoading}
                                        className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50"
                                    >
                                        {passwordLoading ? <Loader2 size={18} className="animate-spin" /> : 'Update Password'}
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
