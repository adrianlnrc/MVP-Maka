from datetime import timedelta

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from app.schemas.user import UserPublic
from app.services import auth_service, email_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

REFRESH_COOKIE = "maka_refresh"
COOKIE_MAX_AGE = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600


def _set_refresh_cookie(response: Response, raw_token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=raw_token,
        httponly=True,
        samesite="strict",
        secure=False,  # Set True in production with HTTPS
        max_age=COOKIE_MAX_AGE,
        path="/api/auth",
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, data)
    access_token, raw_refresh = auth_service.create_tokens(db, user)
    _set_refresh_cookie(response, raw_refresh)
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )
    access_token, raw_refresh = auth_service.create_tokens(db, user)
    _set_refresh_cookie(response, raw_refresh)
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    response: Response,
    db: Session = Depends(get_db),
    maka_refresh: str | None = Cookie(default=None),
):
    if not maka_refresh:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não encontrado")

    result = auth_service.rotate_refresh_token(db, maka_refresh)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

    access_token, raw_refresh, _ = result
    _set_refresh_cookie(response, raw_refresh)
    return TokenResponse(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    db: Session = Depends(get_db),
    maka_refresh: str | None = Cookie(default=None),
):
    if maka_refresh:
        auth_service.revoke_refresh_token(db, maka_refresh)
    response.delete_cookie(key=REFRESH_COOKIE, path="/api/auth")


@router.post("/forgot-password", status_code=status.HTTP_204_NO_CONTENT)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    raw_token = auth_service.create_password_reset_token(db, data.email)
    if raw_token:
        email_service.send_password_reset_email(data.email, raw_token)
    # Always return 204 to avoid user enumeration


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    success = auth_service.reset_password(db, data.token, data.new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado",
        )


@router.get("/me", response_model=UserPublic)
def me(current_user: User = Depends(get_current_user)):
    return current_user
