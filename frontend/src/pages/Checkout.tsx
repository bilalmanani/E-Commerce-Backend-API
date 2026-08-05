import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CreditCard, MapPin, Tag, CheckCircle } from 'lucide-react';
import api from '../api/axios';
import { Cart, Address } from '../types';

export const Checkout: React.FC = () => {
  const [cart, setCart] = useState<Cart | null>(null);
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [selectedAddressId, setSelectedAddressId] = useState<number | null>(null);
  const [couponCode, setCouponCode] = useState('');
  const [discountPercent, setDiscountPercent] = useState<number | null>(null);
  const [placingOrder, setPlacingOrder] = useState(false);
  const [validatingCoupon, setValidatingCoupon] = useState(false);
  const [couponError, setCouponError] = useState<string | null>(null);
  
  // New address form state
  const [showAddressForm, setShowAddressForm] = useState(false);
  const [streetAddress, setStreetAddress] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [postalCode, setPostalCode] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([
      api.get<Cart>('/cart'),
      api.get<Address[]>('/addresses')
    ])
      .then(([cartRes, addrRes]) => {
        setCart(cartRes.data);
        setAddresses(addrRes.data);
        if (addrRes.data.length > 0) {
          setSelectedAddressId(addrRes.data[0].id);
        }
      })
      .catch(() => navigate('/cart'));
  }, [navigate]);

  const handleCreateAddress = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.post<Address>('/addresses', {
        street_address: streetAddress,
        city,
        state,
        postal_code: postalCode,
        country: 'USA'
      });
      setAddresses([...addresses, res.data]);
      setSelectedAddressId(res.data.id);
      setShowAddressForm(false);
      setStreetAddress('');
      setCity('');
      setState('');
      setPostalCode('');
    } catch {
      alert('Could not save address');
    }
  };

  const handleValidateCoupon = async () => {
    if (!couponCode) return;
    setValidatingCoupon(true);
    setCouponError(null);
    try {
      const res = await api.post('/coupons/validate', { code: couponCode });
      setDiscountPercent(Number(res.data.discount_percentage));
    } catch (err: any) {
      setCouponError(err.response?.data?.message || 'Invalid coupon code');
      setDiscountPercent(null);
    } finally {
      setValidatingCoupon(false);
    }
  };

  const handlePlaceOrder = async () => {
    if (!selectedAddressId) {
      alert('Please select or add a shipping address');
      return;
    }

    setPlacingOrder(true);
    try {
      await api.post('/orders', {
        shipping_address_id: selectedAddressId,
        coupon_code: couponCode || undefined
      });
      navigate('/orders');
    } catch (err: any) {
      alert(err.response?.data?.message || 'Could not place order');
    } finally {
      setPlacingOrder(false);
    }
  };

  if (!cart) return null;

  const originalTotal = Number(cart.total_price);
  const discountAmount = discountPercent ? (originalTotal * discountPercent) / 100 : 0;
  const finalTotal = originalTotal - discountAmount;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      <h1 className="text-3xl font-black text-gray-900">Checkout</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Addresses & Payment Method */}
        <div className="lg:col-span-2 space-y-6">
          {/* Shipping Addresses */}
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
                <MapPin className="w-5 h-5 text-indigo-600" />
                <span>1. Shipping Address</span>
              </h2>
              <button
                onClick={() => setShowAddressForm(!showAddressForm)}
                className="text-xs font-semibold text-indigo-600 hover:text-indigo-700"
              >
                {showAddressForm ? 'Cancel' : '+ Add Address'}
              </button>
            </div>

            {showAddressForm ? (
              <form onSubmit={handleCreateAddress} className="bg-gray-50 p-4 rounded-xl space-y-3 border border-gray-200">
                <input
                  type="text"
                  required
                  placeholder="Street Address (e.g. 123 Main St)"
                  value={streetAddress}
                  onChange={(e) => setStreetAddress(e.target.value)}
                  className="w-full p-2.5 bg-white border border-gray-300 rounded-lg text-sm"
                />
                <div className="grid grid-cols-3 gap-3">
                  <input
                    type="text"
                    required
                    placeholder="City"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="p-2.5 bg-white border border-gray-300 rounded-lg text-sm"
                  />
                  <input
                    type="text"
                    required
                    placeholder="State"
                    value={state}
                    onChange={(e) => setState(e.target.value)}
                    className="p-2.5 bg-white border border-gray-300 rounded-lg text-sm"
                  />
                  <input
                    type="text"
                    required
                    placeholder="Zip Code"
                    value={postalCode}
                    onChange={(e) => setPostalCode(e.target.value)}
                    className="p-2.5 bg-white border border-gray-300 rounded-lg text-sm"
                  />
                </div>
                <button type="submit" className="bg-indigo-600 text-white text-xs font-bold px-4 py-2 rounded-lg">
                  Save Address
                </button>
              </form>
            ) : addresses.length === 0 ? (
              <p className="text-sm text-gray-500">No addresses saved. Please add one above.</p>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {addresses.map((addr) => (
                  <div
                    key={addr.id}
                    onClick={() => setSelectedAddressId(addr.id)}
                    className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${
                      selectedAddressId === addr.id
                        ? 'border-indigo-600 bg-indigo-50/50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <p className="font-bold text-sm text-gray-900">{addr.street_address}</p>
                    <p className="text-xs text-gray-500 mt-1">{addr.city}, {addr.state} {addr.postal_code}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Payment Simulation */}
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
            <h2 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
              <CreditCard className="w-5 h-5 text-indigo-600" />
              <span>2. Payment Method</span>
            </h2>
            <div className="bg-emerald-50 border border-emerald-200 p-4 rounded-xl text-emerald-800 text-sm flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 shrink-0" />
              <span>Test Checkout Mode: Order will process transactional stock deduction automatically.</span>
            </div>
          </div>
        </div>

        {/* Right Column: Order Summary & Coupon */}
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-6">
            <h2 className="text-lg font-bold text-gray-900">Order Summary</h2>

            {/* Coupon Code Section */}
            <div className="space-y-2">
              <label className="block text-xs font-semibold text-gray-700">Promo / Coupon Code</label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="SAVE20"
                  value={couponCode}
                  onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm uppercase"
                />
                <button
                  onClick={handleValidateCoupon}
                  disabled={validatingCoupon || !couponCode}
                  className="bg-gray-900 text-white text-xs font-bold px-3 py-2 rounded-lg hover:bg-gray-800 disabled:opacity-50"
                >
                  Apply
                </button>
              </div>
              {discountPercent && (
                <p className="text-xs text-emerald-600 font-semibold">✓ Coupon applied: {discountPercent}% OFF</p>
              )}
              {couponError && <p className="text-xs text-red-500 font-semibold">{couponError}</p>}
            </div>

            {/* Price Calculations */}
            <div className="space-y-3 text-sm border-t border-b border-gray-100 py-4">
              <div className="flex justify-between text-gray-600">
                <span>Subtotal</span>
                <span>${originalTotal.toFixed(2)}</span>
              </div>
              {discountAmount > 0 && (
                <div className="flex justify-between text-emerald-600 font-semibold">
                  <span>Discount ({discountPercent}%)</span>
                  <span>-${discountAmount.toFixed(2)}</span>
                </div>
              )}
              <div className="flex justify-between text-gray-600">
                <span>Shipping</span>
                <span className="text-emerald-600 font-semibold">FREE</span>
              </div>
              <div className="flex justify-between font-black text-lg text-gray-900 pt-2 border-t border-gray-100">
                <span>Total Amount</span>
                <span>${finalTotal.toFixed(2)}</span>
              </div>
            </div>

            <button
              onClick={handlePlaceOrder}
              disabled={placingOrder || !selectedAddressId}
              className="w-full bg-indigo-600 text-white font-extrabold text-base py-3.5 rounded-xl hover:bg-indigo-700 disabled:opacity-50 transition-colors shadow-md"
            >
              {placingOrder ? 'Processing Order...' : 'Place Order Now'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
