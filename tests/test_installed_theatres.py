"""Installed theatres probe: SQLite cache, refresh, classification."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from dcs_miz_planner.cli import main
from dcs_miz_planner.install import AvailabilityState, InventoryService
from dcs_miz_planner.install.discover import discover_dcs_roots
from dcs_miz_planner.install.parse import parse_terrain_entry
from dcs_miz_planner.install.probe import probe_installations


def write_autoupdate(root: Path, modules: list[str]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "autoupdate.cfg").write_text(
        json.dumps({"version": "2.9.0", "modules": modules}),
        encoding="utf-8",
    )


def write_terrain(
    root: Path,
    *,
    folder: str,
    theatre_id: str,
    update_id: str,
    extra_lua: str = "",
) -> Path:
    terrain = root / "Mods" / "terrains" / folder
    terrain.mkdir(parents=True, exist_ok=True)
    (terrain / "entry.lua").write_text(
        f"""
theatre =
{{
\t['state'] = "installed";
\t['type'] = "terrain";
\t['update_id'] = "{update_id}";
\t['id'] = "{theatre_id}";
}}
{extra_lua}
local self_ID = "{theatre_id}";
declare_plugin(self_ID, theatre);
plugin_done()
""",
        encoding="utf-8",
    )
    return terrain


def write_plugins_enabled(saved_games: Path, overrides: dict[str, bool]) -> None:
    cfg = saved_games / "Config"
    cfg.mkdir(parents=True, exist_ok=True)
    lines = ["pluginsEnabled = {"]
    for key, value in overrides.items():
        lines.append(f'    ["{key}"] = {"true" if value else "false"},')
    lines.append("}")
    (cfg / "pluginsEnabled.lua").write_text("\n".join(lines) + "\n", encoding="utf-8")


@pytest.fixture
def dcs_home(tmp_path: Path) -> Path:
    root = tmp_path / "DCS World"
    write_autoupdate(
        root,
        [
            "WORLD",
            "THECHANNEL_terrain",
            "NORMANDY_terrain",
            "CAUCASUS_terrain",
            "SYRIA_terrain",
        ],
    )
    write_terrain(
        root, folder="TheChannel", theatre_id="TheChannel", update_id="THECHANNEL_terrain"
    )
    write_terrain(root, folder="Normandy", theatre_id="Normandy", update_id="NORMANDY_terrain")
    write_terrain(root, folder="Caucasus", theatre_id="Caucasus", update_id="CAUCASUS_terrain")
    write_terrain(root, folder="Syria", theatre_id="Syria", update_id="SYRIA_terrain")
    return root


@pytest.fixture
def saved_games(tmp_path: Path) -> Path:
    profile = tmp_path / "Saved Games" / "DCS"
    write_plugins_enabled(profile, {"Caucasus": False, "MarianaIslands": False})
    return profile


def test_channel_discovered_exact_ids(dcs_home: Path, saved_games: Path, tmp_path: Path):
    inv = probe_installations(dcs_root=dcs_home, saved_games=saved_games)
    channel = next(t for t in inv.theatres if t.theatre_id == "TheChannel")
    assert channel.update_id == "THECHANNEL_terrain"
    assert channel.state is AvailabilityState.AVAILABLE
    assert channel.planner_supported is True


def test_entry_lua_not_executed(tmp_path: Path):
    root = tmp_path / "DCS"
    write_autoupdate(root, ["THECHANNEL_terrain"])
    bomb = "os.execute('echo pwned')"
    write_terrain(
        root,
        folder="TheChannel",
        theatre_id="TheChannel",
        update_id="THECHANNEL_terrain",
        extra_lua=bomb,
    )
    fields, diags = parse_terrain_entry(root / "Mods/terrains/TheChannel/entry.lua")
    assert fields["id"] == "TheChannel"
    assert not any("pwned" in d.message for d in diags)
    inv = probe_installations(dcs_root=root, saved_games=tmp_path / "empty-sg")
    assert any(t.theatre_id == "TheChannel" for t in inv.theatres)


def test_disabled_and_refresh_enable(dcs_home: Path, saved_games: Path, tmp_path: Path):
    db = tmp_path / "inventory.sqlite"
    service = InventoryService(db_path=db, dcs_root=dcs_home, saved_games=saved_games)
    first = service.refresh()
    caucasus = next(t for t in first.theatres if t.theatre_id == "Caucasus")
    assert caucasus.state is AvailabilityState.DISABLED

    write_plugins_enabled(saved_games, {"Caucasus": True})
    cached = service.get()
    assert cached.from_cache is True
    assert next(t for t in cached.theatres if t.theatre_id == "Caucasus").state is (
        AvailabilityState.DISABLED
    )

    refreshed = service.refresh()
    assert refreshed.from_cache is False
    assert next(t for t in refreshed.theatres if t.theatre_id == "Caucasus").state is (
        AvailabilityState.AVAILABLE
    )


def test_install_uninstall_via_refresh(dcs_home: Path, saved_games: Path, tmp_path: Path):
    db = tmp_path / "inventory.sqlite"
    service = InventoryService(db_path=db, dcs_root=dcs_home, saved_games=saved_games)
    service.refresh()
    assert any(t.theatre_id == "Normandy" for t in service.get().theatres)

    # Uninstall Normandy from disk + updater
    shutil.rmtree(dcs_home / "Mods/terrains/Normandy")
    write_autoupdate(dcs_home, ["WORLD", "THECHANNEL_terrain", "CAUCASUS_terrain"])
    after = service.refresh()
    assert not any(t.theatre_id == "Normandy" for t in after.theatres)


def test_incomplete_when_updater_and_disk_disagree(tmp_path: Path):
    root = tmp_path / "DCS"
    write_autoupdate(root, ["WORLD"])  # Channel on disk but not in updater
    write_terrain(
        root, folder="TheChannel", theatre_id="TheChannel", update_id="THECHANNEL_terrain"
    )
    inv = probe_installations(dcs_root=root, saved_games=tmp_path / "sg")
    channel = next(t for t in inv.theatres if t.theatre_id == "TheChannel")
    assert channel.state is AvailabilityState.INCOMPLETE


def test_unsupported_installed_map(dcs_home: Path, saved_games: Path):
    inv = probe_installations(dcs_root=dcs_home, saved_games=saved_games)
    # Syria is on disk in the fixture but not planner-supported.
    syria = next(t for t in inv.theatres if t.theatre_id == "Syria")
    assert syria.state is AvailabilityState.AVAILABLE
    assert syria.planner_supported is False


def test_normandy_installed_and_supported(dcs_home: Path, saved_games: Path):
    inv = probe_installations(dcs_root=dcs_home, saved_games=saved_games)
    normandy = next(t for t in inv.theatres if t.theatre_id == "Normandy")
    assert normandy.state is AvailabilityState.AVAILABLE
    assert normandy.planner_supported is True


def test_caucasus_installed_and_supported(dcs_home: Path, saved_games: Path):
    inv = probe_installations(dcs_root=dcs_home, saved_games=saved_games)
    caucasus = next(t for t in inv.theatres if t.theatre_id == "Caucasus")
    assert caucasus.planner_supported is True


def test_missing_dcs_root(tmp_path: Path):
    inv = probe_installations(dcs_root=tmp_path / "missing", saved_games=tmp_path / "sg")
    assert inv.dcs_roots == ()
    assert inv.diagnostics
    assert (
        main(
            [
                "theatres",
                "--dcs-root",
                str(tmp_path / "missing"),
                "--db",
                str(tmp_path / "x.sqlite"),
            ]
        )
        == 2
    )


def test_multiple_installs_not_merged(tmp_path: Path):
    a = tmp_path / "DCS A"
    b = tmp_path / "DCS B"
    for root, theatre in ((a, "TheChannel"), (b, "Normandy")):
        write_autoupdate(root, [f"{theatre.upper()}_terrain".replace("THECHANNEL", "THECHANNEL")])
    write_autoupdate(a, ["THECHANNEL_terrain"])
    write_autoupdate(b, ["NORMANDY_terrain"])
    write_terrain(a, folder="TheChannel", theatre_id="TheChannel", update_id="THECHANNEL_terrain")
    write_terrain(b, folder="Normandy", theatre_id="Normandy", update_id="NORMANDY_terrain")

    # Probe each explicitly — multiple roots stay scoped when discovered separately.
    inv_a = probe_installations(dcs_root=a, saved_games=tmp_path / "sg")
    inv_b = probe_installations(dcs_root=b, saved_games=tmp_path / "sg")
    assert all(t.dcs_root == str(a.resolve()) for t in inv_a.theatres)
    assert all(t.dcs_root == str(b.resolve()) for t in inv_b.theatres)


def test_cli_json_and_cache(dcs_home: Path, saved_games: Path, tmp_path: Path, capsys):
    db = tmp_path / "inv.sqlite"
    code = main(
        [
            "theatres",
            "--dcs-root",
            str(dcs_home),
            "--saved-games",
            str(saved_games),
            "--db",
            str(db),
            "--refresh",
            "--json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["from_cache"] is False
    assert any(t["theatre_id"] == "TheChannel" for t in payload["theatres"])

    code = main(
        [
            "theatres",
            "--dcs-root",
            str(dcs_home),
            "--saved-games",
            str(saved_games),
            "--db",
            str(db),
            "--json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["from_cache"] is True


def test_legacy_compile_cli_still_works(tmp_path: Path):
    # Smoke: missing spec still exit 2 via legacy path
    assert main([str(tmp_path / "nope.yaml")]) == 2


def test_registry_paths_are_considered(tmp_path: Path, monkeypatch):
    root = tmp_path / "Custom DCS"
    write_autoupdate(root, ["THECHANNEL_terrain"])
    write_terrain(
        root, folder="TheChannel", theatre_id="TheChannel", update_id="THECHANNEL_terrain"
    )
    monkeypatch.setattr(
        "dcs_miz_planner.install.discover._registry_dcs_paths",
        lambda: [root],
    )
    # Empty env so Program Files candidates are skipped.
    found, diags = discover_dcs_roots(env={})
    assert found == [root.resolve()]
    assert not any("No DCS installation found" in d.message for d in diags)
