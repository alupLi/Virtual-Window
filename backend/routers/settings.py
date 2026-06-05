from fastapi import APIRouter, Depends, Response, Cookie
from sqlalchemy.orm import Session
from typing import Optional

import models
import schemas
from database import get_db
from auth_utils import get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/settings", tags=["settings"])

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

@router.get("/", response_model=schemas.SettingsOut)
def get_settings(user=Depends(require_user), db: Session = Depends(get_db)):
    s = db.query(models.UserSettings).filter(models.UserSettings.user_id == user.id).first()
    if not s:
        s = models.UserSettings(user_id=user.id)
        db.add(s)
        db.commit()
        db.refresh(s)
    return s

@router.put("/", response_model=schemas.SettingsOut)
def update_settings(body: schemas.SettingsUpdate, user=Depends(require_user), db: Session = Depends(get_db)):
    s = db.query(models.UserSettings).filter(models.UserSettings.user_id == user.id).first()
    if not s:
        s = models.UserSettings(user_id=user.id)
        db.add(s)

    for field, val in body.model_dump(exclude_none=True).items():
        setattr(s, field, val)

    db.commit()
    db.refresh(s)
    return s