import { Outlet } from 'react-router-dom';
export default function AuthLayout() {
    return <div className="min-h-screen bg-navy-900 flex items-center justify-center text-white"><Outlet /></div>;
}