# ⚡ Enterprise E-Commerce Backend API & Storefront

A production-ready, high-performance E-Commerce platform built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, **PostgreSQL**, **Pydantic v2**, and **React (Vite + Tailwind CSS)**.

![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0_Async-red.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB.svg?style=for-the-badge&logo=React&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)

---

## 🌟 Key Features

### 🔐 Authentication & Security
- **OAuth2 JWT Token Authentication**: Dual token system with access and refresh tokens.
- **Bcrypt Password Hashing**: Safe UTF-8 password hashing with length validation.
- **Role-Based Access Control (RBAC)**: Fine-grained permissions for `customer` and `admin` roles.

### 🛍️ Product & Catalog Engine
- **Hierarchical Categories**: Dynamic category creation with automatic slugification.
- **Full-Text Search & Filtering**: Multi-field search (title, description), category filtering, min/max price range thresholds, and dynamic sorting.
- **Discount & Pricing Engine**: Supports standard price, discount price, auto-percentage savings calculation, and stock availability flags.
- **Rich Media Support**: Integrated product image URLs with graceful fallbacks.

### 🛒 Shopping Cart & Orders
- **Persistent Shopping Cart**: Async cart management per user with real-time stock checks.
- **Atomic Checkout Pipeline**: Converts shopping cart items into verified orders with stock deduction in a database transaction.
- **Order Tracking & History**: Full order history, item snapshots, shipping address linkage, and order status workflow.

### ⭐ Reviews, Wishlist & Discounts
- **Product Reviews & Ratings**: 1 to 5-star ratings with review text.
- **User Wishlist**: Add/remove favorite products.
- **Coupon Code System**: Percentage and fixed amount discount coupons.

### 📊 Storefront Interfaces
- **Interactive Single-Page Storefront** (`static/`): Lightweight HTML5/CSS3/JavaScript app with dark mode glassmorphism design, category pills, search bar, and cart modal.
- **Modern React Single-Page Application** (`frontend/`): Full React 18 frontend built with Vite, TypeScript, and Tailwind CSS.

---

## 🏗️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI** | High performance async web framework with automatic OpenAPI documentation. |
| **Database ORM** | **SQLAlchemy 2.0** | Fully asynchronous ORM using `asyncpg` driver. |
| **Database** | **PostgreSQL** | Relational database engine for production storage. |
| **Data Validation** | **Pydantic v2** | Strict schema validation and serialization. |
| **Migrations** | **Alembic** | Database schema versioning and migration tool. |
| **Testing** | **Pytest & Pytest-Asyncio** | Async automated test suite covering auth, products, and checkout. |
| **Frontend** | **React / Vite / Tailwind** | Responsive frontend interface with TypeScript. |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.11+
- PostgreSQL server running locally or via Docker
- Node.js & npm (for React frontend)

### 2. Repository Setup

Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/E-Commerce-Backend-API.git
cd E-Commerce-Backend-API
```

Set up a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the example environment file and set your database credentials:
```bash
cp .env.example .env
```

`.env` configuration example:
```env
APP_NAME="E-Commerce API"
APP_ENV=development
DEBUG=True
PORT=8000

# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce_db
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ecommerce_db

# Security & JWT
SECRET_KEY=supersecretkey_change_this_in_production_32bytes_min
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 4. Database Migrations & Seeding

Apply Alembic migrations to create database tables:
```bash
alembic upgrade head
```

Run the automated seed script to populate realistic demo products, categories, images, and user accounts:
```bash
python seed_demo_data.py
```

### 5. Running the Application

#### Start the Backend API Server:
```bash
uvicorn app.main:app --reload --port 8000
```
- Interactive Swagger API Docs: `http://localhost:8000/docs`
- ReDoc API Documentation: `http://localhost:8000/redoc`
- Built-in Storefront UI: `http://localhost:8000/`

#### Start the React Frontend (Optional):
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` (or `http://localhost:3001`) in your browser.

---

## 🔑 Demo Account Credentials

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `bilalmandani7@gmail.com` | `password123` |
| **Customer** | `bilalmandani4@gmail.com` | `password123` |
| **Customer** | `bilalmandani9@gmail.com` | `password123` |

---

## 📡 API Endpoints Matrix

### 🔓 Public Endpoints
- `GET /products` - Search, filter, sort & paginate products.
- `GET /products/{id}` - Retrieve detailed product information.
- `GET /categories` - List active product categories.
- `GET /health` - API health check status.

### 🔐 Authentication
- `POST /auth/register` - Create a customer or admin account.
- `POST /auth/login` - Obtain JWT Access & Refresh tokens.
- `POST /auth/refresh` - Refresh an expired access token.

### 🛒 Customer Endpoints (Auth Required)
- `GET /users/me` - Fetch authenticated profile.
- `GET /cart` - Retrieve current shopping cart & items.
- `POST /cart/items` - Add product to cart.
- `DELETE /cart/items/{item_id}` - Remove item from cart.
- `POST /orders` - Place order & checkout cart items.
- `GET /orders` - View user order history.

### 🛡️ Admin Endpoints (Admin Token Required)
- `POST /products` - Create a new product.
- `PUT /products/{id}` - Update product attributes.
- `DELETE /products/{id}` - Delete product.
- `POST /categories` - Create new product category.
- `GET /admin/analytics` - View store metrics & sales summary.

---

## 🧪 Automated Testing

Run the full pytest suite with asynchronous support:
```bash
pytest -v
```

Tests cover:
- User registration & duplicate email validation
- Authentication & invalid credentials handling
- Product creation & category filtering
- Shopping cart management & order checkout flow

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
