from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db import init_db
from routers import favorites, profiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Woofr API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Served under /api so the Vite dev proxy forwards image requests too.
app.mount(
    "/api/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)

app.include_router(profiles.router)
app.include_router(favorites.router)
