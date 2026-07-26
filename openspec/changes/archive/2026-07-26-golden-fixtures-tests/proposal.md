## Why

Manston compile tests already assert a few mission fields, but regressions still rely on
ad-hoc checks that are easy to weaken or forget as the compiler grows (triggers, weather,
radio, zip layout). M2’s last hardening step is a durable golden-fixture harness so
spec → `.miz` structure stays pinned before the agent layer (M3) starts changing Specs.

## What Changes

- Add a checked-in golden fixture for the Manston cold free-flight compile path (extracted
  structural artifacts, not opaque binary-only comparison).
- Add pytest that compiles the example Spec (injected Channel inventory) and asserts
  against those fixtures (zip members + selected mission/theatre content).
- Refactor or thin existing Manston compile asserts so the golden path is the primary
  regression surface (avoid duplicating the same checks in two places).
- Document how to refresh fixtures when an intentional compiler change is accepted.

## Non-goals

- No compiler behavior changes unless a fixture refresh reveals a bug.
- No full byte-identical `.miz` golden (PyDCS / zip metadata churn).
- No combat/trigger goldens (those wait for M4/M6).
- No CI publish, package versioning, or git tags.
- No storing real DCS install dumps from `research/` as product fixtures.

## Capabilities

### New Capabilities

- `golden-fixtures`: Checked-in structural goldens + pytest regression for free-flight
  compile output (starting with Manston).

### Modified Capabilities

- `miz-compiler`: Require that the Manston free-flight acceptance path be covered by the
  golden-fixture suite (structural asserts remain part of the compiler contract).

## Impact

- New files under `tests/fixtures/` (or similar) and tests; possibly a small refresh helper.
- Touches `tests/test_compile_manston.py` (thin or replace overlapping asserts).
- Docs: brief README / ARCHITECTURE / BACKLOG note; acceptance still includes opening the
  compiled Manston `.miz` in DCS ME / Instant Action if any compiler code changes — otherwise
  green suite + existing compile path is enough.
