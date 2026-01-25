
from pydantic import BaseModel, Field, computed_field

# Real-life example: Product with computed price after tax
class Product(BaseModel):
	name: str
	price: float = Field(..., gt=0)
	tax_rate: float = Field(default=0.1, ge=0, le=1)

	@computed_field
	@property
	def price_with_tax(self) -> float:
		return round(self.price * (1 + self.tax_rate), 2)

product = Product(name="Laptop", price=1000.0, tax_rate=0.18)
print(product)
print(f"Price with tax: {product.price_with_tax}")

# Example with default tax rate
product2 = Product(name="Book", price=50.0)
print(product2)
print(f"Price with tax: {product2.price_with_tax}")
