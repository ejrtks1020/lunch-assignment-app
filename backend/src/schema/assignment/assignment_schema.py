from pydantic import BaseModel
from datetime import date

class AssignmentResponse(BaseModel):
    user_id: int
    restaurant_id: int
    assignment_date: date

    class Config:
        from_attributes = True

class AssignmentGroupResponse(BaseModel):
    restaurant_id: int
    restaurant_name: str
    users: list[str]
    assignment_date: date

    class Config:
        from_attributes = True
