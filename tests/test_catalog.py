"""Agent catalog SQLite: sync from YAML/Spec, theatre join with install inventory."""

from __future__ import annotations

import json
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
        "recon",
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


def test_offerable_normandy_when_known() -> None:
    known = frozenset({"TheChannel", "Normandy"})
    inventory = TheatreInventory(
        scanned_at=datetime(2026, 7, 26, tzinfo=UTC),
        dcs_roots=("C:/DCS",),
        saved_games_roots=(),
        theatres=(
            TheatreRecord(
                theatre_id="Normandy",
                update_id="NORMANDY_terrain",
                dcs_root="C:/DCS",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
        ),
    )
    views = {v.theatre_id: v for v in join_theatre_views(known, inventory)}
    assert views["Normandy"].known is True
    assert views["Normandy"].offerable is True


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
    normandy = next(r for r in payload["rows"] if r["theatre_id"] == "Normandy")
    assert normandy["known"] is True

    buf2 = io.StringIO()
    with redirect_stdout(buf2):
        assert main(["catalog", "list", "--db", str(db), "--known-only", "--json"]) == 0
    known_only = json.loads(buf2.getvalue())
    assert {r["theatre_id"] for r in known_only["rows"]} == {
        "TheChannel",
        "Normandy",
        "Caucasus",
        "Syria",
        "Nevada",
        "Falklands",
        "Kola",
    }


def test_packaged_sync_matches_channel_registry(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    assert "TheChannel" in {t.theatre_id for t in snap.theatres}
    assert "Normandy" in {t.theatre_id for t in snap.theatres}
    assert "Caucasus" in {t.theatre_id for t in snap.theatres}
    assert "Syria" in {t.theatre_id for t in snap.theatres}
    assert "Nevada" in {t.theatre_id for t in snap.theatres}
    assert "Falklands" in {t.theatre_id for t in snap.theatres}
    assert "Kola" in {t.theatre_id for t in snap.theatres}
    assert "Manston" in {a.name for a in snap.airfields}
    assert "NeedsOarPoint" in {a.name for a in snap.airfields}
    assert "Batumi" in {a.name for a in snap.airfields}
    assert "Mozdok" in {a.name for a in snap.airfields}
    assert "Incirlik" in {a.name for a in snap.airfields}
    assert "Nellis" in {a.name for a in snap.airfields}
    assert "GroomLake" in {a.name for a in snap.airfields}
    assert "MountPleasant" in {a.name for a in snap.airfields}
    assert "RioGallegos" in {a.name for a in snap.airfields}
    assert "PortStanley" in {a.name for a in snap.airfields}
    by_af = {a.name: a for a in snap.airfields}
    assert by_af["Manston"].theatre_id == "TheChannel"
    assert by_af["NeedsOarPoint"].theatre_id == "Normandy"
    assert by_af["NeedsOarPoint"].airdrome_id == 28
    assert by_af["Batumi"].theatre_id == "Caucasus"
    assert by_af["Batumi"].airdrome_id == 22
    assert by_af["Mozdok"].theatre_id == "Caucasus"
    assert by_af["Mozdok"].airdrome_id == 28
    assert by_af["Incirlik"].theatre_id == "Syria"
    assert by_af["Incirlik"].airdrome_id == 16
    assert by_af["Palmyra"].theatre_id == "Syria"
    assert by_af["Palmyra"].airdrome_id == 28
    assert "Syria" in {c.value for c in snap.countries}
    assert by_af["Nellis"].theatre_id == "Nevada"
    assert by_af["Nellis"].airdrome_id == 4
    assert by_af["GroomLake"].theatre_id == "Nevada"
    assert by_af["GroomLake"].airdrome_id == 2
    assert by_af["MountPleasant"].theatre_id == "Falklands"
    assert by_af["MountPleasant"].airdrome_id == 2
    assert by_af["RioGallegos"].theatre_id == "Falklands"
    assert by_af["RioGallegos"].airdrome_id == 5
    assert by_af["Bodo"].theatre_id == "Kola"
    assert by_af["Bodo"].airdrome_id == 7
    assert "Norway" in {c.value for c in snap.countries}
    assert "Argentina" in {c.value for c in snap.countries}
    assert by_af["FordAF"].theatre_id == "Normandy"
    assert by_af["FordAF"].airdrome_id == 31
    assert "SpitfireLFMkIX" in {a.aircraft_id for a in snap.aircraft}
    assert "Su-25T" in {a.aircraft_id for a in snap.aircraft}
    assert "Russia" in {c.value for c in snap.countries}
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
    by_unit = {u.unit_id: u for u in snap.strike_units}
    assert by_unit["Uboat_VIIC"].domain == "sea"
    assert by_unit["Blitz_36-6700A"].domain == "land"
    uboat_classes = json.loads(by_unit["Uboat_VIIC"].class_ids_json)
    assert "sea_craft" in uboat_classes
    assert "soft_vehicles" in json.loads(by_unit["Blitz_36-6700A"].class_ids_json)
    assert "aaa_guns" in json.loads(by_unit["flak18"].class_ids_json)


def test_invent_heuristic_meta_after_sync(tmp_path: Path) -> None:
    """#8d: preferred_motion / preferred_ai_preset cue mapping in planning_options."""
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    by_key = {(o.family, o.id): o for o in snap.planning_options}

    soft = json.loads(by_key[("strike_target_class", "soft_vehicles")].meta_json)
    assert soft["preferred_motion"] == "path"
    assert soft["preferred_ai_preset"] == "convoy_transit"

    aaa = json.loads(by_key[("strike_target_class", "aaa_guns")].meta_json)
    assert aaa["preferred_motion"] == "static"
    assert aaa["preferred_ai_preset"] == "aaa_alert"

    sea = json.loads(by_key[("strike_target_class", "sea_craft")].meta_json)
    assert sea["preferred_motion"] == "patrol"
    assert sea["preferred_ai_preset"] == "ship_under_way"
    assert sea["harbour_ai_preset"] == "harbour_static"
    assert sea["harbour_motion"] == "static"

    assert (
        json.loads(by_key[("ground_ai_preset", "convoy_transit")].meta_json)["preferred_motion"]
        == "path"
    )
    assert (
        json.loads(by_key[("ground_ai_preset", "aaa_alert")].meta_json)["preferred_motion"]
        == "static"
    )
    assert (
        json.loads(by_key[("ground_ai_preset", "ship_under_way")].meta_json)["preferred_motion"]
        == "patrol"
    )
    assert (
        json.loads(by_key[("ground_ai_preset", "harbour_static")].meta_json)["preferred_motion"]
        == "static"
    )

    mid = json.loads(by_key[("channel_place", "mid_channel_shipping")].meta_json)
    assert mid["preferred_ai_preset"] == "ship_under_way"
    assert mid["preferred_motion"] == "patrol"


def test_channel_place_geometry_recipes_after_sync(tmp_path: Path) -> None:
    """#8f: numeric Manston-relative recipes on channel_place cards."""
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    by_key = {(o.family, o.id): o for o in snap.planning_options}

    inland = json.loads(by_key[("channel_place", "french_coast_strike_belt")].meta_json)
    assert inland["strike_bearing_deg"] == 125
    assert inland["strike_distance_km"] == 76
    assert inland["domain"] == "land"
    assert isinstance(inland.get("path_point_deltas"), list)
    assert len(inland["path_point_deltas"]) >= 2

    mid = json.loads(by_key[("channel_place", "mid_channel_shipping")].meta_json)
    assert mid["strike_bearing_deg"] == 140
    assert mid["strike_distance_km"] == 40
    assert mid["domain"] == "sea"

    harbour = json.loads(by_key[("channel_place", "coastal_harbour")].meta_json)
    assert harbour["strike_bearing_deg"] == 120
    assert harbour["strike_distance_km"] == 68
    assert harbour["preferred_ai_preset"] == "harbour_static"
    assert harbour["domain"] == "sea"
    assert harbour.get("sea_units_only") is True


def test_catalog_list_strike_units_cli(tmp_path: Path) -> None:
    import io
    from contextlib import redirect_stdout

    db = tmp_path / "planner.sqlite"
    assert main(["catalog", "sync", "--db", str(db)]) == 0
    buf = io.StringIO()
    with redirect_stdout(buf):
        assert main(["catalog", "list", "--type", "strike_units", "--db", str(db), "--json"]) == 0
    payload = json.loads(buf.getvalue())
    ids = {r["unit_id"] for r in payload["rows"]}
    assert "Uboat_VIIC" in ids
    assert "Blitz_36-6700A" in ids
    uboat = next(r for r in payload["rows"] if r["unit_id"] == "Uboat_VIIC")
    assert uboat["domain"] == "sea"
    assert "sea_craft" in uboat["class_ids"]


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
