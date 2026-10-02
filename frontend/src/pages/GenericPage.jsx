import { FileQuestion, Search } from 'lucide-react';

export default function GenericPage({ title }) {
    return (
        <div className="space-y-6 h-full flex flex-col">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
                    <p className="text-slate-500 mt-1">Manage and monitor {title.toLowerCase()}.</p>
                </div>
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
                    <input 
                        type="text" 
                        placeholder={"Search " + title.toLowerCase() + "..."} 
                        className="w-full sm:w-64 pl-10 pr-4 py-2 bg-white border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 rounded-lg text-sm transition-all outline-none"
                    />
                </div>
            </div>
            
            <div className="flex-1 bg-white p-12 rounded-2xl border border-slate-100 shadow-sm text-center flex flex-col items-center justify-center min-h-[400px]">
                <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                    <FileQuestion className="w-8 h-8 text-slate-400" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">{title} data is not available</h3>
                <p className="text-slate-500 max-w-md">
                    The {title.toLowerCase()} listing requires integration with the core backend API endpoints which are currently under development.
                </p>
            </div>
        </div>
    );
}
