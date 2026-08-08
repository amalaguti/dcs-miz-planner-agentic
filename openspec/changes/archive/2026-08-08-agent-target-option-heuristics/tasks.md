## 1. Planning options meta

- [x] 1.1 Align `strike_target_class` soft/aaa/sea meta: `preferred_motion`,
      `preferred_ai_preset`, optional short `cues`
- [x] 1.2 Align `ground_ai_preset` rows with `preferred_motion` + examples
- [x] 1.3 Enrich key `channel_place` rows (french coast / mid-channel / harbour if
      present) with related_classes / preferred presets where missing

## 2. Invent guidance

- [x] 2.1 Prompts: cue table + call order (`list_mission_options` then
      `list_strike_targets` before `targets[]`)
- [x] 2.2 Spec schema notes for GA/recon mirror the cue table
- [x] 2.3 Tighten `list_strike_targets` / `list_mission_options` tool descriptions

## 3. Tests + backlog + accept

- [x] 3.1 Hermetic tests for preferred_* meta after sync + prompt/schema cues
- [x] 3.2 BACKLOG: `#8d` building→done; add theatre/target **promote checklist**
      idea (future maps + units)
- [x] 3.3 Ruff + full pytest green
- [x] 3.4 Accept: CLI/API / hermetic tests only (no ME required for `#8d`)
