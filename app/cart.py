"""The product catalogue and the shopping cart routes.

All data is held in memory, so it is lost when the server stops.
Prices are whole cents: 4999 means $49.99.
"""

from dataclasses import dataclass
from itertools import count

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/carts", tags=["carts"])
products_router = APIRouter(prefix="/products", tags=["products"])


@dataclass
class Product:
    id: str
    name: str
    price_cents: int
    stock: int


class ProductResponse(BaseModel):
    id: str
    name: str
    price_cents: int
    stock: int


class AddItemRequest(BaseModel):
    """The body of a request to add a product to a cart."""

    model_config = ConfigDict(extra="forbid")

    product_id: str = Field(min_length=1)
    quantity: int = Field(gt=0, strict=True)


class LineItem(BaseModel):
    """One product in a cart or an order, with its cost."""

    product_id: str
    name: str
    unit_price_cents: int
    quantity: int
    line_total_cents: int


class CartResponse(BaseModel):
    id: int
    items: list[LineItem]
    total_cents: int


def default_products() -> dict[str, Product]:
    """Return the catalogue the shop starts with."""
    return {
        "keyboard": Product("keyboard", "Mechanical Keyboard", 4999, 10),
        "mouse": Product("mouse", "Wireless Mouse", 2499, 25),
        "monitor": Product("monitor", "27-inch Monitor", 19999, 5),
    }


products: dict[str, Product] = default_products()

# Each cart maps a product id to the quantity of that product in the cart.
carts: dict[int, dict[str, int]] = {}
_cart_ids = count(1)


def reset_cart_data() -> None:
    """Put the catalogue and carts back to their starting state."""
    global _cart_ids
    products.clear()
    products.update(default_products())
    carts.clear()
    _cart_ids = count(1)


def get_cart_or_404(cart_id: int) -> dict[str, int]:
    """Return a cart, or respond with 404 if it does not exist."""
    if cart_id not in carts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart {cart_id} not found",
        )
    return carts[cart_id]


def build_line_items(cart: dict[str, int]) -> list[LineItem]:
    """Turn a cart's product ids and quantities into priced line items."""
    line_items = []
    for product_id, quantity in cart.items():
        product = products[product_id]
        line_items.append(
            LineItem(
                product_id=product.id,
                name=product.name,
                unit_price_cents=product.price_cents,
                quantity=quantity,
                line_total_cents=product.price_cents * quantity,
            )
        )
    return line_items


def build_cart_response(cart_id: int, cart: dict[str, int]) -> CartResponse:
    """Build the API's view of a cart, including its total."""
    line_items = build_line_items(cart)
    return CartResponse(
        id=cart_id,
        items=line_items,
        total_cents=sum(item.line_total_cents for item in line_items),
    )


@products_router.get("", response_model=list[ProductResponse])
def list_products() -> list[ProductResponse]:
    """Return every product with its price and current stock."""
    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            price_cents=product.price_cents,
            stock=product.stock,
        )
        for product in products.values()
    ]


@router.post("", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def create_cart() -> CartResponse:
    """Create a new, empty cart."""
    cart_id = next(_cart_ids)
    carts[cart_id] = {}
    return build_cart_response(cart_id, carts[cart_id])


@router.get("/{cart_id}", response_model=CartResponse)
def get_cart(cart_id: int) -> CartResponse:
    """Return a cart with its items and total."""
    return build_cart_response(cart_id, get_cart_or_404(cart_id))


@router.post(
    "/{cart_id}/items",
    response_model=CartResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_item(cart_id: int, request: AddItemRequest) -> CartResponse:
    """Add a product to a cart. Stock is checked when the order is placed."""
    cart = get_cart_or_404(cart_id)
    if request.product_id not in products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{request.product_id}' not found",
        )
    cart[request.product_id] = cart.get(request.product_id, 0) + request.quantity
    return build_cart_response(cart_id, cart)


@router.delete("/{cart_id}/items/{product_id}", response_model=CartResponse)
def remove_item(cart_id: int, product_id: str) -> CartResponse:
    """Remove a product from a cart."""
    cart = get_cart_or_404(cart_id)
    if product_id not in cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{product_id}' is not in cart {cart_id}",
        )
    del cart[product_id]
    return build_cart_response(cart_id, cart)
