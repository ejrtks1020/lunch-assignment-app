from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from datetime import date
import random
from typing import List

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import restaurant as restaurant_repo, user as user_repo, assignment as assignment_repo
from schema.restaurant.restaurant_schema import CreateRestaurantRequest, RestaurantResponse
from schema.assignment.assignment_schema import AssignmentResponse
from model.restaurant.restaurant_model import Restaurant as RestaurantModel
from model.assignment.assignment_model import UserRestaurantAssignment
from db.session import transactional
class RestaurantService:
    @staticmethod
    @transactional
    async def register_restaurant(restaurant_data: CreateRestaurantRequest, session: AsyncSession | None = None):
        restaurant_exist = await RestaurantService.restaurant_name_exists(restaurant_data.name, session=session)

        if restaurant_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant with the given email already exists!!!",
            )

        new_restaurant = await restaurant_repo.RestaurantRepository(session).create(restaurant_data.model_dump())
        session.add(new_restaurant)
        logger.info(f"New restaurant created successfully: {new_restaurant}!!!")
        return JSONResponse(
            content={"message": "Restaurant created successfully"},
            status_code=status.HTTP_201_CREATED,
        )
    
    @staticmethod
    @transactional
    async def get_all_restaurants(session: AsyncSession | None = None) -> list[RestaurantResponse]:
        all_restaurants = await restaurant_repo.RestaurantRepository(session).get_all()
        return [RestaurantResponse.model_validate(_restaurant) for _restaurant in all_restaurants]

    @staticmethod
    @transactional
    async def get_active_restaurants(session: AsyncSession | None = None) -> list[RestaurantResponse]:
        active_restaurants = await restaurant_repo.RestaurantRepository(session).get_active_restaurants()
        return [RestaurantResponse.model_validate(_restaurant) for _restaurant in active_restaurants]

    @staticmethod
    @transactional
    async def restaurant_name_exists(name: str, session: AsyncSession | None = None) -> RestaurantModel | None:
        _restaurant = await restaurant_repo.RestaurantRepository(session).get_by_name(name)
        return _restaurant if _restaurant else None

    @staticmethod
    @transactional
    async def assign_users_to_restaurants(
        assignment_date: date | None = None,
        session: AsyncSession | None = None
    ) -> List[UserRestaurantAssignment]:
        if assignment_date is None:
            assignment_date = date.today()

        # 이미 해당 날짜에 배정이 있는지 확인
        existing_assignments = await RestaurantService.get_assignments_by_date(assignment_date, session=session)
        
        # 이미 해당 날짜에 배정이 있으면 삭제
        if existing_assignments:
            await assignment_repo.AssignmentRepository(session).delete_by_date(assignment_date)

        # 활성 사용자와 레스토랑 조회
        active_users = await user_repo.UserRepository(session).get_active_users()
        active_restaurants = await restaurant_repo.RestaurantRepository(session).get_active_restaurants()

        if not active_restaurants:
            raise ValueError("No active restaurants found")
        
        if not active_users:
            raise ValueError("No active users found")

        # 사용자를 무작위로 섞기
        random.shuffle(active_users)
        random.shuffle(active_restaurants)

        # 사용자를 최소 3명, 최대 4명을 가지는 그룹으로 나누기

        total_users = len(active_users)
        group_size = 4
        num_groups = (total_users + group_size - 1) // group_size

        # 각 그룹의 크기를 계산
        base_size = total_users // num_groups
        remainder = total_users % num_groups

        groups = []
        start = 0
        for i in range(num_groups):
            # remainder가 있으면 그룹 크기를 1 증가
            current_size = base_size + (1 if i < remainder else 0)
            groups.append(active_users[start:start + current_size])
            start += current_size

        print(groups)
        final_restaurants = active_restaurants[:len(groups)]

        assignments = []  
        for group, restaurant in zip(groups, final_restaurants):
            for user in group:
                assignment = UserRestaurantAssignment(
                    user_id=user.id,
                    restaurant_id=restaurant.id,
                    assignment_date=assignment_date
                )
                session.add(assignment)
                assignments.append(assignment)
        return [
            AssignmentResponse(
                user_id=assignment.user_id,
                restaurant_id=assignment.restaurant_id,
                assignment_date=assignment.assignment_date
            ) for assignment in assignments
        ]

    @staticmethod
    @transactional
    async def get_assignments_by_date(
        assignment_date: date, session: AsyncSession | None = None
    ) -> List[AssignmentResponse]:
        assignments = await assignment_repo.AssignmentRepository(session).get_by_date(assignment_date)
        return [
            AssignmentResponse.model_validate(_assignment) for _assignment in assignments
        ]