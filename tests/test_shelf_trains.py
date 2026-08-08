"""Channel trains shelf (#8m) — registry + rail corridor place + example."""

from __future__ import annotations

import json
from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.catalog import CatalogService
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.target_ai import target_ai_class
from dcs_miz_planner.target_motion import speed_profile_for_unit
from dcs_miz_planner.tools.surface import list_strike_targets
from dcs_miz_planner.validation import validate_mission_spec

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "manston_ground_attack_train.yaml"

TRAINS = (
    "Locomotive",
    "German_covered_wagon_G10",
    "German_tank_wagon",
    "DR_50Ton_Flat_Wagon",
)


def test_registry_resolves_trains() -> None:
    reg = get_channel_registry()
    for uid in TRAINS:
        assert reg.get_strike_unit(uid).domain == "land"


def test_trains_ai_class_is_soft() -> None:
    for uid in TRAINS:
        assert target_ai_class(uid, domain="land") == "soft"


def test_train_motion_profile() -> None:
    for uid in TRAINS:
        profile = speed_profile_for_unit(uid, domain="land")
        assert profile.id == "train"
        assert profile.min_kmh == 25
        assert profile.max_kmh == 55


def test_catalog_lists_trains(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    result = list_strike_targets(class_id="trains", db_path=db)
    assert result["ok"]
    ids = {u["unit_id"] for u in result["units"]}
    for uid in TRAINS:
        assert uid in ids


def test_planning_options_trains_and_rail_corridor(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    by_key = {(o.family, o.id): o for o in snap.planning_options}
    trains = json.loads(by_key[("strike_target_class", "trains")].meta_json)
    assert set(TRAINS) <= set(trains["unit_ids"])
    assert trains["preferred_motion"] == "path"
    assert trains["preferred_place"] == "french_coast_rail_corridor"
    place = json.loads(by_key[("channel_place", "french_coast_rail_corridor")].meta_json)
    assert "trains" in place["related_classes"]
    assert place["path_point_deltas"]
    assert place["strike_bearing_deg"] == 125
    assert place["strike_distance_km"] == 76


def test_train_example_validate_compile(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(EXAMPLE)
    result = validate_mission_spec(spec, inventory=inv)
    assert result.ok, result.errors
    out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "train.miz", voice="raf")
    assert out.is_file()
