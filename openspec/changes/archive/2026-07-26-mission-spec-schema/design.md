## Context

M1 delivered a minimal Pydantic `MissionSpec` and a PyDCS compiler that produces a flyable Manston free-flight `.miz`. The model works, but it has no schema version, no documented growth path for combat/triggers, and only light structural validation. Downstream M2 items (registry, validation engine) and M6 (trigger model) need a clearer contract before more fields appear.

Constraints: no LLM-authored DCS Lua; PyDCS stays behind `CompilerInterface`; Channel + SpitfireLFMkIX remain the verified ids for this milestone.

## Goals / Non-Goals

**Goals:**

- Make the Mission Spec an explicit, versioned public contract.
- Preserve Manston free-flight compile behaviour and in-game acceptance.
- Reserve optional extension points for combat / objectives / triggers without implementing them.
- Improve structural error messages for invalid YAML / fields.

**Non-Goals:**

- Combat compile, registry contents, semantic “DCS-exists” validation, golden fixture suite.
- Agent tooling, briefings, Lua snippet libraries.

## Decisions

1. **`schema_version` as a required string on Mission Spec (start at `"1"`)**
   - Rationale: cheap forward-compat marker for agents and loaders.
   - Alternative: implicit version from package — rejected; specs travel as YAML files.

2. **Extension points as optional typed stubs, not free-form dicts**
   - Optional top-level keys reserved: `enemies`, `objectives`, `triggers` (each optional list/object, empty/absent for free flight).
   - Free-flight compiler MUST ignore absent/empty stubs; if non-empty in this change, loader/compiler MUST fail with a clear “not supported yet” error (no silent drop).
   - Alternative: `extra="allow"` catch-all — rejected; invites undeclared agent fields.
   - Alternative: implement combat now — out of scope (M4).

3. **Unknown keys rejected (`extra="forbid"` on Mission Spec models)**
   - Rationale: agents inventing spellings is exactly what the architecture prevents.
   - Alternative: ignore unknowns — rejected for this contract layer.

4. **Exact DCS id strings remain opaque strings in the Spec**
   - Theatre / aircraft stay `str` with documented verified values; registry (M2 `#3`) will later constrain them. Do not invent enums for every DCS id yet.
   - `MissionType` stays an enum; free_flight is the only supported value this change compiles.

5. **Loader owns structural validation; compiler assumes a valid Spec**
   - Keep YAML → Pydantic in `loader.py`; surface Pydantic errors clearly via CLI.
   - Semantic registry checks deferred to `validation-engine`.

6. **Example YAML updated with `schema_version: "1"`**
   - Manston example remains the acceptance fixture; must still compile to a `.miz` openable in ME / Instant Action.

## Risks / Trade-offs

- [Reserved fields confuse agents into filling them] → Clear “not supported yet” errors when non-empty; docs state free_flight only.
- [Breaking existing example YAML without `schema_version`] → Update checked-in example in this change; document required field.
- [Over-designing combat stubs] → Keep stubs as empty optional containers with no nested combat schema yet; expand in M4/M6 changes.
- [Scope creep into registry] → Spec cites verified ids in requirements only; no SQLite/JSON registry work here.

## Migration Plan

1. Add `schema_version` + optional stubs + `extra="forbid"` to models.
2. Update `examples/manston_cold_freeflight.yaml`.
3. Confirm `uv run dcs-miz examples/manston_cold_freeflight.yaml` still produces a loadable `.miz`.
4. Rollback: revert model/example commits; no data migration.

## Open Questions

- Exact nested shapes for `enemies` / `objectives` / `triggers` — defer detailed schemas to M4 / M6; this change only reserves the keys.
- Whether clipped-wing `SpitfireLFMkIXCW` becomes a documented id — backlog pending decision; out of this change.
