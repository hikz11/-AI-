from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.utils.emotion_service import emotion_service

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{file.filename}"

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = emotion_service.predict(file_path)

    return {
        "code": 0,
        "data": result
    }