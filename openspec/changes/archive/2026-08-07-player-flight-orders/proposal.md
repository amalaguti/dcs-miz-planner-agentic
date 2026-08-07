## Why

After `#15b` / `#15c`, the player can fly lead or wingman with join-up, but cannot
issue **section orders** mid-sortie (rejoin, engage, orbit, RTB, …). Authors must
hand-build F10/flag graphs or rely on opaque stock radio. The product needs
**named, curated orders** the Spec (and agent) can select — no free-form chat→Lua.

## What Changes

- Spec: opt-in section-order pack on `player.flight` (omit = no order menu).
  Curated order ids only (e.g. rejoin, engage, cover, orbit, rtb, break).
- Compiler: emit F10 radio items + flag→AI-task packs targeting the AI section
  (lead mates same-group; wingman → separate AI lead group). Prefer native ME /
  PyDCS tasks; no LLM Lua.
- When `role: lead`, document/use stock DCS lead→wingman radio where it already
  works; still emit curated F10 for consistent Spec-selected packs and wingman
  separate-group cases.
- Validation: unknown order ids rejected; orders require `player.flight`.
- Planning options + schema notes + brief honesty; example Spec; structural tests.
- Acceptance: ME shows F10 items; Instant Action smoke for at least rejoin + one
  other order.

## Capabilities

### New Capabilities

- *(none — extend existing surfaces)*

### Modified Capabilities

- `mission-spec`: optional curated section orders on `player.flight`.
- `miz-compiler`: emit F10 + AI task packs for selected orders.
- `mission-validation`: curated ids; require flight when orders set.
- `mission-options`: discoverable order knobs / families.
- `nl-agent`: schema notes for invent.
- `mission-briefing`: brief mentions available section orders when armed.
- `golden-fixtures`: structural asserts on radio / order wiring.

## Impact

- `models.py` (`PlayerFlight`), validation, `compiler/pydcs_compiler.py` (+ emit
  helper), planning_options, examples, tests, BACKLOG `#15d`.
- Pairs with `#15e` (discipline can call the same rejoin order).
- Does **not** invent new ME predicates beyond existing radio/flag/task patterns.
