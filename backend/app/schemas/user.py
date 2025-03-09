from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserInLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=7,
        max_length=20,
        description="Пароль должен содержать 7-20 символов",
    )


class UserInCreate(UserInLogin):
    name: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Имя должно содержать 3-20 символов",
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    name: str


class UserChangeRole(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    is_user: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    is_super_admin: bool = Field(default=False)
