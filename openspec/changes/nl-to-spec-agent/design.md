## Context

Tools + catalog exist. Concept doc targets OpenAI structured outputs + tool calling.
The agent must plan Mission Specs only; PyDCS remains the sole `.miz` writer.

## Goals / Non-Goals

**Goals:**

- End-to-end: NL prompt → (tools) → Mission Spec YAML → optional validate/compile.
- Bind the five existing tools as LLM tools; refuse invented DCS ids (validate catches;
  system prompt + tool use reduce inventing).
- Stub LLM for CI; real OpenAI-compatible client behind env config.
- CLI: `dcs-miz plan "<prompt>"` (write Spec; `--compile` optional).

**Non-Goals:**

- Voice persona, prefs/history, web UI, MCP, new mission types, historical engine.

## Decisions

1. **Provider: OpenAI Python SDK (`openai`) as optional/extra dependency**
   - Concept doc names OpenAI; SDK gives tool calling + structured outputs.
   - Alternative: raw httpx — more code, weaker ergonomics. Rejected for v1.
   - Put `openai` in a dependency group or optional extra (`agent`) so core compile
     path stays lean for users who only compile YAML. **Prefer:** `dependency-groups`
     `agent` or project optional dependency — resolve at apply (`uv add openai` in
     main deps is OK if README documents the key; slight dep weight acceptable for MVP).

2. **Architecture: `agent/` package**
   - `llm.py` — thin client protocol + OpenAI adapter + `StubLLM` for tests
   - `prompts.py` — system instructions (Channel-only, known ids via tools, no Lua)
   - `tool_bridge.py` — map OpenAI tool defs → `dcs_miz_planner.tools.*`
   - `planner.py` — loop: messages → model → tool calls → final structured Spec
   - Final Spec: Pydantic `MissionSpec` (structured output JSON) then dump YAML

3. **Loop shape (v1)**
   - Multi-step tool calling until model returns a final Spec object (or max turns).
   - Always run `validate_mission_spec` on the result before writing YAML; if invalid,
     one repair turn with errors (optional but recommended).
   - Compile only if user passes `--compile` (calls compile tool / compiler).

4. **Config via env**
   - `OPENAI_API_KEY` (required for live)
   - `DCS_MIZ_LLM_MODEL` (default e.g. `gpt-4o-mini` or current cheap structured model)
   - Optional `OPENAI_BASE_URL` for compatible proxies
   - Never log the key

5. **Stub path**
   - `StubLLM` returns a canned Manston free-flight Spec (and can serve scripted tool
     call sequences). Default in pytest; live tests marked and skipped without key.

6. **CLI**
   - `dcs-miz plan "…"` → `out/<stem>.yaml` (and `.miz` with `--compile`)
   - `--stub` flag for offline demo without API key

## Risks / Trade-offs

- [Model invents ids] → Tools + validate gate; system prompt forbids invention.
- [API cost / flaky live tests] → Stub in CI; live optional.
- [openai dep weight] → Document; keep compiler usable without calling agent.
- [Over-scoped agent] → Hard-limit v1 to free_flight + intercept + TheChannel.

## Migration Plan

1. Implement stub planner + tests (no network).
2. Wire OpenAI adapter + CLI; live smoke with Manston prompt → DCS.
3. Later: prefs tools, voice, richer options catalog.

## Open Questions

- Exact default model id — **resolved:** `gpt-4o-mini` via `DCS_MIZ_LLM_MODEL` override.
- Whether repair-on-validate-failure is mandatory in v1 — **yes, one repair attempt**.
