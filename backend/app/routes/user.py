from fastapi import APIRouter

from app.dao.user import UserDAO
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/all/")
async def get_all_users() -> list[UserResponse]:
    return await UserDAO.find_all()
