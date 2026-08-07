## 1. Spec model and planning options

- [x] 1.1 Add `player.flight.orders` (optional list of order enums) to Spec models + validation (unknown / duplicates)
- [x] 1.2 Add planning-options family for each order (label, description, Spec snippet, when_to_use)
- [x] 1.3 Document that orders are ignored (or warn) when `flight` is absent / size 1 with no section AI

## 2. Compiler emit

- [x] 2.1 Resolve section AI group + player group (reuse lead/wingman helpers)
- [x] 2.2 Emit F10 Other radio items + continuous flag→AITaskPush / GroupStop packs for selected orders
- [x] 2.3 Flag reservation (document / avoid collision with Spec triggers)

## 3. Example and tests

- [x] 3.1 Example Spec: Manston CAP or intercept + wingman + subset of orders
- [x] 3.2 Unit tests: model round-trip; emit creates expected radio + trigger count; no-op when orders empty
- [x] 3.3 Update schema notes / brief if F10 section menu is user-facing

## 4. Docs and smoke

- [x] 4.1 Update ARCHITECTURE / BACKLOG `#15d`; lessons + `dcs-dev-player-flight` if needed
- [x] 4.2 Manual Instant Action: F10 items appear; rejoin (wingman) and engage smoke once each
  (Accepted 2026-08-07: ME triggers + Instant Action F10 Other + ack messages cold-start.
  Airborne Rejoin/Engage deferred — BACKLOG M4 do-soon.)
