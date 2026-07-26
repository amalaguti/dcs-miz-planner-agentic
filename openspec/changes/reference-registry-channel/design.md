## Context

After `mission-spec-schema`, free-flight Specs are versioned and strict, but DCS Channel facts still sit in `reference.py` module constants. Compiler, future validator, and agent tools must share one source of truth with exact ids (Manston=5, `SpitfireLFMkIX`, `TheChannel`, radio MHz from stock missions).

## Goals / Non-Goals

**Goals:**

- Committed Channel registry data + Python lookup API.
- Compiler uses that API for airfield / aircraft / radio / theatre / weather-preset resolution.
- Manston free-flight still compiles and loads in DCS.
- Clear errors for unknown registry keys.

**Non-Goals:**

- SQLite database, install probing, full payload catalogues from disk, landmarks dump, validation-engine productization.

## Decisions

1. **YAML as source of truth (not SQLite yet)**
   - Rationale: diffable in PRs, no generate step, matches concept-doc `*.json`/`*.yaml` registry idea; agent can call the same Python API. SQLite can wrap the same data later if SQL is needed.
   - Alternative: SQLite only — rejected for reviewability and tooling friction.
   - Alternative: keep Python dicts — rejected; not a shareable “registry” artifact.

2. **Layout:** `src/dcs_miz_planner/data/channel/` (packaged data)
   - Files e.g. `airfields.yaml`, `aircraft.yaml`, `weather_presets.yaml` (and optional `payloads.yaml` stub).
   - Loaded via `importlib.resources` so installs work without assuming CWD.

3. **API:** `ChannelRegistry` (or module functions) with:
   - `airdrome_id(name)`, `list_airfields()`, `get_aircraft(id)`, `radio_mhz(id)`, `has_theatre(id)`, `weather_preset(name)`
   - Fail with `KeyError` / typed errors listing known keys (same UX as today).

4. **`reference.py` becomes a thin re-export** during migration so existing imports keep working, then compiler switches to registry explicitly.

5. **Payloads:** optional YAML listing verified Spitfire CLSID names only if we have trusted values; free-flight still does not apply payloads; do **not** re-enable PyDCS install payload scanning (LESSONS_LEARNED).

6. **Clipped-wing `SpitfireLFMkIXCW`:** keep in aircraft table as a known id (already in `KNOWN_AIRCRAFT`) but do not require example missions for it.

7. **Landmarks/cities:** omit or empty stub file — do not invent coordinates.

## Risks / Trade-offs

- [Incomplete airfield list vs PyDCS Channel terrain] → Start from current `CHANNEL_AIRDROME_IDS`; document that expansion is data PRs, not compiler hacks.
- [YAML drift from PyDCS] → Unit tests assert Manston=5 and known aircraft; compile Manston as acceptance.
- [Agents invent landmarks] → Don’t ship empty landmark API that returns success; omit until data exists.

## Migration Plan

1. Add YAML + loader + API; mirror current constants.
2. Point compiler at registry; keep `reference.py` façade.
3. Tests for lookups + existing Manston compile tests.
4. Rollback: revert package; constants still recoverable from git.

## Open Questions

- Whether later `validation-engine` imports registry directly or via a `validate(spec, registry)` façade — leave to that change.
- SQLite export as a follow-on research/agent convenience — not this change.
