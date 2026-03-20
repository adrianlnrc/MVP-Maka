from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine
from app.models import *  # noqa: F401, F403 — registers all models with Base
from app.routers.auth import router as auth_router
from app.routers.content import (
    characters_router,
    eras_router,
    search_router,
    stories_router,
    timeline_router,
)
from app.routers.reading_plan import router as reading_plan_router
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Maka API",
    description="API da plataforma Maka — Bíblia Cronológica",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(eras_router)
app.include_router(stories_router)
app.include_router(characters_router)
app.include_router(timeline_router)
app.include_router(search_router)
app.include_router(reading_plan_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "maka-api"}
