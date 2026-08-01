## Why

Catalog and agent tools are ready; the product promise is still unmet: natural language
should become a validated Mission Spec (then deterministic `.miz`). This change adds the
first real planning agent that uses structured outputs and the existing tool surface —
without letting the LLM write DCS Lua or invent unverified ids.

## What Changes

- Add an NL→Spec agent loop that:
  - accepts a user prompt (CLI and/or Python API)
  - may call `dcs_miz_planner.tools` (lookups, options, validate, compile)
  - emits a Mission Spec (YAML file and/or in-memory model) via structured output
- Provider: OpenAI-compatible chat API (API key via env); pluggable enough to swap later
- Scope of missions the agent may plan in v1: **free_flight** and **intercept** on
  **TheChannel** with known catalog aircraft/airfields only
- Tests with a fake/stub LLM (no network in CI); optional live smoke when key is set
- Docs: how to run, env vars, principle reminder (AI plans / software compiles)

**Non-goals:** squadron-commander voice (`#11`), prefs/history (`#8b`), FastAPI/UI,
MCP server, historical validation, new mission types, expanding known YAML,
multi-user auth, PostgreSQL.

**Acceptance:** From a prompt like “cold Spitfire free flight at Manston, sunny, 09:00”,
produce a Spec that validates and compiles; open the `.miz` in DCS ME / Instant Action
when using a live API key. CI acceptance is the stubbed path + validate/compile.

## Capabilities

### New Capabilities
- `nl-agent`: Natural-language planning agent that uses tools + structured Mission Spec
  output; never emits mission Lua.

### Modified Capabilities
- (none — tools, catalog, validation, and compiler requirements unchanged)

## Impact

- New package area (e.g. `src/dcs_miz_planner/agent/`)
- Optional new dependency: official OpenAI Python SDK (or httpx + JSON schema) — decide in design
- CLI subcommand under `dcs-miz`
- Env: API key + model name; never commit secrets
- Unlocks richer agent work (voice, prefs) on a working plan→Spec path
