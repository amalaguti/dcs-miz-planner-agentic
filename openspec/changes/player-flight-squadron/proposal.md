## Why

Every compiled sortie still places a **solo** Skill=Player Spitfire. Classic Channel ops
are multi-ship sections (pair / four), and users want to fly as **flight lead** with AI
wingmen or as a **wingman** in an AI-led flight. Escort `package` is friendly AI cargo —
not the player’s own section.

## What Changes

- Extend Mission Spec with an optional **`player.flight`** block: size 2–4 (default omit =
  solo / size 1), role `lead` | `wingman`, optional AI skill for non-player slots.
- Compiler: emit one multi-unit player group (`group_size` from Spec); exactly one unit
  Skill=`Player` at the role index; remaining units AI skill; same aircraft / start /
  parking / radio as today. Mission-type tasking (CAP / intercept / GA / escort) stays on
  that group.
- Validation: size/role bounds; reject `player.skill` overrides that fight the flight
  model; briefing/voice mention flight size and role when present.
- Example + golden: Manston free-flight (or CAP) 4-ship lead; optional wingman smoke.
- Agent schema / planning options learn `player.flight` knobs.

## Non-goals

- Multiplayer `Client` slots / net-co-op seating.
- Mixed aircraft types or mixed start types inside the flight.
- Separate controllable player flights; formation editor UI; custom taxi/join-up scripts.
- Changing escort `package` semantics (still escorted friends, not player section).
- `#22` Lua snippets; `#22b` aircraft failures; recon / new mission types.

## Capabilities

### New Capabilities

- *(none — extend existing mission-spec / compiler / validation / options / agent surfaces)*

### Modified Capabilities

- `mission-spec`: optional `player.flight` (size, role, AI skill).
- `miz-compiler`: multi-unit player group; Player skill on role slot.
- `mission-validation`: flight size/role/skill rules.
- `golden-fixtures`: structural asserts for multi-ship player group.
- `mission-options`: expose flight size/role as planning knobs.
- `mission-briefing` / `squadron-voice` (light): brief language for section ops.
- `nl-agent` / `agent-tools` (light): schema/examples for `player.flight`.

## Impact

- `models.py`, `validation.py`, `compiler/pydcs_compiler.py`, planning_options, agent
  schema/voice, examples, goldens, BACKLOG `#15b`.
- Acceptance: open a 2–4 ship `.miz` in DCS ME / Instant Action; human in lead or
  wingman slot; AI section mates present and tasked with the same sortie.
