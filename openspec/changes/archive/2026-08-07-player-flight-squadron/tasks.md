## 1. Spec model + validation

- [x] 1.1 Add `PlayerFlight` model + optional `player.flight` (`size` 2–4, `role` lead|wingman, `ai_skill`) in `models.py`
- [x] 1.2 Validate flight rules in `validation.py` (size/role/`ai_skill` allowlist; `player.skill` MUST be `Player` with flight; reject Client/Player as `ai_skill`)
- [x] 1.3 Unit tests for valid lead/wingman Specs and rejection cases

## 2. Compiler emit

- [x] 2.1 Emit `group_size` from flight (default 1); assign `Player` to lead/wingman slot and `ai_skill` to mates
- [x] 2.2 Pass human unit id (role slot) as `player_unit_id` for altitude/speed gates
- [x] 2.3 Apply GA payload to all units in the player group when Spec has payload
- [x] 2.4 Compile smoke: Manston free-flight 4-ship lead + 2-ship wingman

## 3. Example, golden, options, agent surfaces

- [x] 3.1 Add example Spec (e.g. `examples/manston_freeflight_flight_lead.yaml`) size 4 lead
- [x] 3.2 Golden / structural asserts: group size + Player on lead unit
- [x] 3.3 Add planning_options entries for flight size/role; sync catalog if needed
- [x] 3.4 Update Spec schema tool / invent reminders for `player.flight`
- [x] 3.5 Brief/voice: mention section size + lead/wingman when flight present (light tests)

## 4. Docs + acceptance

- [x] 4.1 Update BACKLOG `#15b` → `building` then `done` on accept; README Status if milestone shifts
- [x] 4.2 Append LESSONS if PyDCS multi-unit / parking / skill quirks bite
- [x] 4.3 In-game ME / Instant Action: 4-ship lead at Manston; optional wingman pair smoke
  (accepted 2026-08-07: lead 4-ship cold hangar OK; wingman fixed via separate AI lead
  group — Player-on-units[1] was spectator; size-4 wingman OK. Join-up/Follow → `#15c`)
