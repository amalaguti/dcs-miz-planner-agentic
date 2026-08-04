## 1. Spec model

- [x] 1.1 Add `GroupLifeLessCondition` (`enemy_index` XOR `target_index`, `percent` 1–100) and extend `TriggerCondition` union

## 2. Validate and emit

- [x] 2.1 Validate index XOR, range, and percent in `validation.py`
- [x] 2.2 Map `group_life_less` → PyDCS `GroupLifeLess` in `triggers_emit.py` using enemy/target group id maps

## 3. Example, agent, docs

- [x] 3.1 Add example Spec (prefer ground-attack) with `group_life_less` → message (optional flag/end)
- [x] 3.2 Agent schema/prompt notes; BACKLOG status `building`

## 4. Tests and acceptance

- [x] 4.1 Unit/integration: validate failures + compile structure (`c_group_life_less`); regression on prior triggers
- [x] 4.2 In-game: ME shows GROUP LIFE LESS (or equivalent) on the compiled example
  - Accepted 2026-08-04: ME shows `targets_damaged_enough` / GROUP LIFE LESS at 50% on the truck group.
