"""R13 Channel shelf promote — registry + catalog + examples."""

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
FLAK41 = ROOT / "examples" / "manston_ground_attack_flak41.yaml"
LST = ROOT / "examples" / "manston_ground_attack_lst.yaml"

NEW_AAA = ("flak41", "M45_Quadmount", "QF_37_AA", "Allies_Director")
NEW_ARMOR = ("Tiger_I", "SturmPzIV", "Pz_V_Panther_G", "JagdPz_IV", "Jagdpanther_G1")
NEW_TRAIN = ("Coach cargo", "Coach cargo open")
NEW_SEA = ("LST_Mk2", "USS_Samuel_Chase")


def test_registry_resolves_r13_units() -> None:
    reg = get_channel_registry()
    for uid in NEW_AAA + NEW_ARMOR + NEW_TRAIN:
        assert reg.get_strike_unit(uid).domain == "land"
    for uid in NEW_SEA:
        assert reg.get_strike_unit(uid).domain == "sea"


def test_r13_aaa_ai_class() -> None:
    for uid in NEW_AAA:
        assert target_ai_class(uid, domain="land") == "aaa"
    assert target_ai_class("Tiger_I", domain="land") == "soft"


def test_catalog_lists_r13_classes(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    aaa = {u["unit_id"] for u in list_strike_targets(class_id="aaa_guns", db_path=db)["units"]}
    armor = {u["unit_id"] for u in list_strike_targets(class_id="armor", db_path=db)["units"]}
    trains = {u["unit_id"] for u in list_strike_targets(class_id="trains", db_path=db)["units"]}
    sea = {u["unit_id"] for u in list_strike_targets(class_id="sea_craft", db_path=db)["units"]}
    assert "flak41" in aaa and "M45_Quadmount" in aaa
    assert "Tiger_I" in armor and "Pz_V_Panther_G" in armor
    assert "Coach cargo" in trains
    assert "LST_Mk2" in sea and "USS_Samuel_Chase" in sea


def test_planning_options_r13_shelves(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    by_key = {(o.family, o.id): o for o in snap.planning_options}
    aaa = json.loads(by_key[("strike_target_class", "aaa_guns")].meta_json)
    sea = json.loads(by_key[("strike_target_class", "sea_craft")].meta_json)
    assert "flak41" in aaa["unit_ids"]
    assert "LST_Mk2" in sea["ship_ids"]


def test_r13_examples_validate_compile(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    for path in (FLAK41, LST):
        spec = load_mission_spec(path)
        result = validate_mission_spec(spec, inventory=inv)
        assert result.ok, (path.name, result.errors)
        out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / f"{path.stem}.miz", voice="raf")
        assert out.is_file()
