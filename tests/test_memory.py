"""User memory: prefs, history, feedback; isolated from catalog sync."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from dcs_miz_planner.catalog import CatalogService
from dcs_miz_planner.memory import (
    OUTCOME_SUCCESS,
    OUTCOME_VALIDATION_FAILED,
    USER_SCHEMA_VERSION,
    UserMemoryService,
    UserMemoryStore,
)


def test_prefs_round_trip_and_partial_upsert(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    mem = UserMemoryService(db_path=db)
    assert mem.get_prefs() == {}
    mem.set_prefs({"preferred_airfield": "Manston", "preferred_aircraft": "SpitfireLFMkIX"})
    assert mem.get_prefs()["preferred_airfield"] == "Manston"
    mem.set_prefs({"preferred_weather": "sunny_clear"})
    prefs = mem.get_prefs()
    assert prefs["preferred_airfield"] == "Manston"
    assert prefs["preferred_aircraft"] == "SpitfireLFMkIX"
    assert prefs["preferred_weather"] == "sunny_clear"
    filtered = mem.get_prefs(keys=["preferred_airfield"])
    assert filtered == {"preferred_airfield": "Manston"}


def test_generation_and_feedback_round_trip(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    mem = UserMemoryService(db_path=db)
    gid = mem.record_generation(
        outcome=OUTCOME_SUCCESS,
        prompt="cold Manston free flight",
        mission_type="free_flight",
        theatre="TheChannel",
        spec_path="out/planned.yaml",
        detail={"aircraft": "SpitfireLFMkIX"},
    )
    assert gid >= 1
    rows = mem.list_generations(limit=5)
    assert len(rows) == 1
    assert rows[0].outcome == OUTCOME_SUCCESS
    assert rows[0].spec_path == "out/planned.yaml"
    assert rows[0].detail["aircraft"] == "SpitfireLFMkIX"

    fid = mem.record_feedback(
        source="cli",
        generation_id=gid,
        score=5,
        note="great sortie",
        tags=["loved_weather"],
    )
    assert fid >= 1
    feedback = mem.list_feedback(limit=5)
    assert len(feedback) == 1
    assert feedback[0].generation_id == gid
    assert feedback[0].score == 5
    assert feedback[0].note == "great sortie"


def test_catalog_sync_preserves_prefs(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    mem = UserMemoryService(db_path=db)
    mem.set_prefs({"preferred_airfield": "Manston"})
    CatalogService(db_path=db).sync()
    assert mem.get_prefs()["preferred_airfield"] == "Manston"
    snap = CatalogService(db_path=db).get_snapshot()
    assert snap is not None
    assert any(a.name == "Manston" for a in snap.airfields)


def test_user_schema_bump_leaves_catalog(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    mem = UserMemoryService(db_path=db)
    mem.set_prefs({"preferred_airfield": "Manston"})
    mem.record_generation(outcome=OUTCOME_VALIDATION_FAILED, prompt="bad")

    # Simulate an older/newer user schema stored in meta, then reopen with current code.
    with sqlite3.connect(db) as conn:
        conn.execute(
            "UPDATE user_meta SET value = ? WHERE key = 'user_schema_version'",
            ("999",),
        )
        conn.commit()

    store = UserMemoryStore(db)
    # Current USER_SCHEMA_VERSION is 1 — mismatch wipes only user_* tables.
    assert store.get_prefs() == {}
    assert store.list_generations() == []

    snap = CatalogService(db_path=db).get_snapshot()
    assert snap is not None
    assert any(a.name == "Manston" for a in snap.airfields)

    with sqlite3.connect(db) as conn:
        row = conn.execute(
            "SELECT value FROM user_meta WHERE key = 'user_schema_version'"
        ).fetchone()
        assert int(row[0]) == USER_SCHEMA_VERSION
