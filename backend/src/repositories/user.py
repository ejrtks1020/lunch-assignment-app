from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base import BaseRepository
from model.user.user_model import User


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, user_data) -> User:
        _user = User(**user_data)
        return _user

    async def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return await self.session.scalar(statement=statement)

    async def get_by_email(self, email) -> User | None:
        statement = select(User).where(User.email == email)
        return await self.session.scalar(statement=statement)

    async def get_all(self) -> list[User]:
        statement = select(User).order_by(User.id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
    
    async def get_active_users(self) -> list[User]:
        statement = select(User).where(User.is_active == True)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(User))
        await self.session.commit()

    async def delete_by_id(self, user_id: int) -> User | None:
        _user = await self.get_by_id(user_id=user_id)
        statement = delete(User).where(User.id == user_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _user
