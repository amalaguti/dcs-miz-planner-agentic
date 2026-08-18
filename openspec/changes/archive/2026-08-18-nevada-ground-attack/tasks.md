## 1. Example, place, domain

- [x] 1.1 Add `examples/nellis_creech_ground_attack.yaml` (Nellis, Su-25T,
      `su25t_2x_fab250`, strike 303°/85 km/2000 m, Ural-375/GAZ-66 Russia red,
      document PyDCS measurement: Creech 302.86°/69.47 km; 303/70 REJECT 0.56 km;
      303/85 ACCEPT 15.53 km; station x=-351901.05702 y=-88520.23509)
- [x] 1.2 Add `channel_place` `creech_range_strike`; extend `nellis_home`
      mission_types with `ground_attack`; extend `modern_soft_vehicles` cues
      (do not append Ural ids onto Channel `soft_vehicles`; do not add GA to
      `nellis_north_range_cap`; place mission_types GA only)
- [x] 1.3 Extend `channel_domain.py`: Nevada desert-default land on curated
      ids `{4, 2, 1, 18, 15, 8, 6, 13}` only; near AF 3 km → land; else land;
      do not promote Echo Bay 7; `domain_supported` includes Nevada;
      Channel/Normandy/Caucasus/Syria chords unchanged; Falklands stays
      fail-closed

## 2. Invent, schema, catalog

- [x] 2.1 Allow Nevada `ground_attack` in invent refuse table
      (`_NEVADA_UNSUPPORTED_COMBAT`, `_THEATRE_ALLOWED_TYPES`); recon still
      refuses every turn
- [x] 2.2 Schema: Nevada+GA loads the new example; dedicated `_NEVADA_GA_NOTES`
      (no Manston french-coast concatenation); FF/CAP/intercept/escort example
      files unchanged; lightly edit those notes so they no longer say refuse GA;
      stub LLM stays Manston
- [x] 2.3 Update prompts, `SPEC_SHAPE_REMINDER`, tool_bridge, repair nudges
      (Creech 303/85 not CAP 350/40)
- [x] 2.4 `list_strike_targets(theatre="Nevada")` dual-offers the three modern
      trucks; Channel list excludes them; Falklands stay empty; do not retag
      stored `theatre_id`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; add `test_nevada_strike_domain_classified`
      (350/40 land, 303/85 land); flip `test_domain_fail_closed_on_nevada_strike`
      onto Falklands; Channel goldens unchanged
- [x] 3.2 Schema/invent/catalog flips: `test_schema_theatre_nevada_combat_no_manston_skeleton`
      (GA loads; recon still raises); `test_strike_units_era_and_channel_tag`
      (Nevada Ural-375 present); `test_channel_place_tagged_thechannel`
      (`creech_range_strike`; `nellis_home` has GA; CAP place does not);
      `test_nevada_cap_invent_nudge` (GA no longer refused)
- [x] 3.3 `test_validate_nellis_ground_attack` +
      `test_compile_nellis_ground_attack_contracts` in
      `test_nevada_freeflight.py`; `fixtures_support` `NEVADA_GA` helpers
- [x] 3.4 Chat/planner write tests: `test_chat_nevada_ga_is_captured`,
      `test_planner_nevada_ground_attack_is_written`; repair
      `test_host_spec_repair_nudge_nevada_mismatch_uses_creech`
- [x] 3.5 Update BACKLOG F4f, README, LESSONS (`agent-tooling` / `channel-ids`
      + index), matching skills + orchestrator baseline (Nevada invent
      FF+CAP+intercept+escort+GA; recon still refuse; next promote Nevada recon
      or Falklands B)
- [x] 3.6 `uv run ruff check` + `ruff format --check` + `uv run pytest -q` +
      compile the new example
