from pydantic import BaseModel, Field
from decimal import Decimal

class ProductUpdate(BaseModel):
    label: str = Field(..., min_length=1, max_length=20)
    official_price: Decimal = Field(..., ge=0)
    color: str = Field(..., min_length=4, max_length=10)
    max_seats: int = Field(..., gt=1, le=50)
    description: str = ""

class ProductResponse(BaseModel):
    type: str
    label: str
    official_price: Decimal
    color: str
    max_seats: int
    description: str

    class Config:
        from_attributes = True
