## 1. Spec schema helper

- [x] 1.1 Add shared helper (e.g. `agent/spec_schema.py`) that maps `mission_type` → compact example dict + notes/anti-patterns from `examples/*.yaml` (and/or in-package map)
- [x] 1.2 Ensure each supported type’s example validates as `MissionSpec`; clear error for unknown types

## 2. Tool surface

- [x] 2.1 Expose `get_mission_spec_schema` on `tools/surface.py` (`{ok, …}` result shape)
- [x] 2.2 Register tool in `tool_bridge` / `TOOL_DEFINITIONS` and dispatch path

## 3. Prompts and host repair

- [x] 3.1 Replace hand-maintained full CAP skeleton in system prompt with short anti-patterns + instruction to call `get_mission_spec_schema` (or host-injected derived fragment)
- [x] 3.2 Point `host_spec_repair_nudge` (plan + chat) at the shared helper; infer `mission_type` from rejected JSON when present
- [x] 3.3 Keep chat `/accept` gate unchanged (no write until accept)

## 4. Tests and docs

- [x] 4.1 Pytest: tool returns validating examples for `free_flight` / `intercept` / `cap`; unknown type errors; bridge lists the tool
- [x] 4.2 Pytest: composed prompt mentions schema tool / anti-patterns; invalid chat Spec injects derived example into history
- [x] 4.3 Update README/ARCHITECTURE/BACKLOG/`LESSONS_LEARNED` as needed; Ruff + pytest green

## 5. Acceptance

- [x] 5.1 Pytest green (111); tool + prompt/repair use derived examples from `examples/` (2026-08-01). No DCS .miz acceptance required for this agent-layer change.
