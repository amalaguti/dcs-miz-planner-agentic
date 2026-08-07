"""Agent catalog SQLite: sync from YAML/Spec, theatre join with install inventory."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from dcs_miz_planner.catalog import (
    CatalogService,
    build_snapshot_from_registry,
    join_theatre_views,
)
from dcs_miz_planner.cli import main
from dcs_miz_planner.install.models import (
    AvailabilityState,
    TheatreInventory,
    TheatreRecord,
)
from dcs_miz_planner.registry import AircraftRef, ChannelRegistry, WeatherPresetRef


def _tiny_registry() -> ChannelRegistry:
    return ChannelRegistry(
        airfields={"Manston": 25},
        aircraft={"SpitfireLFMkIX": AircraftRef("SpitfireLFMkIX", 124.0)},
        theatres=frozenset({"TheChannel"}),
        weather_presets={"sunny_clear": WeatherPresetRef("sunny_clear", "clear")},
        payloads={},
    )


def test_build_snapshot_includes_enums_and_registry() -> None:
    snap = build_snapshot_from_registry(
        _tiny_registry(), synced_at=datetime(2026, 7, 26, tzinfo=UTC)
    )
    assert [t.theatre_id for t in snap.theatres] == ["TheChannel"]
    assert snap.airfields[0].name == "Manston"
    assert snap.airfields[0].theatre_id == "TheChannel"
    assert {m.value for m in snap.mission_types} >= {
        "free_flight",
        "intercept",
        "cap",
        "ground_attack",
        "escort",
    }
    assert {c.value for c in snap.countries} == {"ThirdReich", "UK"}
    assert snap.source == "channel_yaml+spec_enums"


def test_sync_idempotent_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    service = CatalogService(db_path=db)
    first = service.sync(_tiny_registry())
    second = service.sync(_tiny_registry())
    loaded = service.get_snapshot()
    assert loaded is not None
    assert loaded.theatres == first.theatres == second.theatres
    assert loaded.airfields == first.airfields
    assert loaded.aircraft[0].aircraft_id == "SpitfireLFMkIX"


def test_offerable_theatre_join() -> None:
    known = frozenset({"TheChannel"})
    inventory = TheatreInventory(
        scanned_at=datetime(2026, 7, 26, tzinfo=UTC),
        dcs_roots=("C:/DCS",),
        saved_games_roots=(),
        theatres=(
            TheatreRecord(
                theatre_id="TheChannel",
                update_id="THECHANNEL_terrain",
                dcs_root="C:/DCS",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
            TheatreRecord(
                theatre_id="Normandy",
                update_id="NORMANDY_terrain",
                dcs_root="C:/DCS",
                state=AvailabilityState.AVAILABLE,
                planner_supported=False,
            ),
            TheatreRecord(
                theatre_id="Caucasus",
                update_id="CAUCASUS_terrain",
                dcs_root="C:/DCS",
                state=AvailabilityState.DISABLED,
                planner_supported=False,
            ),
        ),
    )
    views = {v.theatre_id: v for v in join_theatre_views(known, inventory)}
    assert views["TheChannel"].known is True
    assert views["TheChannel"].offerable is True
    assert views["Normandy"].known is False
    assert views["Normandy"].installed is True
    assert views["Normandy"].offerable is False
    assert views["Caucasus"].offerable is False


def test_catalog_cli_sync_and_list(tmp_path: Path) -> None:
    db = tmp_path / "planner.sqlite"
    assert main(["catalog", "sync", "--db", str(db)]) == 0
    assert main(["catalog", "list", "--type", "aircraft", "--db", str(db), "--json"]) == 0
    assert main(["catalog", "list", "--type", "mission_types", "--db", str(db)]) == 0

    # Discovered-only theatre appears when install inventory is present in same DB.
    from dcs_miz_planner.install.store import InventoryStore

    InventoryStore(db).replace(
        TheatreInventory(
            scanned_at=datetime(2026, 7, 26, tzinfo=UTC),
            dcs_roots=("C:/FakeDCS",),
            saved_games_roots=(),
            theatres=(
                TheatreRecord(
                    theatre_id="Normandy",
                    update_id="NORMANDY_terrain",
                    dcs_root="C:/FakeDCS",
                    state=AvailabilityState.AVAILABLE,
                    planner_supported=False,
                ),
            ),
        )
    )

    # Ensure known catalog still present after install write.
    CatalogService(db_path=db).ensure_synced()
    rc = main(["catalog", "list", "--type", "theatres", "--db", str(db), "--json"])
    assert rc == 0

    # known-only excludes Normandy
    import io
    import json
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        assert main(["catalog", "list", "--db", str(db), "--json"]) == 0
    payload = json.loads(buf.getvalue())
    ids = {r["theatre_id"] for r in payload["rows"]}
    assert "TheChannel" in ids
    assert "Normandy" in ids
    channel = next(r for r in payload["rows"] if r["theatre_id"] == "TheChannel")
    assert channel["known"] is True

    buf2 = io.StringIO()
    with redirect_stdout(buf2):
        assert main(["catalog", "list", "--db", str(db), "--known-only", "--json"]) == 0
    known_only = json.loads(buf2.getvalue())
    assert {r["theatre_id"] for r in known_only["rows"]} == {"TheChannel"}


def test_packaged_sync_matches_channel_registry(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    assert "TheChannel" in {t.theatre_id for t in snap.theatres}
    assert "Manston" in {a.name for a in snap.airfields}
    assert "SpitfireLFMkIX" in {a.aircraft_id for a in snap.aircraft}
    assert "sunny_clear" in {w.name for w in snap.weather_presets}
    assert "dawn_clear" in {w.name for w in snap.weather_presets}
    assert "marginal_vfr" in {w.name for w in snap.weather_presets}
    by_key = {(o.family, o.id): o for o in snap.planning_options}
    assert by_key[("weather", "sunny_clear")].support == "supported"
    assert by_key[("weather", "dawn_clear")].support == "supported"
    assert by_key[("weather", "marginal_vfr")].support == "supported"
    assert by_key[("start_type", "cold_parking")].support == "supported"
    assert by_key[("time_of_day", "dawn")].support == "advisory"
    assert by_key[("roe_seed", "weapons_free")].support == "supported"
    assert by_key[("roe_seed", "weapons_hold")].support == "supported"
    assert by_key[("mission_type", "cap")].support == "supported"
    assert by_key[("randomization", "seeded_reroll")].support == "advisory"


def test_schema_bump_clears_synced_at_so_ensure_resyncs(tmp_path: Path) -> None:
    """After catalog_schema_version changes, empty tables must not look 'already synced'."""
    import sqlite3

    from dcs_miz_planner.catalog.store import CATALOG_SCHEMA_VERSION, CatalogStore

    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    store = CatalogStore(db)
    assert store.has_catalog() is True

    with sqlite3.connect(db) as conn:
        conn.execute(
            "UPDATE catalog_meta SET value = ? WHERE key = 'catalog_schema_version'",
            (str(CATALOG_SCHEMA_VERSION - 1),),
        )
        conn.commit()

    # Opening with the current schema version wipes rows and clears synced_at.
    assert store.has_catalog() is False
    snap = CatalogService(db_path=db).ensure_synced()
    assert len(snap.airfields) > 0
    assert len(snap.planning_options) > 0

    import io
    import json
    from contextlib import redirect_stdout

    db = tmp_path / "inventory.sqlite"
    assert main(["catalog", "sync", "--db", str(db)]) == 0

    service = CatalogService(db_path=db)
    weather = service.list_rows("planning_options", family="weather", support="supported")
    assert {r["id"] for r in weather} >= {
        "sunny_clear",
        "dawn_clear",
        "marginal_vfr",
        "broken_channel",
        "rain_overcast",
        "showers_scattered",
    }

    behaviours = service.list_rows(
        "planning_options", family="mission_behaviour", support="supported"
    )
    behaviour_ids = {r["id"] for r in behaviours}
    assert "altitude_speed_gates" in behaviour_ids
    assert "mark_smoke" in behaviour_ids

    inspirations = service.list_rows("planning_options", family="mission_inspiration")
    assert any(r["id"] == "low_level_channel_hop" for r in inspirations)

    dynamics = service.list_rows("planning_options", family="dynamics_mode")
    assert {r["id"] for r in dynamics} >= {"fixed", "live", "choose", "hybrid"}
    strikes = service.list_rows("planning_options", family="strike_target_class")
    assert any(r["id"] == "soft_vehicles" for r in strikes)
    places = service.list_rows("planning_options", family="channel_place")
    assert any(r["id"] == "manston_home" for r in places)

    buf = io.StringIO()
    with redirect_stdout(buf):
        assert (
            main(
                [
                    "catalog",
                    "list",
                    "--type",
                    "planning_options",
                    "--family",
                    "weather",
                    "--support",
                    "supported",
                    "--db",
                    str(db),
                    "--json",
                ]
            )
            == 0
        )
    payload = json.loads(buf.getvalue())
    assert {r["id"] for r in payload["rows"]} >= {"sunny_clear", "dawn_clear", "marginal_vfr"}
    assert all(r["support"] == "supported" for r in payload["rows"])

    first = CatalogService(db_path=db).sync()
    second = CatalogService(db_path=db).sync()
    assert {(o.family, o.id, o.support) for o in first.planning_options} == {
        (o.family, o.id, o.support) for o in second.planning_options
    }
