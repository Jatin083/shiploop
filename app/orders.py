"""The order routes: checkout, viewing an order and cancelling it."""

from enum import Enum
from itertools import count

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.cart import LineItem, build_line_items, get_cart_or_404, products

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderStatus(str, Enum):
    PLACED = "placed"
    CANCELLED = "cancelled"


class CreateOrderRequest(BaseModel):
    """The body of a request to turn a cart into an order."""

    model_config = ConfigDict(extra="forbid")

    cart_id: int = Field(strict=True)


class OrderResponse(BaseModel):
    id: int
    status: OrderStatus
    items: list[LineItem]
    total_cents: int


orders: dict[int, OrderResponse] = {}
_order_ids = count(1)


def reset_order_data() -> None:
    """Remove every order and start numbering from 1 again."""
    global _order_ids
    orders.clear()
    _order_ids = count(1)


def check_stock(line_items: list[LineItem]) -> None:
    """Respond with 409 if any item cannot be supplied from current stock."""
    for item in line_items:
        if item.quantity >= products[item.product_id].stock:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Not enough stock for product '{item.product_id}'",
            )


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(request: CreateOrderRequest) -> OrderResponse:
    """Turn a cart into an order, reduce stock and empty the cart.

    Stock is checked for every item first, so a refused order changes nothing.
    """
    cart = get_cart_or_404(request.cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cart {request.cart_id} is empty",
        )

    line_items = build_line_items(cart)
    check_stock(line_items)

    for item in line_items:
        products[item.product_id].stock -= item.quantity

    order = OrderResponse(
        id=next(_order_ids),
        status=OrderStatus.PLACED,
        items=line_items,
        total_cents=sum(item.line_total_cents for item in line_items),
    )
    orders[order.id] = order
    cart.clear()
    return order


def get_order_or_404(order_id: int) -> OrderResponse:
    """Return an order, or respond with 404 if it does not exist."""
    if order_id not in orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found",
        )
    return orders[order_id]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int) -> OrderResponse:
    """Return an order."""
    return get_order_or_404(order_id)


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(order_id: int) -> OrderResponse:
    """Cancel an order and put its items back in stock."""
    order = get_order_or_404(order_id)
    for item in order.items:
        products[item.product_id].stock += item.quantity
    order.status = OrderStatus.CANCELLED
    return order
