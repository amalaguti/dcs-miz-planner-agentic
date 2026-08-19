"""Host invent product nudges: Spitfire player, WWII colour, dynamics, motion."""

from __future__ import annotations

from fixtures_support import REPO_ROOT

from dcs_miz_planner.agent.invent_nudges import (
    host_dynamics_nudge,
    host_invent_product_nudge,
    host_spitfire_player_nudge,
    host_wwii_opposition_nudge,
)
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import NarrativeSpec

EX = REPO_ROOT / "examples"


def test_spitfire_player_nudge_on_su25t_batumi() -> None:
    spec = load_mission_spec(EX / "batumi_cold_freeflight.yaml")
    text = host_spitfire_player_nudge("free flight from Batumi", spec)
    assert text is not None
    assert "SpitfireLFMkIX" in text
    assert host_spitfire_player_nudge("fly the Frogfoot from Batumi", spec) is None
    spit = load_mission_spec(EX / "batumi_spitfire_freeflight.yaml")
    assert host_spitfire_player_nudge("hop from Batumi", spit) is None


def test_wwii_opposition_nudge_swaps_su25t_enemies() -> None:
    spec = load_mission_spec(EX / "batumi_black_sea_cap.yaml")
    text = host_wwii_opposition_nudge("1944 Luftwaffe bounce over Batumi", spec)
    assert text is not None
    assert "Bf-109K-4" in text or "FW-190A8" in text
    assert host_wwii_opposition_nudge("modern CAP over Batumi", spec) is None


def test_live_dynamics_nudge_on_static_intercept() -> None:
    spec = load_mission_spec(EX / "manston_dawn_intercept.yaml")
    text = host_dynamics_nudge("make the intercept different each load", spec)
    assert text is not None
    assert "dynamics.mode live" in text
    live = load_mission_spec(EX / "manston_dawn_intercept_dynamics_live.yaml")
    assert host_dynamics_nudge("different each load", live) is None


def test_choose_and_hybrid_dynamics_cues() -> None:
    spec = load_mission_spec(EX / "manston_dawn_intercept.yaml")
    choose = host_dynamics_nudge("let me pick difficulty from the F10 menu", spec)
    assert choose is not None
    assert "dynamics.mode choose" in choose
    hybrid = host_dynamics_nudge("unpredictable dice raid but let me pick from F10", spec)
    assert hybrid is not None
    assert "dynamics.mode hybrid" in hybrid


def test_narrative_xor_skips_dynamics() -> None:
    spec = load_mission_spec(EX / "manston_dawn_intercept.yaml")
    narrated = spec.model_copy(update={"narrative": NarrativeSpec(enabled=True)})
    assert host_dynamics_nudge("different each load", narrated) is None


def test_moving_convoy_nudge_on_static_ga() -> None:
    spec = load_mission_spec(EX / "manston_ground_attack.yaml")
    text = host_dynamics_nudge("ground attack a moving convoy inland", spec)
    assert text is not None
    assert "motion" in text
    assert host_dynamics_nudge("ground attack trucks inland", spec) is None
    moving = load_mission_spec(EX / "manston_ground_attack_convoy.yaml")
    assert host_dynamics_nudge("moving convoy inland", moving) is None


def test_combined_nudge_joins_player_and_wwii() -> None:
    spec = load_mission_spec(EX / "batumi_black_sea_cap.yaml")
    text = host_invent_product_nudge("1944 Luftwaffe CAP from Batumi", spec)
    assert text is not None
    assert "SpitfireLFMkIX" in text
    assert "ThirdReich" in text
