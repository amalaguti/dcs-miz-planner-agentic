"""M8 Spitfire-era planning capacity: USA/P-51, extra homes, artillery, scenery, recon narrative."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.agent.spec_schema import build_spec_schema, infer_theatre
from dcs_miz_planner.allowlists import known_countries
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.narrative import apply_narrative
from dcs_miz_planner.recon import expand_recon_find_pack
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.validation import validate_mission_spec

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "examples"


def _inv():
    return channel_available_inventory()


def test_wwii_countries_include_usa() -> None:
    assert known_countries(era="wwii") == frozenset({"UK", "ThirdReich", "USA"})
    assert "P-51D" in get_channel_registry().list_aircraft(era="wwii")
    assert get_channel_registry().radio_mhz("P-51D") == 124.0
    payload = get_channel_registry().get_payload("p51d_2x_anm64")
    assert payload.aircraft == "P-51D"
    assert {p.pylon for p in payload.pylons} == {4, 7}


def test_channel_accepts_usa_and_p51() -> None:
    spec = load_mission_spec(EX / "manston_p51_freeflight.yaml")
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    ga = load_mission_spec(EX / "manston_p51_ground_attack.yaml")
    ga_result = validate_mission_spec(ga, inventory=_inv())
    assert ga_result.ok, ga_result.errors


def test_channel_still_rejects_georgia() -> None:
    spec = load_mission_spec(EX / "manston_cold_freeflight.yaml")
    spec = spec.model_copy(update={"player": spec.player.model_copy(update={"country": "Georgia"})})
    result = validate_mission_spec(spec, inventory=_inv())
    assert not result.ok
    assert any(e.code == "unknown_country" for e in result.errors)


def test_artillery_shelf_and_example() -> None:
    registry = get_channel_registry()
    for uid in ("LeFH_18-40-105", "Wespe124", "M2A1-105"):
        assert uid in registry.list_ground_units()
    classes = [o for o in registry.list_planning_options() if o.family == "strike_target_class"]
    artillery = next(o for o in classes if o.id == "artillery")
    assert "LeFH_18-40-105" in artillery.meta["unit_ids"]
    spec = load_mission_spec(EX / "manston_ground_attack_artillery.yaml")
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors


def test_extra_home_examples_validate() -> None:
    for name in (
        "hawkinge_cold_freeflight.yaml",
        "hawkinge_cap.yaml",
        "hawkinge_freeflight_pair.yaml",
        "chailey_cold_freeflight.yaml",
    ):
        spec = load_mission_spec(EX / name)
        result = validate_mission_spec(spec, inventory=_inv())
        assert result.ok, (name, result.errors)


def test_infer_theatre_extra_homes() -> None:
    assert infer_theatre('{"player": {"airfield": "Chailey"}}') == "Normandy"
    assert infer_theatre('{"player": {"airfield": "Hawkinge"}}') is None


def test_schema_mentions_extra_homes_and_pair() -> None:
    notes = " ".join(build_spec_schema("free_flight", theatre="TheChannel").notes)
    assert "Hawkinge" in notes
    assert "P-51D" in notes
    assert "size 2" in notes
    ny = " ".join(build_spec_schema("free_flight", theatre="Normandy").notes)
    assert "Chailey" in ny


def test_extra_home_place_recipes_are_not_manston_copies() -> None:
    by_id = {o.id: o for o in get_channel_registry().list_planning_options()}
    hawkinge = by_id["hawkinge_home"].meta
    assert hawkinge["airfield"] == "Hawkinge"
    assert hawkinge["cap_bearing_deg"] == 76
    assert hawkinge["strike_bearing_deg"] == 104
    assert hawkinge["max_flight_size"] == 4
    detling = by_id["detling_home"].meta
    assert detling["cap_bearing_deg"] == 102
    assert detling["strike_distance_km"] == 122
    biggin = by_id["biggin_hill_home"].meta
    assert biggin["airfield"] == "BigginHill"
    assert biggin["cap_distance_km"] == 111
    chailey = by_id["chailey_home"].meta
    assert chailey["airfield"] == "Chailey"
    assert chailey["cap_bearing_deg"] == 228
    tangmere = by_id["tangmere_home"].meta
    assert tangmere["max_flight_size"] == 3
    ford = by_id["ford_af_home"].meta
    assert ford["airfield"] == "FordAF"
    assert ford["cap_bearing_deg"] == 220


def test_recon_narrative_adds_push_then_find() -> None:
    spec = load_mission_spec(EX / "manston_recon_narrative.yaml")
    assert spec.narrative is not None and spec.narrative.enabled
    passed = apply_narrative(spec, voice="raf")
    assert passed.narrative is not None and passed.narrative.enabled
    expanded = expand_recon_find_pack(passed, voice="raf")
    names = [t.name for t in expanded.triggers]
    assert names[0] == "narrative_push"
    assert "recon_area_observed" in names
    assert expanded.narrative is not None
    assert expanded.narrative.enabled is False
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors


def test_scenery_validates_and_unknown_fails() -> None:
    spec = load_mission_spec(EX / "manston_freeflight_scenery.yaml")
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    bad = spec.model_copy(
        update={"scenery": [spec.scenery[0].model_copy(update={"type": "NotARealHangar"})]}
    )
    failed = validate_mission_spec(bad, inventory=_inv())
    assert not failed.ok
    assert any(e.code == "unknown_static" for e in failed.errors)


def test_m8_examples_compile(tmp_path: Path) -> None:
    compiler = PyDCSCompiler()
    for name in (
        "manston_p51_freeflight.yaml",
        "manston_p51_ground_attack.yaml",
        "hawkinge_cold_freeflight.yaml",
        "hawkinge_cap.yaml",
        "hawkinge_freeflight_pair.yaml",
        "chailey_cold_freeflight.yaml",
        "manston_ground_attack_artillery.yaml",
        "manston_freeflight_scenery.yaml",
        "manston_recon_narrative.yaml",
    ):
        out = tmp_path / f"{Path(name).stem}.miz"
        compiler.compile(load_mission_spec(EX / name), out, voice="raf")
        assert out.is_file()
