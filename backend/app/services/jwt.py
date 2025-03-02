from jose import jwt, JWTError
from datetime import datetime, timezone
from fastapi import HTTPException, status, Depends, Request
from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.config import get_auth_data
from app.dao.user import UserDAO


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(
        to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"]
    )
    return encode_jwt


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный!"
        )

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя"
        )

    user = await UserDAO.find_one_or_none(id=UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден"
        )

    return user
