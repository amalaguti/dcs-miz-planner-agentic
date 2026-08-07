## Context

`#15c` armours wingman Follow + shared CAP/route; `#15d` adds F10 section orders
(flags **800+**, rejoin pack). Nothing yet fails or warns a wingman who stays
outside the section after takeoff. Backlog `#15e` wants **opt-in** fail-to-follow
so practice free-flight stays free and training Specs can enforce cohesion.

PyDCS exposes `UnitOutsideMovingZone` / `UnitInMovingZone` (unit vs zone tied to
another unit) — prefer that over Mist distance Lua for v1.

## Goals / Non-Goals

**Goals:** Opt-in Spec discipline for wingman+join_up; soft rejoin message then
stronger curated beat; native moving-zone + flags; reuse `#15d` rejoin flag when
orders include `rejoin`; example + ME/IA smoke.

**Non-Goals:** Always-on; lead-role bubble; free-form Lua; inventing new F10 order
ids; Client/MP; hard balance tuning for every aircraft (Channel Spitfire defaults).

## Decisions

1. **Spec shape** — optional nested object on `player.flight`:
   ```yaml
   discipline:
     radius_m: 2500          # moving bubble around AI lead (default)
     soft_after_s: 45        # continuous time outside before soft warn
     hard_after_s: 120       # further time outside after soft before hard
     hard: message_end       # curated: message_end | mission_end | section_rtb
   ```
   - **Omit / null → off** (default). Empty `{}` uses defaults (= armed).
   - Validation: require `role: wingman` and `join_up: true`; reject lead/solo/
     `join_up: false`. Bounds on radius/time (design mins: radius ≥ 500 m;
     soft/hard ≥ 10 s; hard_after ≥ soft_after).

2. **Who is monitored** — Player unit (`Skill=Player`, group unit #1) vs
   **AI lead group unit #1** (moving-zone host). Never change Player skill.

3. **Emit pattern (native-first)**
   - After short airborne gate (e.g. player altitude > ~150 m AGL **or**
     TimeAfter scramble delay — pick one in apply; prefer altitude so hangar
     parking does not fire).
   - Attach circular moving zone (radius `radius_m`) to AI lead unit.
   - Continuous: `UnitOutsideMovingZone(player, zone, lead_unit)` for
     `soft_after_s` → message “Section — rejoin / form up” + optional set
     `#15d` rejoin flag (**801**) if `orders` contains `rejoin`, else message-only.
   - Escalation: still outside for `hard_after_s` after soft → `hard` action:
     - `message_end` — stronger message only (default for smoke)
     - `mission_end` — end mission (fail)
     - `section_rtb` — push Land on AI lead (reuse RTB pack pattern)
   - Cooldown / flag clear so soft warn does not spam every frame (ONCE with
     latch flag, or ClearFlag + min interval — implement one pattern in apply).

4. **Flag reservation** — discipline internal flags in **820–839** (orders keep
   800–819). Document in emit module + lessons.

5. **Agent** — planning_options family `player_flight_discipline`; schema notes;
   never invent hard-action ids.

6. **Example** — extend CAP wingman Spec (or sibling
   `manston_cap_flight_discipline.yaml`) with discipline + prefer `orders: [rejoin]`
   so soft beat can fire the same rejoin pack.

## Risks / Trade-offs

- [Risk] Moving-zone radius/units quirks in ME → Mitigation: ME smoke radius;
  document metres vs feet if wrong.
- [Risk] Soft fires on parking / taxi → Mitigation: altitude (or time) gate before
  discipline continuous triggers arm.
- [Risk] Hard `mission_end` feels harsh → Mitigation: default `message_end`;
  example uses soft+message_end; document hard options.
- [Risk] Native insufficient for true 3D slant range → Mitigation: v1 moving zone
  2D/ME semantics; `#22` snippet only if acceptance proves zone unusable.

## Migration Plan

- Additive optional field; existing Specs unchanged (discipline off).

## Open Questions

- Exact airborne gate (AGL altitude vs TimeAfter) — resolve in apply with ME smoke.
- Whether soft beat **must** include `orders: [rejoin]` or message-only is enough
  when orders omit rejoin — **Decision:** message always; set rejoin flag only if
  that order is armed.
