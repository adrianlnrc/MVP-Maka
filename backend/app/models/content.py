import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Integer, String, Text, func
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Era(Base):
    __tablename__ = "era"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    approx_date_start: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    approx_date_end: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    color_hex: Mapped[str] = mapped_column(String(7), nullable=False, default="#6366f1")
    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    stories: Mapped[list["Story"]] = relationship(back_populates="era", order_by="Story.order_index")
    characters: Mapped[list["Character"]] = relationship(back_populates="era")
    timeline_events: Mapped[list["TimelineEvent"]] = relationship(back_populates="era", order_by="TimelineEvent.order_index")


class Story(Base):
    __tablename__ = "story"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    era_id: Mapped[int] = mapped_column(Integer, ForeignKey("era.id"), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bible_references: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    themes: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    reading_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    era: Mapped["Era"] = relationship(back_populates="stories")
    story_characters: Mapped[list["StoryCharacter"]] = relationship(back_populates="story", cascade="all, delete-orphan")
    timeline_events: Mapped[list["TimelineEvent"]] = relationship(back_populates="story")


class Character(Base):
    __tablename__ = "character"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    era_id: Mapped[int] = mapped_column(Integer, ForeignKey("era.id"), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    also_known_as: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    birth_approx: Mapped[str | None] = mapped_column(String(50), nullable=True)
    death_approx: Mapped[str | None] = mapped_column(String(50), nullable=True)
    biography: Mapped[str] = mapped_column(Text, nullable=False, default="")
    role: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    significance: Mapped[str] = mapped_column(Text, nullable=False, default="")
    bible_references: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)

    era: Mapped["Era"] = relationship(back_populates="characters")
    story_characters: Mapped[list["StoryCharacter"]] = relationship(back_populates="character")
    timeline_events: Mapped[list["TimelineEvent"]] = relationship(back_populates="character")


class StoryCharacter(Base):
    __tablename__ = "story_character"

    story_id: Mapped[str] = mapped_column(String, ForeignKey("story.id"), primary_key=True)
    character_id: Mapped[str] = mapped_column(String, ForeignKey("character.id"), primary_key=True)
    role_in_story: Mapped[str | None] = mapped_column(String(200), nullable=True)

    story: Mapped["Story"] = relationship(back_populates="story_characters")
    character: Mapped["Character"] = relationship(back_populates="story_characters")


class TimelineEvent(Base):
    __tablename__ = "timeline_event"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    era_id: Mapped[int] = mapped_column(Integer, ForeignKey("era.id"), nullable=False)
    story_id: Mapped[str | None] = mapped_column(String, ForeignKey("story.id"), nullable=True)
    character_id: Mapped[str | None] = mapped_column(String, ForeignKey("character.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, default="event")
    year_approx: Mapped[int] = mapped_column(Integer, nullable=False)
    year_display: Mapped[str] = mapped_column(String(50), nullable=False)
    duration_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    era: Mapped["Era"] = relationship(back_populates="timeline_events")
    story: Mapped["Story | None"] = relationship(back_populates="timeline_events")
    character: Mapped["Character | None"] = relationship(back_populates="timeline_events")
