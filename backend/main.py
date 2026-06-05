from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from database import engine, Base
import models

from routers import auth, locations, scenes, sounds, music, weather, favorites, settings

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Virtual Window API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Routers
app.include_router(auth.router)
app.include_router(locations.router)
app.include_router(scenes.router)
app.include_router(sounds.router)
app.include_router(music.router)
app.include_router(weather.router)
app.include_router(favorites.router)
app.include_router(settings.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Virtual Window API"}
