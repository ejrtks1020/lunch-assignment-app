from model.restaurant.restaurant_model import Restaurant
from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

class RestaurantRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, restaurant_data) -> Restaurant:
        _restaurant = Restaurant(**restaurant_data)
        return _restaurant

    async def get_by_name(self, name: str) -> Restaurant | None:
        statement = select(Restaurant).where(Restaurant.name == name)
        return await self.session.scalar(statement=statement)
    
    async def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        statement = select(Restaurant).where(Restaurant.id == restaurant_id)
        return await self.session.scalar(statement=statement)

    async def get_all(self) -> list[Restaurant]:
        statement = select(Restaurant).order_by(Restaurant.id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def get_active_restaurants(self) -> list[Restaurant]:
        statement = select(Restaurant).where(Restaurant.is_active == True)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Restaurant))
