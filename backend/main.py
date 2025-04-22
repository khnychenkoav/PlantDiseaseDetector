from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.api import router as api_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(api_router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")



@app.get("/")
def read_root():

    return HTMLResponse(content="Plant Disease Detector API")
