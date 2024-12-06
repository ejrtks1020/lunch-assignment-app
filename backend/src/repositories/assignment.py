from sqlalchemy import select, delete
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from model.assignment.assignment_model import UserRestaurantAssignment
from repositories.base import BaseRepository
from datetime import date

class AssignmentRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_date(self, assignment_date: date) -> List[UserRestaurantAssignment]:
        statement = select(UserRestaurantAssignment).where(UserRestaurantAssignment.assignment_date == assignment_date)
        return (await self.session.scalars(statement=statement)).all()

    async def create(self, assignment_data: dict):
        assignment = UserRestaurantAssignment(**assignment_data)
        self.session.add(assignment)
        await self.session.refresh(assignment)
        return assignment
    
    async def delete_all(self):
        await self.session.query(UserRestaurantAssignment).delete()
    
    async def get_all(self) -> List[UserRestaurantAssignment]:
        statement = select(UserRestaurantAssignment)
        return (await self.session.scalars(statement=statement)).all()
    
    async def get_by_id(self, assignment_id: int) -> UserRestaurantAssignment:
        statement = select(UserRestaurantAssignment).where(UserRestaurantAssignment.id == assignment_id)
        return await self.session.scalar(statement=statement)

    async def get_grouped_assignments(self, assignment_date: date):
        query = """
            SELECT 
                r.id as restaurant_id,
                r.name as restaurant_name,
                array_agg(u.name) as users,
                a.assignment_date
            FROM user_restaurant_assignments a
            JOIN restaurants r ON r.id = a.restaurant_id
            JOIN users u ON u.id = a.user_id
            WHERE a.assignment_date = :date
            GROUP BY r.id, r.name, a.assignment_date
        """
        result = await self.session.execute(query, {"date": assignment_date})
        return result.mappings().all()
    
    async def delete_by_date(self, assignment_date: date):
        delete_statement = delete(UserRestaurantAssignment).where(UserRestaurantAssignment.assignment_date == assignment_date)
        await self.session.execute(delete_statement)
