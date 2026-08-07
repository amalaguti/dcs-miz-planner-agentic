## Context

After `#15b`, `role: wingman` emits AI lead group (`"{name} Lead"`) + size-1 Player
group. Mission tasks still attach to the **player** group; no Follow — AI and human
fly independently. PyDCS exposes `Follow(groupid, group_offset, altitude_difference)`
(same pattern family as escort `EscortTaskAction`). Lead same-group flights already
use DCS multi-unit AI; no Follow needed for lead v1.

## Goals / Non-Goals

**Goals:** Wingman Follow → AI lead; shared mission route on AI lead; free-flight
outbound leg for lead; opt-out `join_up`; tests + ME smoke.

**Non-Goals:** `#15d` orders; formation UI; Lua; taxi choreography; lead-role Follow.

## Decisions

1. **Always join-up for wingman by default** — `player.flight.join_up: bool = True`.
   When `false`, keep `#15b` behaviour (separate groups, tasks on player). Ignored /
   warn-only for `role: lead` (same-group already cohesive).

2. **Follow on player group** — After parking create, add climb/join waypoint(s) on
   the player group with `Follow(groupid=lead.id)` (offset ~trail, e.g. Vector2
   (−200, 0), alt diff −50..−200). Do not put Follow on the lead.

3. **Tasking owner when wingman + join_up** — CAP / intercept enemies placement
   unchanged; **route/task** helpers (`_apply_cap`, GA, escort) receive the **AI
   lead** group instead of the player group. Player only Follows. Intercept may
   still be “scramble” — lead gets climb/intercept geometry if any; else lead gets
   a short outbound + player Follows.

4. **Free-flight wingman** — AI lead gets a simple outbound waypoint (~8–15 km from
   airfield on a fixed bearing) so TakeOff→fly gives Follow a moving target; player
   Follows after a short climb WP.

5. **Lead role** — no compiler change beyond docs/brief (mates already in-group).

6. **Escort collision** — player-as-wingman Follow(lead) is distinct from escorting
   `package`; package EscortTaskAction stays on the tasking group (AI lead when
   wingman+join_up).

## Risks / Trade-offs

- [Risk] Cold-start Follow ignored until airborne → Mitigation: document; climb WP
  then Follow; acceptance after takeoff.
- [Risk] AI lead parking delays → Mitigation: Manston; accept DCS AI limits.
- [Risk] Refactor forgets to pass lead group into GA/CAP → Mitigation: single
  `task_group` variable; tests for Follow + task owner.

## Migration Plan

- Additive `join_up` default true for wingman; existing wingman Specs get cohesion
  without YAML edit.

## Open Questions

- None blocking. Formation option ids deferred; `#15d` consumes join-up later.
