## 1. target_dead vocabulary

- [x] 1.1 Add `TargetDeadCondition` to models; wire into TriggerCondition union
- [x] 1.2 Validate `target_index` against `targets[]`; map to GroupDead in triggers_emit
- [x] 1.3 Collect target group ids from `_apply_ground_attack` and pass into zone/trigger emit

## 2. Ground-attack pack

- [x] 2.1 Add `_apply_ground_attack_pack` (strike zone, push, ingress, targets-down win); extend dispatch
- [x] 2.2 Clear errors for missing strike/targets; update unsupported-type list

## 3. Example, agent, docs

- [x] 3.1 Add `examples/manston_ground_attack_narrative.yaml`
- [x] 3.2 Agent schema/prompt notes; BACKLOG/README/LESSONS pointer

## 4. Tests and acceptance

- [x] 4.1 Tests: expand/validate/compile GA narrative; target_dead validation; prior packs regression
- [x] 4.2 In-game: ME Triggers shows GA narrative rules on compiled example
  - Accepted 2026-08-04: ME shows `narrative_push`, `narrative_ingress`, `narrative_targets_down` on `out/manston_ground_attack_narrative.miz`.
