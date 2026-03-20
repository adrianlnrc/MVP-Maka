import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"), unique=True, nullable=False)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("reading_plan.id"), nullable=False)
    current_day: Mapped[int] = mapped_column(Integer, default=1)
    streak_days: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    total_days_completed: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="progress")
    plan: Mapped["ReadingPlan"] = relationship(back_populates="user_progresses")


class UserReadingLog(Base):
    __tablename__ = "user_reading_log"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"), nullable=False)
    plan_day_id: Mapped[int] = mapped_column(Integer, ForeignKey("reading_plan_day.id"), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="reading_logs")
    plan_day: Mapped["ReadingPlanDay"] = relationship(back_populates="reading_logs")


class UserNote(Base):
    __tablename__ = "user_note"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"), nullable=False)
    story_id: Mapped[str | None] = mapped_column(String, ForeignKey("story.id"), nullable=True)
    character_id: Mapped[str | None] = mapped_column(String, ForeignKey("character.id"), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="notes")


# Forward references
from app.models.user import User  # noqa: E402, F401
from app.models.reading_plan import ReadingPlan, ReadingPlanDay  # noqa: E402, F401
