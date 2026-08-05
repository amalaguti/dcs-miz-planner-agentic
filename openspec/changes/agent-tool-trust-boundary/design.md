## Context

C1 — LLM tools mutate disk/memory. Local single-user threat model; still harden.

## Decisions

1. Default `TOOL_DEFINITIONS` / `default_tools()` = planning/read-only only.
2. Keep mutating handlers behind `allow_mutating=True` for hermetic tests/admin.
3. Compile output must be under repo `out/` (resolve + `relative_to`).
4. Hosts (`planner.record_plan`, CLI feedback) unchanged — direct memory service.

## Risks

- [Agent cannot self-compile] → Intended; `/accept` + CLI compile remain.
- [Tests call dispatch compile] → Pass `allow_mutating=True` or call surface API.
