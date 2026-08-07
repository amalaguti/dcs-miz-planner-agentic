## 1. Spec + validation

- [x] 1.1 Add `player.flight.join_up: bool = True` to `PlayerFlight`
- [x] 1.2 Validation: accept boolean; lead+join_up succeeds (no-op)
- [x] 1.3 Unit tests for default / opt-out load

## 2. Compiler join-up emit

- [x] 2.1 Refactor compile path: `task_group` = AI lead when wingman+join_up else player
- [x] 2.2 Free-flight: outbound waypoint on AI lead when wingman+join_up
- [x] 2.3 Attach PyDCS `Follow(lead.id)` on player climb/join waypoint when join_up
- [x] 2.4 CAP / GA / escort apply to `task_group` when wingman+join_up
- [x] 2.5 `join_up: false` preserves `#15b` (tasks on player, no Follow)

## 3. Examples, tests, agent surfaces

- [x] 3.1 Update wingman example (join_up explicit or documented default); optional CAP wingman smoke Spec
- [x] 3.2 Structural tests: Follow + lead outbound / CAP on lead
- [x] 3.3 Planning option + schema note + brief/voice join-up phrasing

## 4. Docs + acceptance

- [x] 4.1 BACKLOG `#15c` → building/done; README/LESSONS if Follow quirks bite
- [x] 4.2 In-game ME / Instant Action: wingman 4-ship join-up after takeoff
  (accepted 2026-08-07 — proceed; optional deeper after-takeoff Follow smoke later)
