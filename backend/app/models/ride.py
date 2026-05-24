from datetime import datetime

from sqlalchemy import Column, BigInteger, String, Numeric, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Ride(Base):
    __tablename__ = "rides"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    title = Column(String(100), nullable=False)
    product = Column(String(30), ForeignKey("products.type"), nullable=False, index=True)
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    total_seats = Column(Integer, nullable=False)
    recruit_seats = Column(Integer, nullable=False, default=1)
    price_per_month = Column(Numeric(10, 2), nullable=False)
    duration = Column(Integer, nullable=False)  # in months
    warranty_days = Column(Integer, nullable=False, default=30)
    description = Column(Text, default="")  # Public description
    contact_info = Column(Text, default="")  # Owner's contact info (WeChat, etc.) - only visible after purchase
    contact_website = Column(String(255), default="")
    contact_price = Column(Numeric(10, 2), nullable=False, default=0)  # Price to view contact info (CNY)
    status = Column(String(20), nullable=False, default="open", index=True)  # open, closed, expired
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="rides_owned")
    product_details = relationship("Product")
    orders = relationship("Order", back_populates="ride", cascade="all, delete-orphan")
