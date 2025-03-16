from fastapi import APIRouter, Response, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound

from app.dao.user import UserDAO
from app.schemas.user import UserResponse, UserChangeRole
from app.repository.models import User
from app.services.jwt import get_current_user
from app.depends.user import get_current_admin_user

router = APIRouter()


@router.get("/all/", summary="Получить всех пользователей")
async def get_all_users(
    admin: User = Depends(get_current_admin_user),
) -> list[UserResponse]:
    return await UserDAO.find_all()


@router.post("/logout/", summary="Выйти")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}


@router.get("/me/", summary="Получить данные")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.put("/change_role/", summary="Изменить роль пользователя")
async def change_role(
    admin: User = Depends(get_current_admin_user),
    user_data: UserChangeRole = Depends(),
):
    user_dict = user_data.model_dump()
    try:
        await UserDAO.update_user(user_dict)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь не найден",
        )

    return {"message": "Роль изменена"}
