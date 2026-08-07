## Why

Wingman + `join_up` puts the player on Follow, but nothing warns or fails the
sortie if they wander off section. Free-flight practice should stay free; training
CAP/intercept Specs need an **opt-in** fail-to-follow discipline so section
cohesion is enforceable without LLM Lua.

## What Changes

- Optional Spec field on `player.flight` (e.g. `discipline` / nested knobs) —
  **default off** when omitted.
- Only meaningful for `role: wingman` + `join_up: true` (reject or no-op otherwise).
- Compiler emits progressive beats after airborne: soft radio/message “rejoin”,
  then stronger outcomes (flag / abort or RTB / mission_end) using distance/time
  thresholds.
- Prefer native ME zones+flags+messages; reuse `#15d` rejoin flag/pack when
  available; curated Lua snippet **only** if unit-to-group range cannot be
  expressed natively.
- Planning options + schema notes; example Spec; ME/Instant Action acceptance
  (deliberately lag behind section → soft warn).

## Non-goals

- Always-on discipline for every multi-ship Spec.
- Full AI chat / free-form NL→Lua.
- Lead same-group “keep mates in bubble” (v1 is wingman→AI lead only).
- Client/MP; escort `package` discipline.
- Replacing `#15d` F10 orders (discipline may *fire* rejoin; it does not invent
  new order ids).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-spec`: optional discipline knobs on `player.flight`
- `mission-validation`: reject invalid discipline (solo / lead / join_up false /
  bad thresholds)
- `miz-compiler`: emit warn → escalate packs when discipline armed
- `mission-options`: planning-options family for discipline
- `mission-briefing`: brief note when discipline is armed
- `nl-agent`: schema documents discipline fields
- `golden-fixtures`: structural asserts for discipline example

## Impact

- Models / validation / compiler (likely `section_orders_emit` hook or new
  `discipline_emit`); planning_options YAML; example under `examples/`;
  BACKLOG `#15e`; lessons / `dcs-dev-player-flight` if ME distance pitfalls appear.
- Acceptance: Instant Action after takeoff — leave section → soft rejoin message;
  optional hard beat once.
