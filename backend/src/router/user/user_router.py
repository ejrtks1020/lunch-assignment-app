from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from icecream import ic
from db.session import get_session
from schema.user.user_schema import Token, ChangePasswordIn, UserBase, UserOut
from service.user.user_service import UserService

router = APIRouter(tags=["User"], prefix="/user")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserBase,
):
    return await UserService.register_user(user_data)


@router.post("/token", status_code=status.HTTP_200_OK)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    ic("token - form_data ", form_data)
    return await UserService.login(form_data)


@router.get("/get_by_id/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int,
) -> UserOut:
    return await UserService.get_user_by_id(user_id)


@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all_users() -> list[UserOut]:
    return await UserService.get_all_users()


@router.delete("/delete_by_id/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_by_id(
    user_id: int
):
    return await UserService.delete_user_by_id(user_id)


@router.delete("/delete_all", status_code=status.HTTP_200_OK)
async def delete_all_users():
    return await UserService.delete_all_users()
