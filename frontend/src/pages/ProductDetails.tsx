import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ShoppingCart, Star, Heart, ArrowLeft, CheckCircle2 } from 'lucide-react';
import api from '../api/axios';
import { Product } from '../types';

interface Review {
  id: number;
  rating: number;
  comment?: string;
  created_at: string;
  user?: {
    first_name: string;
    last_name: string;
  };
}

export const ProductDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<Product | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [quantity, setQuantity] = useState(1);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [submittingReview, setSubmittingReview] = useState(false);
  const [added, setAdded] = useState(false);

  useEffect(() => {
    if (!id) return;

    Promise.all([
      api.get<Product>(`/products/${id}`),
      api.get<Review[]>(`/reviews/product/${id}`)
    ])
      .then(([prodRes, revRes]) => {
        setProduct(prodRes.data);
        setReviews(revRes.data);
      })
      .catch(() => {
        navigate('/products');
      })
      .finally(() => setLoading(false));
  }, [id, navigate]);

  const handleAddToCart = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return navigate('/login');

    try {
      await api.post('/cart/items', {
        product_id: product?.id,
        quantity
      });
      setAdded(true);
      setTimeout(() => setAdded(false), 2500);
    } catch {
      alert('Could not add product to cart');
    }
  };

  const handleReviewSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem('access_token');
    if (!token) return navigate('/login');

    setSubmittingReview(true);
    try {
      await api.post('/reviews', {
        product_id: product?.id,
        rating,
        comment
      });
      // Refresh reviews
      const revRes = await api.get<Review[]>(`/reviews/product/${id}`);
      setReviews(revRes.data);
      setComment('');
    } catch (err: any) {
      alert(err.response?.data?.message || 'Could not submit review');
    } finally {
      setSubmittingReview(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 animate-pulse space-y-8">
        <div className="h-96 bg-gray-200 rounded-2xl w-full"></div>
      </div>
    );
  }

  if (!product) return null;

  const price = product.discount_price ? Number(product.discount_price) : Number(product.price);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-12">
      <button
        onClick={() => navigate(-1)}
        className="inline-flex items-center space-x-2 text-sm font-medium text-gray-600 hover:text-indigo-600 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Products</span>
      </button>

      {/* Main Details Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 shadow-sm">
        <div className="bg-gray-50 rounded-xl p-8 flex items-center justify-center min-h-[350px]">
          {product.image_url ? (
            <img src={product.image_url} alt={product.title} className="max-h-80 object-contain" />
          ) : (
            <span className="text-gray-400 font-medium">No Image Available</span>
          )}
        </div>

        <div className="space-y-6">
          <div>
            <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">
              {product.category?.name || 'Category'}
            </span>
            <h1 className="text-3xl font-black text-gray-900 mt-1">{product.title}</h1>
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-3xl font-extrabold text-gray-900">${price.toFixed(2)}</span>
            {product.discount_price && (
              <span className="text-lg text-gray-400 line-through">${Number(product.price).toFixed(2)}</span>
            )}
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              product.stock > 0 ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'
            }`}>
              {product.stock > 0 ? `In Stock (${product.stock})` : 'Out of Stock'}
            </span>
          </div>

          <p className="text-gray-600 text-sm leading-relaxed border-t border-b border-gray-100 py-4">
            {product.description}
          </p>

          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <label className="text-sm font-medium text-gray-700">Quantity:</label>
              <input
                type="number"
                min={1}
                max={product.stock}
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                className="w-20 px-3 py-1.5 border border-gray-300 rounded-lg text-sm text-center"
              />
            </div>

            <div className="flex items-center space-x-4">
              <button
                onClick={handleAddToCart}
                disabled={product.stock === 0}
                className="flex-1 bg-indigo-600 text-white font-bold py-3 px-6 rounded-xl hover:bg-indigo-700 disabled:opacity-50 transition-colors flex items-center justify-center space-x-2"
              >
                {added ? (
                  <>
                    <CheckCircle2 className="w-5 h-5 text-emerald-300" />
                    <span>Added to Cart!</span>
                  </>
                ) : (
                  <>
                    <ShoppingCart className="w-5 h-5" />
                    <span>Add to Shopping Cart</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Customer Reviews Section */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-8">
        <h2 className="text-xl font-bold text-gray-900">Customer Reviews ({reviews.length})</h2>

        {/* Add Review Form */}
        <form onSubmit={handleReviewSubmit} className="bg-gray-50 p-4 rounded-xl space-y-4 border border-gray-200">
          <h3 className="text-sm font-bold text-gray-900">Write a Review</h3>
          <div className="flex items-center space-x-2">
            <label className="text-xs font-medium text-gray-600">Rating:</label>
            <select
              value={rating}
              onChange={(e) => setRating(Number(e.target.value))}
              className="bg-white border border-gray-300 text-xs rounded-lg px-2 py-1"
            >
              <option value={5}>5 Stars ★★★★★</option>
              <option value={4}>4 Stars ★★★★☆</option>
              <option value={3}>3 Stars ★★★☆☆</option>
              <option value={2}>2 Stars ★★☆☆☆</option>
              <option value={1}>1 Star ★☆☆☆☆</option>
            </select>
          </div>

          <textarea
            rows={3}
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Share your feedback about this product..."
            className="w-full p-3 border border-gray-300 rounded-lg text-sm focus:ring-indigo-500"
          ></textarea>

          <button
            type="submit"
            disabled={submittingReview}
            className="bg-gray-900 text-white text-xs font-bold px-4 py-2 rounded-lg hover:bg-gray-800 disabled:opacity-50 transition-colors"
          >
            {submittingReview ? 'Submitting...' : 'Submit Review'}
          </button>
        </form>

        {/* Reviews List */}
        <div className="space-y-4 divide-y divide-gray-100">
          {reviews.length === 0 ? (
            <p className="text-sm text-gray-500">No reviews yet for this product.</p>
          ) : (
            reviews.map((rev) => (
              <div key={rev.id} className="pt-4 space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sm text-gray-900">
                    {rev.user ? `${rev.user.first_name} ${rev.user.last_name}` : 'Customer'}
                  </span>
                  <div className="flex items-center text-amber-400">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className={`w-3.5 h-3.5 ${i < rev.rating ? 'fill-amber-400' : 'text-gray-300'}`} />
                    ))}
                  </div>
                </div>
                {rev.comment && <p className="text-gray-600 text-sm">{rev.comment}</p>}
              </div>
            ))
          ) }
        </div>
      </div>
    </div>
  );
};
