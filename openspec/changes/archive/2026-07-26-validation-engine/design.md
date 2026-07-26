## Context

Loader-level Pydantic checks reject malformed YAML and unknown fields. The compiler’s
`_validate` then checks theatre/aircraft/weather/airfield against the Channel registry.
Local install availability (SQLite inventory) is not consulted at all. Agents will need a
single `validate_mission_spec` tool; duplicating rules in the compiler forever will drift.

## Goals / Non-Goals

**Goals:**

- One validation API over a loaded `MissionSpec` with structured, multi-error results.
- DCS-exists checks against packaged registry **and** cached install inventory (theatre
  available + planner-supported).
- Free-flight semantic checks appropriate to schema_version `"1"`.
- CLI `validate` and compile both use the same engine.
- Manston example still validates and compiles for DCS acceptance.

**Non-Goals:**

- Historical plausibility, combat/trigger graph validation, golden fixtures, auto inventory
  refresh on every call, new package dependencies.

## Decisions

1. **API shape: result object, not only exceptions**
   - `validate_mission_spec(spec) -> ValidationResult` with `ok: bool` and
     `errors: list[ValidationError]` (`path`, `code`, `message`, optional `hint`).
   - Collect **all** independent errors in one pass where practical (better for agents than
     fail-fast only).
   - Raising `MissionValidationError` (wrapping the result) remains available for call sites
     that prefer exceptions (compiler/CLI).
   - Alternative: exceptions only — rejected; agents need a full error list.

2. **Layering**
   - **Load** stays in `loader.py` / Pydantic (`SpecLoadError`) — not reimplemented.
   - **Engine** assumes a valid `MissionSpec` instance.
   - Checks (v1):
     - Theatre in registry (`has_theatre`).
     - Theatre locally `available` in install inventory **and** `planner_supported` (intersect).
     - Aircraft known in registry; weather preset known; airfield maps to `airdromeId` for
       Channel (current registry scope).
     - Free-flight: `mission_type` free_flight; extension lists empty (already on model —
       re-assert with a clear validation code if reached).
     - Start type limited to supported enum values already on the model.
   - Country/coalition deep checks stay light (UK/blue for Manston path) — only flag unknown
     country if we can do so without inventing DCS country tables; defer rich country registry.

3. **Install inventory: cache by default**
   - Use `get_inventory()` (SQLite cache). Do not force `--refresh` inside validate.
   - If inventory is empty/unusable (no DCS roots), theatre availability checks fail with a
     diagnostic pointing at `dcs-miz theatres --refresh` / `--dcs-root`.
   - Optional injectables for tests: pass a fake inventory / registry into the engine.

4. **Compiler integration**
   - Replace `PyDCSCompiler._validate` body with a call to the shared engine; map failures to
     a single clear exception listing errors.
   - Keep PyDCS plane_map / country existence as backend-specific compile-time checks (not
     duplicated into the product validation engine unless we later add a PyDCS-free plane
     registry).

5. **CLI**
   - `dcs-miz validate <spec.yaml> [--json]` — load then validate; exit `0` ok, `2` load/validate
     failure (same family as bad-spec compile).
   - Preserve legacy compile and `theatres` subcommands.

## Risks / Trade-offs

- [Stale install cache rejects a newly installed map] → Document refresh; do not auto-rescan.
- [No DCS install on CI] → Tests inject inventory fixtures; CI never requires a real install.
- [Over-strict country checks break Manston] → Keep country checks minimal in v1.
- [Error-message churn vs golden fixtures] → Prefer stable `code` fields; message text may evolve.

## Migration Plan

1. Add validation models + engine + unit tests with injected registry/inventory.
2. CLI `validate`; point compiler at the engine.
3. Docs / architecture; Manston validate + compile acceptance.
4. Rollback: restore compiler-local `_validate`; remove validate CLI.

## Open Questions

- Whether a later agent should treat “planner-supported but not installed” as a soft warning
  vs hard error — v1: **hard error** for compilable offers.
- When to add a dedicated country/coalition registry table — defer past this change.
