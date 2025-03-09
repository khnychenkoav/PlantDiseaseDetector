from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routes.api import router as api_router

from app.routes import disease, history, user, authentication
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(disease.router, tags=["Болезни"], prefix="/diseases")
app.include_router(history.router, tags=["История запросов"], prefix="/history")
app.include_router(user.router, tags=["Пользователи"], prefix="/users")
app.include_router(authentication.router, tags=["Авторизация"], prefix="/users")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():

    return HTMLResponse(content="Plant Disease Detector API")
