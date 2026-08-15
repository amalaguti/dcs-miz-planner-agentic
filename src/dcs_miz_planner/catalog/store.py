"""SQLite persistence for known agent catalog tables."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from .models import (
    CatalogAircraft,
    CatalogAirfield,
    CatalogEnumRow,
    CatalogPayload,
    CatalogPlanningOption,
    CatalogSnapshot,
    CatalogStrikeUnit,
    CatalogTheatre,
    CatalogWeatherPreset,
)

CATALOG_SCHEMA_VERSION = 6

_SCHEMA = """
CREATE TABLE IF NOT EXISTS catalog_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS catalog_theatres (
    theatre_id TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS catalog_airfields (
    name TEXT PRIMARY KEY,
    airdrome_id INTEGER NOT NULL,
    theatre_id TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS catalog_aircraft (
    aircraft_id TEXT PRIMARY KEY,
    radio_mhz REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS catalog_weather_presets (
    name TEXT PRIMARY KEY,
    description TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS catalog_payloads (
    name TEXT PRIMARY KEY,
    meta_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS catalog_planning_options (
    family TEXT NOT NULL,
    id TEXT NOT NULL,
    label TEXT NOT NULL,
    description TEXT NOT NULL,
    support TEXT NOT NULL,
    meta_json TEXT NOT NULL,
    PRIMARY KEY (family, id)
);
CREATE TABLE IF NOT EXISTS catalog_strike_units (
    unit_id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    domain TEXT NOT NULL,
    theatre_id TEXT NOT NULL,
    era_id TEXT NOT NULL,
    class_ids_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS catalog_mission_types (
    value TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS catalog_start_types (
    value TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS catalog_coalitions (
    value TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS catalog_objective_types (
    value TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS catalog_countries (
    value TEXT PRIMARY KEY
);
"""

_KNOWN_TABLES = (
    "catalog_theatres",
    "catalog_airfields",
    "catalog_aircraft",
    "catalog_weather_presets",
    "catalog_payloads",
    "catalog_planning_options",
    "catalog_strike_units",
    "catalog_mission_types",
    "catalog_start_types",
    "catalog_coalitions",
    "catalog_objective_types",
    "catalog_countries",
)


class CatalogStore:
    """Read/write known catalog rows (shares DB file with install inventory)."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.executescript(_SCHEMA)
        row = conn.execute(
            "SELECT value FROM catalog_meta WHERE key = 'catalog_schema_version'"
        ).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO catalog_meta(key, value) VALUES ('catalog_schema_version', ?)",
                (str(CATALOG_SCHEMA_VERSION),),
            )
            conn.commit()
        elif int(row["value"]) != CATALOG_SCHEMA_VERSION:
            for table in _KNOWN_TABLES:
                conn.execute(f"DROP TABLE IF EXISTS {table}")
            conn.executescript(_SCHEMA)
            conn.execute(
                "UPDATE catalog_meta SET value = ? WHERE key = 'catalog_schema_version'",
                (str(CATALOG_SCHEMA_VERSION),),
            )
            # Force ensure_synced() to rebuild from packaged YAML after a schema bump.
            conn.execute("DELETE FROM catalog_meta WHERE key IN ('synced_at', 'source')")
            conn.commit()
        return conn

    def has_catalog(self) -> bool:
        if not self.db_path.is_file():
            return False
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM catalog_meta WHERE key = 'synced_at'").fetchone()
            return row is not None

    def replace_snapshot(self, snapshot: CatalogSnapshot) -> None:
        with self._connect() as conn:
            for table in _KNOWN_TABLES:
                conn.execute(f"DELETE FROM {table}")
            conn.executemany(
                "INSERT INTO catalog_theatres(theatre_id) VALUES (?)",
                [(t.theatre_id,) for t in snapshot.theatres],
            )
            conn.executemany(
                "INSERT INTO catalog_airfields(name, airdrome_id, theatre_id) VALUES (?, ?, ?)",
                [(a.name, a.airdrome_id, a.theatre_id) for a in snapshot.airfields],
            )
            conn.executemany(
                "INSERT INTO catalog_aircraft(aircraft_id, radio_mhz) VALUES (?, ?)",
                [(a.aircraft_id, a.radio_mhz) for a in snapshot.aircraft],
            )
            conn.executemany(
                "INSERT INTO catalog_weather_presets(name, description) VALUES (?, ?)",
                [(w.name, w.description) for w in snapshot.weather_presets],
            )
            conn.executemany(
                "INSERT INTO catalog_payloads(name, meta_json) VALUES (?, ?)",
                [(p.name, p.meta_json) for p in snapshot.payloads],
            )
            conn.executemany(
                "INSERT INTO catalog_planning_options"
                "(family, id, label, description, support, meta_json) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (o.family, o.id, o.label, o.description, o.support, o.meta_json)
                    for o in snapshot.planning_options
                ],
            )
            conn.executemany(
                "INSERT INTO catalog_strike_units"
                "(unit_id, label, domain, theatre_id, era_id, class_ids_json) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (
                        u.unit_id,
                        u.label,
                        u.domain,
                        u.theatre_id,
                        u.era_id,
                        u.class_ids_json,
                    )
                    for u in snapshot.strike_units
                ],
            )
            for table, rows in (
                ("catalog_mission_types", snapshot.mission_types),
                ("catalog_start_types", snapshot.start_types),
                ("catalog_coalitions", snapshot.coalitions),
                ("catalog_objective_types", snapshot.objective_types),
                ("catalog_countries", snapshot.countries),
            ):
                conn.executemany(
                    f"INSERT INTO {table}(value) VALUES (?)",
                    [(r.value,) for r in rows],
                )
            conn.execute(
                "INSERT INTO catalog_meta(key, value) VALUES ('synced_at', ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (snapshot.synced_at.isoformat(),),
            )
            conn.execute(
                "INSERT INTO catalog_meta(key, value) VALUES ('source', ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (snapshot.source,),
            )
            conn.commit()

    def load_snapshot(self) -> CatalogSnapshot | None:
        if not self.has_catalog():
            return None
        with self._connect() as conn:
            synced = conn.execute(
                "SELECT value FROM catalog_meta WHERE key = 'synced_at'"
            ).fetchone()
            source = conn.execute("SELECT value FROM catalog_meta WHERE key = 'source'").fetchone()
            theatres = tuple(
                CatalogTheatre(row["theatre_id"])
                for row in conn.execute(
                    "SELECT theatre_id FROM catalog_theatres ORDER BY theatre_id"
                )
            )
            airfields = tuple(
                CatalogAirfield(row["name"], row["airdrome_id"], row["theatre_id"])
                for row in conn.execute(
                    "SELECT name, airdrome_id, theatre_id FROM catalog_airfields ORDER BY name"
                )
            )
            aircraft = tuple(
                CatalogAircraft(row["aircraft_id"], float(row["radio_mhz"]))
                for row in conn.execute(
                    "SELECT aircraft_id, radio_mhz FROM catalog_aircraft ORDER BY aircraft_id"
                )
            )
            weather = tuple(
                CatalogWeatherPreset(row["name"], row["description"])
                for row in conn.execute(
                    "SELECT name, description FROM catalog_weather_presets ORDER BY name"
                )
            )
            payloads = tuple(
                CatalogPayload(row["name"], row["meta_json"])
                for row in conn.execute(
                    "SELECT name, meta_json FROM catalog_payloads ORDER BY name"
                )
            )
            planning_options = tuple(
                CatalogPlanningOption(
                    row["family"],
                    row["id"],
                    row["label"],
                    row["description"],
                    row["support"],
                    row["meta_json"],
                )
                for row in conn.execute(
                    "SELECT family, id, label, description, support, meta_json "
                    "FROM catalog_planning_options ORDER BY family, id"
                )
            )
            strike_units = tuple(
                CatalogStrikeUnit(
                    row["unit_id"],
                    row["label"],
                    row["domain"],
                    row["theatre_id"],
                    row["era_id"],
                    row["class_ids_json"],
                )
                for row in conn.execute(
                    "SELECT unit_id, label, domain, theatre_id, era_id, class_ids_json "
                    "FROM catalog_strike_units ORDER BY unit_id"
                )
            )

            def enum_rows(table: str) -> tuple[CatalogEnumRow, ...]:
                return tuple(
                    CatalogEnumRow(row["value"])
                    for row in conn.execute(f"SELECT value FROM {table} ORDER BY value")
                )

            return CatalogSnapshot(
                synced_at=datetime.fromisoformat(synced["value"]),
                source=source["value"] if source else "unknown",
                theatres=theatres,
                airfields=airfields,
                aircraft=aircraft,
                weather_presets=weather,
                payloads=payloads,
                planning_options=planning_options,
                strike_units=strike_units,
                mission_types=enum_rows("catalog_mission_types"),
                start_types=enum_rows("catalog_start_types"),
                coalitions=enum_rows("catalog_coalitions"),
                objective_types=enum_rows("catalog_objective_types"),
                countries=enum_rows("catalog_countries"),
            )
