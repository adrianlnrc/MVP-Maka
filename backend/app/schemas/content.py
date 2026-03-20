from datetime import datetime

from pydantic import BaseModel


class EraOut(BaseModel):
    id: int
    slug: str
    name: str
    description: str
    order_index: int
    approx_date_start: str
    approx_date_end: str
    color_hex: str
    cover_image_url: str | None
    story_count: int = 0

    model_config = {"from_attributes": True}


class CharacterBrief(BaseModel):
    id: str
    slug: str
    name: str
    role: str
    image_url: str | None

    model_config = {"from_attributes": True}


class StoryBrief(BaseModel):
    id: str
    slug: str
    title: str
    summary: str
    order_index: int
    reading_time_minutes: int
    era_id: int
    themes: list[str]

    model_config = {"from_attributes": True}


class StoryOut(BaseModel):
    id: str
    slug: str
    title: str
    summary: str
    content: str
    order_index: int
    bible_references: list[str]
    themes: list[str]
    reading_time_minutes: int
    era: EraOut
    characters: list[CharacterBrief] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CharacterOut(BaseModel):
    id: str
    slug: str
    name: str
    also_known_as: list[str]
    birth_approx: str | None
    death_approx: str | None
    biography: str
    role: str
    significance: str
    bible_references: list[str]
    image_url: str | None
    era: EraOut
    stories: list[StoryBrief] = []

    model_config = {"from_attributes": True}


class TimelineEventOut(BaseModel):
    id: str
    era_id: int
    story_id: str | None
    character_id: str | None
    title: str
    description: str
    event_type: str
    year_approx: int
    year_display: str
    duration_years: int | None
    order_index: int

    model_config = {"from_attributes": True}


class PaginatedStories(BaseModel):
    items: list[StoryBrief]
    total: int
    page: int
    page_size: int
    pages: int


class PaginatedCharacters(BaseModel):
    items: list[CharacterBrief]
    total: int
    page: int
    page_size: int
    pages: int
