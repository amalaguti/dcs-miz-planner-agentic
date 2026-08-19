"""R13 leftover Channel shelf — remaining campaign vehicle ids."""

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
V1 = ROOT / "examples" / "manston_ground_attack_v1.yaml"
GUN = ROOT / "examples" / "manston_ground_attack_coastal_gun.yaml"

LEFTOVER_ARTILLERY = ("v1_launcher", "SK_C_28_naval_gun")
LEFTOVER_TRAIN = ("Coach a tank yellow", "Coach a tank blue", "Coach a platform")


def test_registry_resolves_r13_leftovers() -> None:
    reg = get_channel_registry()
    for uid in LEFTOVER_ARTILLERY + LEFTOVER_TRAIN:
        assert reg.get_strike_unit(uid).domain == "land"


def test_r13_leftovers_are_soft_ai() -> None:
    for uid in LEFTOVER_ARTILLERY:
        assert target_ai_class(uid, domain="land") == "soft"


def test_catalog_lists_r13_leftover_classes(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    arty = {u["unit_id"] for u in list_strike_targets(class_id="artillery", db_path=db)["units"]}
    trains = {u["unit_id"] for u in list_strike_targets(class_id="trains", db_path=db)["units"]}
    assert "v1_launcher" in arty and "SK_C_28_naval_gun" in arty
    assert "Coach a tank yellow" in trains


def test_planning_options_r13_leftover_shelves(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    by_key = {(o.family, o.id): o for o in snap.planning_options}
    arty = json.loads(by_key[("strike_target_class", "artillery")].meta_json)
    trains = json.loads(by_key[("strike_target_class", "trains")].meta_json)
    assert "v1_launcher" in arty["unit_ids"]
    assert "SK_C_28_naval_gun" in arty["unit_ids"]
    assert "Coach a tank yellow" in trains["unit_ids"]


def test_r13_leftover_examples_validate_compile(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    for path in (V1, GUN):
        spec = load_mission_spec(path)
        result = validate_mission_spec(spec, inventory=inv)
        assert result.ok, (path.name, result.errors)
        out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / f"{path.stem}.miz", voice="raf")
        assert out.is_file()
