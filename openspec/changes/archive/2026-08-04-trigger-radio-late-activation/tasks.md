## 1. Spec model

- [x] 1.1 Add `late_activation` to `EnemyFlight` and `GroundTarget`
- [x] 1.2 Add actions `radio_item_add`, `radio_item_remove`, `activate_group`, `deactivate_group` to models + TriggerAction union

## 2. Validate and emit

- [x] 2.1 Validate activate/deactivate indices; radio label/flag non-empty
- [x] 2.2 Map new actions in `triggers_emit.py` (flag ids; coalition radio default)
- [x] 2.3 Set PyDCS `late_activation` when placing enemies/targets; keep group id lists for activate

## 3. Example, agent, docs

- [x] 3.1 Add example Spec (F10 Easy/Med/Hard → activate late enemies)
- [x] 3.2 Agent schema/prompt notes; BACKLOG status building

## 4. Tests and acceptance

- [x] 4.1 Unit/integration: validate + compile structure; regression on prior triggers/narrative
- [x] 4.2 In-game: ME shows radio items and late-activated groups on compiled example
  - Accepted 2026-08-04: ME Triggers show radio_menu + activate_*; enemy groups Late Activation checked; F10 path documented for Instant Action.
