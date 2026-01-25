
from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator, model_validator

# Real-life example: Advanced registration form validation
class RegistrationForm(BaseModel):
	username: str = Field(..., min_length=3, max_length=20)
	email: EmailStr
	password: str = Field(..., min_length=8)
	confirm_password: str
	age: int = Field(..., ge=18, le=99)

	@field_validator('username')
	def username_no_spaces(cls, v):
		if ' ' in v:
			raise ValueError('Username must not contain spaces')
		return v

	@model_validator(mode="after")
	def passwords_match(self):
		if self.password != self.confirm_password:
			raise ValueError('Passwords do not match')
		return self

try:
	form = RegistrationForm(
		username="arifkhan",
		email="arif@example.com",
		password="strongpassword",
		confirm_password="strongpassword",
		age=25
	)
	print(form)
except ValidationError as e:
	print("Validation error:", e)

# Example of validation error
try:
	bad_form = RegistrationForm(
		username="bad user",
		email="bademail",
		password="short",
		confirm_password="notmatching",
		age=15
	)
except ValidationError as e:
	print("Validation error for bad_form:", e)
