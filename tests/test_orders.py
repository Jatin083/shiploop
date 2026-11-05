"""Tests for the order routes."""

import pytest

from app.cart import products


def add_item(client, cart_id, product_id, quantity):
    response = client.post(
        f"/carts/{cart_id}/items",
        json={"product_id": product_id, "quantity": quantity},
    )
    assert response.status_code == 201


def place_order(client, cart_id):
    response = client.post("/orders", json={"cart_id": cart_id})
    assert response.status_code == 201
    return response.json()


def test_create_order_returns_items_and_total(client, cart_id):
    add_item(client, cart_id, "keyboard", 2)
    add_item(client, cart_id, "mouse", 1)

    response = client.post("/orders", json={"cart_id": cart_id})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["status"] == "placed"
    assert [item["product_id"] for item in body["items"]] == ["keyboard", "mouse"]
    assert body["total_cents"] == 2 * 4999 + 2499


def test_create_order_reduces_stock(client, cart_id):
    add_item(client, cart_id, "monitor", 2)

    place_order(client, cart_id)

    assert products["monitor"].stock == 3


def test_create_order_empties_the_cart(client, cart_id):
    add_item(client, cart_id, "mouse", 1)

    place_order(client, cart_id)

    assert client.get(f"/carts/{cart_id}").json() == {
        "id": cart_id,
        "items": [],
        "total_cents": 0,
    }


def test_create_order_from_empty_cart_returns_400(client, cart_id):
    response = client.post("/orders", json={"cart_id": cart_id})

    assert response.status_code == 400
    assert response.json() == {"detail": f"Cart {cart_id} is empty"}


def test_create_order_from_unknown_cart_returns_404(client):
    assert client.post("/orders", json={"cart_id": 999}).status_code == 404


@pytest.mark.parametrize(
    "body",
    [{}, {"cart_id": "1"}, {"cart_id": 1.5}, {"cart_id": 1, "total_cents": 1}],
)
def test_create_order_rejects_invalid_body(client, body):
    assert client.post("/orders", json=body).status_code == 422


def test_order_for_more_than_stock_returns_409(client, cart_id):
    add_item(client, cart_id, "monitor", 6)

    response = client.post("/orders", json={"cart_id": cart_id})

    assert response.status_code == 409
    assert response.json() == {"detail": "Not enough stock for product 'monitor'"}


def test_refused_order_changes_nothing(client, cart_id):
    add_item(client, cart_id, "mouse", 1)
    add_item(client, cart_id, "monitor", 6)

    assert client.post("/orders", json={"cart_id": cart_id}).status_code == 409

    assert products["mouse"].stock == 25
    assert products["monitor"].stock == 5
    assert len(client.get(f"/carts/{cart_id}").json()["items"]) == 2
    assert client.get("/orders/1").status_code == 404


def test_get_order(client, cart_id):
    add_item(client, cart_id, "mouse", 1)
    order = place_order(client, cart_id)

    response = client.get(f"/orders/{order['id']}")

    assert response.status_code == 200
    assert response.json() == order


def test_get_unknown_order_returns_404(client):
    response = client.get("/orders/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order 999 not found"}


def test_cancel_order_sets_status_and_restores_stock(client, cart_id):
    add_item(client, cart_id, "monitor", 2)
    order = place_order(client, cart_id)

    response = client.post(f"/orders/{order['id']}/cancel")

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"
    assert client.get(f"/orders/{order['id']}").json()["status"] == "cancelled"
    assert products["monitor"].stock == 5


def test_cancel_unknown_order_returns_404(client):
    assert client.post("/orders/999/cancel").status_code == 404
