"""Channel unit shelf expand (#8e batch) — registry + catalog + examples."""

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
FLAK_BATTERY = ROOT / "examples" / "manston_ground_attack_flak_battery.yaml"
HARBOUR = ROOT / "examples" / "manston_ground_attack_harbour.yaml"

NEW_SOFT = ("Sd_Kfz_2", "Horch_901_typ_40_kfz_21", "Willys_MB")
NEW_AAA = (
    "flak30",
    "flak37",
    "flak38",
    "Flakscheinwerfer_37",
    "KDO_Mod40",
    "bofors40",
)
NEW_SEA = ("Dry-cargo ship-2", "HarborTug", "Higgins_boat")


def test_registry_resolves_expanded_units() -> None:
    reg = get_channel_registry()
    for uid in NEW_SOFT + NEW_AAA:
        assert reg.get_strike_unit(uid).domain == "land"
    for uid in NEW_SEA:
        assert reg.get_strike_unit(uid).domain == "sea"


def test_aaa_ai_class_includes_new_flak_ids() -> None:
    for uid in NEW_AAA:
        assert target_ai_class(uid, domain="land") == "aaa"
    assert target_ai_class("Sd_Kfz_2", domain="land") == "soft"


def test_catalog_lists_expanded_strike_units(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    sea = list_strike_targets(domain="sea", db_path=db)
    assert sea["ok"]
    sea_ids = {u["unit_id"] for u in sea["units"]}
    assert "HarborTug" in sea_ids
    assert "Dry-cargo ship-2" in sea_ids

    aaa = list_strike_targets(class_id="aaa_guns", db_path=db)
    assert aaa["ok"]
    aaa_ids = {u["unit_id"] for u in aaa["units"]}
    assert "flak38" in aaa_ids
    assert "Flakscheinwerfer_37" in aaa_ids

    soft = list_strike_targets(class_id="soft_vehicles", db_path=db)
    soft_ids = {u["unit_id"] for u in soft["units"]}
    assert "Sd_Kfz_2" in soft_ids


def test_planning_options_class_shelves_list_new_ids(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    by_key = {(o.family, o.id): o for o in snap.planning_options}
    soft = json.loads(by_key[("strike_target_class", "soft_vehicles")].meta_json)
    aaa = json.loads(by_key[("strike_target_class", "aaa_guns")].meta_json)
    sea = json.loads(by_key[("strike_target_class", "sea_craft")].meta_json)
    assert "Sd_Kfz_2" in soft["unit_ids"]
    assert "flak38" in aaa["unit_ids"]
    assert "HarborTug" in sea["ship_ids"]


def test_flak_battery_and_harbour_examples_validate_compile(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    for path in (FLAK_BATTERY, HARBOUR):
        spec = load_mission_spec(path)
        result = validate_mission_spec(spec, inventory=inv)
        assert result.ok, (path.name, result.errors)
        out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / f"{path.stem}.miz", voice="raf")
        assert out.is_file()
