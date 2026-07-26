"""Scan a DCS install and classify theatre availability."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from ..registry import get_channel_registry
from .discover import discover_dcs_roots, discover_saved_games_roots
from .models import AvailabilityState, Diagnostic, TheatreInventory, TheatreRecord
from .parse import parse_autoupdate_modules, parse_plugins_enabled, parse_terrain_entry


def _merge_plugin_overrides(
    saved_games_roots: list[Path],
) -> tuple[dict[str, bool], list[Diagnostic]]:
    merged: dict[str, bool] = {}
    diagnostics: list[Diagnostic] = []
    for root in saved_games_roots:
        path = root / "Config" / "pluginsEnabled.lua"
        overrides, diags = parse_plugins_enabled(path)
        diagnostics.extend(diags)
        for key, value in overrides.items():
            if key not in merged:
                merged[key] = value
    return merged, diagnostics


def _classify(
    *,
    theatre_id: str | None,
    update_id: str | None,
    has_entry: bool,
    modules: set[str],
    plugin_overrides: dict[str, bool],
    plugin_id: str | None,
) -> AvailabilityState:
    if not theatre_id:
        return AvailabilityState.UNKNOWN

    in_updater = bool(update_id and update_id in modules)
    if has_entry and update_id and not in_updater:
        return AvailabilityState.INCOMPLETE
    if in_updater and not has_entry:
        return AvailabilityState.INCOMPLETE
    if not has_entry and not in_updater:
        return AvailabilityState.UNKNOWN

    for key in (theatre_id, plugin_id):
        if key and key in plugin_overrides and plugin_overrides[key] is False:
            return AvailabilityState.DISABLED

    if has_entry and in_updater:
        return AvailabilityState.AVAILABLE
    return AvailabilityState.UNKNOWN


def probe_installations(
    *,
    dcs_root: Path | str | None = None,
    saved_games: Path | str | None = None,
    env: dict[str, str] | None = None,
) -> TheatreInventory:
    """Scan selected or discovered installs and return a typed inventory (no cache I/O)."""
    diagnostics: list[Diagnostic] = []
    dcs_roots, dcs_diags = discover_dcs_roots(explicit=dcs_root, env=env)
    diagnostics.extend(dcs_diags)
    sg_roots, sg_diags = discover_saved_games_roots(explicit=saved_games, env=env)
    diagnostics.extend(sg_diags)

    plugin_overrides, plugin_diags = _merge_plugin_overrides(sg_roots)
    diagnostics.extend(plugin_diags)

    supported_set = set(get_channel_registry().list_theatres())
    theatres: list[TheatreRecord] = []
    sg_root_str = str(sg_roots[0]) if sg_roots else None

    for root in dcs_roots:
        modules: set[str] = set()
        cfg = root / "autoupdate.cfg"
        if cfg.is_file():
            modules, mod_diags = parse_autoupdate_modules(cfg)
            diagnostics.extend(mod_diags)
        else:
            diagnostics.append(Diagnostic("autoupdate.cfg missing", str(cfg)))

        terrains_dir = root / "Mods" / "terrains"
        seen_update_ids: set[str] = set()

        if terrains_dir.is_dir():
            for terrain_dir in sorted(p for p in terrains_dir.iterdir() if p.is_dir()):
                entry = terrain_dir / "entry.lua"
                fields, entry_diags = parse_terrain_entry(entry)
                diagnostics.extend(entry_diags)
                theatre_id = fields.get("id")
                update_id = fields.get("update_id")
                plugin_id = fields.get("plugin_id") or theatre_id
                if update_id:
                    seen_update_ids.add(update_id)

                state = _classify(
                    theatre_id=theatre_id,
                    update_id=update_id,
                    has_entry=bool(theatre_id),
                    modules=modules,
                    plugin_overrides=plugin_overrides,
                    plugin_id=plugin_id,
                )
                if not theatre_id:
                    theatre_id = terrain_dir.name
                    state = AvailabilityState.UNKNOWN

                evidence: list[str] = []
                if update_id and update_id in modules:
                    evidence.append(f"updater:{update_id}")
                if entry.is_file():
                    evidence.append(f"entry:{entry}")
                if plugin_id and plugin_id in plugin_overrides:
                    evidence.append(f"pluginsEnabled[{plugin_id}]={plugin_overrides[plugin_id]}")

                theatres.append(
                    TheatreRecord(
                        theatre_id=theatre_id,
                        update_id=update_id,
                        dcs_root=str(root),
                        state=state,
                        planner_supported=theatre_id in supported_set,
                        terrain_path=str(terrain_dir),
                        saved_games_root=sg_root_str,
                        evidence=tuple(evidence),
                    )
                )

        for module in sorted(m for m in modules if m.endswith("_terrain")):
            if module in seen_update_ids:
                continue
            theatres.append(
                TheatreRecord(
                    theatre_id=module.removesuffix("_terrain"),
                    update_id=module,
                    dcs_root=str(root),
                    state=AvailabilityState.INCOMPLETE,
                    planner_supported=False,
                    terrain_path=None,
                    saved_games_root=sg_root_str,
                    evidence=(f"updater-only:{module}",),
                )
            )

    return TheatreInventory(
        scanned_at=datetime.now(UTC),
        dcs_roots=tuple(str(p) for p in dcs_roots),
        saved_games_roots=tuple(str(p) for p in sg_roots),
        theatres=tuple(theatres),
        diagnostics=tuple(diagnostics),
        from_cache=False,
    )
