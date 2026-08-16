"""Aircraft module harvest into inventory cache + catalog join."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from test_installed_theatres import write_autoupdate, write_terrain

from dcs_miz_planner.catalog import CatalogService, join_aircraft_views
from dcs_miz_planner.cli import main
from dcs_miz_planner.install import InventoryService
from dcs_miz_planner.install.aircraft_modules import harvest_aircraft_modules
from dcs_miz_planner.install.models import AircraftModuleRecord, TheatreInventory
from dcs_miz_planner.install.probe import probe_installations


def _write_aircraft_tree(root: Path) -> None:
    spit = root / "Mods" / "aircraft" / "SpitfireLFMkIX"
    spit.mkdir(parents=True)
    (spit / "entry.lua").write_text("-- spit\n", encoding="utf-8")
    ww2 = root / "CoreMods" / "WWII Units"
    (ww2 / "Bf-109K-4").mkdir(parents=True)
    (ww2 / "Weapons").mkdir(parents=True)
    (ww2 / "FW-190A-8").mkdir(parents=True)
    other = root / "CoreMods" / "aircraft" / "Su-25T"
    other.mkdir(parents=True)
    (other / "entry.lua").write_text("-- su\n", encoding="utf-8")
    # No entry.lua → ignored under CoreMods/aircraft
    (root / "CoreMods" / "aircraft" / "AircraftWeaponPack").mkdir(parents=True)


def test_harvest_skips_shared_wwii_dirs(tmp_path: Path) -> None:
    root = tmp_path / "DCS"
    _write_aircraft_tree(root)
    modules = harvest_aircraft_modules([root])
    names = {(m.source, m.folder_name) for m in modules}
    assert ("Mods/aircraft", "SpitfireLFMkIX") in names
    assert ("CoreMods/WWII Units", "Bf-109K-4") in names
    assert ("CoreMods/WWII Units", "FW-190A-8") in names
    assert ("CoreMods/aircraft", "Su-25T") in names
    su = next(m for m in modules if m.folder_name == "Su-25T")
    assert su.known_aircraft_ids == ("Su-25T",)
    assert ("CoreMods/WWII Units", "Weapons") not in names
    assert ("CoreMods/aircraft", "AircraftWeaponPack") not in names
    spit = next(m for m in modules if m.folder_name == "SpitfireLFMkIX")
    assert "SpitfireLFMkIX" in spit.known_aircraft_ids
    assert "SpitfireLFMkIXCW" in spit.known_aircraft_ids
    fw = next(m for m in modules if m.folder_name == "FW-190A-8")
    assert fw.known_aircraft_ids == ("FW-190A8",)


def test_probe_and_cache_aircraft_modules(tmp_path: Path) -> None:
    root = tmp_path / "DCS World"
    write_autoupdate(root, ["WORLD", "THECHANNEL_terrain"])
    write_terrain(
        root, folder="TheChannel", theatre_id="TheChannel", update_id="THECHANNEL_terrain"
    )
    _write_aircraft_tree(root)
    db = tmp_path / "inventory.sqlite"
    svc = InventoryService(db_path=db, dcs_root=root, saved_games=tmp_path / "sg")
    fresh = svc.refresh()
    assert fresh.from_cache is False
    assert any(m.folder_name == "SpitfireLFMkIX" for m in fresh.aircraft_modules)
    assert not any(m.folder_name == "Weapons" for m in fresh.aircraft_modules)

    cached = svc.get()
    assert cached.from_cache is True
    assert {m.folder_name for m in cached.aircraft_modules} == {
        m.folder_name for m in fresh.aircraft_modules
    }


def test_join_aircraft_known_and_discovered() -> None:
    inventory = TheatreInventory(
        scanned_at=datetime(2026, 8, 5, tzinfo=UTC),
        dcs_roots=("C:/FakeDCS",),
        saved_games_roots=(),
        theatres=(),
        aircraft_modules=(
            AircraftModuleRecord(
                folder_name="SpitfireLFMkIX",
                dcs_root="C:/FakeDCS",
                source="Mods/aircraft",
                folder_path="C:/FakeDCS/Mods/aircraft/SpitfireLFMkIX",
                known_aircraft_ids=("SpitfireLFMkIX", "SpitfireLFMkIXCW"),
                planner_supported=True,
            ),
            AircraftModuleRecord(
                folder_name="Su-25T",
                dcs_root="C:/FakeDCS",
                source="CoreMods/aircraft",
                folder_path="C:/FakeDCS/CoreMods/aircraft/Su-25T",
            ),
        ),
    )
    known = frozenset({"SpitfireLFMkIX", "Bf-109K-4"})
    views = {v.aircraft_id: v for v in join_aircraft_views(known, inventory)}
    assert views["SpitfireLFMkIX"].known is True
    assert views["SpitfireLFMkIX"].installed is True
    assert views["SpitfireLFMkIX"].offerable is True
    assert views["SpitfireLFMkIXCW"].known is False
    assert views["SpitfireLFMkIXCW"].installed is True
    assert views["Bf-109K-4"].known is True
    assert views["Bf-109K-4"].installed is False
    assert views["Su-25T"].known is False
    assert views["Su-25T"].installed is True
    assert views["Su-25T"].offerable is False


def test_catalog_cli_aircraft_join(tmp_path: Path) -> None:
    db = tmp_path / "planner.sqlite"
    assert main(["catalog", "sync", "--db", str(db)]) == 0

    root = tmp_path / "DCS World"
    write_autoupdate(root, ["WORLD", "THECHANNEL_terrain"])
    write_terrain(
        root, folder="TheChannel", theatre_id="TheChannel", update_id="THECHANNEL_terrain"
    )
    _write_aircraft_tree(root)
    assert (
        main(
            [
                "theatres",
                "--dcs-root",
                str(root),
                "--db",
                str(db),
                "--refresh",
                "--json",
            ]
        )
        == 0
    )

    import json
    import sys
    from io import StringIO

    buf = StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        assert main(["catalog", "list", "--type", "aircraft", "--db", str(db), "--json"]) == 0
    finally:
        sys.stdout = old
    payload = json.loads(buf.getvalue())
    rows = {r["aircraft_id"]: r for r in payload["rows"]}
    assert rows["SpitfireLFMkIX"]["known"] is True
    assert rows["SpitfireLFMkIX"]["installed"] is True
    assert rows["Su-25T"]["known"] is True
    assert rows["Su-25T"]["installed"] is True
    assert "note" not in payload

    known_only = CatalogService(db_path=db).list_aircraft(include_discovered=False)
    assert all(v.known for v in known_only)
    assert any(v.aircraft_id == "Su-25T" for v in known_only)


def test_probe_includes_aircraft_without_terrains(tmp_path: Path) -> None:
    root = tmp_path / "DCS"
    write_autoupdate(root, ["WORLD"])
    _write_aircraft_tree(root)
    inv = probe_installations(dcs_root=root, saved_games=tmp_path / "sg")
    assert any(m.folder_name == "Su-25T" for m in inv.aircraft_modules)
