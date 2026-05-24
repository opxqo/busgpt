from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import backref, relationship
from app.database import Base

class RideMember(Base):
    __tablename__ = "ride_members"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    ride_id = Column(BigInteger, ForeignKey("rides.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False, default="passenger")  # owner, passenger
    joined_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    ride = relationship("Ride", backref=backref("members", cascade="all, delete-orphan"))
    user = relationship("User", backref=backref("memberships", cascade="all, delete-orphan"))

    __table_args__ = (
        UniqueConstraint("ride_id", "user_id", name="uk_ride_user"),
    )
