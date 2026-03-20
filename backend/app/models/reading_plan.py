from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReadingPlan(Base):
    __tablename__ = "reading_plan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    total_days: Mapped[int] = mapped_column(Integer, nullable=False, default=365)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    days: Mapped[list["ReadingPlanDay"]] = relationship(
        back_populates="plan", order_by="ReadingPlanDay.day_number"
    )
    user_progresses: Mapped[list["UserProgress"]] = relationship(back_populates="plan")


class ReadingPlanDay(Base):
    __tablename__ = "reading_plan_day"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("reading_plan.id"), nullable=False)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    story_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    bible_passages: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    reflection_prompt: Mapped[str] = mapped_column(Text, nullable=False, default="")

    plan: Mapped["ReadingPlan"] = relationship(back_populates="days")
    reading_logs: Mapped[list["UserReadingLog"]] = relationship(back_populates="plan_day")


# Forward references
from app.models.progress import UserProgress, UserReadingLog  # noqa: E402, F401
