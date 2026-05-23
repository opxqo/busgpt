from sqlalchemy import Column, String, Numeric, Integer, Text
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    type = Column(String(30), primary_key=True, index=True)
    label = Column(String(20), nullable=False)
    official_price = Column(Numeric(10, 2), nullable=False)
    color = Column(String(10), nullable=False)
    max_seats = Column(Integer, nullable=False)
    description = Column(Text, default="")
