# Player flight (section / wingman)

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## F10 section orders (`player.flight.orders`) (2026-08-07)

- **Date:** 2026-08-07
- **Lesson:** Optional Spec `player.flight.orders: [rejoin|engage|orbit|rtb|break]`
  emits F10 Other radio items (`Section: …`) that set reserved flags **800+**,
  then continuous triggers push AI tasks (`Orbit`, `AttackGroup`, `Land`,
  `Follow`, or `GroupStop`) onto the **section AI group**. Wingman → AI lead
  group; lead → player multi-unit group. Rejoin as lead is **message-only**
  (mates already share the group / formation). Prefer Specs that already put
  CAP/intercept tasking on that group so Engage/Orbit have useful context.
  Do not collide Spec `triggers` flags into 800+.
- **Code / notes:** `compiler/section_orders_emit.py`; planning options
  `player_flight_order_*`; example `manston_cap_flight_orders.yaml`; backlog `#15d`.

## Player flight wingman Follow / join-up (2026-08-07)

- **Date:** 2026-08-07
- **Lesson:** Wingman + `join_up` (default true): mission route/tasking goes on the
  **AI lead** group; the size-1 Player group gets climb + PyDCS `Follow(lead.id)`.
  Cold-start Follow engages after airborne — join-up smoke after takeoff, not in
  the hangar. Free-flight/intercept give the lead a short “Section outbound” leg
  so Follow has a moving target. `join_up: false` keeps `#15b` independent groups.
  Lead same-group mates need no Follow.
- **Code / notes:** `player_flight_join_up_enabled`, `_apply_player_follow_lead`,
  `_apply_wingman_lead_outbound`; examples wingman free-flight +
  `manston_cap_flight_wingman.yaml`; backlog `#15c`.

## Player flight: SP Player must be group unit #1 (2026-08-07)

- **Date:** 2026-08-07
- **Symptom:** Wingman Spec put `Skill=Player` on `units[1]` of a 2-ship group;
  in Instant Action the human only got F7 cameras / hangar roof view, no cockpit
  control; both aircraft taxied under AI.
- **Cause:** DCS single-player only hands the controllable aircraft to
  `Skill=Player` on the **first unit of a group**. Player on unit 2+ is ignored
  for control (spectator).
- **Fix:** `role: lead` → one multi-unit group, Player on `units[0]`.
  `role: wingman` → **separate** AI lead group (`"{name} Lead"`, size−1) plus a
  size-1 Player group. No same-group Player-on-slot-2. Formation Follow / join-up
  deferred. Prefer Manston for size-4 parking.
- **Code / notes:** `player_flight_is_wingman`, `player_ai_lead_group_size`,
  `compiler/pydcs_compiler.py`; examples lead/wingman; backlog `#15b`.
