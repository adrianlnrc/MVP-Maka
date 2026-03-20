import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.exceptions import not_found_exception
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.content import (
    CharacterBrief,
    CharacterOut,
    EraOut,
    PaginatedCharacters,
    PaginatedStories,
    StoryBrief,
    StoryOut,
    TimelineEventOut,
)
from app.services import content_service

router = APIRouter(tags=["content"])

# ── Eras ──────────────────────────────────────────────────────────────────────

eras_router = APIRouter(prefix="/api/eras")


@eras_router.get("", response_model=list[EraOut])
def list_eras(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    eras = content_service.get_all_eras(db)
    counts = content_service.count_stories_per_era(db)
    result = []
    for era in eras:
        era_out = EraOut.model_validate(era)
        era_out.story_count = counts.get(era.id, 0)
        result.append(era_out)
    return result


@eras_router.get("/{slug}", response_model=EraOut)
def get_era(
    slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    era = content_service.get_era_by_slug(db, slug)
    if not era:
        raise not_found_exception
    counts = content_service.count_stories_per_era(db)
    era_out = EraOut.model_validate(era)
    era_out.story_count = counts.get(era.id, 0)
    return era_out


# ── Stories ───────────────────────────────────────────────────────────────────

stories_router = APIRouter(prefix="/api/stories")


@stories_router.get("", response_model=PaginatedStories)
def list_stories(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    era_id: int | None = Query(None),
    theme: str | None = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    items, total = content_service.get_stories_paginated(db, page, page_size, era_id, theme)
    return PaginatedStories(
        items=[StoryBrief.model_validate(s) for s in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total else 0,
    )


@stories_router.get("/{slug}", response_model=StoryOut)
def get_story(
    slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    story = content_service.get_story_by_slug(db, slug)
    if not story:
        raise not_found_exception

    story_out = StoryOut.model_validate(story)
    story_out.characters = [
        CharacterBrief.model_validate(sc.character)
        for sc in story.story_characters
    ]
    return story_out


@stories_router.get("/{slug}/related", response_model=list[StoryBrief])
def get_related_stories(
    slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    story = content_service.get_story_by_slug(db, slug)
    if not story:
        raise not_found_exception
    return [StoryBrief.model_validate(s) for s in content_service.get_related_stories(db, story)]


# ── Characters ────────────────────────────────────────────────────────────────

characters_router = APIRouter(prefix="/api/characters")


@characters_router.get("", response_model=PaginatedCharacters)
def list_characters(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    era_id: int | None = Query(None),
    role: str | None = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    items, total = content_service.get_characters_paginated(db, page, page_size, era_id, role)
    return PaginatedCharacters(
        items=[CharacterBrief.model_validate(c) for c in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total else 0,
    )


@characters_router.get("/{slug}", response_model=CharacterOut)
def get_character(
    slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    character = content_service.get_character_by_slug(db, slug)
    if not character:
        raise not_found_exception

    char_out = CharacterOut.model_validate(character)
    char_out.stories = [
        StoryBrief.model_validate(sc.story)
        for sc in character.story_characters
        if sc.story.is_published
    ]
    return char_out


# ── Timeline ──────────────────────────────────────────────────────────────────

timeline_router = APIRouter(prefix="/api/timeline")


@timeline_router.get("", response_model=list[TimelineEventOut])
def get_timeline(
    era: str | None = Query(None),
    character: str | None = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    events = content_service.get_timeline_events(db, era_slug=era, character_slug=character)
    return [TimelineEventOut.model_validate(e) for e in events]


# ── Search ────────────────────────────────────────────────────────────────────

search_router = APIRouter(prefix="/api/search")


@search_router.get("")
def search(
    q: str = Query("", min_length=1),
    type: str = Query("all", pattern="^(all|stories|characters)$"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    from app.services.search_service import search as do_search
    from app.schemas.content import StoryBrief, CharacterBrief

    results = do_search(db, q, type)
    return {
        "stories": [StoryBrief.model_validate(s) for s in results.get("stories", [])],
        "characters": [CharacterBrief.model_validate(c) for c in results.get("characters", [])],
    }
