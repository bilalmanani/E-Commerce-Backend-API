import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Home } from './pages/Home';
import { ProductListing } from './pages/ProductListing';
import { ProductDetails } from './pages/ProductDetails';
import { ShoppingCartPage } from './pages/ShoppingCart';
import { Checkout } from './pages/Checkout';
import { UserProfile } from './pages/UserProfile';
import { MyOrders } from './pages/MyOrders';
import { AdminDashboard } from './pages/AdminDashboard';

export const App: React.FC = () => {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<ProductListing />} />
            <Route path="/products/:id" element={<ProductDetails />} />
            <Route path="/cart" element={<ShoppingCartPage />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/profile" element={<UserProfile />} />
            <Route path="/orders" element={<MyOrders />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<Home />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
