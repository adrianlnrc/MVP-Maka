from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserPublic, UserStats, UserUpdate
from app.services.reading_plan_service import get_or_create_progress

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.put("/me", response_model=UserPublic)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if data.full_name is not None:
        user.full_name = data.full_name
    db.commit()
    db.refresh(user)
    return user


@router.get("/me/stats", response_model=UserStats)
def get_stats(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        progress = get_or_create_progress(db, user)
        return UserStats(
            total_days_completed=progress.total_days_completed,
            streak_days=progress.streak_days,
            longest_streak=progress.longest_streak,
            current_day=progress.current_day,
        )
    except ValueError:
        return UserStats(
            total_days_completed=0,
            streak_days=0,
            longest_streak=0,
            current_day=None,
        )
