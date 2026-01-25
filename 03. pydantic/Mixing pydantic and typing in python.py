
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ValidationError

# Real-life example: User registration data
class Address(BaseModel):
	street: str
	city: str
	zip_code: str

class User(BaseModel):
	id: int
	name: str
	email: EmailStr
	is_active: bool = True
	tags: Optional[List[str]] = None
	address: Optional[Address] = None

try:
	user = User(
		id=1,
		name="Alice",
		email="alice@example.com",
		tags=["admin", "premium"],
		address={
			"street": "123 Main St",
			"city": "Wonderland",
			"zip_code": "12345"
		}
	)
	print(user)
	print("Serialized JSON:", user.json())
except ValidationError as e:
	print("Validation error:", e)

# Example of validation error
try:
	bad_user = User(id=2, name="Bob", email="not-an-email")
except ValidationError as e:
	print("Validation error for bad_user:", e)
