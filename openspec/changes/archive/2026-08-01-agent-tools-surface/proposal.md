## Why

The catalog SQLite layer exists, but nothing yet exposes a stable, agent-callable tool
surface over lookups and the existing validate/compile path. Without that, `nl-to-spec-agent`
has no clean contract. This change adds thin tools now so the later agent can bind without
rewriting core modules.

## What Changes

- Add a Python tool module with typed callables (and JSON-friendly results) for:
  - `find_airfield` — lookup known airfields (catalog; optional name filter)
  - `get_aircraft_details` — known aircraft id + radio_mhz (catalog)
  - `list_mission_options` — Spec enums / planning knobs already in catalog (mission types,
    start types, weather, coalitions, offerable theatres, etc.)
  - `validate_mission_spec` — wrap shared `validate_mission_spec` (registry/install-backed)
  - `compile_mission` — wrap `PyDCSCompiler` to write a `.miz`
- Optional thin CLI or smoke entry so tools can be exercised without an LLM
- Tests for each tool; docs note tools are for the agent, not a second SoT
- **Non-goals:** NL agent, LLM/MCP wiring, prefs/history, expanding YAML known set,
  aircraft module discovery, new mission types, changing validate/compile semantics

Acceptance for this change is **CLI/API** (tool calls return correct catalog and
validate/compile results for checked-in examples). Opening a `.miz` in DCS is only needed
if compile output regresses — reuse existing Manston examples.

## Capabilities

### New Capabilities
- `agent-tools`: Stable tool functions the future agent (and tests/CLI) use to query the
  catalog and run validate/compile without importing internal module details.

### Modified Capabilities
- (none — catalog, validation, and compiler requirements stay as-is; tools wrap them)

## Impact

- New package area under `src/dcs_miz_planner/` (e.g. `tools/`)
- Depends on `catalog`, `validation`, `compiler`, `loader` — no PyDCS outside compiler
- `docs/ARCHITECTURE.md`, README, BACKLOG (`idea` → `proposed`/`building`)
- Unlocks `nl-to-spec-agent`; optional later MCP adapter maps to the same functions
