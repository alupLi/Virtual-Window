from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("/", response_model=List[schemas.LocationOut])
def get_locations(db: Session = Depends(get_db)):
    return db.query(models.Location).all()

@router.get("/{location_id}", response_model=schemas.LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    return loc