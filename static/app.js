const API_BASE = "http://127.0.0.1:8000";
let token = localStorage.getItem("access_token");
let currentUser = null;
let selectedCategoryId = null;
let currentSearch = "";

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  fetchCategories();
  fetchProducts();
  checkAuth();
});

// Toast notification helper
function showToast(msg, isError = false) {
  const toast = document.getElementById("toast");
  toast.innerText = msg;
  toast.style.borderLeftColor = isError ? "#ef4444" : "#10b981";
  toast.classList.add("active");
  setTimeout(() => toast.classList.remove("active"), 3000);
}

// Fetch and render category pills
async function fetchCategories() {
  try {
    const res = await fetch(`${API_BASE}/categories`);
    if (!res.ok) return;
    const categories = await res.json();

    const pillsContainer = document.getElementById("category-pills");
    if (!pillsContainer) return;

    pillsContainer.innerHTML = `
      <button class="category-pill ${selectedCategoryId === null ? 'active' : ''}" onclick="selectCategory(null)">
        All Products
      </button>
    `;

    categories.forEach(cat => {
      const btn = document.createElement("button");
      btn.className = `category-pill ${selectedCategoryId === cat.id ? 'active' : ''}`;
      btn.innerText = cat.name;
      btn.onclick = () => selectCategory(cat.id);
      pillsContainer.appendChild(btn);
    });
  } catch (err) {
    console.error("Failed to load categories", err);
  }
}

function selectCategory(catId) {
  selectedCategoryId = catId;
  
  // Update active pill styling
  document.querySelectorAll(".category-pill").forEach(btn => {
    btn.classList.remove("active");
  });
  
  fetchCategories();
  fetchProducts(currentSearch);
}

// Fetch and render products
async function fetchProducts(search = "") {
  try {
    currentSearch = search;
    let url = `${API_BASE}/products?limit=50`;
    if (search) url += `&search=${encodeURIComponent(search)}`;
    if (selectedCategoryId !== null) url += `&category_id=${selectedCategoryId}`;

    const res = await fetch(url);
    const data = await res.json();
    
    const grid = document.getElementById("products-grid");
    grid.innerHTML = "";

    if (!data.items || data.items.length === 0) {
      grid.innerHTML = `<p style="color: var(--text-secondary); grid-column: 1/-1; text-align:center; padding: 3rem 0;">No products found.</p>`;
      return;
    }

    data.items.forEach(prod => {
      const card = document.createElement("div");
      card.className = "product-card";
      
      const price = parseFloat(prod.price);
      const discountPrice = prod.discount_price ? parseFloat(prod.discount_price) : null;
      const hasDiscount = discountPrice !== null && discountPrice < price;
      
      const discountPercent = hasDiscount 
        ? Math.round(((price - discountPrice) / price) * 100)
        : 0;

      const fallbackImg = "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop";
      const imgUrl = prod.image_url || fallbackImg;

      const categoryName = prod.category ? prod.category.name : "";

      card.innerHTML = `
        <div>
          <div class="product-img-wrapper">
            <img src="${imgUrl}" alt="${prod.title}" class="product-img" onerror="this.onerror=null;this.src='${fallbackImg}';" />
            ${hasDiscount ? `<span class="discount-badge">SAVE ${discountPercent}%</span>` : ""}
          </div>
          ${categoryName ? `<div class="category-tag">${categoryName}</div>` : ""}
          <div class="product-title">${prod.title}</div>
          <div class="product-desc">${prod.description}</div>
        </div>
        <div>
          <div class="price-container">
            ${hasDiscount 
              ? `<span class="product-price">$${discountPrice.toFixed(2)}</span>
                 <span class="original-price">$${price.toFixed(2)}</span>`
              : `<span class="product-price">$${price.toFixed(2)}</span>`
            }
          </div>
          <button class="btn-primary" style="width:100%;" onclick="addToCart(${prod.id})">🛒 Add to Cart</button>
        </div>
      `;
      grid.appendChild(card);
    });
  } catch (err) {
    showToast("Failed to load products", true);
  }
}

