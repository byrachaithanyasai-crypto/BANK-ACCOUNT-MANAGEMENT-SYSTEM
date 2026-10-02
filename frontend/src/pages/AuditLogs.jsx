import React, { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';

export default function AuditLogs() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');

    const fetchData = async () => {
        try {
            const res = await api.get('/api/audit-logs');
            setData(res.data);
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
        if(window.confirm('Are you sure you want to delete this record?')) {
            try {
                await api.delete(`/api/audit-logs/${row.log_id}`);
                fetchData();
            } catch (err) {
                alert('Failed to delete record. It may be restricted by existing relationships or permissions.');
            }
        }
    };

    const columns = [{"header": "Timestamp", "accessor": "action_timestamp"}, {"header": "User ID", "accessor": "user_id"}, {"header": "Action", "accessor": "action"}, {"header": "Table", "accessor": "table_name"}, {"header": "Record ID", "accessor": "record_id"}];

    const filteredData = data.filter(row => 
        Object.values(row).some(val => 
            String(val).toLowerCase().includes(searchQuery.toLowerCase())
        )
    );

    return (
        <DataTable 
            title="AuditLogs" 
            columns={columns} 
            data={filteredData} 
            loading={loading} 
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            onDelete={handleDelete}
            onAdd={() => alert('Please implement full modal forms here.')}
        />
    );
}
