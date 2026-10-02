import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Plus, X } from 'lucide-react';
import DataTable from '../components/DataTable';
import api from '../services/api';

export default function Customers() {
    const { user } = useContext(AuthContext);
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingRecord, setEditingRecord] = useState(null);
    const [formData, setFormData] = useState({ 
        first_name: '', last_name: '', email: '', phone: '', address: '', city: '', state: '', zip_code: '', date_of_birth: '', kyc_status: 'PENDING' 
    });
    const [formLoading, setFormLoading] = useState(false);

    const fetchData = async () => {
        try {
            const res = await api.get('/api/customers');
            setData(res.data);
        } catch (err) { console.error(err); }
        finally { setLoading(false); }
    };
    useEffect(() => { fetchData(); }, []);

    const handleDelete = async (row) => {
        if(window.confirm('Delete customer?')) {
            try { 
                await api.delete('/api/customers/' + row.customer_id); 
                fetchData(); 
            }
            catch (err) { alert(err.response?.data?.detail || 'Failed to delete customer.'); }
        }
    };

    const handleEdit = (row) => {
        setEditingRecord(row);
        setFormData({ 
            first_name: row.first_name || '', last_name: row.last_name || '', 
            email: row.email || '', phone: row.phone || '', 
            address: row.address || '', city: row.city || '', 
            state: row.state || '', zip_code: row.zip_code || '', 
            date_of_birth: row.date_of_birth || '', kyc_status: row.kyc_status || 'PENDING' 
        });
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingRecord(null);
        setFormData({ 
            first_name: '', last_name: '', email: '', phone: '', 
            address: '', city: '', state: '', zip_code: '', 
            date_of_birth: '', kyc_status: 'PENDING' 
        });
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault(); setFormLoading(true);
        try {
            const payload = { ...formData };
            if (!payload.date_of_birth) delete payload.date_of_birth;
            
            if (editingRecord) await api.put('/api/customers/' + editingRecord.customer_id, payload);
            else await api.post('/api/customers', payload);
            
            setIsModalOpen(false); fetchData();
        } catch (err) { alert(err.response?.data?.detail || 'Error saving customer'); }
        finally { setFormLoading(false); }
    };

    const canEdit = ["ADMIN", "MANAGER"].includes(user?.role);
    const canDelete = user?.role === "ADMIN";
    const canCreate = ["ADMIN", "MANAGER"].includes(user?.role);

    const columns = [
        { header: "Name", accessor: "name", render: (row) => <div className="font-semibold text-slate-800">{row.first_name + ' ' + row.last_name}</div> },
        { header: "Contact", accessor: "contact", render: (row) => (
            <div className="text-sm">
                <div className="text-slate-900">{row.email}</div>
                <div className="text-slate-500">{row.phone}</div>
            </div>
        )},
        { header: "Address", accessor: "address", render: (row) => (
            <div className="text-sm text-slate-600">
                {row.city ? row.city + ', ' + row.state : '-'}
            </div>
        )},
        { header: "KYC", accessor: "kyc_status", render: (row) => (
            <span className={'px-2 py-1 rounded-full text-xs font-semibold ' + (row.kyc_status === 'VERIFIED' ? 'bg-emerald-100 text-emerald-700' : row.kyc_status === 'REJECTED' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700')}>
                {row.kyc_status}
            </span>
        )}
    ];

    if (canEdit || canDelete) {
        columns.push({
            header: "Actions",
            accessor: "actions",
            render: (row) => (
                <div className="flex items-center gap-3">
                    {canEdit && <button onClick={() => handleEdit(row)} className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>}
                    {canDelete && <button onClick={() => handleDelete(row)} className="text-red-600 hover:text-red-800 font-medium">Delete</button>}
                </div>
            )
        });
    }

    const filteredData = data.filter(row => Object.values(row).some(val => String(val).toLowerCase().includes(searchQuery.toLowerCase())));

    return (
        <div className="h-full relative">
            <DataTable 
                title="Customers" 
                columns={columns} 
                data={filteredData} 
                loading={loading} 
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                onAdd={canCreate ? handleAdd : null}
            />

            {isModalOpen && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4 overflow-y-auto">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl my-8">
                        <div className="flex justify-between items-center p-6 border-b border-slate-100">
                            <h2 className="text-xl font-bold text-slate-900">
                                {editingRecord ? 'Edit Customer' : 'Add New Customer'}
                            </h2>
                            <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                                <X size={20} />
                            </button>
                        </div>
                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">First Name</label><input required type="text" value={formData.first_name} onChange={e => setFormData({...formData, first_name: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" /></div>
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Last Name</label><input required type="text" value={formData.last_name} onChange={e => setFormData({...formData, last_name: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" /></div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Email</label><input required type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" /></div>
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Phone</label><input required type="text" value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" /></div>
                            </div>
                            <div><label className="block text-sm font-medium text-slate-700 mb-1">Address</label><input type="text" value={formData.address} onChange={e => setFormData({...formData, address: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" /></div>
                            <div className="grid grid-cols-3 gap-4">
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">City</label><input type="text" value={formData.city} onChange={e => setFormData({...formData, city: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" /></div>
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">State</label><input type="text" value={formData.state} onChange={e => setFormData({...formData, state: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" /></div>
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Zip Code</label><input type="text" value={formData.zip_code} onChange={e => setFormData({...formData, zip_code: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" /></div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">Date of Birth</label><input type="date" value={formData.date_of_birth} onChange={e => setFormData({...formData, date_of_birth: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" /></div>
                                <div><label className="block text-sm font-medium text-slate-700 mb-1">KYC Status</label>
                                    <select value={formData.kyc_status} onChange={e => setFormData({...formData, kyc_status: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none">
                                        <option value="PENDING">Pending</option><option value="VERIFIED">Verified</option><option value="REJECTED">Rejected</option>
                                    </select>
                                </div>
                            </div>
                            <div className="pt-4 flex justify-end gap-3">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-100 rounded-lg transition-colors">Cancel</button>
                                <button type="submit" disabled={formLoading} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50">{formLoading ? 'Saving...' : 'Save Customer'}</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
