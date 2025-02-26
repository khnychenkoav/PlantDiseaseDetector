from fastapi import APIRouter

from app.routes import disease, history, user, authentication

router = APIRouter()
router.include_router(disease.router, tags=["Болезни"], prefix="/diseases")
router.include_router(history.router, tags=["История запросов"], prefix="/history")
router.include_router(user.router, tags=["Пользователи"], prefix="/users")
router.include_router(authentication.router, tags=["Авторизация"], prefix="/users")
