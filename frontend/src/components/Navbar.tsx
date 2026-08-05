import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingBag, User as UserIcon, LogOut, ShoppingCart, ShieldCheck } from 'lucide-react';
import api from '../api/axios';
import { User } from '../types';

export const Navbar: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('access_token');

  useEffect(() => {
    if (isAuthenticated) {
      api.get<User>('/users/me')
        .then((res) => setUser(res.data))
        .catch(() => {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setUser(null);
        });
    } else {
      setUser(null);
    }
  }, [isAuthenticated]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    navigate('/login');
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2 text-indigo-600 font-black text-xl">
          <ShoppingBag className="w-6 h-6" />
          <span>FASTSTORE</span>
        </Link>

        <nav className="flex items-center space-x-6">
          <Link to="/products" className="text-sm font-medium text-gray-700 hover:text-indigo-600">
            Products
          </Link>

          {isAuthenticated ? (
            <>
              <Link to="/cart" className="flex items-center space-x-1 text-sm font-medium text-gray-700 hover:text-indigo-600">
                <ShoppingCart className="w-5 h-5" />
                <span>Cart</span>
              </Link>

              <Link to="/orders" className="text-sm font-medium text-gray-700 hover:text-indigo-600">
                My Orders
              </Link>

              <Link to="/profile" className="flex items-center space-x-1 text-sm font-medium text-gray-700 hover:text-indigo-600">
                <UserIcon className="w-4 h-4" />
                <span>{user?.first_name || 'Profile'}</span>
              </Link>

              {user?.role === 'admin' && (
                <Link to="/admin" className="flex items-center space-x-1 text-sm font-medium text-purple-600 hover:text-purple-700">
                  <ShieldCheck className="w-4 h-4" />
                  <span>Admin</span>
                </Link>
              )}

              <button
                onClick={handleLogout}
                className="text-gray-500 hover:text-red-600 text-sm font-medium p-1"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </>
          ) : (
            <div className="flex items-center space-x-3">
              <Link to="/login" className="text-sm font-medium text-gray-700 hover:text-indigo-600">
                Log in
              </Link>
              <Link
                to="/register"
                className="text-sm font-medium bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Register
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};
