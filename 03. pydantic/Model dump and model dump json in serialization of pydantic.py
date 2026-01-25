
from pydantic import BaseModel, Field

# Real-life example: User model serialization
class User(BaseModel):
	id: int
	name: str
	email: str
	is_active: bool = True

user = User(id=1, name="Arif Khan", email="arif@example.com")
print("Model as dict:", user.model_dump())
print("Model as JSON:", user.model_dump_json())

# Example with nested model
class Address(BaseModel):
	street: str
	city: str
	zip_code: str

class Customer(BaseModel):
	id: int
	name: str
	address: Address

customer = Customer(
	id=2,
	name="Alice",
	address={"street": "123 Main St", "city": "Dhaka", "zip_code": "1207"}
)
print("Customer as dict:", customer.model_dump())
print("Customer as JSON:", customer.model_dump_json())
