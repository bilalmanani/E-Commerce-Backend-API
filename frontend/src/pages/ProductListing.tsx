import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { Product, PaginatedProducts } from '../types';
import { ProductCard } from '../components/ProductCard';
import { SearchBar } from '../components/SearchBar';
import { CategorySidebar } from '../components/CategorySidebar';
import { Pagination } from '../components/Pagination';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import { EmptyState } from '../components/EmptyState';

export const ProductListing: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [total, setTotal] = useState(0);
  const [skip, setSkip] = useState(0);
  const [limit] = useState(12);
  const [search, setSearch] = useState('');
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | null>(null);
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');
  const [loading, setLoading] = useState(true);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.append('skip', skip.toString());
      params.append('limit', limit.toString());
      params.append('sort_by', sortBy);
      params.append('sort_order', sortOrder);

      if (search) params.append('search', search);
      if (selectedCategoryId) params.append('category_id', selectedCategoryId.toString());

      const res = await api.get<PaginatedProducts>(`/products?${params.toString()}`);
      setProducts(res.data.items);
      setTotal(res.data.total);
    } catch {
      setProducts([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, [skip, search, selectedCategoryId, sortBy, sortOrder]);

  const handleCategorySelect = (id: number | null) => {
    setSelectedCategoryId(id);
    setSkip(0);
  };

  const handleSearchChange = (val: string) => {
    setSearch(val);
    setSkip(0);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-gray-900">All Products</h1>
          <p className="text-sm text-gray-500">Filter, search, and browse catalogue items</p>
        </div>

        <div className="flex items-center space-x-3 w-full md:w-auto">
          <div className="w-full md:w-80">
            <SearchBar value={search} onChange={handleSearchChange} />
          </div>

          <select
            value={`${sortBy}_${sortOrder}`}
            onChange={(e) => {
              const [by, order] = e.target.value.split('_');
              setSortBy(by);
              setSortOrder(order);
            }}
            className="bg-white border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="created_at_desc">Newest First</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="title_asc">Title: A to Z</option>
          </select>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        <CategorySidebar
          selectedCategoryId={selectedCategoryId}
          onSelectCategory={handleCategorySelect}
        />

        <div className="flex-1 space-y-6">
          {loading ? (
            <LoadingSkeleton />
          ) : products.length === 0 ? (
            <EmptyState />
          ) : (
            <>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>

              <Pagination
                total={total}
                skip={skip}
                limit={limit}
                onPageChange={(newSkip) => setSkip(newSkip)}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
};
