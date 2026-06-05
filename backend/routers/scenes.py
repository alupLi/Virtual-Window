from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(prefix="/scenes", tags=["scenes"])

@router.get("/", response_model=List[schemas.SceneOut])
def get_scenes(db: Session = Depends(get_db)):
    return db.query(models.Scene).all()

@router.get("/{scene_id}", response_model=schemas.SceneOut)
def get_scene(scene_id: int, db: Session = Depends(get_db)):
    scene = db.query(models.Scene).filter(models.Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    return scene
