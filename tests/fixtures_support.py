"""Shared helpers for Manston golden fixtures (tests only)."""

from __future__ import annotations

import difflib
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
CAP_SPEC = REPO_ROOT / "examples" / "manston_cap.yaml"
GROUND_ATTACK_SPEC = REPO_ROOT / "examples" / "manston_ground_attack.yaml"
ESCORT_SPEC = REPO_ROOT / "examples" / "manston_escort.yaml"
RECON_SPEC = REPO_ROOT / "examples" / "manston_recon.yaml"
RADIO_SPEC = REPO_ROOT / "examples" / "manston_dawn_intercept_radio.yaml"
GATES_SPEC = REPO_ROOT / "examples" / "manston_freeflight_altitude_speed_gates.yaml"
MARKERS_SPEC = REPO_ROOT / "examples" / "manston_ground_attack_markers.yaml"
SOUND_FLAGS_SPEC = REPO_ROOT / "examples" / "manston_freeflight_sound_flags.yaml"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_cold_freeflight"
INTERCEPT_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_dawn_intercept"
CAP_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_cap"
GA_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_ground_attack"
ESCORT_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_escort"
RECON_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_recon"
RADIO_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_dawn_intercept_radio"
GATES_FIXTURE_DIR = (
    Path(__file__).resolve().parent / "fixtures" / "manston_freeflight_altitude_speed_gates"
)
MARKERS_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "manston_ground_attack_markers"
SOUND_FLAGS_FIXTURE_DIR = (
    Path(__file__).resolve().parent / "fixtures" / "manston_freeflight_sound_flags"
)

REQUIRED_MEMBERS = ("mission", "options", "theatre", "warehouses", "l10n/DEFAULT/dictionary")
DICTIONARY_MEMBER = "l10n/DEFAULT/dictionary"
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
CAP_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    "Bf-109K-4",
    '["airdromeId"]=5',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    '["frequency"]=40.0',
    '["task"]="CAP"',
    "Orbit",
    '["pattern"]="Circle"',
    "ControlledTask",
    '["value"]=0',  # OptROE WeaponFree
)
GA_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=5',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    "Ground Attack",
    "British_GP_250LBS_Bomb_MK4_on_LH_Spitfire_Wing_Carrier",
    "SPITFIRE_45GAL_SLIPPER_TANK",
    "Blitz_36-6700A",
    "Bombing",
)
ESCORT_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    "MosquitoFBMkVI",
    "Bf-109K-4",
    '["airdromeId"]=5',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    '["task"]="Escort"',
    "groupId",
    '["value"]=0',  # OptROE WeaponFree
)
RECON_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=5',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    "Reconnaissance",
    "Blitz_36-6700A",
    "recon_aoi",
    "recon_area_observed",
    "a_out_text_delay",
    '["value"]=4',  # OptROE WeaponHold
)
RADIO_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    "Bf-109K-4",
    '["airdromeId"]=5',
    '["start_time"]=21600',
    "TakeOffParking",
    '"Player"',
    "lateActivation",
    "a_activate_group",
    "c_flag_is_true",
    "a_add_radio_item_for_coalition",
)
GATES_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=5',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    "c_unit_altitude_higher_AGL",
    "c_unit_altitude_lower_AGL",
    "c_unit_speed_higher",
    "c_unit_speed_lower",
    "c_time_since_flag",
    "a_set_flag",
    "a_out_text_delay",
)
MARKERS_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=5',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    "Blitz_36-6700A",
    "a_mark_to_all",
    "a_explosion_marker",
    "a_out_text_delay",
)
SOUND_FLAGS_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=5',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    "a_out_sound",
    "c_flag_more",
    "a_inc_flag",
    "a_set_flag_value",
    "c_time_since_flag",
)

