from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import user
from db.session import get_session
from model.user.user_model import User as UserModel
from schema.user.user_schema import Token, TokenData, ChangePasswordIn, UserBase, UserOut
from configs.settings import settings
from util.auth_util import AuthUtil, oauth2_scheme, http_scheme
from db.session import transactional
from icecream import ic


class UserService:
    @staticmethod
    @transactional
    async def register_user(user_data: UserBase, session: AsyncSession | None = None):
        user_exist = await UserService.user_email_exists(user_data.email, session=session)

        if user_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with the given email already exists!!!",
            )

        new_user = await user.UserRepository(session).create(user_data.model_dump())
        session.add(new_user)
        logger.info(f"New user created successfully: {new_user}!!!")
        return JSONResponse(
            content={"message": "User created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    @transactional
    async def authenticate_user(email: str, password: str, session: AsyncSession | None = None) -> UserModel | bool:
        _user = await user.UserRepository(session).get_by_email(email)
        if not _user or not AuthUtil.verify_password(password, _user.password):
            return False
        return _user

    @staticmethod
    @transactional
    async def user_email_exists(email: str, session: AsyncSession | None = None) -> UserModel | None:
        _user = await user.UserRepository(session).get_by_email(email)
        return _user if _user else None

    @staticmethod
    @transactional
    async def login(form_data: OAuth2PasswordRequestForm, session: AsyncSession | None = None) -> Token:
        _user = await UserService.authenticate_user(form_data.username, form_data.password, session)
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthUtil.create_access_token(data={"sub": _user.email}, expires_delta=access_token_expires)
        token_data = {
            "access_token": access_token,
            "token_type": "Bearer",
        }
        ic("login output ")
        return Token(**token_data)

    @staticmethod
    @transactional
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession | None = None,
    ) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if not email:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        _user = await user.UserRepository(session).get_by_email(email=token_data.email)
        if not _user:
            raise credentials_exception
        return _user

    @staticmethod
    @transactional
    async def get_all_users(session: AsyncSession | None = None) -> list[UserOut]:
        all_users = await user.UserRepository(session).get_all()
        return [UserOut.model_validate(_user) for _user in all_users]

    @staticmethod
    @transactional
    async def delete_all_users(session: AsyncSession | None = None):
        await user.UserRepository(session).delete_all()
        return JSONResponse(
            content={"message": "All users deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    @transactional
    async def change_password(
        password_data: ChangePasswordIn,
        current_user: UserModel,
        session: AsyncSession | None = None,
    ):
        if not AuthUtil.verify_password(password_data.old_password, current_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect old password!!!",
            )
        current_user.password = AuthUtil.get_password_hash(password_data.new_password)
        session.add(current_user)
        await session.commit()
        return JSONResponse(
            content={"message": "Password updated successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    @transactional
    async def get_user_by_id(user_id: int, session: AsyncSession | None = None) -> UserOut:
        _user = await user.UserRepository(session).get_by_id(user_id)
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the given id does not exist!!!",
            )
        return UserOut.model_validate(_user)

    @staticmethod
    @transactional
    async def delete_user_by_id(user_id: int, session: AsyncSession | None = None):
        _user = await user.UserRepository(session).delete_by_id(user_id)
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the given id does not exist!!!",
            )
        return JSONResponse(
            content={"message": "User deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )
