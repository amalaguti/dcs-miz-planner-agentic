"""Shared helpers for Manston golden fixtures (tests only)."""

from __future__ import annotations

import json
import re
import zipfile
from datetime import UTC, datetime
from pathlib import Path

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.install.models import AvailabilityState, TheatreInventory, TheatreRecord
from dcs_miz_planner.loader import load_mission_spec

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_SPEC = REPO_ROOT / "examples" / "manston_cold_freeflight.yaml"
INTERCEPT_SPEC = REPO_ROOT / "examples" / "manston_dawn_intercept.yaml"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_cold_freeflight"
INTERCEPT_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_dawn_intercept"

REQUIRED_MEMBERS = ("mission", "options", "theatre", "warehouses")
MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=5',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
)
INTERCEPT_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    "Bf-109K-4",
    '["airdromeId"]=5',
    '["start_time"]=21600',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    '["frequency"]=40.0',
)

# PyDCS assigns a random board number each process; pin it for stable goldens.
_ONBOARD_NUM_RE = re.compile(r'\["onboard_num"\]="\d+"')


def normalize_mission(mission: str) -> str:
    return _ONBOARD_NUM_RE.sub('["onboard_num"]="<num>"', mission)


def channel_available_inventory() -> TheatreInventory:
    return TheatreInventory(
        scanned_at=datetime.now(UTC),
        dcs_roots=("S:/DCS World",),
        saved_games_roots=(),
        theatres=(
            TheatreRecord(
                theatre_id="TheChannel",
                update_id="THECHANNEL_terrain",
                dcs_root="S:/DCS World",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
        ),
    )


def compile_manston(output_path: Path) -> Path:
    spec = load_mission_spec(EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(spec, output_path)


def compile_intercept(output_path: Path) -> Path:
    spec = load_mission_spec(INTERCEPT_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(spec, output_path)


def extract_structural(miz_path: Path) -> tuple[set[str], str, str]:
    with zipfile.ZipFile(miz_path) as z:
        members = set(z.namelist())
        theatre = z.read("theatre").decode("utf-8")
        mission = z.read("mission").decode("utf-8")
    return members, theatre, mission


def write_golden(
    miz_path: Path,
    fixture_dir: Path,
    *,
    source_spec: str,
    mission_contracts: tuple[str, ...],
) -> None:
    members, theatre, mission = extract_structural(miz_path)
    missing = set(REQUIRED_MEMBERS) - members
    if missing:
        raise RuntimeError(f"Compiled .miz missing required members: {sorted(missing)}")

    fixture_dir.mkdir(parents=True, exist_ok=True)
    (fixture_dir / "theatre").write_text(theatre, encoding="utf-8", newline="\n")
    (fixture_dir / "mission").write_text(normalize_mission(mission), encoding="utf-8", newline="\n")
    meta = {
        "required_members": list(REQUIRED_MEMBERS),
        "mission_must_contain": list(mission_contracts),
        "source_spec": source_spec,
        "normalized_fields": ["onboard_num"],
    }
    (fixture_dir / "meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def write_manston_golden(miz_path: Path, fixture_dir: Path = FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_cold_freeflight.yaml",
        mission_contracts=MISSION_CONTRACTS,
    )


def write_intercept_golden(miz_path: Path, fixture_dir: Path = INTERCEPT_FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_dawn_intercept.yaml",
        mission_contracts=INTERCEPT_MISSION_CONTRACTS,
    )


def assert_matches_golden(miz_path: Path, fixture_dir: Path = FIXTURE_DIR) -> None:
    meta = json.loads((fixture_dir / "meta.json").read_text(encoding="utf-8"))
    required = set(meta["required_members"])
    members, theatre, mission = extract_structural(miz_path)

    missing = required - members
    assert not missing, f"missing zip members: {sorted(missing)}"

    expected_theatre = (fixture_dir / "theatre").read_text(encoding="utf-8").rstrip("\n")
    assert theatre.rstrip("\n") == expected_theatre, "theatre member diverges from golden"

    expected_mission = (fixture_dir / "mission").read_text(encoding="utf-8").rstrip("\n")
    assert normalize_mission(mission).rstrip("\n") == expected_mission, (
        "mission member diverges from golden (after normalizing volatile fields)"
    )

    for needle in meta["mission_must_contain"]:
        assert needle in mission, f"mission missing contracted content: {needle!r}"
