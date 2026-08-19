"""Mission Spec validation engine tests."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from dcs_miz_planner.cli import main
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.install.models import AvailabilityState, TheatreInventory, TheatreRecord
from dcs_miz_planner.loader import load_mission_spec
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
from dcs_miz_planner.validation import validate_mission_spec

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "manston_cold_freeflight.yaml"
INTERCEPT_EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "manston_dawn_intercept.yaml"


def _channel_inventory(
    *, state: AvailabilityState = AvailabilityState.AVAILABLE
) -> TheatreInventory:
    return TheatreInventory(
        scanned_at=datetime.now(UTC),
        dcs_roots=("S:/DCS World",),
        saved_games_roots=(),
        theatres=(
            TheatreRecord(
                theatre_id="TheChannel",
                update_id="THECHANNEL_terrain",
                dcs_root="S:/DCS World",
                state=state,
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
            TheatreRecord(
                theatre_id="Kola",
                update_id="KOLA_terrain",
                dcs_root="S:/DCS World",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
        ),
    )


def _base_spec(**player_overrides) -> MissionSpec:
    player = {
        "aircraft": "SpitfireLFMkIX",
        "airfield": "Manston",
    }
    player.update(player_overrides)
    return MissionSpec(
        schema_version="1",
        mission_type=MissionType.FREE_FLIGHT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="09:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(**player),
    )


def test_manston_example_validates(tmp_path: Path):
    spec = load_mission_spec(EXAMPLE)
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert result.ok


def test_manston_on_normandy_fails_validation():
    spec = _base_spec().model_copy(update={"theatre": "Normandy"})
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert not result.ok
    err = next(e for e in result.errors if e.code == "unknown_airfield")
    assert err.path == "player.airfield"
    assert "NeedsOarPoint" in (err.hint or "")
    assert "Manston" not in (err.hint or "")


def test_needs_oar_point_on_channel_fails_validation():
    spec = _base_spec(airfield="NeedsOarPoint")
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert not result.ok
    err = next(e for e in result.errors if e.code == "unknown_airfield")
    assert err.path == "player.airfield"
    assert "Manston" in (err.hint or "")
    assert "NeedsOarPoint" not in (err.hint or "")


def test_intercept_example_validates():
    spec = load_mission_spec(INTERCEPT_EXAMPLE)
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert result.ok


def test_intercept_unknown_enemy_aircraft():
    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.INTERCEPT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="06:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(aircraft="SpitfireLFMkIX", airfield="Manston"),
        enemies=[EnemyFlight(aircraft="NoSuchJet", count=2)],
        objectives=[Objective(type=ObjectiveType.INTERCEPT_ENEMY)],
    )
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert any(
        e.code == "unknown_aircraft" and e.path == "enemies[0].aircraft" for e in result.errors
    )


def test_unknown_airfield():
    spec = _base_spec(airfield="NotARealField")
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert not result.ok
    assert any(e.code == "unknown_airfield" for e in result.errors)


def test_unknown_aircraft_and_airfield_collected():
    bad = _base_spec(aircraft="NoSuchJet", airfield="Nowhere")
    result = validate_mission_spec(bad, inventory=_channel_inventory())
    codes = {e.code for e in result.errors}
    assert "unknown_aircraft" in codes
    assert "unknown_airfield" in codes


def test_unknown_weather_via_registry(monkeypatch):
    from dcs_miz_planner.registry import RegistryError, get_channel_registry

    registry = get_channel_registry()

    def boom(_name: str):
        raise RegistryError("nope")

    monkeypatch.setattr(registry, "weather_preset", boom)
    result = validate_mission_spec(_base_spec(), registry=registry, inventory=_channel_inventory())
    assert any(e.code == "unknown_weather" for e in result.errors)


def test_theatre_not_locally_available():
    spec = load_mission_spec(EXAMPLE)
    result = validate_mission_spec(
        spec, inventory=_channel_inventory(state=AvailabilityState.DISABLED)
    )
    assert not result.ok
    assert any(e.code == "theatre_not_available" for e in result.errors)


def test_empty_inventory_diagnostic():
    spec = load_mission_spec(EXAMPLE)
    empty = TheatreInventory(
        scanned_at=datetime.now(UTC),
        dcs_roots=(),
        saved_games_roots=(),
        theatres=(),
    )
    result = validate_mission_spec(spec, inventory=empty)
    assert any(e.code == "install_inventory_unavailable" for e in result.errors)


def test_cli_validate_success(capsys, monkeypatch):
    monkeypatch.setattr(
        "dcs_miz_planner.cli.validate_mission_spec",
        lambda spec: validate_mission_spec(spec, inventory=_channel_inventory()),
    )
    assert main(["validate", str(EXAMPLE)]) == 0
    assert "Valid:" in capsys.readouterr().out


def test_cli_validate_failure_json(tmp_path: Path, capsys, monkeypatch):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        EXAMPLE.read_text(encoding="utf-8").replace("Manston", "FakeField"),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "dcs_miz_planner.cli.validate_mission_spec",
        lambda spec: validate_mission_spec(spec, inventory=_channel_inventory()),
    )
    assert main(["validate", str(bad), "--json"]) == 2
    import json

    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert any(e["code"] == "unknown_airfield" for e in payload["errors"])


def test_compile_refuses_invalid_without_writing(tmp_path: Path):
    spec = _base_spec(airfield="FakeField")
    out = tmp_path / "nope.miz"
    with pytest.raises(ValueError, match="unknown_airfield|Unknown airfield"):
        PyDCSCompiler(inventory=_channel_inventory()).compile(spec, out)
    assert not out.exists()


def test_compile_manston_with_injected_inventory(tmp_path: Path):
    spec = load_mission_spec(EXAMPLE)
    out = PyDCSCompiler(inventory=_channel_inventory()).compile(spec, tmp_path / "ok.miz")
    assert out.exists()


def test_late_activation_without_activate_fails():
    from dcs_miz_planner.models import Coalition

    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.INTERCEPT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="06:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(aircraft="SpitfireLFMkIX", airfield="Manston"),
        enemies=[
            EnemyFlight(
                aircraft="Bf-109K-4",
                count=2,
                late_activation=True,
                coalition=Coalition.RED,
            )
        ],
        objectives=[Objective(type=ObjectiveType.INTERCEPT_ENEMY)],
    )
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert any(e.code == "late_activation_no_activate" for e in result.errors)


def test_activate_without_late_activation_fails():
    from dcs_miz_planner.models import (
        ActivateGroupAction,
        Coalition,
        FlagIsCondition,
        TriggerRule,
    )

    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.INTERCEPT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="06:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(aircraft="SpitfireLFMkIX", airfield="Manston"),
        enemies=[EnemyFlight(aircraft="Bf-109K-4", count=2, coalition=Coalition.RED)],
        objectives=[Objective(type=ObjectiveType.INTERCEPT_ENEMY)],
        triggers=[
            TriggerRule(
                name="spawn",
                when=[FlagIsCondition(flag="spawn", value=True)],
                then=[ActivateGroupAction(enemy_index=0)],
            )
        ],
    )
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert any(e.code == "activate_not_late" for e in result.errors)


def test_message_delay_s_rejected_at_load():
    from pydantic import ValidationError as PydanticValidationError

    from dcs_miz_planner.models import MessageAction

    with pytest.raises(PydanticValidationError):
        MessageAction(text="hi", delay_s=5)


def test_unknown_country_and_skill():
    spec = _base_spec(country="Germany", skill="SuperAce")
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    codes = {e.code for e in result.errors}
    assert "unknown_country" in codes
    assert "unknown_skill" in codes
    country_err = next(e for e in result.errors if e.code == "unknown_country")
    assert country_err.hint and "ThirdReich" in country_err.hint


def test_friendly_intercept_enemy_fails():
    from dcs_miz_planner.models import Coalition

    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.INTERCEPT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="06:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(aircraft="SpitfireLFMkIX", airfield="Manston"),
        enemies=[
            EnemyFlight(aircraft="Bf-109K-4", count=2, coalition=Coalition.BLUE),
        ],
        objectives=[Objective(type=ObjectiveType.INTERCEPT_ENEMY)],
    )
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert any(e.code == "friendly_enemy" for e in result.errors)


def test_radio_late_activation_example_validates():
    radio = Path(__file__).resolve().parents[1] / "examples" / "manston_dawn_intercept_radio.yaml"
    spec = load_mission_spec(radio)
    result = validate_mission_spec(spec, inventory=_channel_inventory())
    assert result.ok, result.errors


def test_shipped_examples_validate(tmp_path: Path):
    examples = Path(__file__).resolve().parents[1] / "examples"
    inv = _channel_inventory()
    for path in sorted(examples.glob("*.yaml")):
        spec = load_mission_spec(path)
        result = validate_mission_spec(spec, inventory=inv)
        assert result.ok, f"{path.name}: {result.errors}"
