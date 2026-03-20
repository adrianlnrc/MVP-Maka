from datetime import datetime, timezone

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import credentials_exception, subscription_required_exception
from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import SubscriptionStatus, User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not credentials:
        raise credentials_exception

    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise credentials_exception

    return user


def require_active_subscription(user: User = Depends(get_current_user)) -> User:
    is_active = user.subscription_status == SubscriptionStatus.active
    not_expired = (
        user.subscription_expires_at is None
        or user.subscription_expires_at > datetime.now(timezone.utc)
    )
    if not (is_active and not_expired):
        raise subscription_required_exception
    return user
