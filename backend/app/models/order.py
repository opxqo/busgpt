from sqlalchemy import Column, BigInteger, String, Numeric, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        UniqueConstraint('user_id', 'ride_id', name='uq_user_ride'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    ride_id = Column(BigInteger, ForeignKey("rides.id"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="paid")  # paid, refunded
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")
    ride = relationship("Ride", back_populates="orders")
