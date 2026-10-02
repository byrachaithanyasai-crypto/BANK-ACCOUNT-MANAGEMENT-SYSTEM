import React from 'react';
import { AlertCircle, RefreshCw, Home } from 'lucide-react';
import { Link } from 'react-router-dom';

export class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error("ErrorBoundary caught an error", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-[400px] h-full flex flex-col items-center justify-center p-8 bg-white rounded-2xl border border-gray-100 shadow-sm text-center">
                    <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mb-6">
                        <AlertCircle className="w-8 h-8 text-red-600" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-3">Something went wrong</h2>
                    <p className="text-gray-500 max-w-md mx-auto mb-8">
                        We encountered an unexpected error while trying to render this view. 
                        Please try reloading the page or return to the dashboard.
                    </p>
                    <div className="flex gap-4">
                        <button 
                            onClick={() => window.location.reload()}
                            className="flex items-center gap-2 px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-900 rounded-lg font-medium transition-colors"
                        >
                            <RefreshCw size={18} />
                            Retry
                        </button>
                        <Link 
                            to="/dashboard"
                            className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                        >
                            <Home size={18} />
                            Go to Dashboard
                        </Link>
                    </div>
                </div>
            );
        }
        return this.props.children;
    }
}
