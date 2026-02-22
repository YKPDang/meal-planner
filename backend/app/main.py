from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app import config
from backend.app.db import init_db
from backend.app.routers import health, meal_plan, recipes, tags


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Meal Planner API",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    api = APIRouter(prefix="/api")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api.include_router(health.router)
    api.include_router(recipes.router)
    api.include_router(tags.router)
    api.include_router(meal_plan.router)
    app.include_router(api)
    return app


app = create_app()
