from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import get_db
from auth_utils import get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(prefix="/favorites", tags=["favorites"])

COOKIE_OPTS = dict(httponly=True, samesite="lax", secure=False)

def require_user(
    response: Response,
    db: Session = Depends(get_db),
    access_token: Optional[str] = Cookie(default=None),
    refresh_token: Optional[str] = Cookie(default=None),
):
    user, new_token = get_current_user(db, access_token, refresh_token)
    if new_token:
        response.set_cookie("access_token", new_token, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, **COOKIE_OPTS)
    return user

@router.get("/", response_model=List[schemas.FavoriteOut])
def get_favorites(user=Depends(require_user), db: Session = Depends(get_db)):
    return db.query(models.UserFavorite).filter(models.UserFavorite.user_id == user.id).all()

@router.post("/", response_model=schemas.FavoriteOut, status_code=201)
def add_favorite(body: schemas.FavoriteCreate, user=Depends(require_user), db: Session = Depends(get_db)):
    if not body.location_id and not body.scene_id:
        raise HTTPException(status_code=422, detail="Provide location_id or scene_id")
    if body.location_id and body.scene_id:
        raise HTTPException(status_code=422, detail="Provide only one of location_id or scene_id")

    q = db.query(models.UserFavorite).filter(models.UserFavorite.user_id == user.id)
    if body.location_id:
        q = q.filter(models.UserFavorite.location_id == body.location_id)
    else:
        q = q.filter(models.UserFavorite.scene_id == body.scene_id)
    if q.first():
        raise HTTPException(status_code=400, detail="Already in favorites")

    fav = models.UserFavorite(
        user_id=user.id,
        location_id=body.location_id,
        scene_id=body.scene_id,
    )
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav

@router.delete("/{fav_id}", status_code=204)
def remove_favorite(fav_id: int, user=Depends(require_user), db: Session = Depends(get_db)):
    fav = db.query(models.UserFavorite).filter(
        models.UserFavorite.id == fav_id,
        models.UserFavorite.user_id == user.id,
    ).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(fav)
    db.commit()