import os
import shutil

from fastapi import APIRouter, UploadFile, File


from app.services.security import get_hashed_path


router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload/", summary="Загрузить фотографию растения")
async def upload_file(file: UploadFile = File(...)):

    subfolder = get_hashed_path(file.filename)
    save_dir = os.path.join(UPLOAD_DIR, subfolder)
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "path": file_path}
