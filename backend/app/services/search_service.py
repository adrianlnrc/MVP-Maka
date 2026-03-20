from sqlalchemy import func, or_, text
from sqlalchemy.orm import Session

from app.models.content import Character, Story


def search(db: Session, query: str, search_type: str = "all", limit: int = 20) -> dict:
    results: dict = {"stories": [], "characters": []}

    if not query.strip():
        return results

    ts_query = func.plainto_tsquery("portuguese", query)

    if search_type in ("all", "stories"):
        stories = (
            db.query(Story)
            .filter(
                Story.is_published == True,
                or_(
                    Story.search_vector.op("@@")(ts_query),
                    Story.title.ilike(f"%{query}%"),
                ),
            )
            .order_by(func.ts_rank(Story.search_vector, ts_query).desc())
            .limit(limit)
            .all()
        )
        results["stories"] = stories

    if search_type in ("all", "characters"):
        characters = (
            db.query(Character)
            .filter(
                or_(
                    Character.search_vector.op("@@")(ts_query),
                    Character.name.ilike(f"%{query}%"),
                )
            )
            .order_by(func.ts_rank(Character.search_vector, ts_query).desc())
            .limit(limit)
            .all()
        )
        results["characters"] = characters

    return results
