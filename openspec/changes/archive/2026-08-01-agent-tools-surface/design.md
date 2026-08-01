## Context

Catalog SQLite (`catalog_*` + theatre join) and shared validate/compile are in place.
The future NL agent needs a small, stable set of callable tools — not ad-hoc imports of
`CatalogService`, `validation`, and `PyDCSCompiler`.

## Goals / Non-Goals

**Goals:**

- Five tools with clear inputs/outputs: `find_airfield`, `get_aircraft_details`,
  `list_mission_options`, `validate_mission_spec`, `compile_mission`.
- Query tools read the known catalog (ensure sync if empty); theatre options use offerable join.
- Validate/compile stay registry- and install-backed (existing engines); tools only wrap.
- JSON-serializable results suitable for later LLM tool calling.
- Tests + minimal smoke path (Python API; optional `dcs-miz tools …` if cheap).

**Non-Goals:**

- LLM provider, MCP server, conversation loop, squadron voice.
- Prefs/history recording.
- Changing Mission Spec schema or inventing DCS ids.
- Full “planning knobs” productization (`mission-option-catalog` remains a later change).

## Decisions

1. **Module: `src/dcs_miz_planner/tools/`**
   - One façade (`surface.py` or `__init__.py` exports) so agent code imports from
     `dcs_miz_planner.tools` only.
   - Alternative considered: hang methods on `CatalogService` — rejected; validate/compile
     are not catalog concerns.

2. **Lookups → catalog; validate/compile → existing APIs**
   - `find_airfield` / `get_aircraft_details` / `list_mission_options` use `CatalogService`
     (auto `ensure_synced`).
   - `list_mission_options` returns a structured bag of enum lists + offerable theatres
     (and maybe known weather/aircraft counts) — enough for the agent to ask/suggest;
     not a second Spec schema.
   - `validate_mission_spec` accepts a path or already-loaded dict/YAML path via loader;
     returns the same multi-error shape as today (ok + errors list).
   - `compile_mission` loads Spec, validates via compiler path, writes `.miz`; returns path
     or structured failure.

3. **Error model**
   - Not-found lookups return structured `{ok: false, error: …}` (or raise a small
     `ToolError`) — prefer structured results for agent friendliness; pick one style and
     use everywhere.
   - Decision at apply: **structured result dicts** with `ok` bool (easier for JSON tools).

4. **CLI**
   - Prefer Python tests as primary acceptance; add `dcs-miz tools <name> …` only if it
     stays thin. If CLI bloats the change, ship API + pytest only.

5. **No new dependencies** — stdlib + existing package.

## Risks / Trade-offs

- [Agent expects rich option catalog] → Document that `list_mission_options` is v1 enums +
  offerable theatres; `#9` expands later.
- [Tools drift from CLI] → Tools call the same services as CLI; tests cover examples.
- [Empty catalog DB] → `ensure_synced` on first query tool call.

## Migration Plan

1. Implement tools + tests; update ARCHITECTURE/README/BACKLOG.
2. Accept via pytest (and optional CLI) on Manston examples — no new DCS ME requirement
   unless compile regresses.
3. Next change: `nl-to-spec-agent` binds to these functions.

## Open Questions

- Exact CLI shape — **resolved at apply:** API + pytest only (no `dcs-miz tools` CLI).
