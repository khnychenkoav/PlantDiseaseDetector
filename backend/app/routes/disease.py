import os
import shutil
import json

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.services.security import get_hashed_path
from app.services.jwt import get_current_user
from app.repository.models import User
from app.dao.disease import DiseaseDAO
from app.dao.history import HistoryDAO
from app.schemas.disease import DiseasesInCreate, DiseasesInResponse
from app.depends.user import get_current_admin_user
from app.services.model_service import model_service


router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post(
    "/upload/",
    summary="Загрузить фотографию растения",
    response_model=DiseasesInResponse,
)
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    subfolder = get_hashed_path(file.filename)
    save_dir = os.path.join(UPLOAD_DIR, subfolder)
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    disease_name = model_service.predict(file_path)
    diseases = await DiseaseDAO.find_one_or_none(name=disease_name["ru"])
    if diseases is None:
        diseases = await DiseaseDAO.find_one_or_none(name="НеизвестнаяБолезнь")
    await HistoryDAO.create_record(user.id, diseases.id, file_path)

    return DiseasesInResponse(
        diseases_name=diseases.name,
        reason=diseases.reason,
        recommendation=diseases.recommendations,
        time=diseases.created_at,
        image_url=file_path,
    )


@router.post("/create/", summary="Создать запись растения")
async def create(
    disease: DiseasesInCreate,
    admin: User = Depends(get_current_admin_user),
):
    await DiseaseDAO.create_record(
        disease.name,
        disease.reason,
        disease.recommendation,
    )


@router.post("/create/init", summary="Инициализировать базу болезнями растений")
async def init_diseases(admin: User = Depends(get_current_admin_user)):
    try:
        with open("ml_model/class_disease.json", "r", encoding="utf-8") as f:
            diseases = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения файла: {e}")

    created = 0
    duplicates = 0

    for disease in diseases:
        name = disease["ru"]
        reason = disease.get("cause", "")
        recommendation = disease.get("treatment", "")
        existing = await DiseaseDAO.find_one_or_none(name=disease["ru"])
        if existing:
            duplicates += 1
            continue

        try:
            await DiseaseDAO.create_record(name, reason, recommendation)
            created += 1
        except Exception:
            continue

    return {
        "status": "ok",
        "created": created,
        "duplicates": duplicates,
        "total_processed": len(diseases),
    }
