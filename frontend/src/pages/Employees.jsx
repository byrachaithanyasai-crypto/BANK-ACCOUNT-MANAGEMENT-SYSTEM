import React, { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import { X } from 'lucide-react';

export default function Employees() {
    const [data, setData] = useState([]);
    const [branches, setBranches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingRecord, setEditingRecord] = useState(null);
    const [formData, setFormData] = useState({ 
        branch_id: '', first_name: '', last_name: '', email: '', phone: '', position: '', hire_date: '' 
    });
    const [formLoading, setFormLoading] = useState(false);

    const fetchData = async () => {
        try {
            const [empRes, brRes] = await Promise.all([
                api.get('/api/employees'),
                api.get('/api/branches')
            ]);
            setData(empRes.data);
            setBranches(brRes.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleDelete = async (row) => {
        if(window.confirm('Are you sure you want to delete this employee?')) {
            try {
                await api.delete(`/api/employees/${row.employee_id}`);
                fetchData();
            } catch (err) {
                alert('Failed to delete employee. Ensure they are not linked to critical records.');
            }
        }
    };
    
    const handleEdit = (row) => {
        setEditingRecord(row);
        setFormData({
            branch_id: row.branch_id || '',
            first_name: row.first_name,
            last_name: row.last_name,
            email: row.email,
            phone: row.phone || '',
            position: row.position || '',
            hire_date: row.hire_date || ''
        });
        setIsModalOpen(true);
    };

    const handleAdd = () => {
        setEditingRecord(null);
        setFormData({ 
            branch_id: branches[0]?.branch_id || '', first_name: '', last_name: '', 
            email: '', phone: '', position: '', hire_date: new Date().toISOString().split('T')[0] 
        });
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormLoading(true);
        try {
            const payload = {
                ...formData,
                branch_id: formData.branch_id ? parseInt(formData.branch_id) : null
            };
            if (editingRecord) {
                await api.put(`/api/employees/${editingRecord.employee_id}`, payload);
            } else {
                await api.post('/api/employees', payload);
            }
            setIsModalOpen(false);
            fetchData();
        } catch (err) {
            alert(err.response?.data?.detail || 'An error occurred saving the employee.');
        } finally {
            setFormLoading(false);
        }
    };

    const columns = [
        { header: "ID", accessor: "employee_id" },
        { header: "First Name", accessor: "first_name" },
        { header: "Last Name", accessor: "last_name" },
        { header: "Email", accessor: "email" },
        { header: "Position", accessor: "position" },
        { header: "Hire Date", accessor: "hire_date" },
        { header: "Edit", accessor: "edit", render: (row) => (
            <button onClick={() => handleEdit(row)} className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>
        )}
    ];

    const filteredData = data.filter(row => 
        Object.values(row).some(val => 
            String(val).toLowerCase().includes(searchQuery.toLowerCase())
        )
    );

    return (
        <div className="h-full relative">
            <DataTable 
                title="Employees" 
                columns={columns} 
                data={filteredData} 
                loading={loading} 
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                onDelete={handleDelete}
                onAdd={handleAdd}
            />

            {isModalOpen && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4 overflow-y-auto">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-md my-8">
                        <div className="flex justify-between items-center p-6 border-b border-slate-100">
                            <h2 className="text-xl font-bold text-slate-900">
                                {editingRecord ? 'Edit Employee' : 'Add New Employee'}
                            </h2>
                            <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                                <X size={20} />
                            </button>
                        </div>
                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">First Name</label>
                                    <input required type="text" value={formData.first_name} onChange={e => setFormData({...formData, first_name: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Last Name</label>
                                    <input required type="text" value={formData.last_name} onChange={e => setFormData({...formData, last_name: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                                <input required type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Phone</label>
                                    <input type="text" value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Hire Date</label>
                                    <input type="date" value={formData.hire_date} onChange={e => setFormData({...formData, hire_date: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Position</label>
                                <input type="text" value={formData.position} onChange={e => setFormData({...formData, position: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Assigned Branch</label>
                                <select required value={formData.branch_id} onChange={e => setFormData({...formData, branch_id: e.target.value})} className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-500 outline-none">
                                    <option value="">Select a branch...</option>
                                    {branches.map(b => <option key={b.branch_id} value={b.branch_id}>{b.branch_name}</option>)}
                                </select>
                            </div>
                            
                            <div className="pt-4 flex justify-end gap-3">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-100 rounded-lg transition-colors">Cancel</button>
                                <button type="submit" disabled={formLoading} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50">
                                    {formLoading ? 'Saving...' : 'Save Employee'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
