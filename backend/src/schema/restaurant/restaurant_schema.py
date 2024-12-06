from pydantic import BaseModel
from datetime import date

class CreateRestaurantRequest(BaseModel):
    name: str

class RestaurantResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
