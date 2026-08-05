import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, Heart } from 'lucide-react';
import { Product } from '../types';
import api from '../api/axios';

interface ProductCardProps {
  product: Product;
  onCartAdded?: () => void;
}

const DEFAULT_PRODUCT_IMAGE = "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80";

export const ProductCard: React.FC<ProductCardProps> = ({ product, onCartAdded }) => {
  const [adding, setAdding] = useState(false);
  const [inWishlist, setInWishlist] = useState(false);
  const navigate = useNavigate();

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    setAdding(true);
    try {
      await api.post('/cart/items', {
        product_id: product.id,
        quantity: 1
      });
      if (onCartAdded) onCartAdded();
    } catch {
      alert('Could not add to cart');
    } finally {
      setAdding(false);
    }
  };

  const handleToggleWishlist = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      if (inWishlist) {
        await api.delete(`/wishlist/${product.id}`);
        setInWishlist(false);
      } else {
        await api.post(`/wishlist/${product.id}`);
        setInWishlist(true);
      }
    } catch {
      // Handled silently
    }
  };

  const currentPrice = product.discount_price ? Number(product.discount_price) : Number(product.price);
  const originalPrice = product.discount_price ? Number(product.price) : null;
  const imageUrl = product.image_url || DEFAULT_PRODUCT_IMAGE;

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between group">
      <Link to={`/products/${product.id}`} className="block relative">
        <div className="h-48 bg-gray-50 flex items-center justify-center p-4 overflow-hidden relative">
          <img
            src={imageUrl}
            alt={product.title}
            onError={(e) => { (e.target as HTMLImageElement).src = DEFAULT_PRODUCT_IMAGE; }}
            className="max-h-full object-contain group-hover:scale-105 transition-transform duration-300"
          />
          <button
            onClick={handleToggleWishlist}
            className="absolute top-3 right-3 p-2 rounded-full bg-white/80 backdrop-blur-sm text-gray-600 hover:text-red-500 transition-colors shadow-sm"
          >
            <Heart className={`w-4 h-4 ${inWishlist ? 'fill-red-500 text-red-500' : ''}`} />
          </button>
        </div>

        <div className="p-4 space-y-2">
          <div className="text-xs font-semibold text-indigo-600 uppercase tracking-wider">
            {product.category?.name || 'General'}
          </div>
          <h3 className="font-bold text-gray-900 text-base line-clamp-1 group-hover:text-indigo-600 transition-colors">
            {product.title}
          </h3>
          <p className="text-gray-500 text-xs line-clamp-2 leading-relaxed">
            {product.description}
          </p>
        </div>
      </Link>

      <div className="p-4 pt-0 flex items-center justify-between mt-auto">
        <div>
          <span className="text-lg font-extrabold text-gray-900">${currentPrice.toFixed(2)}</span>
          {originalPrice && (
            <span className="text-xs text-gray-400 line-through ml-2">${originalPrice.toFixed(2)}</span>
          )}
        </div>

        <button
          onClick={handleAddToCart}
          disabled={adding || !product.is_available || product.stock === 0}
          className="flex items-center space-x-1.5 bg-indigo-600 text-white text-xs font-semibold px-3 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          <ShoppingCart className="w-3.5 h-3.5" />
          <span>{adding ? 'Adding...' : 'Add'}</span>
        </button>
      </div>
    </div>
  );
};
