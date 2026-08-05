import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { Category } from '../types';

interface CategorySidebarProps {
  selectedCategoryId: number | null;
  onSelectCategory: (id: number | null) => void;
}

export const CategorySidebar: React.FC<CategorySidebarProps> = ({
  selectedCategoryId,
  onSelectCategory
}) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<Category[]>('/categories')
      .then((res) => setCategories(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <aside className="bg-white border border-gray-200 rounded-xl p-4 w-full md:w-64 shrink-0 shadow-sm h-fit">
      <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider mb-3">Categories</h3>

      {loading ? (
        <div className="space-y-2 animate-pulse">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-6 bg-gray-100 rounded w-full"></div>
          ))}
        </div>
      ) : (
        <div className="space-y-1">
          <button
            onClick={() => onSelectCategory(null)}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              selectedCategoryId === null
                ? 'bg-indigo-50 text-indigo-700 font-semibold'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            All Categories
          </button>

          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => onSelectCategory(cat.id)}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedCategoryId === cat.id
                  ? 'bg-indigo-50 text-indigo-700 font-semibold'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              {cat.name}
            </button>
          ))}
        </div>
      )}
    </aside>
  );
};
