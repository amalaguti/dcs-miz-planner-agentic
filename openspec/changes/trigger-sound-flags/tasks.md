## 1. Sound registry and Spec model

- [x] 1.1 Add sound-asset registry (`data/sounds/` YAML + at least one tiny sample audio file) and lookup API
- [x] 1.2 Add models: `sound`, `flag_equals` / `flag_more` / `flag_less` / `time_since_flag`, `inc_flag` / `set_flag_value`; extend TriggerCondition / TriggerAction unions

## 2. Validate and emit

- [x] 2.1 Validate flag names, numeric fields, and known `asset_id`s in `validation.py`
- [x] 2.2 Map new conditions/actions in `triggers_emit.py`; collect numeric flag names into flag id map
- [x] 2.3 Embed resolved sound files via PyDCS `map_resource` and emit `SoundToAll` in compile path

## 3. Example, agent, docs

- [x] 3.1 Add example Spec (sound + numeric/timed flag chain)
- [x] 3.2 Agent schema/prompt notes; BACKLOG status `building`

## 4. Tests and acceptance

- [x] 4.1 Unit/integration: validate + compile structure (sound resource + flag predicates); regression on prior triggers/narrative/radio
- [x] 4.2 In-game: ME shows SOUND TO ALL and numeric flag rules on compiled example
  - Accepted 2026-08-04: beep at T+10s; flag-chain messages followed (beats = demo numeric flag).
