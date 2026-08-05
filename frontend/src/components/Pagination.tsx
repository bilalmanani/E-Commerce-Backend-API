import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
  total: number;
  skip: number;
  limit: number;
  onPageChange: (newSkip: number) => void;
}

export const Pagination: React.FC<PaginationProps> = ({ total, skip, limit, onPageChange }) => {
  const currentPage = Math.floor(skip / limit) + 1;
  const totalPages = Math.ceil(total / limit);

  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 rounded-xl mt-8 shadow-sm">
      <div className="text-sm text-gray-700">
        Showing <span className="font-medium">{skip + 1}</span> to{' '}
        <span className="font-medium">{Math.min(skip + limit, total)}</span> of{' '}
        <span className="font-medium">{total}</span> results
      </div>

      <div className="flex items-center space-x-2">
        <button
          onClick={() => onPageChange(skip - limit)}
          disabled={skip === 0}
          className="p-2 rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-50 disabled:opacity-40 transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>

        <span className="text-sm font-semibold text-gray-700 px-2">
          Page {currentPage} of {totalPages}
        </span>

        <button
          onClick={() => onPageChange(skip + limit)}
          disabled={skip + limit >= total}
          className="p-2 rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-50 disabled:opacity-40 transition-colors"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
