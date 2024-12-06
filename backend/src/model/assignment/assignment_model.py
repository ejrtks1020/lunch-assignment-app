from sqlalchemy import Column, Integer, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from model.base_model import Base

class UserRestaurantAssignment(Base):
    __tablename__ = "user_restaurant_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    assignment_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="assignments")
    restaurant = relationship("Restaurant", back_populates="assignments") 