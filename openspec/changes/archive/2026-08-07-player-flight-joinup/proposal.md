## Why

`#15b` places multi-ship sections, but wingman sorties use a **separate** AI lead
group with no Follow or shared route — the section does not fly together. Lead
same-group mates already stick via DCS; wingman needs native ME Follow + tasking
on the AI lead so the human can join the squadron.

## What Changes

- Compiler: when `player.flight.role: wingman`, attach PyDCS `Follow` on the player
  group to the AI lead group id; put CAP / intercept / GA / escort (and a minimal
  free-flight outbound leg) on the **AI lead** group so the section has a route to
  join.
- Spec: optional `player.flight.join_up` (default `true` when wingman) to allow
  opt-out; lead role unchanged (same-group AI cohesion).
- Validation, example(s), structural tests, brief/schema note that wingman joins
  the AI lead after takeoff.
- Acceptance: ME / Instant Action wingman 4-ship shows Follow + lead route; player
  controllable and can form on the lead.

## Non-goals

- `#15d` curated section orders / F10 order packs / stock radio documentation slice.
- Custom formation editor, Lua join-up scripts, multipayer Client seats.
- Perfect taxi join-up (Follow is post-takeoff oriented); no custom taxi scripts.
- Changing escort `package` semantics.

## Capabilities

### New Capabilities

- *(none — extend existing mission-spec / compiler / validation / options / agent surfaces)*

### Modified Capabilities

- `mission-spec`: optional `join_up` on `player.flight`.
- `miz-compiler`: wingman Follow + mission tasking on AI lead; free-flight lead leg.
- `mission-validation`: `join_up` rules (wingman-only meaningful).
- `golden-fixtures` / structural tests: Follow + lead group tasking asserts.
- `mission-options` / `nl-agent` / `mission-briefing` / `squadron-voice` (light):
  join-up / follow-the-lead wording.

## Impact

- `models.py`, `validation.py`, `compiler/pydcs_compiler.py`, examples, tests,
  planning_options / schema / voice, BACKLOG `#15c`.
- Acceptance: open wingman `.miz` in DCS ME / Instant Action; confirm Follow on
  player and route on AI lead; fly join-up smoke.
