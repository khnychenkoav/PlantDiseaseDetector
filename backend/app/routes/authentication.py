from fastapi import APIRouter, Depends


from app.schemas.user import UserInCreate, UserInLogin, UserResponse
from app.dao.user import UserDAO

router = APIRouter()


@router.post("/login/", summary="Авторизироваться")
async def login(user: UserInLogin):
    pass


@router.post("/register/", summary="Зарегистрироваться")
async def register(user: UserInCreate = Depends()) -> UserResponse:
    await UserDAO.create_user(user.name, user.email, user.password)
    return UserResponse(email=user.email, name=user.name)
