"""Tests for the cart routes."""

import pytest


def test_create_cart_starts_empty(client):
    response = client.post("/carts")

    assert response.status_code == 201
    assert response.json() == {"id": 1, "items": [], "total_cents": 0}


def test_each_new_cart_gets_its_own_id(client):
    first = client.post("/carts").json()
    second = client.post("/carts").json()

    assert first["id"] != second["id"]


def test_get_cart_returns_saved_items(client, cart_id):
    client.post(f"/carts/{cart_id}/items", json={"product_id": "mouse", "quantity": 2})

    response = client.get(f"/carts/{cart_id}")

    assert response.status_code == 200
    assert response.json()["items"] == [
        {
            "product_id": "mouse",
            "name": "Wireless Mouse",
            "unit_price_cents": 2499,
            "quantity": 2,
            "line_total_cents": 4998,
        }
    ]


def test_get_unknown_cart_returns_404(client):
    response = client.get("/carts/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cart 999 not found"}


def test_cart_id_must_be_a_number(client):
    assert client.get("/carts/not-a-number").status_code == 422


def test_add_item_returns_updated_cart(client, cart_id):
    response = client.post(
        f"/carts/{cart_id}/items", json={"product_id": "keyboard", "quantity": 3}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["items"][0]["product_id"] == "keyboard"
    assert body["items"][0]["quantity"] == 3
    assert body["total_cents"] == 14997


def test_total_adds_up_different_products(client, cart_id):
    client.post(f"/carts/{cart_id}/items", json={"product_id": "keyboard", "quantity": 1})
    client.post(f"/carts/{cart_id}/items", json={"product_id": "mouse", "quantity": 2})

    assert client.get(f"/carts/{cart_id}").json()["total_cents"] == 4999 + 2 * 2499


def test_add_item_to_unknown_cart_returns_404(client):
    response = client.post(
        "/carts/999/items", json={"product_id": "mouse", "quantity": 1}
    )

    assert response.status_code == 404


def test_add_unknown_product_returns_404(client, cart_id):
    response = client.post(
        f"/carts/{cart_id}/items", json={"product_id": "toaster", "quantity": 1}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product 'toaster' not found"}


@pytest.mark.parametrize(
    "body",
    [
        {"product_id": "mouse", "quantity": 0},
        {"product_id": "mouse", "quantity": -1},
        {"product_id": "mouse", "quantity": 1.5},
        {"product_id": "mouse", "quantity": "2"},
        {"product_id": "mouse", "quantity": True},
        {"product_id": "", "quantity": 1},
        {"product_id": "mouse"},
        {"quantity": 1},
        {"product_id": "mouse", "quantity": 1, "price_cents": 1},
    ],
)
def test_add_item_rejects_invalid_body(client, cart_id, body):
    response = client.post(f"/carts/{cart_id}/items", json=body)

    assert response.status_code == 422
    assert client.get(f"/carts/{cart_id}").json()["items"] == []


def test_remove_item(client, cart_id):
    client.post(f"/carts/{cart_id}/items", json={"product_id": "keyboard", "quantity": 1})
    client.post(f"/carts/{cart_id}/items", json={"product_id": "mouse", "quantity": 1})

    response = client.delete(f"/carts/{cart_id}/items/keyboard")

    assert response.status_code == 200
    body = response.json()
    assert [item["product_id"] for item in body["items"]] == ["mouse"]
    assert body["total_cents"] == 2499


def test_remove_item_not_in_cart_returns_404(client, cart_id):
    assert client.delete(f"/carts/{cart_id}/items/mouse").status_code == 404


def test_remove_item_from_unknown_cart_returns_404(client):
    assert client.delete("/carts/999/items/mouse").status_code == 404
