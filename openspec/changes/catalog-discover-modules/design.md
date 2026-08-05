## Context

Theatre inventory already uses probe → SQLite replace → get/refresh. Aircraft soft-warn
(`#38`) maps Spec ids → folders but does not harvest. Local installs change rarely.

## Goals / Non-Goals

**Goals:**
- Cache aircraft folders on the same inventory refresh as theatres
- Join known catalog aircraft with discovered folders for CLI/agent listing
- Filter shared non-aircraft dirs under `WWII Units`

**Non-Goals:**
- Auto-promote; enable-state; new Spec aircraft support

## Decisions

1. **Same `InventoryService.refresh()`** writes theatres + `aircraft_modules` (one
   `scan_meta`). Bump `SCHEMA_VERSION` to 2.
2. **Scan roots:** `Mods/aircraft`, `CoreMods/WWII Units`, `CoreMods/aircraft`.
   Skip shared WWII folders (`Encyclopedia`, `Weapons`, `l10n`, …). Under
   `Mods/aircraft` / `CoreMods/aircraft`, require `entry.lua` when present pattern
   applies; WWII Units use skip-list only (often no entry.lua).
3. **Ids:** Map folders via reverse `_AIRCRAFT_FOLDERS` to Spec ids; unmapped folders
   appear as discovered-only keyed by folder name. Never insert into YAML.
4. **Join:** Mirror `TheatreAvailabilityView` → `AircraftAvailabilityView`
   (`known`, `installed`, `planner_supported`, `offerable`, `source`, `dcs_root`).

## Risks / Trade-offs

- [Schema bump clears old cache] → Expected; next `--refresh` rebuilds
- [Weapon/pack folders slip through] → entry.lua filter + skip list; refine later
- [Folder name ≠ Spec id] → reverse map for Channel known set; discovered-only keep folder name
