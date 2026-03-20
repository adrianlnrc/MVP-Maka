from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import bible_api_service as bible
from app.services import translation_service

router = APIRouter(prefix="/api/bible", tags=["bible"])


def _handle(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"IQ Bible API error: {exc}") from exc


# ── Verse endpoints ───────────────────────────────────────────────────────────

@router.get("/verse/{verse_id}")
def get_verse(
    verse_id: str,
    version: str = Query("kjv"),
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Retorna um versículo. Ex: 01001001 (Gên 1:1) — formato: BB CCC VVV sem espaços."""
    data = _handle(bible.get_verse, verse_id, version)
    if translate:
        data = translation_service.translate_fields(data, ["t"], db)
    return data


@router.get("/random")
def get_random_verse(
    version: str = Query("kjv"),
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Retorna um versículo aleatório."""
    data = _handle(bible.get_random_verse, version)
    if translate:
        data = translation_service.translate_fields(data, ["t"], db)
    return data


@router.get("/parallel/{verse_id}")
def get_parallel_verses(
    verse_id: str,
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Retorna um versículo em todas as traduções disponíveis."""
    data = _handle(bible.get_parallel_verses, verse_id)
    if translate:
        data = translation_service.translate_fields(data, ["t"], db)
    return data


# ── Chapter endpoints ─────────────────────────────────────────────────────────

@router.get("/chapter")
def get_chapter(
    book_id: str = Query(..., description="Ex: Gen"),
    chapter: int = Query(..., description="Número do capítulo"),
    version: str = Query("kjv"),
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Retorna todos os versículos de um capítulo."""
    data = _handle(bible.get_chapter, book_id, chapter, version)
    if translate:
        data = translation_service.translate_fields(data, ["t"], db)
    return data


# ── Search endpoints ──────────────────────────────────────────────────────────

@router.get("/search")
def search_bible(
    q: str = Query(..., description="Termo de busca"),
    version: str = Query("kjv"),
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Busca simples na Bíblia."""
    data = _handle(bible.search_bible, q, version)
    if translate:
        data = translation_service.translate_fields(data, ["t"], db)
    return data


@router.get("/search/advanced")
def search_bible_advanced(
    q: str = Query(..., description="Termo de busca"),
    book_id: str | None = Query(None, description="Filtrar por livro (ex: Gen)"),
    version: str = Query("kjv"),
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Busca avançada com filtro por livro."""
    data = _handle(bible.search_bible_advanced, q, book_id, version)
    if translate:
        data = translation_service.translate_fields(data, ["t"], db)
    return data


# ── Cross references & Commentary ─────────────────────────────────────────────

@router.get("/cross-references/{verse_id}")
def get_cross_references(verse_id: str):
    """Referências cruzadas de um versículo."""
    return _handle(bible.get_cross_references, verse_id)


@router.get("/commentary/{verse_id}")
def get_commentary(
    verse_id: str,
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Comentário bíblico de um versículo."""
    data = _handle(bible.get_commentary, verse_id)
    if translate:
        data = translation_service.translate_fields(data, ["c"], db)
    return data


# ── Original languages ────────────────────────────────────────────────────────

@router.get("/original/{verse_id}")
def get_original_text(verse_id: str):
    """Texto original (Hebraico/Grego) com transliteração."""
    return _handle(bible.get_original_text, verse_id)


@router.get("/strongs/{strongs_id}")
def get_strongs(
    strongs_id: str,
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Dicionário Strong. Ex: H430 (heb.) ou G2316 (gr.)."""
    data = _handle(bible.get_strongs, strongs_id)
    if translate:
        data = translation_service.translate_fields(data, ["def"], db)
    return data


# ── Book info ─────────────────────────────────────────────────────────────────

@router.get("/book/{book_id}")
def get_book_info(
    book_id: str,
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Informações sobre um livro bíblico."""
    data = _handle(bible.get_book_info, book_id)
    if translate:
        data = translation_service.translate_fields(data, ["introduction", "genre", "author"], db)
    return data


# ── Reading plans ─────────────────────────────────────────────────────────────

@router.get("/reading-plan")
def get_bible_reading_plan(
    plan_id: str | None = Query(None),
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Planos de leitura bíblica da API."""
    data = _handle(bible.get_bible_reading_plan, plan_id)
    if translate:
        data = translation_service.translate_fields(data, ["title", "description"], db)
    return data


@router.get("/reading-plan/topic")
def get_bible_reading_plan_by_topic(
    topic: str = Query(...),
    translate: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Plano de leitura por tópico."""
    data = _handle(bible.get_bible_reading_plan_by_topic, topic)
    if translate:
        data = translation_service.translate_fields(data, ["title", "description"], db)
    return data
