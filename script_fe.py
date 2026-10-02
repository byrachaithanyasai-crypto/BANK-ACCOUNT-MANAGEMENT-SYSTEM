import os

src_dir = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\src'
dirs = [
    'components/common', 'components/layout', 'components/dashboard', 
    'components/charts', 'components/tables', 'components/forms', 'components/banking',
    'pages', 'layouts', 'services', 'hooks', 'context', 'routes', 'styles'
]

for d in dirs:
    os.makedirs(os.path.join(src_dir, d), exist_ok=True)

env_content = "VITE_API_BASE_URL=http://127.0.0.1:8000\n"
with open(r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\.env.example', 'w') as f:
    f.write(env_content)
with open(r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\.env', 'w') as f:
    f.write(env_content)

tailwind_config = '''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0a192f',
          800: '#112240',
          700: '#233554'
        },
        electric: '#64ffda',
        purple: {
          dark: '#2d1b69',
          light: '#6b46c1'
        }
      }
    },
  },
  plugins: [],
}'''
with open(r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\tailwind.config.js', 'w') as f:
    f.write(tailwind_config)

index_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-navy-900 text-white font-sans;
}
'''
with open(os.path.join(src_dir, 'index.css'), 'w') as f:
    f.write(index_css)

api_service = '''import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = Bearer ;
    }
    return config;
});

export default api;
'''
with open(os.path.join(src_dir, 'services', 'api.js'), 'w') as f:
    f.write(api_service)

auth_context = '''import { createContext, useState, useEffect } from 'react';
import api from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const res = await api.get('/api/auth/me');
                    setUser(res.data);
                } catch (e) {
                    localStorage.removeItem('token');
                }
            }
            setLoading(false);
        };
        checkAuth();
    }, []);

    const login = async (username, password) => {
        const res = await api.post('/api/auth/login', { username, password });
        localStorage.setItem('token', res.data.access_token);
        const userRes = await api.get('/api/auth/me');
        setUser(userRes.data);
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
'''
with open(os.path.join(src_dir, 'context', 'AuthContext.jsx'), 'w') as f:
    f.write(auth_context)

main_jsx = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { AuthProvider } from './context/AuthContext'
import { BrowserRouter } from 'react-router-dom'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
'''
with open(os.path.join(src_dir, 'main.jsx'), 'w') as f:
    f.write(main_jsx)

app_jsx = '''import { Routes, Route, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './context/AuthContext';
import MainLayout from './layouts/MainLayout';
import AuthLayout from './layouts/AuthLayout';

// Mock pages for Phase 5 scope
const Landing = () => <div className="p-10"><h1 className="text-4xl text-electric">BANKX</h1><p>Smart Banking Database System</p></div>;
const Login = () => {
    const { login } = useContext(AuthContext);
    const handleLogin = (e) => {
        e.preventDefault();
        login('admin', 'password').catch(err => alert('Login failed'));
    };
    return (
        <form onSubmit={handleLogin} className="p-10 bg-navy-800 rounded">
            <h2 className="text-2xl mb-4">Login</h2>
            <button type="submit" className="bg-electric text-navy-900 px-4 py-2 rounded">Login as Admin</button>
        </form>
    );
};
const Dashboard = () => <div className="p-5"><h2>Dashboard</h2><p>Welcome to BANKX Analytics.</p></div>;

const ProtectedRoute = ({ children }) => {
    const { user, loading } = useContext(AuthContext);
    if (loading) return <div>Loading...</div>;
    return user ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
      </Route>
      <Route element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
      </Route>
    </Routes>
  );
}

export default App;
'''
with open(os.path.join(src_dir, 'App.jsx'), 'w') as f:
    f.write(app_jsx)

layouts = {
    'AuthLayout.jsx': '''import { Outlet } from 'react-router-dom';
export default function AuthLayout() {
    return <div className="min-h-screen bg-navy-900 flex items-center justify-center text-white"><Outlet /></div>;
}''',
    'MainLayout.jsx': '''import { Outlet, Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export default function MainLayout() {
    const { user, logout } = useContext(AuthContext);
    return (
        <div className="flex min-h-screen bg-navy-900 text-white">
            <aside className="w-64 bg-navy-800 p-5">
                <h1 className="text-2xl text-electric mb-10">BANKX</h1>
                <nav className="space-y-4 flex flex-col">
                    <Link to="/dashboard" className="hover:text-electric">Dashboard</Link>
                    <button onClick={logout} className="text-left text-red-400 mt-10">Logout</button>
                </nav>
            </aside>
            <main className="flex-1 p-10">
                <header className="mb-10 flex justify-between">
                    <div>Welcome, {user?.username} ({user?.role})</div>
                </header>
                <Outlet />
            </main>
        </div>
    );
}'''
}
for name, content in layouts.items():
    with open(os.path.join(src_dir, 'layouts', name), 'w') as f:
        f.write(content)

print("Frontend scaffolded.")