# PyDCS assigns a random board number each process; pin it for stable goldens.
_ONBOARD_NUM_RE = re.compile(r'\["onboard_num"\]="\d+"')
# Liveries come from a local DCS install scan; absent on CI → omit the field.
_LIVERY_LINE_RE = re.compile(r'\n\t+\["livery_id"\]="[^"]*",')


def normalize_mission(mission: str) -> str:
    mission = _ONBOARD_NUM_RE.sub('["onboard_num"]="<num>"', mission)
    return _LIVERY_LINE_RE.sub("", mission)


def channel_available_inventory() -> TheatreInventory:
    """Hermetic inventory: Channel + Normandy + Caucasus + Syria + Nevada + Falklands when planner-bound."""
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
            TheatreRecord(
                theatre_id="Normandy",
                update_id="NORMANDY_terrain",
                dcs_root="S:/DCS World",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
            TheatreRecord(
                theatre_id="Caucasus",
                update_id="CAUCASUS_terrain",
                dcs_root="S:/DCS World",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
            TheatreRecord(
                theatre_id="Syria",
                update_id="SYRIA_terrain",
                dcs_root="S:/DCS World",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
            TheatreRecord(
                theatre_id="Nevada",
                update_id="NEVADA_terrain",
                dcs_root="S:/DCS World",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
            TheatreRecord(
                theatre_id="Falklands",
                update_id="FALKLANDS_terrain",
                dcs_root="S:/DCS World",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
        ),
    )


def compile_manston(output_path: Path) -> Path:
    spec = load_mission_spec(EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


NORMANDY_EXAMPLE_SPEC = REPO_ROOT / "examples" / "needs_oar_point_cold_freeflight.yaml"
NORMANDY_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=28',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
)


def compile_needs_oar_point(output_path: Path) -> Path:
    spec = load_mission_spec(NORMANDY_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


NORMANDY_CAP_EXAMPLE_SPEC = REPO_ROOT / "examples" / "needs_oar_point_cap.yaml"
NORMANDY_CAP_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    "Bf-109K-4",
    '["airdromeId"]=28',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    '["frequency"]=40.0',
    '["task"]="CAP"',
    "Orbit",
    '["pattern"]="Circle"',
)


def compile_needs_oar_point_cap(output_path: Path) -> Path:
    spec = load_mission_spec(NORMANDY_CAP_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


NORMANDY_GA_EXAMPLE_SPEC = REPO_ROOT / "examples" / "needs_oar_point_ground_attack.yaml"
NORMANDY_GA_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=28',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    "Ground Attack",
    "British_GP_250LBS_Bomb_MK4_on_LH_Spitfire_Wing_Carrier",
    "SPITFIRE_45GAL_SLIPPER_TANK",
    "Blitz_36-6700A",
    "flak18",
    "Bombing",
)


def compile_needs_oar_point_ground_attack(output_path: Path) -> Path:
    spec = load_mission_spec(NORMANDY_GA_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


NORMANDY_INTERCEPT_EXAMPLE_SPEC = REPO_ROOT / "examples" / "needs_oar_point_dawn_intercept.yaml"
NORMANDY_INTERCEPT_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    "Bf-109K-4",
    '["airdromeId"]=28',
    '["start_time"]=21600',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    '["frequency"]=40.0',
    "78296.390625",
    "-84372.234375",
)


def compile_needs_oar_point_intercept(output_path: Path) -> Path:
    spec = load_mission_spec(NORMANDY_INTERCEPT_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


NORMANDY_ESCORT_EXAMPLE_SPEC = REPO_ROOT / "examples" / "needs_oar_point_escort.yaml"
NORMANDY_ESCORT_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    "MosquitoFBMkVI",
    "Bf-109K-4",
    '["airdromeId"]=28',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    '["frequency"]=40.0',
    '["task"]="Escort"',
    "groupId",
    '["value"]=0',
)


def compile_needs_oar_point_escort(output_path: Path) -> Path:
    spec = load_mission_spec(NORMANDY_ESCORT_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


NORMANDY_RECON_EXAMPLE_SPEC = REPO_ROOT / "examples" / "needs_oar_point_recon.yaml"
NORMANDY_RECON_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=28',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
    "Reconnaissance",
    "Blitz_36-6700A",
    "recon_aoi",
    "recon_area_observed",
    "a_out_text_delay",
    '["value"]=4',
)


def compile_needs_oar_point_recon(output_path: Path) -> Path:
    spec = load_mission_spec(NORMANDY_RECON_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


CAUCASUS_EXAMPLE_SPEC = REPO_ROOT / "examples" / "batumi_cold_freeflight.yaml"
CAUCASUS_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=22',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
)


def compile_batumi(output_path: Path) -> Path:
    spec = load_mission_spec(CAUCASUS_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


BATUMI_CAP_EXAMPLE_SPEC = REPO_ROOT / "examples" / "batumi_black_sea_cap.yaml"
BATUMI_CAP_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=22',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
    '["task"]="CAP"',
    "Orbit",
    '["pattern"]="Circle"',
    "Russia",
)


def compile_batumi_cap(output_path: Path) -> Path:
    spec = load_mission_spec(BATUMI_CAP_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


BATUMI_GA_EXAMPLE_SPEC = REPO_ROOT / "examples" / "batumi_kutaisi_ground_attack.yaml"
BATUMI_GA_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=22',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
    "Ground Attack",
    "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
    '["type"]="Ural-375"',
    '["type"]="GAZ-66"',
    "Russia",
    "Bombing",
)


def compile_batumi_ground_attack(output_path: Path) -> Path:
    spec = load_mission_spec(BATUMI_GA_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


BATUMI_INTERCEPT_EXAMPLE_SPEC = REPO_ROOT / "examples" / "batumi_dawn_intercept.yaml"
BATUMI_INTERCEPT_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=22',
    '["start_time"]=21600',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
    "Russia",
    "-355810.6875",
    "577386.1875",
)


def compile_batumi_intercept(output_path: Path) -> Path:
    spec = load_mission_spec(BATUMI_INTERCEPT_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


BATUMI_ESCORT_EXAMPLE_SPEC = REPO_ROOT / "examples" / "batumi_black_sea_escort.yaml"
BATUMI_ESCORT_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=22',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
    '["task"]="Escort"',
    "Russia",
)


def compile_batumi_escort(output_path: Path) -> Path:
    spec = load_mission_spec(BATUMI_ESCORT_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


BATUMI_RECON_EXAMPLE_SPEC = REPO_ROOT / "examples" / "batumi_kutaisi_recon.yaml"
BATUMI_RECON_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=22',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
    "Reconnaissance",
    "Ural-375",
    "recon_aoi",
    "recon_area_observed",
    "a_out_text_delay",
    '["value"]=4',
)


def compile_batumi_recon(output_path: Path) -> Path:
    spec = load_mission_spec(BATUMI_RECON_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


BATUMI_SPITFIRE_EXAMPLE_SPEC = REPO_ROOT / "examples" / "batumi_spitfire_freeflight.yaml"
BATUMI_SPITFIRE_MISSION_CONTRACTS = (
    "SpitfireLFMkIX",
    '["airdromeId"]=22',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=124.0',
)


def compile_batumi_spitfire(output_path: Path) -> Path:
    spec = load_mission_spec(BATUMI_SPITFIRE_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


MOZDOK_EXAMPLE_SPEC = REPO_ROOT / "examples" / "mozdok_cold_freeflight.yaml"
MOZDOK_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=28',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
    "Russia",
)


def compile_mozdok(output_path: Path) -> Path:
    spec = load_mission_spec(MOZDOK_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


PALMYRA_EXAMPLE_SPEC = REPO_ROOT / "examples" / "palmyra_cold_freeflight.yaml"
PALMYRA_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=28',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
    "Syria",
)


def compile_palmyra(output_path: Path) -> Path:
    spec = load_mission_spec(PALMYRA_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


SYRIA_EXAMPLE_SPEC = REPO_ROOT / "examples" / "incirlik_cold_freeflight.yaml"
SYRIA_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=16',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
)


def compile_incirlik(output_path: Path) -> Path:
    spec = load_mission_spec(SYRIA_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


INCIRLIK_CAP_EXAMPLE_SPEC = REPO_ROOT / "examples" / "incirlik_iskenderun_cap.yaml"
INCIRLIK_CAP_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=16',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
    '["task"]="CAP"',
    "Orbit",
    '["pattern"]="Circle"',
    "Syria",
)


def compile_incirlik_cap(output_path: Path) -> Path:
    spec = load_mission_spec(INCIRLIK_CAP_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


NEVADA_EXAMPLE_SPEC = REPO_ROOT / "examples" / "nellis_cold_freeflight.yaml"
NEVADA_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=4',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
)


def compile_nellis(output_path: Path) -> Path:
    spec = load_mission_spec(NEVADA_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


FALKLANDS_EXAMPLE_SPEC = REPO_ROOT / "examples" / "mount_pleasant_cold_freeflight.yaml"
FALKLANDS_MISSION_CONTRACTS = (
    "Su-25T",
    '["airdromeId"]=2',
    '["start_time"]=32400',
    "TakeOffParking",
    '"Player"',
    '["frequency"]=251.0',
)


def compile_mount_pleasant(output_path: Path) -> Path:
    spec = load_mission_spec(FALKLANDS_EXAMPLE_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


def compile_intercept(output_path: Path) -> Path:
    spec = load_mission_spec(INTERCEPT_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


def compile_cap(output_path: Path) -> Path:
    spec = load_mission_spec(CAP_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


def compile_ground_attack(output_path: Path) -> Path:
    spec = load_mission_spec(GROUND_ATTACK_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


def compile_escort(output_path: Path) -> Path:
    spec = load_mission_spec(ESCORT_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


def compile_recon(output_path: Path) -> Path:
    spec = load_mission_spec(RECON_SPEC)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


def _compile_example(spec_path: Path, output_path: Path) -> Path:
    spec = load_mission_spec(spec_path)
    return PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, output_path, voice="raf"
    )


def compile_radio(output_path: Path) -> Path:
    return _compile_example(RADIO_SPEC, output_path)


def compile_gates(output_path: Path) -> Path:
    return _compile_example(GATES_SPEC, output_path)


def compile_markers(output_path: Path) -> Path:
    return _compile_example(MARKERS_SPEC, output_path)


def compile_sound_flags(output_path: Path) -> Path:
    return _compile_example(SOUND_FLAGS_SPEC, output_path)


def extract_structural(miz_path: Path) -> tuple[set[str], str, str, str]:
    with zipfile.ZipFile(miz_path) as z:
        members = set(z.namelist())
        theatre = z.read("theatre").decode("utf-8")
        mission = z.read("mission").decode("utf-8")
        dictionary = z.read(DICTIONARY_MEMBER).decode("utf-8")
    return members, theatre, mission, dictionary


def write_golden(
    miz_path: Path,
    fixture_dir: Path,
    *,
    source_spec: str,
    mission_contracts: tuple[str, ...],
) -> None:
    members, theatre, mission, dictionary = extract_structural(miz_path)
    missing = set(REQUIRED_MEMBERS) - members
    if missing:
        raise RuntimeError(f"Compiled .miz missing required members: {sorted(missing)}")

    fixture_dir.mkdir(parents=True, exist_ok=True)
    (fixture_dir / "theatre").write_text(theatre, encoding="utf-8", newline="\n")
    (fixture_dir / "mission").write_text(normalize_mission(mission), encoding="utf-8", newline="\n")
    (fixture_dir / "dictionary").write_text(dictionary, encoding="utf-8", newline="\n")
    meta = {
        "required_members": list(REQUIRED_MEMBERS),
        "mission_must_contain": list(mission_contracts),
        "source_spec": source_spec,
        "normalized_fields": ["onboard_num", "livery_id"],
        "briefing_voice": "raf",
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


def write_cap_golden(miz_path: Path, fixture_dir: Path = CAP_FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_cap.yaml",
        mission_contracts=CAP_MISSION_CONTRACTS,
    )


def write_ground_attack_golden(miz_path: Path, fixture_dir: Path = GA_FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_ground_attack.yaml",
        mission_contracts=GA_MISSION_CONTRACTS,
    )


def write_escort_golden(miz_path: Path, fixture_dir: Path = ESCORT_FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_escort.yaml",
        mission_contracts=ESCORT_MISSION_CONTRACTS,
    )


def write_recon_golden(miz_path: Path, fixture_dir: Path = RECON_FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_recon.yaml",
        mission_contracts=RECON_MISSION_CONTRACTS,
    )


def write_radio_golden(miz_path: Path, fixture_dir: Path = RADIO_FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_dawn_intercept_radio.yaml",
        mission_contracts=RADIO_MISSION_CONTRACTS,
    )


def write_gates_golden(miz_path: Path, fixture_dir: Path = GATES_FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_freeflight_altitude_speed_gates.yaml",
        mission_contracts=GATES_MISSION_CONTRACTS,
    )


def write_markers_golden(miz_path: Path, fixture_dir: Path = MARKERS_FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_ground_attack_markers.yaml",
        mission_contracts=MARKERS_MISSION_CONTRACTS,
    )


def write_sound_flags_golden(miz_path: Path, fixture_dir: Path = SOUND_FLAGS_FIXTURE_DIR) -> None:
    write_golden(
        miz_path,
        fixture_dir,
        source_spec="examples/manston_freeflight_sound_flags.yaml",
        mission_contracts=SOUND_FLAGS_MISSION_CONTRACTS,
    )


def _first_diff(expected: str, actual: str, *, limit: int = 8) -> str:
    """Short unified-diff snippet for golden assertion messages."""
    lines = list(
        difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile="golden",
            tofile="compiled",
            lineterm="",
            n=2,
        )
    )
    if not lines:
        return "(no line diff; length or trailing newline mismatch)"
    return "\n".join(lines[:limit])


def assert_matches_golden(miz_path: Path, fixture_dir: Path = FIXTURE_DIR) -> None:
    meta = json.loads((fixture_dir / "meta.json").read_text(encoding="utf-8"))
    required = set(meta["required_members"])
    members, theatre, mission, dictionary = extract_structural(miz_path)

    missing = required - members
    assert not missing, f"missing zip members: {sorted(missing)}"

    expected_theatre = (fixture_dir / "theatre").read_text(encoding="utf-8").rstrip("\n")
    assert theatre.rstrip("\n") == expected_theatre, "theatre member diverges from golden"

    expected_mission = normalize_mission(
        (fixture_dir / "mission").read_text(encoding="utf-8")
    ).rstrip("\n")
    actual_mission = normalize_mission(mission).rstrip("\n")
    assert actual_mission == expected_mission, (
        "mission member diverges from golden (after normalizing volatile fields)\n"
        + _first_diff(expected_mission, actual_mission)
    )

    expected_dictionary = (fixture_dir / "dictionary").read_text(encoding="utf-8").rstrip("\n")
    assert dictionary.rstrip("\n") == expected_dictionary, "l10n dictionary diverges from golden"
    for key in (
        "DictKey_Translation_1",
        "DictKey_Translation_2",
        "DictKey_Translation_4",
    ):
        assert f'["{key}"]=""' not in dictionary, f"empty briefing entry: {key}"

    for needle in meta["mission_must_contain"]:
        assert needle in mission, f"mission missing contracted content: {needle!r}"
