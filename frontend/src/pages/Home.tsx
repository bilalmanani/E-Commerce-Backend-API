import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, ShoppingBag, Zap, Shield, RefreshCw } from 'lucide-react';
import api from '../api/axios';
import { Product } from '../types';
import { ProductCard } from '../components/ProductCard';

export const Home: React.FC = () => {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/products?limit=8')
      .then((res) => setFeaturedProducts(res.data.items || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-12 pb-16">
      {/* Hero Banner */}
      <section className="bg-gradient-to-br from-indigo-900 via-indigo-800 to-slate-900 text-white rounded-3xl p-8 sm:p-12 lg:p-16 my-6 max-w-7xl mx-auto shadow-xl relative overflow-hidden">
        <div className="max-w-2xl relative z-10 space-y-6">
          <span className="bg-indigo-500/30 text-indigo-200 text-xs font-semibold px-3 py-1.5 rounded-full border border-indigo-400/30">
            Powered by FastAPI & PostgreSQL
          </span>
          <h1 className="text-4xl sm:text-5xl font-black tracking-tight leading-tight">
            High Performance Modern E-Commerce Platform
          </h1>
          <p className="text-indigo-200 text-base sm:text-lg">
            Experience lightning fast checkout, real-time inventory management, and seamless authorization built with SQLAlchemy 2.0.
          </p>
          <div className="pt-2 flex items-center space-x-4">
            <Link
              to="/products"
              className="inline-flex items-center space-x-2 bg-white text-indigo-900 font-bold px-6 py-3 rounded-xl hover:bg-indigo-50 transition-colors shadow-lg"
            >
              <span>Explore Products</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Feature Highlights */}
      <section className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-start space-x-4">
          <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
            <Zap className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-gray-900 text-base">Async Performance</h3>
            <p className="text-gray-500 text-xs mt-1">Built with Python 3.12 asyncpg and SQLAlchemy 2.0 for maximum concurrent throughput.</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-start space-x-4">
          <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-gray-900 text-base">JWT Security</h3>
            <p className="text-gray-500 text-xs mt-1">Dual-token architecture with OAuth2 password bearer and role-based authorization.</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-start space-x-4">
          <div className="p-3 bg-purple-50 text-purple-600 rounded-xl">
            <RefreshCw className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-gray-900 text-base">ACID Checkout</h3>
            <p className="text-gray-500 text-xs mt-1">Transactional stock deduction, price freezing, and automated order processing.</p>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="max-w-7xl mx-auto px-4 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-black text-gray-900">Featured Products</h2>
            <p className="text-gray-500 text-sm">Fetched directly from your PostgreSQL database</p>
          </div>
          <Link to="/products" className="text-sm font-semibold text-indigo-600 hover:text-indigo-700">
            View All →
          </Link>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 animate-pulse">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl p-4 h-64 border border-gray-100"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
};
