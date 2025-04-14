import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends

from ml_model.predict import predict, model_resnet
from app.services.security import get_hashed_path
from app.services.jwt import get_current_user
from app.repository.models import User
from app.dao.disease import DiseaseDAO
from app.dao.history import HistoryDAO
from app.schemas.disease import DiseasesInCreate
from app.depends.user import get_current_admin_user


router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload/", summary="Загрузить фотографию растения")
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

    disease_name = predict(file_path, model_resnet)
    diseases = await DiseaseDAO.find_one_or_none(name=disease_name["ru"])
    await HistoryDAO.create_record(user.id, diseases.id, file_path)

    return {
        "filename": file.filename,
        "path": file_path,
        "name_disease": disease_name["ru"],
    }


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
