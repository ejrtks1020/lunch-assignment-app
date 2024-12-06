from service.user.user_service import UserService
from service.restaurant.restaurant_service import RestaurantService
from schema.user.user_schema import UserBase
from schema.restaurant.restaurant_schema import CreateRestaurantRequest
from db.session import AsyncSessionFactory

async def add_dummy_data():
    for i in range(10):
        await UserService.register_user(UserBase(email=f"test{i}@test.com", name=f"test{i}"))
        await RestaurantService.register_restaurant(CreateRestaurantRequest(name=f"restaurant{i}", active=True))
