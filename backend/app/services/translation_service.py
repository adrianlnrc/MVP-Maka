"""
Serviço de tradução EN→PT-BR com cache no PostgreSQL.
Usa deep-translator (GoogleTranslator, gratuito, sem chave de API).
"""
import hashlib
import logging

from deep_translator import GoogleTranslator
from sqlalchemy.orm import Session

from app.models.translation import TranslationCache

logger = logging.getLogger(__name__)


def translate_to_pt(text: str, db: Session) -> str:
    """Traduz texto EN→PT, usando cache no PostgreSQL."""
    if not text or not text.strip():
        return text

    source_hash = hashlib.sha256(text.encode()).hexdigest()

    cached = db.query(TranslationCache).filter_by(source_hash=source_hash).first()
    if cached:
        return cached.translated_text

    try:
        translated = GoogleTranslator(source="en", target="pt").translate(text)
    except Exception as exc:
        logger.warning("Falha ao traduzir texto: %s", exc)
        return text

    db.add(TranslationCache(
        source_hash=source_hash,
        source_text=text,
        translated_text=translated,
    ))
    db.commit()

    return translated


def translate_fields(data: dict | list, fields: list[str], db: Session) -> dict | list:
    """Traduz campos específicos de um dict ou lista de dicts."""
    if isinstance(data, list):
        return [translate_fields(item, fields, db) for item in data]
    if isinstance(data, dict):
        return {
            k: translate_to_pt(v, db) if k in fields and isinstance(v, str) else v
            for k, v in data.items()
        }
    return data
