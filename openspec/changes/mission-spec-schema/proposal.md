## Why

M1 shipped a working free-flight compile path, but the Mission Spec is still a one-mission Pydantic shape with no documented extension points. Registry, validation, agent tools, and later combat / trigger models all need a stable, versioned contract they can grow against. Formalizing that contract now — while only free flight is implemented — prevents ad-hoc fields from accumulating in the compiler.

## What Changes

- Document and harden the Mission Spec as the public AI ↔ compiler contract (Pydantic models + YAML loading).
- Add an explicit schema version field so future changes can evolve without silent breakage.
- Introduce reserved / optional extension points for combat and immersion (enemies, objectives, triggers) that free-flight missions leave unset and the current compiler ignores.
- Tighten structural validation errors so invalid specs fail clearly before compile.
- Keep the Manston cold free-flight example as the canonical checked-in free-flight fixture; it MUST still compile and load in DCS Mission Editor / Instant Action.

## Non-goals

- Implementing combat mission compilation (intercept, CAP, escort, ground attack).
- Full Channel reference registry, semantic validation engine, or golden fixture suite (those are M2 `#3`–`#6`).
- Agent / NL planning layer, briefings, Lua triggers, or squadron-commander voice.
- Changing theatre beyond `TheChannel` or adding `SpitfireLFMkIXCW`.
- Emitting DCS Lua from an LLM.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-spec`: Formalize free-flight schema with `schema_version`, clearer structural rules, and documented optional extension points for future combat/trigger fields that MUST NOT affect free-flight compilation when absent.
- `miz-compiler`: Confirm free-flight compile remains unchanged for the Manston example when optional extension fields are absent; reject or ignore undeclared unknowns per design (no combat compile path yet).

## Impact

- `src/dcs_miz_planner/models.py`, loader, and example YAML.
- OpenSpec main specs for `mission-spec` (and a small `miz-compiler` delta if compile acceptance is restated).
- Unblocks `reference-registry-channel`, `validation-engine`, and later M6 `trigger-model-spec`.
- Acceptance still hinges on compiling the Manston example to a `.miz` that opens in DCS Mission Editor / Instant Action.
