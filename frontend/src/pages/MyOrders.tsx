import React, { useEffect, useState } from 'react';
import { Package, Clock, Ban } from 'lucide-react';
import api from '../api/axios';
import { Order } from '../types';

export const MyOrders: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = async () => {
    try {
      const res = await api.get<Order[]>('/orders');
      setOrders(res.data);
    } catch {
      setOrders([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleCancelOrder = async (orderId: number) => {
    if (!confirm('Are you sure you want to cancel this order? Item stock will be restored.')) return;
    try {
      await api.post(`/orders/${orderId}/cancel`);
      fetchOrders();
    } catch (err: any) {
      alert(err.response?.data?.message || 'Could not cancel order');
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 animate-pulse space-y-4">
        <div className="h-32 bg-gray-200 rounded-2xl"></div>
        <div className="h-32 bg-gray-200 rounded-2xl"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <h1 className="text-3xl font-black text-gray-900">My Orders & Purchase History</h1>

      {orders.length === 0 ? (
        <div className="text-center py-16 bg-white border border-gray-200 rounded-2xl p-8 space-y-2">
          <Package className="w-16 h-16 text-gray-300 mx-auto" />
          <h2 className="text-lg font-bold text-gray-800">No orders found</h2>
          <p className="text-gray-500 text-sm">You haven't placed any orders yet.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => (
            <div key={order.id} className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
              {/* Order Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-gray-100">
                <div>
                  <span className="text-xs text-gray-500 font-mono">Order ID: #{order.id}</span>
                  <div className="flex items-center space-x-2 mt-1">
                    <Clock className="w-3.5 h-3.5 text-gray-400" />
                    <span className="text-xs text-gray-500">
                      {new Date(order.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>

                <div className="flex items-center space-x-4">
                  <span className={`text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider ${
                    order.status === 'delivered' ? 'bg-emerald-100 text-emerald-800' :
                    order.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                    order.status === 'shipped' ? 'bg-blue-100 text-blue-800' :
                    'bg-amber-100 text-amber-800'
                  }`}>
                    {order.status}
                  </span>

                  {order.status === 'pending' && (
                    <button
                      onClick={() => handleCancelOrder(order.id)}
                      className="text-xs font-semibold text-red-600 hover:text-red-700 flex items-center space-x-1"
                    >
                      <Ban className="w-3.5 h-3.5" />
                      <span>Cancel Order</span>
                    </button>
                  )}
                </div>
              </div>

              {/* Order Items */}
              <div className="space-y-3">
                {order.items.map((item) => (
                  <div key={item.id} className="flex justify-between items-center text-sm">
                    <div>
                      <span className="font-bold text-gray-900">{item.product?.title || `Product #${item.product_id}`}</span>
                      <span className="text-xs text-gray-500 ml-2">x{item.quantity}</span>
                    </div>
                    <span className="font-mono text-gray-700">${Number(item.price_at_purchase).toFixed(2)}</span>
                  </div>
                ))}
              </div>

              {/* Order Footer */}
              <div className="pt-4 border-t border-gray-100 flex justify-between items-center font-bold text-sm">
                <span className="text-gray-600">Total Paid:</span>
                <span className="text-lg font-black text-gray-900">${Number(order.total_amount).toFixed(2)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
