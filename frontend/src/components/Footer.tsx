import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-gray-400 py-8 mt-auto border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm">
        <p>© 2026 FASTSTORE. Designed & Developed by <span className="font-semibold text-white">Bilal Ahmad</span>. Built with FastAPI, PostgreSQL & React.</p>
      </div>
    </footer>
  );
};
