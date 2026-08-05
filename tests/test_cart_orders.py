import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_cart_and_order_checkout_flow(
    client: AsyncClient,
    auth_headers: dict,
    admin_auth_headers: dict
):
    """
    Complete end-to-end integration test:
    1. Admin creates category and product.
    2. Customer adds shipping address.
    3. Customer adds product to cart.
    4. Customer places order (checks stock deduction and cart clearance).
    5. Customer cancels order (checks stock restoration).
    """
    # 1. Admin creates category & product (stock = 5)
    cat_res = await client.post(
        "/categories",
        json={"name": "Audio", "description": "Headphones and speakers"},
        headers=admin_auth_headers
    )
    cat_id = cat_res.json()["id"]

    prod_res = await client.post(
        "/products",
        json={
            "title": "Wireless Headphones",
            "description": "Noise cancelling over-ear headphones",
            "price": 199.99,
            "stock": 5,
            "category_id": cat_id,
            "is_available": True
        },
        headers=admin_auth_headers
    )
    product_id = prod_res.json()["id"]

    # 2. Customer creates shipping address
    addr_res = await client.post(
        "/addresses",
        json={
            "street_address": "456 Test Ave",
            "city": "Boston",
            "state": "MA",
            "postal_code": "02108",
            "country": "USA"
        },
        headers=auth_headers
    )
    address_id = addr_res.json()["id"]

    # 3. Customer adds 2 headphones to cart
    cart_res = await client.post(
        "/cart/items",
        json={"product_id": product_id, "quantity": 2},
        headers=auth_headers
    )
    assert cart_res.status_code == 200
    assert len(cart_res.json()["items"]) == 1

    # 4. Customer places order
    order_res = await client.post(
        "/orders",
        json={"shipping_address_id": address_id},
        headers=auth_headers
    )
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]
    assert order_res.json()["total_amount"] == "399.98"

    # Verify product stock reduced from 5 to 3
    get_prod = await client.get(f"/products/{product_id}")
    assert get_prod.json()["stock"] == 3

    # Verify cart is now empty
    get_cart = await client.get("/cart", headers=auth_headers)
    assert len(get_cart.json()["items"]) == 0

    # 5. Customer cancels order
    cancel_res = await client.post(f"/orders/{order_id}/cancel", headers=auth_headers)
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "cancelled"

    # Verify product stock restored from 3 back to 5
    get_prod_restored = await client.get(f"/products/{product_id}")
    assert get_prod_restored.json()["stock"] == 5
