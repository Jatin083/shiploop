# ShipLoop

A small Cart and Orders API built with FastAPI for the Flip the Switch Hackathon.

Data is stored in memory, so it resets whenever the server restarts. Prices are
whole cents: `4999` means $49.99.

## Requirements

- Python 3.13
- Git

## Setup

Clone the repository and go into it:

```
git clone https://github.com/Jatin083/shiploop.git
cd shiploop
```

Create a virtual environment and install the dependencies.

Windows (PowerShell):

```
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS or Linux:

```
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the API

```
python -m uvicorn app.main:app --reload
```

The API runs at http://127.0.0.1:8000, with interactive documentation at
http://127.0.0.1:8000/docs.

## Run the tests

```
python -m pytest
```

## Endpoints

| Method | Path | What it does | Success |
|---|---|---|---|
| GET | `/products` | List products with their prices and current stock | 200 |
| POST | `/carts` | Create an empty cart | 201 |
| GET | `/carts/{cart_id}` | Show a cart, its items and total | 200 |
| POST | `/carts/{cart_id}/items` | Add a product to a cart | 201 |
| DELETE | `/carts/{cart_id}/items/{product_id}` | Remove a product from a cart | 200 |
| POST | `/orders` | Turn a cart into an order | 201 |
| GET | `/orders/{order_id}` | Show an order | 200 |
| POST | `/orders/{order_id}/cancel` | Cancel an order | 200 |

Error responses:

| Status | Meaning |
|---|---|
| 400 | The cart is empty, so it cannot become an order |
| 404 | The cart, product or order does not exist |
| 409 | There is not enough stock for the order |
| 422 | The request is invalid, such as a quantity of 0 |

## Products

| Product id | Name | Price (cents) | Starting stock |
|---|---|---:|---:|
| `keyboard` | Mechanical Keyboard | 4999 | 10 |
| `mouse` | Wireless Mouse | 2499 | 25 |
| `monitor` | 27-inch Monitor | 19999 | 5 |

## Example

```
curl -X POST http://127.0.0.1:8000/carts
curl -X POST http://127.0.0.1:8000/carts/1/items -H "Content-Type: application/json" -d "{\"product_id\": \"mouse\", \"quantity\": 2}"
curl -X POST http://127.0.0.1:8000/orders -H "Content-Type: application/json" -d "{\"cart_id\": 1}"
```

In Windows PowerShell, use `curl.exe` instead of `curl`.

## Project layout

```
app/main.py         Creates the app and connects the routes
app/cart.py         Product catalogue and cart routes
app/orders.py       Checkout, order and cancellation routes
tests/conftest.py   Resets the data before each test
tests/              The test suite
```
