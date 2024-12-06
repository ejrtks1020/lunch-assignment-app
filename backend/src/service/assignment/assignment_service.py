from datetime import date
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import assignment as assignment_repo
from schema.assignment.assignment_schema import AssignmentResponse, AssignmentGroupResponse

class AssignmentService:
    @staticmethod
    async def get_assignments_by_date(session: AsyncSession, assignment_date: date) -> List[AssignmentResponse]:
        assignments = await assignment_repo.AssignmentRepository(session).get_by_date(assignment_date)
        if not assignments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No assignments found for date: {assignment_date}"
            )
        return [AssignmentResponse.model_validate(assignment) for assignment in assignments]

    @staticmethod
    async def get_grouped_assignments(session: AsyncSession, assignment_date: date) -> List[AssignmentGroupResponse]:
        assignments = await assignment_repo.AssignmentRepository(session).get_grouped_assignments(assignment_date)
        if not assignments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No assignments found for date: {assignment_date}"
            )
        return [AssignmentGroupResponse.model_validate(assignment) for assignment in assignments] 