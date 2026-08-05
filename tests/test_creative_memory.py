"""Creative decision detail + history→bias helper."""

from __future__ import annotations

from pathlib import Path

from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.memory import (
    OUTCOME_SUCCESS,
    UserMemoryService,
    build_creative_detail,
    creative_bias_from_history,
    detail_with_inferred_creative,
    format_creative_bias_fragment,
    infer_creative_from_spec,
    merge_creative_into_detail,
)
from dcs_miz_planner.tools import list_generation_history, record_feedback, record_generation


def test_build_and_merge_creative_detail() -> None:
    creative = build_creative_detail(
        behaviours=["altitude_speed_gates"],
        inspirations=["low_level_channel_hop"],
        sources=["catalog"],
    )
    detail = merge_creative_into_detail({"voice": "raf"}, creative)
    assert detail["voice"] == "raf"
    assert detail["creative"]["behaviours"] == ["altitude_speed_gates"]
    assert detail["creative"]["inspirations"] == ["low_level_channel_hop"]


def test_generation_detail_creative_round_trip(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    creative = build_creative_detail(
        behaviours=["mark_smoke"],
        sources=["catalog"],
    )
    result = record_generation(
        outcome=OUTCOME_SUCCESS,
        prompt="strike with marks",
        mission_type="ground_attack",
        theatre="TheChannel",
        detail={"creative": creative, "note": "test"},
        db_path=db,
    )
    assert result["ok"] is True
    listed = list_generation_history(db_path=db)
    assert listed["ok"] is True
    assert listed["generations"]
    detail = listed["generations"][0]["detail"]
    assert detail["creative"]["behaviours"] == ["mark_smoke"]
    assert detail["note"] == "test"


def test_bias_empty_history() -> None:
    bias = creative_bias_from_history([])
    assert bias.prefer == ()
    assert bias.avoid == ()
    assert format_creative_bias_fragment(bias) == ""


def test_bias_high_score_prefers_behaviours(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    mem = UserMemoryService(db_path=db)
    gid = mem.record_generation(
        outcome=OUTCOME_SUCCESS,
        mission_type="free_flight",
        detail={
            "creative": build_creative_detail(
                behaviours=["altitude_speed_gates", "sound_flag_chain"]
            )
        },
    )
    mem.record_feedback(
        source="test", generation_id=gid, score=5, tags=["liked:altitude_speed_gates"]
    )
    gens = mem.list_generations()
    fbs = mem.list_feedback()
    bias = creative_bias_from_history(gens, fbs, mission_type="free_flight")
    assert "altitude_speed_gates" in bias.prefer
    frag = format_creative_bias_fragment(bias)
    assert "altitude_speed_gates" in frag
    assert "Prefer" in frag


def test_bias_mission_type_filter(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    mem = UserMemoryService(db_path=db)
    gid = mem.record_generation(
        outcome=OUTCOME_SUCCESS,
        mission_type="intercept",
        detail={"creative": build_creative_detail(behaviours=["radio_late_activation"])},
    )
    mem.record_feedback(source="test", generation_id=gid, score=5)
    gens = mem.list_generations()
    fbs = mem.list_feedback()
    assert creative_bias_from_history(gens, fbs, mission_type="free_flight").prefer == ()
    assert (
        "radio_late_activation"
        in creative_bias_from_history(gens, fbs, mission_type="intercept").prefer
    )


def test_bias_avoid_tag_and_prefs(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    mem = UserMemoryService(db_path=db)
    gid = mem.record_generation(
        outcome=OUTCOME_SUCCESS,
        mission_type="cap",
        detail={"creative": build_creative_detail(behaviours=["narrative_pack"])},
    )
    mem.record_feedback(source="test", generation_id=gid, score=1, tags=["avoid:narrative_pack"])
    gens = mem.list_generations()
    fbs = mem.list_feedback()
    bias = creative_bias_from_history(
        gens,
        fbs,
        mission_type="cap",
        prefs={"preferred_behaviours": ["mark_smoke"], "avoid_behaviours": ["narrative_pack"]},
    )
    assert "mark_smoke" in bias.prefer
    assert "narrative_pack" in bias.avoid
    assert "narrative_pack" not in bias.prefer


def test_infer_creative_from_gates_example() -> None:
    root = Path(__file__).resolve().parents[1]
    spec = load_mission_spec(root / "examples" / "manston_freeflight_altitude_speed_gates.yaml")
    creative = infer_creative_from_spec(spec)
    assert creative is not None
    assert "altitude_speed_gates" in creative["behaviours"]
    detail = detail_with_inferred_creative({"voice": "raf"}, spec)
    assert detail["creative"]["behaviours"]
    # Does not overwrite existing creative
    kept = detail_with_inferred_creative(
        {"creative": build_creative_detail(behaviours=["mark_smoke"])},
        spec,
    )
    assert kept["creative"]["behaviours"] == ["mark_smoke"]


def test_infer_skips_incomplete_late_activation() -> None:
    from dcs_miz_planner.models import (
        EnemyFlight,
        MissionDate,
        MissionSpec,
        MissionType,
        Objective,
        ObjectiveType,
        Player,
        WeatherPreset,
    )

    half = MissionSpec(
        schema_version="1",
        mission_type=MissionType.INTERCEPT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="06:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(aircraft="SpitfireLFMkIX", airfield="Manston"),
        enemies=[EnemyFlight(aircraft="Bf-109K-4", count=2, late_activation=True)],
        objectives=[Objective(type=ObjectiveType.INTERCEPT_ENEMY)],
    )
    creative = infer_creative_from_spec(half)
    behaviours = (creative or {}).get("behaviours") or []
    assert "radio_late_activation" not in behaviours

    root = Path(__file__).resolve().parents[1]
    full = load_mission_spec(root / "examples" / "manston_dawn_intercept_radio.yaml")
    full_c = infer_creative_from_spec(full)
    assert full_c is not None
    assert "radio_late_activation" in full_c["behaviours"]


def test_spec_shape_reminder_allows_triggers() -> None:
    from dcs_miz_planner.agent.prompts import compose_system_prompt
    from dcs_miz_planner.agent.spec_schema import SPEC_SHAPE_REMINDER

    assert "must be []" not in SPEC_SHAPE_REMINDER
    assert "non-empty OK" in SPEC_SHAPE_REMINDER or "Immersion" in SPEC_SHAPE_REMINDER
    prompt = compose_system_prompt("raf")
    assert "must be []" not in prompt
    assert "randomize_mission" in prompt
    assert "vague first ask" in prompt or "Do NOT use randomize_mission" in prompt


def test_prompts_mention_history_bias() -> None:
    from dcs_miz_planner.agent.prompts import compose_system_prompt
    from dcs_miz_planner.agent.tool_bridge import TOOL_DEFINITIONS

    prompt = compose_system_prompt(
        "raf",
        creative_bias_fragment=format_creative_bias_fragment(
            creative_bias_from_history([])  # empty → no fragment
        ),
    )
    assert "list_generation_history" in prompt
    assert "detail.creative" in prompt or "creative" in prompt
    biased = compose_system_prompt(
        "raf",
        creative_bias_fragment="Creative taste from past generations:\n- Prefer: altitude_speed_gates",
    )
    assert "altitude_speed_gates" in biased
    rec = next(t for t in TOOL_DEFINITIONS if t["function"]["name"] == "record_generation")
    assert "creative" in rec["function"]["description"].lower()


def test_record_feedback_tool_tags(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    gen = record_generation(
        outcome=OUTCOME_SUCCESS,
        mission_type="free_flight",
        detail={"creative": build_creative_detail(behaviours=["sound_flag_chain"])},
        db_path=db,
    )
    fb = record_feedback(
        source="cli",
        generation_id=gen["generation_id"],
        score=4,
        tags=["liked:sound_flag_chain"],
        db_path=db,
    )
    assert fb["ok"] is True
