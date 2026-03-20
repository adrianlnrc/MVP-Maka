from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.exceptions import not_found_exception
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.reading_plan import (
    CompleteDayRequest,
    ReadingPlanDayOut,
    ReadingPlanOut,
    UserProgressOut,
)
from app.services import reading_plan_service

router = APIRouter(prefix="/api", tags=["reading-plan"])


@router.get("/reading-plan", response_model=ReadingPlanOut)
def get_plan(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    plan = reading_plan_service.get_default_plan(db)
    if not plan:
        raise not_found_exception
    return ReadingPlanOut.model_validate(plan)


@router.get("/reading-plan/today", response_model=ReadingPlanDayOut)
def get_today(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    progress = reading_plan_service.get_or_create_progress(db, user)
    day = reading_plan_service.get_day(db, progress.plan_id, progress.current_day)
    if not day:
        raise not_found_exception
    return ReadingPlanDayOut.model_validate(day)


@router.get("/reading-plan/day/{day_number}", response_model=ReadingPlanDayOut)
def get_day(
    day_number: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    progress = reading_plan_service.get_or_create_progress(db, user)
    day = reading_plan_service.get_day(db, progress.plan_id, day_number)
    if not day:
        raise not_found_exception
    return ReadingPlanDayOut.model_validate(day)


@router.post("/reading-plan/start", response_model=UserProgressOut)
def start_plan(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    progress = reading_plan_service.get_or_create_progress(db, user)
    return UserProgressOut.model_validate(progress)


@router.get("/progress", response_model=UserProgressOut)
def get_progress(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    progress = reading_plan_service.get_or_create_progress(db, user)
    return UserProgressOut.model_validate(progress)


@router.post("/progress/complete-day", response_model=UserProgressOut)
def complete_day(
    data: CompleteDayRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    progress = reading_plan_service.complete_day(db, user, data.day_number, data.notes)
    return UserProgressOut.model_validate(progress)
