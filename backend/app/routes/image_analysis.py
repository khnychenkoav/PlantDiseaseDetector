from fastapi import APIRouter

router = APIRouter()


@router.post("/analyze")
async def analyze_image():
    return {"disease": "Healthy"}
