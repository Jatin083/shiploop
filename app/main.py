"""Creates the ShipLoop API and connects its routes."""

from fastapi import FastAPI

from app.cart import router as cart_router
from app.orders import router as orders_router

app = FastAPI(
    title="ShipLoop Cart and Orders API",
    description="A small shop backend for the Flip the Switch Hackathon.",
    version="0.1.0",
)

app.include_router(cart_router)
app.include_router(orders_router)
