## Why

Mission Spec loading and compilation each enforce fragments of validity in different
places (Pydantic, compiler `_validate`, ad-hoc `ValueError`s). Agents and users need one
shared `validate_mission_spec` surface with clear, structured errors — and the registry
plus install inventory now exist to support real DCS-exists checks. Centralizing
validation unblocks trustworthy agent tools and keeps the compiler from being the only
gate.

## What Changes

- Add a validation engine that checks a loaded `MissionSpec` in three layers: structural
  (schema already largely covered by the loader), DCS-exists (registry + local theatre
  availability), and semantic (combinations this free-flight planner supports).
- Expose a Python API returning structured success or a list of field-oriented errors
  (path, message, known alternatives when applicable).
- Add a CLI `dcs-miz validate <spec.yaml>` that prints those errors without compiling.
- Wire compile to run the same engine before PyDCS work so rules cannot drift.
- Keep Manston free-flight compile + in-game load as the regression acceptance check.

## Non-goals

- Historical period validation (date → plausible aircraft) — later / research track.
- Combat/trigger graph validation beyond “extension points must stay empty.”
- Golden fixture platform (M2 `#6`) or agent tool MCP surface (M3).
- Replacing Pydantic load-time checks; the engine consumes an already-parsed `MissionSpec`
  (or fails clearly if called with raw YAML via the CLI loader).
- Auto-refreshing the install inventory on every validate (use cached SQLite; callers may
  refresh separately).

## Capabilities

### New Capabilities

- `mission-validation`: Structured Mission Spec validation API and CLI covering structural
  follow-ups, registry/install existence, and free-flight semantic rules with clear errors.

### Modified Capabilities

- `miz-compiler`: Compilation MUST refuse specs that fail the shared validation engine,
  using the same error semantics as standalone validate (no silent redefinition of rules
  inside PyDCS-only paths).

## Impact

- New `validate` / validation module; CLI gains a `validate` subcommand.
- Compiler delegates pre-compile checks to the engine; Manston example must still compile
  and open in DCS Mission Editor / Instant Action.
- Unblocks `agent-tools-surface` (`validate_mission_spec`) and pairs with later
  `golden-fixtures-tests`.
