"""Shared test setup: every test starts from the same clean data."""

import pytest
from fastapi.testclient import TestClient

from app.cart import reset_cart_data
from app.main import app
from app.orders import reset_order_data


@pytest.fixture(autouse=True)
def clean_data():
    """Reset all in-memory data before each test."""
    reset_cart_data()
    reset_order_data()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def cart_id(client):
    """Create an empty cart and return its id."""
    return client.post("/carts").json()["id"]
