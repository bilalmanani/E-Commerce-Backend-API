import React from 'react';
import { PackageX } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  message?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = "No products found",
  message = "Try adjusting your search or category filters to find what you are looking for."
}) => {
  return (
    <div className="text-center py-16 px-4 bg-white rounded-xl border border-gray-100 shadow-sm max-w-md mx-auto my-8">
      <PackageX className="w-16 h-16 text-gray-400 mx-auto mb-4" />
      <h3 className="text-lg font-bold text-gray-900 mb-1">{title}</h3>
      <p className="text-sm text-gray-500">{message}</p>
    </div>
  );
};
