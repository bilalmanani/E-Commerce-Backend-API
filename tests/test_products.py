import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category_admin_only(client: AsyncClient, admin_auth_headers: dict):
    """Test admin can create a new product category."""
    cat_payload = {
        "name": "Electronics",
        "description": "Gadgets and tech items"
    }
    response = await client.post("/categories", json=cat_payload, headers=admin_auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Electronics"
    assert data["slug"] == "electronics"


@pytest.mark.asyncio
async def test_create_category_forbidden_for_customer(client: AsyncClient, auth_headers: dict):
    """Test non-admin customer cannot create categories (403 Forbidden)."""
    cat_payload = {
        "name": "Unauthorized Cat",
        "description": "Should fail"
    }
    response = await client.post("/categories", json=cat_payload, headers=auth_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_and_filter_products(client: AsyncClient, admin_auth_headers: dict):
    """Test creating products and filtering them by category and search keyword."""
    # 1. Create Category
    cat_res = await client.post(
        "/categories",
        json={"name": "Laptops", "description": "High performance laptops"},
        headers=admin_auth_headers
    )
    category_id = cat_res.json()["id"]

    # 2. Create Product
    prod_payload = {
        "title": "MacBook Pro 16",
        "description": "High performance Apple Silicon laptop",
        "price": 2499.99,
        "stock": 10,
        "category_id": category_id,
        "is_available": True
    }
    prod_res = await client.post("/products", json=prod_payload, headers=admin_auth_headers)
    assert prod_res.status_code == 201

    # 3. List products & search filter
    list_res = await client.get("/products?search=MacBook")
    assert list_res.status_code == 200
    items = list_res.json()["items"]
    assert len(items) == 1
    assert items[0]["title"] == "MacBook Pro 16"
