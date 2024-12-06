from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from icecream import ic
from service.restaurant.restaurant_service import RestaurantService
from schema.restaurant.restaurant_schema import CreateRestaurantRequest
from schema.assignment.assignment_schema import AssignmentResponse
from datetime import date

router = APIRouter(tags=["Restaurant"], prefix="/restaurant")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_restaurant(
    restaurant_data: CreateRestaurantRequest,
):
    return await RestaurantService.register_restaurant(restaurant_data)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_active_restaurants(
):
    return await RestaurantService.get_active_restaurants()

@router.post("/assign")
async def assign_users(
    assignment_date: date = None
) -> List[AssignmentResponse]:
    try:
        response = await RestaurantService.assign_users_to_restaurants(assignment_date)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/assignments/{date}")
async def get_assignments(date: date) -> List[AssignmentResponse]:
    response = await RestaurantService.get_assignments_by_date(date)
    return response
