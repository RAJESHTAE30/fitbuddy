from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .database import init_db
from .routes import router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="AI-powered personalized workout and nutrition planning.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()
