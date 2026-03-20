#!/usr/bin/env python3
"""Popula o banco com os dados iniciais do Maka."""
import json
import sys
from pathlib import Path

# Add parent to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine
from app.models import *  # noqa: F401, F403
from app.database import Base


def load_json(name: str) -> list:
    data_dir = Path(__file__).parent.parent / "app" / "data"
    with open(data_dir / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # ── Eras ──────────────────────────────────────────────────────────────
        print("Seeding eras...")
        from app.models.content import Era
        for era_data in load_json("eras"):
            era = db.query(Era).filter(Era.slug == era_data["slug"]).first()
            if not era:
                era = Era(**era_data)
                db.add(era)
            else:
                for k, v in era_data.items():
                    setattr(era, k, v)
        db.commit()
        print(f"  ✓ {db.query(Era).count()} eras")

        # ── Characters ────────────────────────────────────────────────────────
        print("Seeding characters...")
        from app.models.content import Character
        era_map = {e.slug: e.id for e in db.query(Era).all()}

        for char_data in load_json("characters"):
            era_slug = char_data.pop("era_slug")
            char_data["era_id"] = era_map[era_slug]

            char = db.query(Character).filter(Character.slug == char_data["slug"]).first()
            if not char:
                char = Character(**char_data)
                db.add(char)
            else:
                for k, v in char_data.items():
                    setattr(char, k, v)
        db.commit()
        print(f"  ✓ {db.query(Character).count()} characters")

        # ── Stories ───────────────────────────────────────────────────────────
        print("Seeding stories...")
        from app.models.content import Story
        for story_data in load_json("stories"):
            era_slug = story_data.pop("era_slug")
            story_data["era_id"] = era_map[era_slug]

            story = db.query(Story).filter(Story.slug == story_data["slug"]).first()
            if not story:
                story = Story(**story_data)
                db.add(story)
            else:
                for k, v in story_data.items():
                    setattr(story, k, v)
        db.commit()
        print(f"  ✓ {db.query(Story).count()} stories")

        # ── Timeline Events ───────────────────────────────────────────────────
        print("Seeding timeline events...")
        from app.models.content import TimelineEvent
        for event_data in load_json("timeline_events"):
            era_slug = event_data.pop("era_slug")
            event_data["era_id"] = era_map[era_slug]

            event = db.query(TimelineEvent).filter(
                TimelineEvent.era_id == event_data["era_id"],
                TimelineEvent.title == event_data["title"],
            ).first()
            if not event:
                event = TimelineEvent(**event_data)
                db.add(event)
            else:
                for k, v in event_data.items():
                    setattr(event, k, v)
        db.commit()
        print(f"  ✓ {db.query(TimelineEvent).count()} timeline events")

        # ── Reading Plan ──────────────────────────────────────────────────────
        print("Seeding reading plan...")
        from app.models.reading_plan import ReadingPlan, ReadingPlanDay
        plan = db.query(ReadingPlan).filter(ReadingPlan.is_default == True).first()
        if not plan:
            plan = ReadingPlan(
                name="Plano 365 — Bíblia Cronológica",
                description="Uma jornada de 365 dias através da Bíblia em ordem cronológica, da Criação ao Apocalipse.",
                total_days=365,
                is_default=True,
            )
            db.add(plan)
            db.commit()
            db.refresh(plan)

        days_data = load_json("reading_plan_365")
        for day_data in days_data:
            day_data["plan_id"] = plan.id
            if "story_ids" not in day_data:
                day_data["story_ids"] = []
            if "reflection_prompt" not in day_data:
                day_data["reflection_prompt"] = ""

            existing = db.query(ReadingPlanDay).filter(
                ReadingPlanDay.plan_id == plan.id,
                ReadingPlanDay.day_number == day_data["day_number"],
            ).first()
            if not existing:
                existing = ReadingPlanDay(**day_data)
                db.add(existing)
        db.commit()
        print(f"  ✓ {db.query(ReadingPlanDay).count()} reading plan days")

        print("\n✅ Seed completo!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
