from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from service.assignment.assignment_service import AssignmentService
from schema.assignment.assignment_schema import AssignmentResponse, AssignmentGroupResponse

router = APIRouter(tags=["Assignment"], prefix="/assignment")

@router.get("/{date}", response_model=List[AssignmentResponse])
async def get_assignments(
    date: date,
    session: AsyncSession = Depends(get_session)
) -> List[AssignmentResponse]:
    return await AssignmentService.get_assignments_by_date(session, date)

@router.get("/group/{date}", response_model=List[AssignmentGroupResponse])
async def get_grouped_assignments(
    date: date,
    session: AsyncSession = Depends(get_session)
) -> List[AssignmentGroupResponse]:
    return await AssignmentService.get_grouped_assignments(session, date) 