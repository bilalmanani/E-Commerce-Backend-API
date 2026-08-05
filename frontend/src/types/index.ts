export type Role = 'admin' | 'customer';

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: Role;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  title: string;
  slug: string;
  description: string;
  price: string | number;
  discount_price?: string | number | null;
  stock: number;
  is_available: boolean;
  image_url?: string | null;
  category_id: number;
  category?: Category;
  created_at: string;
  updated_at: string;
}

export interface PaginatedProducts {
  items: Product[];
  total: number;
  skip: number;
  limit: number;
}

export interface CartItem {
  id: number;
  cart_id: number;
  product_id: number;
  quantity: number;
  product: Product;
  subtotal: string | number;
}

export interface Cart {
  id: number;
  user_id: number;
  items: CartItem[];
  total_price: string | number;
}

export interface OrderItem {
  id: number;
  product_id: number;
  quantity: number;
  price_at_purchase: string | number;
  product?: Product;
}

export type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';

export interface Address {
  id: number;
  user_id: number;
  street_address: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  is_default: boolean;
}

export interface Order {
  id: number;
  user_id: number;
  shipping_address_id?: number;
  total_amount: string | number;
  status: OrderStatus;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
  shipping_address?: Address;
}

export interface DashboardStats {
  total_users: number;
  total_products: number;
  total_orders: number;
  total_revenue: string | number;
  orders_by_status: Record<string, number>;
}
