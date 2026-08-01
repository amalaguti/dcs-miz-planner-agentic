"""SQLite persistence for user prefs, generation history, and feedback."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import FeedbackRecord, GenerationRecord

USER_SCHEMA_VERSION = 1

_PROMPT_MAX_LEN = 2000

_USER_TABLES = (
    "user_prefs",
    "generation_history",
    "satisfaction_feedback",
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS user_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS user_prefs (
    key TEXT PRIMARY KEY,
    value_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS generation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    prompt TEXT,
    mission_type TEXT,
    theatre TEXT,
    spec_path TEXT,
    miz_path TEXT,
    outcome TEXT NOT NULL,
    detail_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS satisfaction_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    generation_id INTEGER,
    score INTEGER,
    note TEXT,
    tags_json TEXT NOT NULL DEFAULT '[]',
    source TEXT NOT NULL,
    FOREIGN KEY (generation_id) REFERENCES generation_history(id)
);
"""


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _truncate_prompt(prompt: str | None) -> str | None:
    if prompt is None:
        return None
    if len(prompt) <= _PROMPT_MAX_LEN:
        return prompt
    return prompt[:_PROMPT_MAX_LEN] + "…"


class UserMemoryStore:
    """Read/write user-memory tables (shares DB file with install + catalog)."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.executescript(_SCHEMA)
        row = conn.execute(
            "SELECT value FROM user_meta WHERE key = 'user_schema_version'"
        ).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO user_meta(key, value) VALUES ('user_schema_version', ?)",
                (str(USER_SCHEMA_VERSION),),
            )
            conn.commit()
        elif int(row["value"]) != USER_SCHEMA_VERSION:
            for table in _USER_TABLES:
                conn.execute(f"DELETE FROM {table}")
            conn.execute(
                "UPDATE user_meta SET value = ? WHERE key = 'user_schema_version'",
                (str(USER_SCHEMA_VERSION),),
            )
            conn.commit()
        return conn

    def get_prefs(self, keys: list[str] | None = None) -> dict[str, Any]:
        with self._connect() as conn:
            if keys:
                placeholders = ",".join("?" for _ in keys)
                rows = conn.execute(
                    f"SELECT key, value_json FROM user_prefs WHERE key IN ({placeholders})",
                    tuple(keys),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT key, value_json FROM user_prefs ORDER BY key"
                ).fetchall()
        out: dict[str, Any] = {}
        for row in rows:
            try:
                out[row["key"]] = json.loads(row["value_json"])
            except json.JSONDecodeError:
                out[row["key"]] = row["value_json"]
        return out

    def set_prefs(self, prefs: dict[str, Any]) -> dict[str, Any]:
        if not prefs:
            return self.get_prefs()
        now = _utc_now()
        with self._connect() as conn:
            for key, value in prefs.items():
                conn.execute(
                    """
                    INSERT INTO user_prefs(key, value_json, updated_at)
                    VALUES (?, ?, ?)
                    ON CONFLICT(key) DO UPDATE SET
                        value_json = excluded.value_json,
                        updated_at = excluded.updated_at
                    """,
                    (str(key), json.dumps(value), now),
                )
            conn.commit()
        return self.get_prefs()

    def append_generation(
        self,
        *,
        outcome: str,
        prompt: str | None = None,
        mission_type: str | None = None,
        theatre: str | None = None,
        spec_path: str | None = None,
        miz_path: str | None = None,
        detail: dict[str, Any] | None = None,
    ) -> int:
        detail = detail or {}
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO generation_history(
                    created_at, prompt, mission_type, theatre,
                    spec_path, miz_path, outcome, detail_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    _utc_now(),
                    _truncate_prompt(prompt),
                    mission_type,
                    theatre,
                    spec_path,
                    miz_path,
                    outcome,
                    json.dumps(detail),
                ),
            )
            conn.commit()
            return int(cur.lastrowid)

    def list_generations(self, *, limit: int = 20) -> list[GenerationRecord]:
        limit = max(1, min(int(limit), 200))
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, created_at, prompt, mission_type, theatre,
                       spec_path, miz_path, outcome, detail_json
                FROM generation_history
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [_row_to_generation(r) for r in rows]

    def add_feedback(
        self,
        *,
        source: str,
        generation_id: int | None = None,
        score: int | None = None,
        note: str | None = None,
        tags: list[Any] | None = None,
    ) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO satisfaction_feedback(
                    created_at, generation_id, score, note, tags_json, source
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    _utc_now(),
                    generation_id,
                    score,
                    note,
                    json.dumps(tags or []),
                    source,
                ),
            )
            conn.commit()
            return int(cur.lastrowid)

    def list_feedback(self, *, limit: int = 20) -> list[FeedbackRecord]:
        limit = max(1, min(int(limit), 200))
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, created_at, generation_id, score, note, tags_json, source
                FROM satisfaction_feedback
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [_row_to_feedback(r) for r in rows]


def _row_to_generation(row: sqlite3.Row) -> GenerationRecord:
    try:
        detail = json.loads(row["detail_json"] or "{}")
    except json.JSONDecodeError:
        detail = {}
    if not isinstance(detail, dict):
        detail = {}
    return GenerationRecord(
        id=int(row["id"]),
        created_at=row["created_at"],
        prompt=row["prompt"],
        mission_type=row["mission_type"],
        theatre=row["theatre"],
        spec_path=row["spec_path"],
        miz_path=row["miz_path"],
        outcome=row["outcome"],
        detail=detail,
    )


def _row_to_feedback(row: sqlite3.Row) -> FeedbackRecord:
    try:
        tags = json.loads(row["tags_json"] or "[]")
    except json.JSONDecodeError:
        tags = []
    if not isinstance(tags, list):
        tags = []
    return FeedbackRecord(
        id=int(row["id"]),
        created_at=row["created_at"],
        generation_id=row["generation_id"],
        score=row["score"],
        note=row["note"],
        tags=tags,
        source=row["source"],
    )
