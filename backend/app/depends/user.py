from fastapi import HTTPException, Depends, status

from app.services.jwt import get_current_user
from app.repository.models import User


async def get_current_admin_user(current_user: User = Depends(get_current_user)):

    if current_user.is_admin:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав!"
    )
