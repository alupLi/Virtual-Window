from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import get_db

router = APIRouter(prefix="/sounds", tags=["sounds"])

@router.get("/", response_model=List[schemas.SoundOut])
def get_sounds(
    location_id: Optional[int] = Query(default=None),
    scene_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Sound)
    if location_id is not None:
        q = q.filter(models.Sound.location_id == location_id)
    elif scene_id is not None:
        q = q.filter(models.Sound.scene_id == scene_id)
    return q.all()