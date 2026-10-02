import React, { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import { X } from 'lucide-react';

export default function Branches() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingRecord, setEditingRecord] = useState(null);
    const [formData, setFormData] = useState({ branch_code: '', branch_name: '', city: '', phone: '' });
    const [formLoading, setFormLoading] = useState(false);

    const fetchData = async () => {
        try {
            const res = await api.get('/api/branches');
            setData(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };
    useEffect(() => { fetchData(); }, []);

    const handleDelete = async (row) => {
        if(window.confirm('Delete branch?')) {
            try { await api.delete(`/api/branches/${row.branch_id}`); fetchData(); }
            catch (err) { alert('Failed to delete. Accounts or employees may be linked.'); }
        }
    };
    
    const handleEdit = (row) => {
        setEditingRecord(row);
        setFormData({ branch_code: row.branch_code, branch_name: row.branch_name, city: row.city || '', phone: row.phone || '' });
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingRecord(null);
        setFormData({ branch_code: '', branch_name: '', city: '', phone: '' });
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormLoading(true);
        try {
            if (editingRecord) await api.put(`/api/branches/${editingRecord.branch_id}`, formData);
            else await api.post('/api/branches', formData);
            setIsModalOpen(false); fetchData();
        } catch (err) { alert(err.response?.data?.detail || 'Error saving branch'); } 
        finally { setFormLoading(false); }
    };

    const columns = [
        { header: "Code", accessor: "branch_code" },
        { header: "Name", accessor: "branch_name" },
        { header: "City", accessor: "city" },
        { header: "Phone", accessor: "phone" },
        { header: "Edit", accessor: "edit", render: (row) => (
            <button onClick={() => handleEdit(row)} className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>
        )}
    ];

    const filteredData = data.filter(row => Object.values(row).some(val => String(val).toLowerCase().includes(searchQuery.toLowerCase())));

    return (
        <div className="h-full relative">
            <DataTable title="Branches" columns={columns} data={filteredData} loading={loading} searchQuery={searchQuery} setSearchQuery={setSearchQuery} onDelete={handleDelete} onAdd={handleAdd} />
            {isModalOpen && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden">
                        <div className="flex justify-between items-center p-6 border-b border-slate-100">
                            <h2 className="text-xl font-bold">{editingRecord ? 'Edit Branch' : 'Add Branch'}</h2>
                            <button onClick={() => setIsModalOpen(false)}><X size={20} /></button>
                        </div>
                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            <div><label className="block text-sm font-medium mb-1">Branch Code</label><input required value={formData.branch_code} onChange={e=>setFormData({...formData, branch_code: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div><label className="block text-sm font-medium mb-1">Name</label><input required value={formData.branch_name} onChange={e=>setFormData({...formData, branch_name: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div><label className="block text-sm font-medium mb-1">City</label><input value={formData.city} onChange={e=>setFormData({...formData, city: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div><label className="block text-sm font-medium mb-1">Phone</label><input value={formData.phone} onChange={e=>setFormData({...formData, phone: e.target.value})} className="w-full px-3 py-2 border rounded-lg outline-none focus:border-blue-500" /></div>
                            <div className="pt-4 flex justify-end gap-3"><button type="button" onClick={()=>setIsModalOpen(false)} className="px-4 py-2 hover:bg-slate-100 rounded-lg">Cancel</button><button type="submit" disabled={formLoading} className="px-4 py-2 bg-blue-600 text-white rounded-lg">Save</button></div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
