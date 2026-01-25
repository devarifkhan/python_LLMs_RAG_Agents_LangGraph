
from pydantic import BaseModel, Field, EmailStr, ValidationError
from pydantic import field_validator, model_validator

# Real-life example: User registration with custom validators
class User(BaseModel):
	name: str = Field(..., min_length=2, max_length=50)
	age: int = Field(..., ge=18, le=99)
	email: EmailStr
	password: str = Field(..., min_length=8)
	confirm_password: str

	@field_validator('name')
	def name_must_be_alpha(cls, v):
		if not v.isalpha():
			raise ValueError('Name must contain only alphabetic characters')
		return v

	@model_validator(mode="after")
	def passwords_match(self):
		if self.password != self.confirm_password:
			raise ValueError('Passwords do not match')
		return self

try:
	user = User(
		name="Alice",
		age=30,
		email="alice@example.com",
		password="supersecret123",
		confirm_password="supersecret123"
	)
	print(user)
except ValidationError as e:
	print("Validation error:", e)

# Example of validation error
try:
	bad_user = User(
		name="Bob123",
		age=17,
		email="bademail",
		password="short",
		confirm_password="notmatching"
	)
except ValidationError as e:
	print("Validation error for bad_user:", e)
