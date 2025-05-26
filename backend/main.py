import asyncio

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.routes.api import router as api_router
from app.services.model_service import model_service
from app.services.clean_up import periodic_cleanup


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_service.load_model()
    asyncio.create_task(periodic_cleanup())
    yield
    pass


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://plantdetector.ru",
        "http://www.plantdetector.ru",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def read_root():
    return HTMLResponse(content="Plant Disease Detector API")
