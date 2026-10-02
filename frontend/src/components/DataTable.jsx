import React from 'react';
import { Search, Loader2 } from 'lucide-react';

export default function DataTable({ 
    title, 
    columns, 
    data, 
    loading, 
    onAdd, 
    onDelete, 
    searchQuery, 
    setSearchQuery,
    addButtonLabel = "Add New"
}) {
    return (
        <div className="space-y-6 flex flex-col h-full">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
                    <p className="text-slate-500 mt-1">Manage and view {title.toLowerCase()} records.</p>
                </div>
                <div className="flex items-center gap-3">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
                        <input 
                            type="text" 
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder={`Search ${title.toLowerCase()}...`} 
                            className="w-full sm:w-64 pl-10 pr-4 py-2 bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 rounded-lg text-sm transition-all outline-none"
                        />
                    </div>
                    {onAdd && (
                        <button 
                            onClick={onAdd}
                            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors whitespace-nowrap"
                        >
                            {addButtonLabel}
                        </button>
                    )}
                </div>
            </div>
            
            <div className="flex-1 bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
                <div className="overflow-x-auto flex-1 custom-scrollbar">
                    <table className="w-full text-left text-sm whitespace-nowrap">
                        <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200 sticky top-0 z-10">
                            <tr>
                                {columns.map((col, idx) => (
                                    <th key={idx} className="px-6 py-4">{col.header}</th>
                                ))}
                                {onDelete && <th className="px-6 py-4 text-right">Actions</th>}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {loading ? (
                                <tr>
                                    <td colSpan={columns.length + (onDelete ? 1 : 0)} className="px-6 py-20 text-center text-slate-500">
                                        <div className="flex flex-col items-center justify-center">
                                            <Loader2 className="w-8 h-8 animate-spin text-blue-500 mb-4" />
                                            <p>Loading {title.toLowerCase()}...</p>
                                        </div>
                                    </td>
                                </tr>
                            ) : data.length === 0 ? (
                                <tr>
                                    <td colSpan={columns.length + (onDelete ? 1 : 0)} className="px-6 py-20 text-center text-slate-500">
                                        <p className="font-medium text-slate-900">No {title.toLowerCase()} found</p>
                                        <p className="mt-1">Try adjusting your search criteria.</p>
                                    </td>
                                </tr>
                            ) : (
                                data.map((row, rowIdx) => (
                                    <tr key={rowIdx} className="hover:bg-slate-50/50 transition-colors">
                                        {columns.map((col, colIdx) => (
                                            <td key={colIdx} className="px-6 py-4 text-slate-700">
                                                {col.render ? col.render(row) : row[col.accessor]}
                                            </td>
                                        ))}
                                        {onDelete && (
                                            <td className="px-6 py-4 text-right">
                                                <button 
                                                    onClick={() => onDelete(row)}
                                                    className="text-red-500 hover:text-red-700 font-medium text-xs px-3 py-1.5 rounded-lg hover:bg-red-50 transition-colors"
                                                >
                                                    Delete
                                                </button>
                                            </td>
                                        )}
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

