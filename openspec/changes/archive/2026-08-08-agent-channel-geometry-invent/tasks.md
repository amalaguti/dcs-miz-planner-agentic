## 1. Place geometry meta

- [x] 1.1 Add numeric recipes to `french_coast_strike_belt` and
      `mid_channel_shipping` (bearing/distance; optional path offsets; notes)
- [x] 1.2 Add or enrich harbour/coastal sea place (or harbour keys) with a
      water/coastal band — not UK-field distances

## 2. Invent guidance + repair

- [x] 2.1 Prompts + Spec schema: use place recipes; land path on land; sea on water
- [x] 2.2 Enrich `host_spec_repair_nudge` for domain mismatch codes with recipes
- [x] 2.3 Tool description note if needed (`list_mission_options` place meta)

## 3. Tests + backlog + accept

- [x] 3.1 Hermetic tests for place meta + repair nudge geometry text
- [x] 3.2 BACKLOG `#8f` building→done; next promote note
- [x] 3.3 Ruff + full pytest green
- [x] 3.4 Accept: hermetic tests green; live invent re-eval still fails some
      convoy path points over water (follow-on: path clamp / fewer path points)
