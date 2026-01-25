
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, ForwardRef

# Real-life example: Organization chart with self-referencing Employee model
EmployeeRef = ForwardRef('Employee')

class Employee(BaseModel):
	name: str
	position: str
	subordinates: Optional[List[EmployeeRef]] = None

Employee.model_rebuild()

try:
	ceo = Employee(
		name="Arif Khan",
		position="CEO",
		subordinates=[
			Employee(
				name="Alice",
				position="CTO",
				subordinates=[
					Employee(name="Bob", position="Dev")
				]
			),
			Employee(
				name="Charlie",
				position="CFO"
			)
		]
	)
	print(ceo)
	print("Serialized JSON:", ceo.json())
except ValidationError as e:
	print("Validation error:", e)
