from fastapi import APIRouter, Depends


from app.dao.history import HistoryDAO
from app.services.jwt import get_current_user
from app.repository.models import User
from app.schemas.disease import DiseasesInResponse


router = APIRouter()


@router.get(
    "/all/",
    summary="Получить историю запросов пользователя",
    response_model=list[DiseasesInResponse],
)
async def get_history(user: User = Depends(get_current_user)):
    history = await HistoryDAO.get_history(user_id=user.id)
    response_data = []
    for record in history:
        response_data.append(
            DiseasesInResponse(
                diseases_name=record.disease.name,
                time=record.created_at,
                reason=record.disease.reason,
                recommendation=record.disease.recommendations,
                image_url=record.image_path,
            )
        )
    return response_data
