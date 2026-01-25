
from pydantic import BaseModel, Field, ValidationError, EmailStr

# Real-life example: User with nested Address model
class Address(BaseModel):
	street: str
	city: str
	zip_code: str = Field(..., min_length=5, max_length=10)

class User(BaseModel):
	id: int
	name: str
	email: EmailStr
	address: Address

try:
	user = User(
		id=1,
		name="Arif Khan",
		email="arif@example.com",
		address={
			"street": "456 Elm St",
			"city": "Dhaka",
			"zip_code": "1207"
		}
	)
	print(user)
	print("Serialized JSON:", user.json())
except ValidationError as e:
	print("Validation error:", e)

# Example of validation error
try:
	bad_user = User(
		id=2,
		name="Bob",
		email="bademail",
		address={
			"street": "No St",
			"city": "Nowhere",
			"zip_code": "12"
		}
	)
except ValidationError as e:
	print("Validation error for bad_user:", e)
