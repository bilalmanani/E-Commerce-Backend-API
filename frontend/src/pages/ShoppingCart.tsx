import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Trash2, ShoppingBag, ArrowRight } from 'lucide-react';
import api from '../api/axios';
import { Cart } from '../types';

export const ShoppingCartPage: React.FC = () => {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchCart = async () => {
    try {
      const res = await api.get<Cart>('/cart');
      setCart(res.data);
    } catch {
      setCart(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const handleUpdateQuantity = async (itemId: number, newQuantity: number) => {
    if (newQuantity < 1) return;
    try {
      await api.put(`/cart/items/${itemId}`, { quantity: newQuantity });
      fetchCart();
    } catch {
      alert('Could not update item quantity');
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    try {
      await api.delete(`/cart/items/${itemId}`);
      fetchCart();
    } catch {
      alert('Could not remove item');
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 animate-pulse space-y-4">
        <div className="h-20 bg-gray-200 rounded-xl"></div>
        <div className="h-20 bg-gray-200 rounded-xl"></div>
      </div>
    );
  }

  const isEmpty = !cart || !cart.items || cart.items.length === 0;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <h1 className="text-3xl font-black text-gray-900">Your Shopping Cart</h1>

      {isEmpty ? (
        <div className="text-center py-16 bg-white border border-gray-200 rounded-2xl p-8 space-y-4">
          <ShoppingBag className="w-16 h-16 text-gray-300 mx-auto" />
          <h2 className="text-lg font-bold text-gray-800">Your cart is empty</h2>
          <p className="text-gray-500 text-sm">Add some products to your cart to begin shopping.</p>
          <Link
            to="/products"
            className="inline-flex items-center space-x-2 bg-indigo-600 text-white font-semibold text-sm px-6 py-2.5 rounded-xl hover:bg-indigo-700 transition-colors"
          >
            <span>Browse Products</span>
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-2xl divide-y divide-gray-100 shadow-sm overflow-hidden">
            {cart.items.map((item) => (
              <div key={item.id} className="p-4 sm:p-6 flex items-center justify-between gap-4">
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-16 bg-gray-50 rounded-lg flex items-center justify-center p-2 border border-gray-100 shrink-0">
                    {item.product.image_url ? (
                      <img src={item.product.image_url} alt={item.product.title} className="max-h-full object-contain" />
                    ) : (
                      <span className="text-xs text-gray-400">No Image</span>
                    )}
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900 text-sm">{item.product.title}</h3>
                    <p className="text-xs text-gray-500 mt-0.5">
                      ${Number(item.product.discount_price || item.product.price).toFixed(2)} each
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-6">
                  <div className="flex items-center space-x-2 border border-gray-200 rounded-lg p-1">
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                      className="px-2 text-gray-600 hover:text-indigo-600 font-bold"
                    >
                      -
                    </button>
                    <span className="text-xs font-bold px-2">{item.quantity}</span>
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                      className="px-2 text-gray-600 hover:text-indigo-600 font-bold"
                    >
                      +
                    </button>
                  </div>

                  <span className="font-extrabold text-gray-900 text-base w-20 text-right">
                    ${Number(item.subtotal).toFixed(2)}
                  </span>

                  <button
                    onClick={() => handleRemoveItem(item.id)}
                    className="text-gray-400 hover:text-red-500 p-1.5 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <span className="text-gray-500 text-sm">Total Cart Amount</span>
              <div className="text-3xl font-black text-gray-900">
                ${Number(cart.total_price).toFixed(2)}
              </div>
            </div>

            <button
              onClick={() => navigate('/checkout')}
              className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 bg-indigo-600 text-white font-bold text-base px-8 py-3.5 rounded-xl hover:bg-indigo-700 transition-colors shadow-md"
            >
              <span>Proceed to Checkout</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
