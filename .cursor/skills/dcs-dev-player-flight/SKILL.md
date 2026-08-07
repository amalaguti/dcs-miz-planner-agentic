---
name: dcs-dev-player-flight
description: >-
  Player section / squadron flight compile rules for DCS single-player. Use when
  implementing or debugging player.flight, lead vs wingman groups, join_up /
  Follow, or multi-ship Player parking.
---

# Player flight (section)

## Read first

[`docs/lessons/player-flight.md`](../../../docs/lessons/player-flight.md)

## Hard rules

1. **SP controllable aircraft** = `Skill=Player` on **group `units[0]` only**.
   Player on unit 2+ → spectator / F7 / no cockpit (DCS SP).
2. **`role: lead`** → one multi-unit group, Player on `units[0]`, AI mates.
3. **`role: wingman`** → **separate** AI lead group (`"{name} Lead"`, size−1) +
   size-1 Player group. Never same-group Player-on-slot-2.
4. **`join_up` (default true, wingman):** route/tasking on **AI lead**; Player gets
   climb + PyDCS `Follow(lead.id)`. Smoke **after takeoff**, not in hangar.
   Free-flight/intercept: short lead outbound leg so Follow has a moving target.
   `join_up: false` → independent groups (`#15b` behaviour).
5. Prefer **Manston** for size-4 parking.

## Code touchpoints

`player_flight_*` helpers in `models.py`; `compiler/pydcs_compiler.py`;
examples `manston_freeflight_flight_*.yaml`, `manston_cap_flight_wingman.yaml`.
