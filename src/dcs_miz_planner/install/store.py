"""SQLite persistence for the user-local theatre inventory."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

from .models import AvailabilityState, Diagnostic, TheatreInventory, TheatreRecord

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS scan_meta (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    scanned_at TEXT NOT NULL,
    dcs_roots TEXT NOT NULL,
    saved_games_roots TEXT NOT NULL,
    diagnostics TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS theatres (
    theatre_id TEXT NOT NULL,
    update_id TEXT,
    dcs_root TEXT NOT NULL,
    state TEXT NOT NULL,
    planner_supported INTEGER NOT NULL,
    terrain_path TEXT,
    saved_games_root TEXT,
    evidence TEXT NOT NULL,
    PRIMARY KEY (theatre_id, dcs_root)
);
"""


def default_db_path(*, env: dict[str, str] | None = None) -> Path:
    env = env if env is not None else os.environ
    override = env.get("DCS_MIZ_INVENTORY_DB")
    if override:
        return Path(override).expanduser()
    local = env.get("LOCALAPPDATA")
    if local:
        return Path(local) / "dcs-miz-planner" / "inventory.sqlite"
    return Path.home() / ".local" / "share" / "dcs-miz-planner" / "inventory.sqlite"


class InventoryStore:
    """Read/write theatre inventory rows in SQLite."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.executescript(_SCHEMA)
        row = conn.execute("SELECT value FROM meta WHERE key = 'schema_version'").fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO meta(key, value) VALUES ('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
            conn.commit()
        elif int(row["value"]) != SCHEMA_VERSION:
            # Incompatible: recreate theatre tables on next replace.
            conn.execute("DELETE FROM theatres")
            conn.execute("DELETE FROM scan_meta")
            conn.execute(
                "UPDATE meta SET value = ? WHERE key = 'schema_version'",
                (str(SCHEMA_VERSION),),
            )
            conn.commit()
        return conn

    def has_inventory(self) -> bool:
        if not self.db_path.is_file():
            return False
        with self._connect() as conn:
            row = conn.execute("SELECT 1 FROM scan_meta WHERE id = 1").fetchone()
            return row is not None

    def load(self) -> TheatreInventory | None:
        if not self.has_inventory():
            return None
        with self._connect() as conn:
            meta = conn.execute("SELECT * FROM scan_meta WHERE id = 1").fetchone()
            if meta is None:
                return None
            rows = conn.execute("SELECT * FROM theatres ORDER BY theatre_id, dcs_root").fetchall()

        diagnostics = [
            Diagnostic(**d) if isinstance(d, dict) else Diagnostic(str(d))
            for d in json.loads(meta["diagnostics"])
        ]
        theatres = [
            TheatreRecord(
                theatre_id=row["theatre_id"],
                update_id=row["update_id"],
                dcs_root=row["dcs_root"],
                state=AvailabilityState(row["state"]),
                planner_supported=bool(row["planner_supported"]),
                terrain_path=row["terrain_path"],
                saved_games_root=row["saved_games_root"],
                evidence=tuple(json.loads(row["evidence"])),
            )
            for row in rows
        ]
        return TheatreInventory(
            scanned_at=datetime.fromisoformat(meta["scanned_at"]),
            dcs_roots=tuple(json.loads(meta["dcs_roots"])),
            saved_games_roots=tuple(json.loads(meta["saved_games_roots"])),
            theatres=tuple(theatres),
            diagnostics=tuple(diagnostics),
            from_cache=True,
        )

    def replace(self, inventory: TheatreInventory) -> None:
        diagnostics = [{"message": d.message, "source": d.source} for d in inventory.diagnostics]
        with self._connect() as conn:
            conn.execute("DELETE FROM theatres")
            conn.execute("DELETE FROM scan_meta")
            conn.execute(
                """
                INSERT INTO scan_meta(id, scanned_at, dcs_roots, saved_games_roots, diagnostics)
                VALUES (1, ?, ?, ?, ?)
                """,
                (
                    inventory.scanned_at.isoformat(),
                    json.dumps(list(inventory.dcs_roots)),
                    json.dumps(list(inventory.saved_games_roots)),
                    json.dumps(diagnostics),
                ),
            )
            conn.executemany(
                """
                INSERT INTO theatres(
                    theatre_id, update_id, dcs_root, state, planner_supported,
                    terrain_path, saved_games_root, evidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        t.theatre_id,
                        t.update_id,
                        t.dcs_root,
                        t.state.value,
                        1 if t.planner_supported else 0,
                        t.terrain_path,
                        t.saved_games_root,
                        json.dumps(list(t.evidence)),
                    )
                    for t in inventory.theatres
                ],
            )
            conn.commit()
