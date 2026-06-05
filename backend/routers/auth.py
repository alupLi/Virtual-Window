from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, status
from sqlalchemy.orm import Session
from typing import Optional

import models
import schemas
from database import get_db
from auth_utils import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    get_current_user, decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS,
)

router = APIRouter(prefix="/auth", tags=["auth"])

COOKIE_OPTS = dict(httponly=True, samesite="lax", secure=False)

@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(body: schemas.UserRegister, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        username=body.username,
        email=body.email,
        password_hash=hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    db.add(models.UserSettings(user_id=user.id))
    db.commit()

    return user

@router.post("/login", response_model=schemas.UserOut)
def login(body: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    response.set_cookie("access_token", access_token, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, **COOKIE_OPTS)
    response.set_cookie("refresh_token", refresh_token, max_age=REFRESH_TOKEN_EXPIRE_DAYS * 86400, **COOKIE_OPTS)

    return user

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}

@router.get("/me", response_model=schemas.UserOut)
def me(
    response: Response,
    db: Session = Depends(get_db),
    access_token: Optional[str] = Cookie(default=None),
    refresh_token: Optional[str] = Cookie(default=None),
):
    user, new_token = get_current_user(db, access_token, refresh_token)
    if new_token:
        response.set_cookie("access_token", new_token, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, **COOKIE_OPTS)
    return user

@router.post("/refresh")
def refresh(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: Optional[str] = Cookie(default=None),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    user_id = decode_token(refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_access_token(user_id)
    response.set_cookie("access_token", new_access, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, **COOKIE_OPTS)
    return {"detail": "Token refreshed"}