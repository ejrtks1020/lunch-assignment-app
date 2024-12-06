from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class UserBase(BaseModel):
    email: EmailStr
    name: str
    model_config = ConfigDict(from_attributes=True)

class UserOut(UserBase):
    id: int


class ChangePasswordIn(BaseModel):
    old_password: str
    new_password: str

    @field_validator("old_password")
    @classmethod
    def old_password_is_not_blank(cls, value):
        if not value:
            raise ValueError("Old password field can't be blank!!!")
        return value

    @field_validator("new_password")
    @classmethod
    def new_password_is_not_blank(cls, value):
        if not value:
            raise ValueError("New password field can't be blank!!!")
        return value
