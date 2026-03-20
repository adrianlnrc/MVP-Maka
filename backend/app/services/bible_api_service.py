"""
IQ Bible API service — wraps iq-bible.p.rapidapi.com endpoints.
All methods return parsed JSON from the API.
"""
import httpx

from app.config import settings

_BASE_URL = "https://iq-bible.p.rapidapi.com"


def _headers() -> dict:
    return {
        "x-rapidapi-key": settings.IQBIBLE_API_KEY,
        "x-rapidapi-host": "iq-bible.p.rapidapi.com",
    }


def _get(path: str, params: dict | None = None) -> dict | list:
    with httpx.Client(timeout=15) as client:
        response = client.get(f"{_BASE_URL}{path}", headers=_headers(), params=params or {})
        response.raise_for_status()
        return response.json()


# ── Verse ────────────────────────────────────────────────────────────────────

def get_verse(verse_id: str, version: str = "kjv") -> dict:
    """verse_id format: '01001001' (BB=book, CCC=chapter, VVV=verse, zero-padded). Ex: 01001001 = Gen 1:1"""
    return _get("/GetVerse", {"verseId": verse_id, "versionId": version})


def get_random_verse(version: str = "kjv") -> dict:
    return _get("/GetRandomVerse", {"versionId": version})


def get_parallel_verses(verse_id: str) -> list:
    """Returns the verse in all available translations."""
    return _get("/GetParallelVerses", {"verseId": verse_id})


# ── Chapter ──────────────────────────────────────────────────────────────────

def get_chapter(book_id: str, chapter_number: int, version: str = "kjv") -> list:
    return _get("/GetChapter", {
        "bookId": book_id,
        "chapterId": str(chapter_number),
        "versionId": version,
    })


# ── Search ───────────────────────────────────────────────────────────────────

def search_bible(query: str, version: str = "kjv") -> list:
    return _get("/GetSearch", {"text": query, "versionId": version})


def search_bible_advanced(query: str, book_id: str | None = None, version: str = "kjv") -> list:
    params: dict = {"text": query, "versionId": version}
    if book_id:
        params["bookId"] = book_id
    return _get("/GetSearchAdvanced", params)


# ── Cross references & Commentary ───────────────────────────────────────────

def get_cross_references(verse_id: str) -> list:
    return _get("/GetCrossReferences", {"verseId": verse_id})


def get_commentary(verse_id: str) -> list:
    return _get("/GetCommentary", {"verseId": verse_id})


# ── Original languages ───────────────────────────────────────────────────────

def get_original_text(verse_id: str) -> list:
    """Returns Hebrew/Greek words with transliteration."""
    return _get("/GetOriginalText", {"verseId": verse_id})


def get_strongs(strongs_id: str) -> dict:
    """strongs_id: e.g. 'H430' (Hebrew) or 'G2316' (Greek)."""
    return _get("/GetStrongs", {"strongsId": strongs_id})


# ── Books ────────────────────────────────────────────────────────────────────

def get_book_info(book_id: str) -> dict:
    return _get("/GetBookInfo", {"bookId": book_id})


# ── Reading plans ────────────────────────────────────────────────────────────

def get_bible_reading_plan(plan_id: str | None = None) -> list:
    params = {"planId": plan_id} if plan_id else {}
    return _get("/GetBibleReadingPlan", params)


def get_bible_reading_plan_by_topic(topic: str) -> list:
    return _get("/GetBibleReadingPlanByTopic", {"topic": topic})
