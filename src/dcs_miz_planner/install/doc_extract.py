"""Opt-in campaign Doc PDF text extract with mtime/size SQLite cache."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_PAGES = 8
MAX_EXCERPT_CHARS = 2000
MAX_DOCS_PER_CAMPAIGN = 4

_CACHE_SCHEMA = """
CREATE TABLE IF NOT EXISTS campaign_doc_cache (
    path TEXT PRIMARY KEY,
    mtime_ns INTEGER NOT NULL,
    size INTEGER NOT NULL,
    excerpt TEXT NOT NULL,
    extracted_at TEXT NOT NULL
);
"""


@dataclass(frozen=True)
class DocExcerpt:
    filename: str
    excerpt: str | None = None
    cached: bool = False


class DocTextCache:
    """SQLite cache for PDF excerpts keyed by path + mtime_ns + size."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.executescript(_CACHE_SCHEMA)
        return conn

    def get(self, path: Path, *, mtime_ns: int, size: int) -> str | None:
        key = str(path.resolve())
        with self._connect() as conn:
            row = conn.execute(
                "SELECT excerpt, mtime_ns, size FROM campaign_doc_cache WHERE path = ?",
                (key,),
            ).fetchone()
        if row is None:
            return None
        if int(row["mtime_ns"]) != mtime_ns or int(row["size"]) != size:
            return None
        return str(row["excerpt"])

    def put(self, path: Path, *, mtime_ns: int, size: int, excerpt: str) -> None:
        key = str(path.resolve())
        now = datetime.now(UTC).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO campaign_doc_cache(path, mtime_ns, size, excerpt, extracted_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    mtime_ns = excluded.mtime_ns,
                    size = excluded.size,
                    excerpt = excluded.excerpt,
                    extracted_at = excluded.extracted_at
                """,
                (key, mtime_ns, size, excerpt, now),
            )
            conn.commit()


def extract_pdf_text(path: Path, *, max_pages: int = MAX_PAGES) -> str:
    """Extract plain text from a local PDF (raises on hard failure)."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    parts: list[str] = []
    for i, page in enumerate(reader.pages):
        if i >= max_pages:
            break
        parts.append(page.extract_text() or "")
    text = "\n".join(parts)
    text = " ".join(text.split())
    return text.strip()


def excerpt_for_pdf(
    path: Path,
    *,
    cache: DocTextCache | None = None,
    extract_fn=None,
) -> tuple[str | None, bool]:
    """
    Return (excerpt, from_cache).

    Skips oversized files; soft-fails to (None, False) on extract errors.
    """
    if extract_fn is None:
        extract_fn = extract_pdf_text
    try:
        st = path.stat()
    except OSError:
        return None, False
    if st.st_size <= 0 or st.st_size > MAX_FILE_BYTES:
        return None, False
    mtime_ns = getattr(st, "st_mtime_ns", int(st.st_mtime * 1_000_000_000))
    size = int(st.st_size)

    if cache is not None:
        hit = cache.get(path, mtime_ns=mtime_ns, size=size)
        if hit is not None:
            return hit, True

    try:
        text = extract_fn(path)
    except Exception:  # noqa: BLE001 — soft-fail unreadable PDFs
        return None, False
    if not text:
        return None, False
    excerpt = text[:MAX_EXCERPT_CHARS]
    if cache is not None:
        cache.put(path, mtime_ns=mtime_ns, size=size, excerpt=excerpt)
    return excerpt, False


def enrich_campaign_docs(
    campaign_path: str | Path,
    filenames: list[str],
    *,
    cache: DocTextCache | None = None,
    extract_fn=None,
) -> list[DocExcerpt]:
    """Attach excerpts for up to MAX_DOCS_PER_CAMPAIGN Doc PDFs."""
    if extract_fn is None:
        extract_fn = extract_pdf_text
    root = Path(campaign_path) / "Doc"
    out: list[DocExcerpt] = []
    for i, name in enumerate(filenames):
        if i >= MAX_DOCS_PER_CAMPAIGN:
            out.append(DocExcerpt(filename=name, excerpt=None, cached=False))
            continue
        pdf = root / name
        excerpt, cached = excerpt_for_pdf(pdf, cache=cache, extract_fn=extract_fn)
        out.append(DocExcerpt(filename=name, excerpt=excerpt, cached=cached))
    return out
