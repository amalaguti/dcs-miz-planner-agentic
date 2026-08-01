## Why

The NL agent can plan from catalog facts, but it forgets the pilot: preferred airfield,
start type, voice, and what already flew. Without local prefs, generation history, and
light satisfaction feedback, every session starts cold and cannot improve suggestions.

## What Changes

- Persist **user preferences**, **mission-generation history**, and **satisfaction
  feedback** in the same local SQLite file as install/catalog, under a distinct
  `user_*` table namespace (never wiped by `catalog sync`)
- Expose agent tools to **read/update prefs**, **record a generation**, and **record
  feedback** (same `{ok: …}` dict style as existing tools)
- Teach the NL planner to **consult prefs** when filling unset knobs and to **append
  history** on successful (and clearly failed) plans
- Optional thin CLI for humans to inspect/set prefs and leave feedback without the LLM
- Docs: BACKLOG/ARCHITECTURE/README status for this memory layer

**Non-goals:** squadron-commander voice implementation (`#11` — prefs may store a
voice key for later); ML “learning”; multi-user accounts or cloud sync; UI/MCP;
auto-promoting prefs into YAML known; Normandy/multi-theatre; changing compile/validate
SoT; post-flight telemetry from DCS itself.

**Acceptance:** pytest covers store round-trips and tool/planner hooks (stub LLM). No
new `.miz` content required for this change.

## Capabilities

### New Capabilities
- `user-memory`: Local prefs, generation history, and satisfaction feedback in SQLite
  (distinct from `catalog_*` / install tables), with clear schema versioning.

### Modified Capabilities
- `agent-tools`: Add prefs/history/feedback tools to the importable tools surface.
- `nl-agent`: Planner consults prefs and records generation outcomes.

## Impact

- New module area (e.g. `src/dcs_miz_planner/memory/` or `prefs/`) using
  `install.store.default_db_path()`
- Extend `tools/surface.py`, `agent/tool_bridge.py`, `agent/planner.py`, prompts
- Optional CLI subcommands under `dcs-miz`
- Tests under `tests/`; docs touch BACKLOG, ARCHITECTURE, README
