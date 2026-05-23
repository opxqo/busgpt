from datetime import datetime

from sqlalchemy import Column, BigInteger, Integer, String, Numeric, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        UniqueConstraint('user_id', 'ride_id', name='uq_user_ride'),
    )

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    ride_id = Column(BigInteger, ForeignKey("rides.id"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="pending", index=True)  # pending, paid, cancelled, expired, refunded
    payment_provider = Column(String(30), nullable=False, default="mock")
    payment_no = Column(String(64), nullable=True, unique=True, index=True)
    payment_status = Column(String(20), nullable=False, default="pending", index=True)
    paid_at = Column(DateTime, nullable=True)
    contact_unlocked_at = Column(DateTime, nullable=True, index=True)
    expired_at = Column(DateTime, nullable=True, index=True)
    idempotency_key = Column(String(64), nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")
    ride = relationship("Ride", back_populates="orders")
