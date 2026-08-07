## Context

Compiler always emits `flight_group_from_airport(..., group_size=1)` and sets
`units[0].skill = Player`. Escort `package` is a separate friendly AI flight. Users want
a **player section** of 2–4 Spits with the human as lead or wingman. PyDCS already
supports `group_size` > 1; DCS single-player allows exactly one `Skill.Player` per
mission (AI skills on mates). Triggers that bind `player_unit_id` today use `units[0].id`
and must follow the human slot.

## Goals / Non-Goals

**Goals:** Optional Spec `player.flight`; compile multi-unit group; lead/wingman Player
slot; validate; example + golden; brief/agent awareness.

**Non-Goals:** Multiplayer `Client` seats; mixed types/starts; custom formation Lua;
changing escort package meaning; failures (`#22b`).

## Decisions

1. **Spec shape — nested `player.flight`** (omit = solo):
   - `size`: int 2–4
   - `role`: `lead` | `wingman` (default `lead`)
   - `ai_skill`: AI skill for non-player units (default `Average`; allowlist minus
     Player/Client)
   - Alternatives considered: top-level `player_flight` (rejected — keeps aircraft/
     airfield/start on `player`); per-unit roster (rejected — overkill for v1).

2. **Human control / wingman emit** — DCS single-player only controls `Skill=Player`
   on the **first unit of a group**. Therefore:
   - `lead`: one group, `group_size=size`, Player on `units[0]`, AI mates on the rest.
   - `wingman`: **two groups** — AI lead (`"{name} Lead"`, size−1) + size-1 Player
     group. Do **not** put Player on `units[1]` of a mixed group (spectator bug).
   - `player_unit_id` is always `player_group.units[0].id`.
   Alternatives rejected: same-group slot index (broken in SP); multipayer `Client`
   seats (out of scope).

3. **`player.skill`** — remains the human unit skill; MUST be `Player` when
   `player.flight` is present (reject `Client` / AI names). Compiler forces Player on
   the player group’s first unit and `ai_skill` on AI mates / AI lead group.

4. **Emit** — as above; payload (GA) via `group.load_pylon` on the player group
   (applies to all units in that group). Wingman AI lead does not share the player
   group payload in v1 unless we later load both.

5. **Mission types** — CAP/intercept/GA/escort tasking attaches to the **player**
   group (human flies the planned route). AI lead for wingman is a colocated
   section mate without Follow/join-up scripts in v1.

6. **Parking / join-up** — PyDCS airport parking for both groups; no custom taxi /
   Follow scripts in v1. Document Manston parking-capacity risk for size 4.

7. **Brief / agent** — voice/brief mention section size + role when `flight` present;
   planning_options + schema tool document the knobs.

## Risks / Trade-offs

- [Risk] Insufficient parking at small fields for size 4 → Mitigation: prefer Manston
  example; validate soft-warn later if needed; acceptance on Manston first.
- [Risk] Wingman AI lead taxis poorly / leaves human → Mitigation: accept DCS AI limits;
  document; no Lua workarounds in v1.
- [Risk] Forgetting `player_unit_id` remapping breaks gates → Mitigation: single helper
  for human index; golden + unit test on wingman slot id.
- [Risk] Agents invent `Client` for co-op → Mitigation: validate reject with flight.

## Migration Plan

- Additive optional field; existing Specs omit `flight` → unchanged solo compile.

## Open Questions

- None blocking for propose. Optional later: `slot` 1–size for wingman #3/#4.
