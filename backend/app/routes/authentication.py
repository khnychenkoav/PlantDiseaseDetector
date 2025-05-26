from fastapi import APIRouter, Depends, HTTPException, status, Response


from app.schemas.user import UserInCreate, UserInLogin, UserResponse
from app.repository.models import User
from app.dao.user import UserDAO
from app.services.security import verify_password
from app.services.jwt import create_access_token

router = APIRouter()


@router.post("/login/", summary="Авторизироваться")
async def login(response: Response, user_data: UserInLogin):
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if not user or verify_password(user_data.password, user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверная почта или пароль",
        )

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        httponly=True,
        secure=False,
    )
    return {"access_token": access_token, "refresh_token": None}


@router.post("/register/", summary="Зарегистрироваться", response_model=UserResponse)
async def register(user_data: UserInCreate) -> UserResponse:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует",
        )
    await UserDAO.create_user(
        user_data.name,
        user_data.email,
        user_data.password,
    )
    return UserResponse(email=user_data.email, name=user_data.name)
