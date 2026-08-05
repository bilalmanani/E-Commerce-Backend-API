import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    """Test user registration with valid payload."""
    payload = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "strongpassword123",
        "role": "customer"
    }
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_user_duplicate_email(client: AsyncClient):
    """Test registration fails when email is already registered."""
    payload = {
        "email": "duplicate@example.com",
        "first_name": "Dup",
        "last_name": "User",
        "password": "password123",
        "role": "customer"
    }
    # First registration
    res1 = await client.post("/auth/register", json=payload)
    assert res1.status_code == 201

    # Second duplicate registration
    res2 = await client.post("/auth/register", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["message"].lower()


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test user login returns access and refresh tokens."""
    # Register user first
    reg_payload = {
        "email": "loginuser@example.com",
        "first_name": "Login",
        "last_name": "Test",
        "password": "mypassword123",
        "role": "customer"
    }
    await client.post("/auth/register", json=reg_payload)

    # Login with form data
    login_data = {
        "username": "loginuser@example.com",
        "password": "mypassword123"
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login fails with incorrect password."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 401
