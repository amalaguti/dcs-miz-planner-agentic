"""Channel radar_c3 shelf (#8l) — registry + catalog + example."""

from __future__ import annotations

import json
from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.catalog import CatalogService
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.target_ai import target_ai_class
from dcs_miz_planner.tools.surface import list_strike_targets
from dcs_miz_planner.validation import validate_mission_spec

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "manston_ground_attack_radar.yaml"

RADARS = ("FuMG-401", "FuSe-65")


def test_registry_resolves_radar() -> None:
    reg = get_channel_registry()
    for uid in RADARS:
        assert reg.get_strike_unit(uid).domain == "land"


def test_radar_ai_class_is_soft() -> None:
    for uid in RADARS:
        assert target_ai_class(uid, domain="land") == "soft"


def test_catalog_lists_radar_c3(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    result = list_strike_targets(class_id="radar_c3", db_path=db)
    assert result["ok"]
    ids = {u["unit_id"] for u in result["units"]}
    for uid in RADARS:
        assert uid in ids


def test_planning_options_radar_class(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    by_key = {(o.family, o.id): o for o in snap.planning_options}
    radar = json.loads(by_key[("strike_target_class", "radar_c3")].meta_json)
    assert set(RADARS) <= set(radar["unit_ids"])
    assert radar["preferred_motion"] == "static"
    assert radar["preferred_ai_preset"] == "convoy_transit"
    place = json.loads(by_key[("channel_place", "french_coast_strike_belt")].meta_json)
    assert "radar_c3" in place["related_classes"]


def test_radar_example_validate_compile(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(EXAMPLE)
    result = validate_mission_spec(spec, inventory=inv)
    assert result.ok, result.errors
    out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "radar.miz", voice="raf")
    assert out.is_file()
