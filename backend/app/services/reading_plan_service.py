from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.models.progress import UserProgress, UserReadingLog
from app.models.reading_plan import ReadingPlan, ReadingPlanDay
from app.models.user import User


def get_default_plan(db: Session) -> ReadingPlan | None:
    return db.query(ReadingPlan).filter(ReadingPlan.is_default == True).first()


def get_or_create_progress(db: Session, user: User) -> UserProgress:
    progress = db.query(UserProgress).filter(UserProgress.user_id == user.id).first()
    if progress:
        return progress

    plan = get_default_plan(db)
    if not plan:
        raise ValueError("Nenhum plano de leitura configurado")

    progress = UserProgress(user_id=user.id, plan_id=plan.id)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def get_day(db: Session, plan_id: int, day_number: int) -> ReadingPlanDay | None:
    return (
        db.query(ReadingPlanDay)
        .filter(
            ReadingPlanDay.plan_id == plan_id,
            ReadingPlanDay.day_number == day_number,
        )
        .first()
    )


def complete_day(db: Session, user: User, day_number: int, notes: str | None = None) -> UserProgress:
    progress = get_or_create_progress(db, user)

    plan_day = get_day(db, progress.plan_id, day_number)
    if not plan_day:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dia não encontrado no plano")

    # Check if already completed
    already = (
        db.query(UserReadingLog)
        .filter(
            UserReadingLog.user_id == user.id,
            UserReadingLog.plan_day_id == plan_day.id,
        )
        .first()
    )
    if already:
        return progress

    log = UserReadingLog(user_id=user.id, plan_day_id=plan_day.id, notes=notes)
    db.add(log)

    now = datetime.now(timezone.utc)

    # Streak logic
    if progress.last_read_at:
        last_date = progress.last_read_at.date() if hasattr(progress.last_read_at, 'date') else progress.last_read_at
        today = now.date()
        delta = (today - last_date).days
        if delta == 1:
            progress.streak_days += 1
        elif delta > 1:
            progress.streak_days = 1
        # delta == 0 means same day — no change to streak
    else:
        progress.streak_days = 1

    if progress.streak_days > progress.longest_streak:
        progress.longest_streak = progress.streak_days

    progress.last_read_at = now
    progress.total_days_completed += 1

    # Advance to next day if completing current day
    if day_number == progress.current_day:
        plan = db.query(ReadingPlan).filter(ReadingPlan.id == progress.plan_id).first()
        if plan and progress.current_day < plan.total_days:
            progress.current_day += 1

    db.commit()
    db.refresh(progress)
    return progress
