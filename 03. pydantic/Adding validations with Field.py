
from pydantic import BaseModel, Field, ValidationError, EmailStr

# Real-life example: User registration with validation
class User(BaseModel):
	id: int = Field(..., gt=0, description="User ID must be positive")
	name: str = Field(..., min_length=2, max_length=50)
	age: int = Field(..., ge=18, le=99, description="Age must be between 18 and 99")
	email: EmailStr
	password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

try:
	user = User(
		id=1,
		name="Alice",
		age=30,
		email="alice@example.com",
		password="supersecret123"
	)
	print(user)
except ValidationError as e:
	print("Validation error:", e)

# Example of validation error
try:
	bad_user = User(id=-5, name="A", age=15, email="bademail", password="123")
except ValidationError as e:
	print("Validation error for bad_user:", e)
