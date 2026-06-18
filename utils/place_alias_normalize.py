"""Normalize place alias text for case/diacritic-insensitive search."""

from __future__ import annotations

import re
import unicodedata

_WS_RE = re.compile(r"\s+")


def normalize_place_alias(text: str) -> str:
    """Lowercase, strip diacritics, collapse whitespace."""
    if not text:
        return ""
    folded = unicodedata.normalize("NFKD", text.strip())
    asciiish = "".join(ch for ch in folded if not unicodedata.combining(ch))
    return _WS_RE.sub(" ", asciiish).lower().strip()


def split_geonames_alternates(raw: str) -> list[str]:
    """Split GeoNames comma-separated alternatenames field."""
    if not raw or not str(raw).strip():
        return []
    seen: set[str] = set()
    out: list[str] = []
    for part in str(raw).split(","):
        alias = part.strip()
        if not alias or len(alias) < 2:
            continue
        key = normalize_place_alias(alias)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(alias)
    return out
