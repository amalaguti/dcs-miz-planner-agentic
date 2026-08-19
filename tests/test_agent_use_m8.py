"""M9: agent uses M8 extra homes, schema-by-airfield, geometry clamp, knob nudges."""

from __future__ import annotations

from fixtures_support import REPO_ROOT

from dcs_miz_planner.agent.extra_homes import (
    host_m8_knob_nudge,
    infer_airfield,
    try_clamp_extra_home_stations,
)
from dcs_miz_planner.agent.prompts import host_spec_repair_nudge
from dcs_miz_planner.agent.spec_schema import build_spec_schema
from dcs_miz_planner.agent.tool_bridge import TOOL_DEFINITIONS
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.tools.surface import get_mission_spec_schema

EX = REPO_ROOT / "examples"


def test_hawkinge_cap_schema_is_not_manston_135_25() -> None:
    view = build_spec_schema("cap", theatre="TheChannel", airfield="Hawkinge")
    player = view.example["player"]
    cap = view.example["cap"]
    assert player["airfield"] == "Hawkinge"
    assert cap["bearing_deg"] == 76
    assert cap["distance_km"] == 32
    tool = get_mission_spec_schema("cap", theatre="TheChannel", airfield="Hawkinge")
    assert tool["ok"]
    assert tool["example"]["player"]["airfield"] == "Hawkinge"
    assert tool["example"]["cap"]["bearing_deg"] == 76


def test_detling_cap_schema_rewrites_from_place_card() -> None:
    view = build_spec_schema("cap", theatre="TheChannel", airfield="Detling")
    assert view.example["player"]["airfield"] == "Detling"
    assert view.example["cap"]["bearing_deg"] == 102
    assert view.example["cap"]["distance_km"] == 71


def test_chailey_cap_schema_is_not_needs_oar_point_180_63() -> None:
    view = build_spec_schema("cap", theatre="Normandy", airfield="Chailey")
    assert view.example["player"]["airfield"] == "Chailey"
    assert view.example["cap"]["bearing_deg"] == 228
    assert view.example["cap"]["distance_km"] == 130


def test_manston_default_cap_schema_unchanged() -> None:
    view = build_spec_schema("cap", theatre="TheChannel")
    assert view.example["player"]["airfield"] == "Manston"
    assert view.example["cap"]["bearing_deg"] == 135
    assert view.example["cap"]["distance_km"] == 25
    same = build_spec_schema("cap", theatre="TheChannel", airfield="Manston")
    assert same.example["player"]["airfield"] == "Manston"
    assert same.example["cap"]["bearing_deg"] == 135


def test_unknown_airfield_ignored() -> None:
    view = build_spec_schema("cap", theatre="TheChannel", airfield="NotARealField")
    assert view.example["player"]["airfield"] == "Manston"


def test_clamp_hawkinge_cap_135_25_to_76_32() -> None:
    spec = load_mission_spec(EX / "hawkinge_cap.yaml")
    cloned = spec.model_copy(
        update={"cap": spec.cap.model_copy(update={"bearing_deg": 135, "distance_km": 25})}
    )
    clamped = try_clamp_extra_home_stations(cloned, prompt="pair from Hawkinge")
    assert clamped is not None
    assert clamped.cap is not None
    assert clamped.cap.bearing_deg == 76
    assert clamped.cap.distance_km == 32


def test_clamp_does_not_touch_manston() -> None:
    spec = load_mission_spec(EX / "manston_cap.yaml")
    assert try_clamp_extra_home_stations(spec, prompt="CAP from Manston") is None


def test_clamp_skips_named_french_coast_place() -> None:
    spec = load_mission_spec(EX / "hawkinge_cap.yaml")
    cloned = spec.model_copy(
        update={"cap": spec.cap.model_copy(update={"bearing_deg": 135, "distance_km": 25})}
    )
    assert (
        try_clamp_extra_home_stations(cloned, prompt="CAP from Hawkinge over the French coast")
        is None
    )


def test_chailey_clamp_rewrites_180_63() -> None:
    spec = load_mission_spec(EX / "chailey_cold_freeflight.yaml")
    from dcs_miz_planner.models import Cap, CapPattern, Engagement, MissionType

    cap_spec = spec.model_copy(
        update={
            "mission_type": MissionType.CAP,
            "cap": Cap(
                bearing_deg=180,
                distance_km=63,
                altitude_m=4000,
                pattern=CapPattern.CIRCLE,
                engagement=Engagement.WEAPONS_FREE,
            ),
        }
    )
    clamped = try_clamp_extra_home_stations(cap_spec, prompt="CAP from Chailey")
    assert clamped is not None
    assert clamped.cap is not None
    assert clamped.cap.bearing_deg == 228
    assert clamped.cap.distance_km == 130


def test_repair_nudge_infers_hawkinge_airfield() -> None:
    rejected = '{"mission_type":"cap","theatre":"TheChannel","player":{"airfield":"Hawkinge"}}'
    text = host_spec_repair_nudge("bad json", rejected_text=rejected)
    assert infer_airfield(rejected) == "Hawkinge"
    assert "Hawkinge" in text
    assert '"bearing_deg": 76' in text or '"bearing_deg":76' in text


def test_artillery_nudge_when_draft_uses_trucks() -> None:
    ga = load_mission_spec(EX / "manston_ground_attack.yaml")
    assert "list_strike_targets" in (host_m8_knob_nudge("hunt leFH howitzers inland", ga) or "")
    arty = load_mission_spec(EX / "manston_ground_attack_artillery.yaml")
    assert host_m8_knob_nudge("hunt artillery", arty) is None


def test_pair_nudge_when_cap_omits_flight() -> None:
    cap = load_mission_spec(EX / "hawkinge_cap.yaml")
    assert cap.player.flight is None
    assert "size 2" in (host_m8_knob_nudge("take a pair from Hawkinge", cap) or "")
    assert host_m8_knob_nudge("CAP from Hawkinge", cap) is None
    orders = host_m8_knob_nudge("take a pair, give me F10 section orders to rejoin and engage", cap)
    assert orders is not None
    assert "orders" in orders
    assert "size 2 role lead" not in orders


def test_discipline_nudge_matches_wander_off() -> None:
    spec = load_mission_spec(EX / "hawkinge_freeflight_pair.yaml")
    assert spec.player.flight is not None
    assert spec.player.flight.discipline is None
    text = host_m8_knob_nudge(
        "I'm flying as two, put me as wingman and fail me if I wander off", spec
    )
    assert text is not None
    assert "discipline" in text


def test_mustang_nudge_and_bare_pair_does_not_stack() -> None:
    spit = load_mission_spec(EX / "hawkinge_freeflight_pair.yaml")
    assert host_m8_knob_nudge("take a pair from Hawkinge, keep it simple", spit) is None
    assert "P-51D" in host_m8_knob_nudge("Channel Mustang hop from Manston", spit)
    p51 = load_mission_spec(EX / "manston_p51_freeflight.yaml")
    assert host_m8_knob_nudge("Mustang hop", p51) is None


def test_schema_tool_documents_airfield() -> None:
    schema_tool = next(
        t for t in TOOL_DEFINITIONS if t["function"]["name"] == "get_mission_spec_schema"
    )
    props = schema_tool["function"]["parameters"]["properties"]
    assert "airfield" in props
