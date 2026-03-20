from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.content import Character, Era, Story, TimelineEvent


def get_all_eras(db: Session) -> list[Era]:
    return db.query(Era).order_by(Era.order_index).all()


def get_era_by_slug(db: Session, slug: str) -> Era | None:
    return db.query(Era).filter(Era.slug == slug).first()


def get_stories_paginated(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    era_id: int | None = None,
    theme: str | None = None,
) -> tuple[list[Story], int]:
    q = db.query(Story).filter(Story.is_published == True)

    if era_id:
        q = q.filter(Story.era_id == era_id)
    if theme:
        q = q.filter(Story.themes.contains([theme]))

    total = q.count()
    items = q.order_by(Story.era_id, Story.order_index).offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def get_story_by_slug(db: Session, slug: str) -> Story | None:
    return db.query(Story).filter(Story.slug == slug, Story.is_published == True).first()


def get_related_stories(db: Session, story: Story, limit: int = 4) -> list[Story]:
    return (
        db.query(Story)
        .filter(Story.era_id == story.era_id, Story.id != story.id, Story.is_published == True)
        .order_by(Story.order_index)
        .limit(limit)
        .all()
    )


def get_characters_paginated(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    era_id: int | None = None,
    role: str | None = None,
) -> tuple[list[Character], int]:
    q = db.query(Character)

    if era_id:
        q = q.filter(Character.era_id == era_id)
    if role:
        q = q.filter(Character.role.ilike(f"%{role}%"))

    total = q.count()
    items = q.order_by(Character.name).offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def get_character_by_slug(db: Session, slug: str) -> Character | None:
    return db.query(Character).filter(Character.slug == slug).first()


def get_timeline_events(
    db: Session,
    era_slug: str | None = None,
    character_slug: str | None = None,
) -> list[TimelineEvent]:
    q = db.query(TimelineEvent)

    if era_slug:
        era = get_era_by_slug(db, era_slug)
        if era:
            q = q.filter(TimelineEvent.era_id == era.id)

    if character_slug:
        char = get_character_by_slug(db, character_slug)
        if char:
            q = q.filter(TimelineEvent.character_id == char.id)

    return q.order_by(TimelineEvent.year_approx, TimelineEvent.order_index).all()


def count_stories_per_era(db: Session) -> dict[int, int]:
    rows = (
        db.query(Story.era_id, func.count(Story.id))
        .filter(Story.is_published == True)
        .group_by(Story.era_id)
        .all()
    )
    return {era_id: count for era_id, count in rows}
