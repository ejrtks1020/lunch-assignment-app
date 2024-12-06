
from fastapi import APIRouter

from router.user.user_router import router as user_router
from router.restaurant.restaurant_router import router as restaurant_router
from router.assignment.assignment_router import router as assignment_router
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_router)
api_router.include_router(restaurant_router)
api_router.include_router(assignment_router)
