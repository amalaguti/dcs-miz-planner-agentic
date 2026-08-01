## Why

The NL agent can already plan thin Specs, but its creative vocabulary is limited to raw
enums. We need a richer, queryable **mission option catalog** — named planning knobs with
descriptions and support level — so the agent (and user) can invent situations that stay
grounded in what Channel free_flight / intercept can actually honor.

## What Changes

- Add packaged planning-option definitions (YAML or similar) for Channel-era missions:
  families such as mission type, start type, weather, time-of-day bands, opposition
  density (intercept), payload families (stub/limited), and related knobs from the backlog
  intent (ROE seeds as **future** if not Spec-backed yet).
- Sync those options into SQLite `catalog_*` (or dedicated `catalog_planning_options`)
  alongside existing known catalog sync.
- Enrich agent/CLI listing (`list_mission_options` and/or catalog list) with family,
  value, description, and **support** (`supported` | `advisory` | `future`).
- **supported** = maps to current Mission Spec + compiler; **advisory** = guidance for
  Spec fields we already have (e.g. dawn → `06:00`); **future** = do not claim compile.

**Non-goals:** Normandy/multi-theatre compile; prefs/history; squadron voice; inventing
unsupported Spec fields that compile silently; enabling extra DCS maps as a requirement.

Acceptance: catalog sync/list (and tool) shows enriched options; stub/live plan still works;
no claim that future knobs compile.

## Capabilities

### New Capabilities
- `mission-options`: Packaged + synced planning option catalog with support levels for
  agent/user discovery.

### Modified Capabilities
- `agent-catalog`: Sync/list includes planning options (or related tables).
- `agent-tools`: `list_mission_options` returns richer option families (not enum lists only).

## Impact

- New data under `data/channel/` (or `data/planning/`); catalog sync/store; tools; docs
- Agent prompt may reference consulting the option catalog
- Does **not** require Normandy or other DCS modules for this change
