
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

# Real-life example: Order with nested Product and Customer models
class Product(BaseModel):
	id: int
	name: str
	price: float = Field(..., gt=0)

class Customer(BaseModel):
	id: int
	name: str
	email: str

class Order(BaseModel):
	order_id: int
	customer: Customer
	products: List[Product]
	total: float = Field(..., gt=0)
	notes: Optional[str] = None

try:
	order = Order(
		order_id=101,
		customer={
			"id": 1,
			"name": "Arif Khan",
			"email": "arif@example.com"
		},
		products=[
			{"id": 1, "name": "Laptop", "price": 1000.0},
			{"id": 2, "name": "Mouse", "price": 25.0}
		],
		total=1025.0,
		notes="Express delivery requested"
	)
	print(order)
	print("Serialized JSON:", order.json())
except ValidationError as e:
	print("Validation error:", e)

# Example of validation error
try:
	bad_order = Order(
		order_id=102,
		customer={"id": 2, "name": "Bob", "email": "bademail"},
		products=[{"id": 3, "name": "Keyboard", "price": -10.0}],
		total=-10.0
	)
except ValidationError as e:
	print("Validation error for bad_order:", e)
