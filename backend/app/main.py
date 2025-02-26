from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routes.api import router as api_router

app = FastAPI()


@app.get("/")
def read_root():

    return HTMLResponse(content="Plant Disease Detector API")


app.include_router(api_router)
