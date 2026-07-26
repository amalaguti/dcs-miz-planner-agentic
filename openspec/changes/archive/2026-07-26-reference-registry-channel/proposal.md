## Why

The Mission Spec is now versioned, but Channel facts still live as ad-hoc dicts in `reference.py`. Registry, validation, and agent tools need one queryable source of truth for airfields, aircraft, weather presets, and related ids — without inventing DCS spellings. Building that now unblocks `validation-engine` and later agent lookups.

## What Changes

- Introduce a Channel **reference registry**: committed, reviewable data plus a small Python query API shared by the compiler (and later the agent/validator).
- Move today’s airfield / aircraft / radio / theatre / weather-preset facts out of opaque module constants into that registry.
- Document verified Channel airfields (including Manston → `airdromeId` 5) and WWII aircraft ids already in use.
- Seed Spitfire payload CLSID entries only where verified; free-flight compile remains payload-free (PyDCS payload scan stays disabled).
- Keep Manston cold free-flight compile + in-game load as the regression acceptance check.

## Non-goals

- Full semantic validation engine (M2 `#5`) or golden fixture platform (M2 `#6`).
- Agent tools / NL planning / SQLite-backed MCP surface.
- Multi-theatre registries; Normandy; landmarks/cities dump beyond a thin optional stub if data is thin.
- Scanning the live DCS install for payloads or theatres (`installed-theatres-probe` is separate).
- Combat mission types, triggers, or LLM-authored Lua.
- Promoting gitignored `research/` dumps wholesale into the product registry.

## Capabilities

### New Capabilities

- `reference-registry`: Queryable Channel reference data (airfields, aircraft, weather presets, radio defaults, optional payload CLSIDs) with a stable lookup API; exact DCS ids only.

### Modified Capabilities

- `miz-compiler`: Resolve theatre/airfield/aircraft/radio (and weather preset names) through the Channel registry API instead of private constants in `reference.py`.

## Impact

- New data files + registry package; `reference.py` becomes a thin façade or is replaced.
- Compiler imports switch to registry lookups; Manston example must still compile and open in DCS Mission Editor / Instant Action.
- Unblocks `validation-engine` and `agent-tools-surface`.
- Settles backlog decision: **YAML tables as source of truth** (diffable); SQLite deferred until an agent needs SQL.
