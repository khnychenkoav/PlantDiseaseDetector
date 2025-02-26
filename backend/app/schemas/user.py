from pydantic import BaseModel, ConfigDict


class UserInLogin(BaseModel):
    email: str
    password: str


class UserInCreate(UserInLogin):
    name: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    name: str
