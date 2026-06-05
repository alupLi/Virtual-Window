from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(prefix="/music", tags=["music"])

@router.get("/", response_model=List[schemas.MusicTrackOut])
def get_tracks(db: Session = Depends(get_db)):
    return db.query(models.MusicTrack).all()