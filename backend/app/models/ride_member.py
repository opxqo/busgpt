from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base

class RideMember(Base):
    __tablename__ = "ride_members"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    ride_id = Column(BigInteger, ForeignKey("rides.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False, default="passenger")  # owner, passenger
    joined_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    ride = relationship("Ride", back_populates="members")
    user = relationship("User", back_populates="memberships")

    __table_args__ = (
        UniqueConstraint("ride_id", "user_id", name="uk_ride_user"),
    )