// Search Handler
function handleSearch(val) {
  fetchProducts(val);
}

// Auth State Check
async function checkAuth() {
  if (!token) return updateAuthUI(false);
  try {
    const res = await fetch(`${API_BASE}/users/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) {
      currentUser = await res.json();
      updateAuthUI(true);
    } else {
      logout();
    }
  } catch {
    updateAuthUI(false);
  }
}

function updateAuthUI(isLoggedIn) {
  const authNav = document.getElementById("auth-nav");
  if (isLoggedIn && currentUser) {
    authNav.innerHTML = `
      <span style="font-size:0.9rem; color:var(--text-secondary);">Hi, <b>${currentUser.first_name}</b></span>
      <button class="nav-btn" onclick="openCartModal()">🛒 Cart</button>
      <button class="nav-btn" onclick="logout()">Logout</button>
    `;
  } else {
    authNav.innerHTML = `
      <button class="nav-btn" onclick="openModal('login-modal')">Login</button>
      <button class="btn-primary" onclick="openModal('register-modal')">Register</button>
    `;
  }
}

// Modal Handlers
function openModal(id) {
  document.getElementById(id).classList.add("active");
}

function closeModal(id) {
  document.getElementById(id).classList.remove("active");
}

// Login Execution
async function executeLogin(e) {
  e.preventDefault();
  const form = e.target;
  const formData = new URLSearchParams();
  formData.append("username", form.username.value);
  formData.append("password", form.password.value);

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData
    });

    if (res.ok) {
      const data = await res.json();
      token = data.access_token;
      localStorage.setItem("access_token", token);
      closeModal("login-modal");
      showToast("Logged in successfully!");
      checkAuth();
    } else {
      showToast("Invalid credentials", true);
    }
  } catch {
    showToast("Login error", true);
  }
}

// Register Execution
async function executeRegister(e) {
  e.preventDefault();
  const form = e.target;
  const payload = {
    email: form.email.value,
    first_name: form.first_name.value,
    last_name: form.last_name.value,
    password: form.password.value,
    role: "customer"
  };

  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      closeModal("register-modal");
      showToast("Registered! Please log in.");
      openModal("login-modal");
    } else {
      showToast("Registration failed", true);
    }
  } catch {
    showToast("Error registering", true);
  }
}

function logout() {
  token = null;
  currentUser = null;
  localStorage.removeItem("access_token");
  updateAuthUI(false);
  showToast("Logged out");
}

// Cart Operations
async function addToCart(productId) {
  if (!token) {
    showToast("Please log in to add items to cart", true);
    openModal("login-modal");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/cart/items`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ product_id: productId, quantity: 1 })
    });

    if (res.ok) {
      showToast("Added to cart!");
    } else {
      showToast("Could not add to cart", true);
    }
  } catch {
    showToast("Error adding to cart", true);
  }
}

async function openCartModal() {
  if (!token) return;
  try {
    const res = await fetch(`${API_BASE}/cart`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) {
      const cart = await res.json();
      const container = document.getElementById("cart-items");
      container.innerHTML = "";

      if (!cart.items || cart.items.length === 0) {
        container.innerHTML = `<p style="color: var(--text-secondary);">Your cart is empty.</p>`;
      } else {
        cart.items.forEach(item => {
          container.innerHTML += `
            <div style="display:flex; justify-content:space-between; margin-bottom:0.8rem; border-bottom:1px solid var(--border-color); padding-bottom:0.5rem;">
              <div>
                <b>${item.product.title}</b> (x${item.quantity})
              </div>
              <div>$${parseFloat(item.subtotal).toFixed(2)}</div>
            </div>
          `;
        });
        container.innerHTML += `<div style="font-weight:800; font-size:1.2rem; margin-top:1rem; text-align:right;">Total: $${parseFloat(cart.total_price).toFixed(2)}</div>`;
      }
      openModal("cart-modal");
    }
  } catch {
    showToast("Error loading cart", true);
  }
}
