import React, { useEffect, useState } from 'react';
import { Users, Package, ShoppingCart, DollarSign, PlusCircle } from 'lucide-react';
import api from '../api/axios';
import { DashboardStats, Category } from '../types';

export const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  // New Category state
  const [catName, setCatName] = useState('');
  const [catDesc, setCatDesc] = useState('');

  // New Product state
  const [prodTitle, setProdTitle] = useState('');
  const [prodDesc, setProdDesc] = useState('');
  const [prodPrice, setProdPrice] = useState('');
  const [prodStock, setProdStock] = useState('');
  const [prodImageUrl, setProdImageUrl] = useState('');
  const [prodCategoryId, setProdCategoryId] = useState<number | ''>('');

  const fetchDashboardData = async () => {
    try {
      const [statsRes, catRes] = await Promise.all([
        api.get<DashboardStats>('/admin/dashboard/stats'),
        api.get<Category[]>('/categories')
      ]);
      setStats(statsRes.data);
      setCategories(catRes.data);
    } catch {
      // Handled
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleCreateCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/categories', {
        name: catName,
        description: catDesc
      });
      setCatName('');
      setCatDesc('');
      fetchDashboardData();
      alert('Category created successfully!');
    } catch (err: any) {
      alert(err.response?.data?.message || 'Could not create category');
    }
  };

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prodCategoryId) return alert('Select a category');
    try {
      await api.post('/products', {
        title: prodTitle,
        description: prodDesc,
        price: parseFloat(prodPrice),
        stock: parseInt(prodStock),
        category_id: prodCategoryId,
        image_url: prodImageUrl || 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80',
        is_available: true
      });
      setProdTitle('');
      setProdDesc('');
      setProdPrice('');
      setProdStock('');
      setProdImageUrl('');
      setProdCategoryId('');
      fetchDashboardData();
      alert('Product created successfully!');
    } catch (err: any) {
      alert(err.response?.data?.message || 'Could not create product');
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 animate-pulse space-y-8">
        <div className="h-32 bg-gray-200 rounded-2xl"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-10">
      <div>
        <h1 className="text-3xl font-black text-gray-900">Admin Control Dashboard</h1>
        <p className="text-sm text-gray-500">Live platform metrics & catalog management</p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex items-center space-x-4">
            <div className="p-3 bg-blue-50 text-blue-600 rounded-xl">
              <Users className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-gray-500 font-semibold uppercase">Total Users</span>
              <div className="text-2xl font-black text-gray-900">{stats.total_users}</div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex items-center space-x-4">
            <div className="p-3 bg-purple-50 text-purple-600 rounded-xl">
              <Package className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-gray-500 font-semibold uppercase">Total Products</span>
              <div className="text-2xl font-black text-gray-900">{stats.total_products}</div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex items-center space-x-4">
            <div className="p-3 bg-amber-50 text-amber-600 rounded-xl">
              <ShoppingCart className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-gray-500 font-semibold uppercase">Total Orders</span>
              <div className="text-2xl font-black text-gray-900">{stats.total_orders}</div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex items-center space-x-4">
            <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
              <DollarSign className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-gray-500 font-semibold uppercase">Total Revenue</span>
              <div className="text-2xl font-black text-gray-900">${Number(stats.total_revenue).toFixed(2)}</div>
            </div>
          </div>
        </div>
      )}

      {/* Catalog Management Forms */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Create Category */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
          <h2 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
            <PlusCircle className="w-5 h-5 text-indigo-600" />
            <span>Create New Category</span>
          </h2>
          <form onSubmit={handleCreateCategory} className="space-y-3">
            <input
              type="text"
              required
              placeholder="Category Name (e.g. Mobile)"
              value={catName}
              onChange={(e) => setCatName(e.target.value)}
              className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
            />
            <textarea
              placeholder="Category Description"
              rows={2}
              value={catDesc}
              onChange={(e) => setCatDesc(e.target.value)}
              className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
            ></textarea>
            <button type="submit" className="w-full bg-indigo-600 text-white font-bold text-xs py-2.5 rounded-lg hover:bg-indigo-700">
              Add Category
            </button>
          </form>
        </div>

        {/* Create Product */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
          <h2 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
            <PlusCircle className="w-5 h-5 text-indigo-600" />
            <span>Create New Product</span>
          </h2>
          <form onSubmit={handleCreateProduct} className="space-y-3">
            <input
              type="text"
              required
              placeholder="Product Title (e.g. Apple iPhone 15)"
              value={prodTitle}
              onChange={(e) => setProdTitle(e.target.value)}
              className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
            />
            <select
              required
              value={prodCategoryId}
              onChange={(e) => setProdCategoryId(Number(e.target.value))}
              className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
            >
              <option value="">Select Category</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <div className="grid grid-cols-2 gap-3">
              <input
                type="number"
                step="0.01"
                required
                placeholder="Price ($)"
                value={prodPrice}
                onChange={(e) => setProdPrice(e.target.value)}
                className="p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
              />
              <input
                type="number"
                required
                placeholder="Stock Inventory"
                value={prodStock}
                onChange={(e) => setProdStock(e.target.value)}
                className="p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
              />
            </div>
            <input
              type="url"
              placeholder="Image URL (e.g. https://images.unsplash.com/...)"
              value={prodImageUrl}
              onChange={(e) => setProdImageUrl(e.target.value)}
              className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
            />
            <textarea
              required
              minLength={10}
              placeholder="Product Description (At least 10 characters)"
              rows={2}
              value={prodDesc}
              onChange={(e) => setProdDesc(e.target.value)}
              className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
            ></textarea>
            <button type="submit" className="w-full bg-gray-900 text-white font-bold text-xs py-2.5 rounded-lg hover:bg-gray-800">
              Add Product to Catalogue
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
