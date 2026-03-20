import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_token,
    refresh_token_expiry,
    verify_password,
)
from app.models.user import PasswordResetToken, RefreshToken, User
from app.schemas.auth import LoginRequest, RegisterRequest


def register_user(db: Session, data: RegisterRequest) -> User:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado",
        )

    user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, data: LoginRequest) -> User | None:
    user = db.query(User).filter(User.email == data.email, User.is_active == True).first()
    if not user or not verify_password(data.password, user.hashed_password):
        return None
    return user


def create_tokens(db: Session, user: User) -> tuple[str, str]:
    """Returns (access_token, raw_refresh_token)."""
    access_token = create_access_token(user.id)
    raw_refresh, hashed_refresh = generate_refresh_token()

    db_token = RefreshToken(
        user_id=user.id,
        token_hash=hashed_refresh,
        expires_at=refresh_token_expiry(),
    )
    db.add(db_token)
    db.commit()
    return access_token, raw_refresh


def rotate_refresh_token(db: Session, raw_token: str) -> tuple[str, str, User] | None:
    """Validates refresh token, rotates it. Returns (access_token, new_raw_refresh, user) or None."""
    token_hash = hash_token(raw_token)
    now = datetime.now(timezone.utc)

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > now,
    ).first()

    if not db_token:
        return None

    user = db.query(User).filter(User.id == db_token.user_id, User.is_active == True).first()
    if not user:
        return None

    # Revoke old token
    db_token.revoked = True

    # Issue new tokens
    access_token = create_access_token(user.id)
    raw_refresh, hashed_refresh = generate_refresh_token()

    new_token = RefreshToken(
        user_id=user.id,
        token_hash=hashed_refresh,
        expires_at=refresh_token_expiry(),
    )
    db.add(new_token)
    db.commit()

    return access_token, raw_refresh, user


def revoke_refresh_token(db: Session, raw_token: str) -> None:
    token_hash = hash_token(raw_token)
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False,
    ).first()
    if db_token:
        db_token.revoked = True
        db.commit()


def create_password_reset_token(db: Session, email: str) -> str | None:
    """Returns raw token if user found, None otherwise."""
    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    if not user:
        return None

    raw = secrets.token_urlsafe(32)
    hashed = hash_token(raw)

    db_token = PasswordResetToken(
        user_id=user.id,
        token_hash=hashed,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    db.add(db_token)
    db.commit()
    return raw


def reset_password(db: Session, raw_token: str, new_password: str) -> bool:
    token_hash = hash_token(raw_token)
    now = datetime.now(timezone.utc)

    db_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_hash,
        PasswordResetToken.used == False,
        PasswordResetToken.expires_at > now,
    ).first()

    if not db_token:
        return False

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        return False

    user.hashed_password = hash_password(new_password)
    db_token.used = True

    # Revoke all refresh tokens for security
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id,
        RefreshToken.revoked == False,
    ).update({"revoked": True})

    db.commit()
    return True
