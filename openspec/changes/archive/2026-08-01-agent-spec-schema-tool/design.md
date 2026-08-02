## Context

`MissionSpec` in `models.py` (Pydantic, `extra=forbid`) is the structural SoT for
validate/compile. The NL agent currently embeds a hand-written CAP JSON skeleton in
`SPEC_JSON_SHAPE` (`agent/prompts.py`) plus a host repair nudge. That fixed live chat
inventing flat JSON, but each new `mission_type` would require another hand skeleton.

Catalog SQLite is a query cache synced from YAML/enums — not a second schema SoT
(`LESSONS_LEARNED.md`). Tools already expose catalog lookups and `validate_mission_spec`.

## Goals / Non-Goals

**Goals:**

- One code path that builds a compact, mission-type-scoped Spec example + notes from
  `MissionSpec` and/or `examples/*.yaml`.
- Agent tool `get_mission_spec_schema(mission_type)` returns that payload.
- System prompt keeps a short always-on anti-pattern reminder; full type example comes
  from the helper (prompt fragment and/or tool) and the host repair nudge.
- Adding a mission type updates models/examples → schema helper follows without a
  separate prompt edit checklist (beyond type allow-list).

**Non-Goals:**

- Structured outputs / Responses API migration.
- Catalog as schema SoT (optional derived cache only; skip cache in v1 if unused).
- New mission types or compiler work.
- Replacing `validate_mission_spec` (validation stays the acceptance gate).

## Decisions

1. **Derivation source: examples first, Pydantic for envelope rules**
   - Prefer loading `examples/manston_*.yaml` (or a small in-package example map keyed by
     `mission_type`) and serializing to JSON for the compact example.
   - Supplement with fixed anti-pattern notes and required-field checklist generated from
     known `MissionSpec` structure (not dumping raw `model_json_schema()` into the LLM).
   - **Why:** Examples are already valid Specs and human-readable; raw JSON Schema is
     noisy for chat models. **Alt:** generate solely from Pydantic — rejected as primary
     because of verbosity and weak “filled example” signal.

2. **Tool name and API: `get_mission_spec_schema(mission_type: str)`**
   - Returns `{ok, mission_type, example, notes, anti_patterns}` (names flexible but
     JSON-friendly). Unknown / unsupported type → structured error.
   - **Why:** Matches existing tool surface style. **Alt:** only inject into system prompt
     with no tool — rejected because models skip reading long prompts and chat may need
     on-demand refresh mid-session.

3. **Prompt strategy: thin always-on + derived fragment**
   - Replace the full CAP skeleton in `SPEC_JSON_SHAPE` with a short DO-NOT list +
     pointer to call `get_mission_spec_schema` before emitting Spec JSON.
   - `host_spec_repair_nudge` and optional Spec-lock hint MUST include the derived
     example for the inferred or last-attempted `mission_type` (default `cap` or from
     partial JSON when present).
   - **Why:** Keeps system prompt stable as types grow; repair path already injects text.

4. **No catalog schema table in v1**
   - Compute on the fly in-process; catalog sync unchanged unless a later change wants
     `/catalog` to show schema summaries.
   - **Why:** Avoid premature DB projection; SoT stays code/examples. **Alt:** sync
     derived rows into `catalog_*` — deferred.

5. **Shared helper module**
   - e.g. `agent/spec_schema.py` used by tools, prompts, session, planner — single
     implementation for example + notes.

## Risks / Trade-offs

- **[Risk] Model still skips the tool** → Mitigation: host repair nudge always injects
  the derived example; thin prompt still lists fatal anti-patterns.
- **[Risk] Example YAML drifts from model after a Spec field rename** → Mitigation:
  pytest loads each type example through `MissionSpec.model_validate`; CI fails on drift.
- **[Risk] Wrong mission_type in repair nudge** → Mitigation: parse `mission_type` from
  rejected JSON when present; else ask tool/default to last draft or `free_flight`.
- **[Trade-off] Examples are Channel/Manston-centric** → Acceptable for MVP; notes say
  ids must still come from tools/prefs.

## Migration Plan

1. Implement helper + tool + bridge; keep tests green.
2. Switch prompts/repair to helper; remove hand CAP skeleton.
3. No DB migration. Rollback = revert commit (prompt skeleton can be restored if needed).

## Open Questions

- None blocking: defer structured outputs and catalog cache to follow-ons.
