"""Tests for the product catalogue route."""


def stock_of(client, product_id):
    products = client.get("/products").json()
    return next(item["stock"] for item in products if item["id"] == product_id)


def test_list_products_returns_the_catalogue(client):
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "keyboard",
            "name": "Mechanical Keyboard",
            "price_cents": 4999,
            "stock": 10,
        },
        {"id": "mouse", "name": "Wireless Mouse", "price_cents": 2499, "stock": 25},
        {"id": "monitor", "name": "27-inch Monitor", "price_cents": 19999, "stock": 5},
    ]


def test_list_products_shows_stock_after_an_order(client, cart_id):
    client.post(f"/carts/{cart_id}/items", json={"product_id": "monitor", "quantity": 2})
    client.post("/orders", json={"cart_id": cart_id})

    assert stock_of(client, "monitor") == 3


def test_list_products_shows_stock_after_a_cancellation(client, cart_id):
    client.post(f"/carts/{cart_id}/items", json={"product_id": "monitor", "quantity": 2})
    order_id = client.post("/orders", json={"cart_id": cart_id}).json()["id"]

    client.post(f"/orders/{order_id}/cancel")

    assert stock_of(client, "monitor") == 5
