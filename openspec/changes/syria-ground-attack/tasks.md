## 1. Example, place, domain

- [x] 1.1 Add `examples/incirlik_aleppo_ground_attack.yaml` (Incirlik, Su-25T,
      `su25t_2x_fab250`, strike 121°/200 km/2000 m, Ural-375 Syria red, document
      PyDCS measurement)
- [x] 1.2 Add `channel_place` `aleppo_inland_strike`; extend `incirlik_home`
      mission_types with `ground_attack`; extend `modern_soft_vehicles` cues
      (do not append Ural ids onto Channel `soft_vehicles`; do not add GA to
      `incirlik_iskenderun_cap`)
- [x] 1.3 Extend `channel_domain.py`: Syria coastal/inland recipe; Incirlik
      seaward 165–195°; Bassel/Beirut 225–315° only; `domain_supported`
      includes Syria; Channel/Normandy/Caucasus chords unchanged

## 2. Invent, schema, catalog

- [x] 2.1 Allow Syria `ground_attack` in invent refuse table; recon still
      refuses every turn
- [x] 2.2 Schema: Syria+GA loads the new example; dedicated notes (no
      Manston french-coast concatenation)
- [x] 2.3 Update prompts, repair nudges (Aleppo 121/200 not Iskenderun 180/40),
      `SPEC_SHAPE_REMINDER`
- [x] 2.4 `list_strike_targets(theatre="Syria")` dual-offers the three modern
      trucks; Channel list excludes them; Nevada/Falklands stay empty

## 3. Tests and docs

- [x] 3.1 Validate+compile example; domain 180/40 sea vs 121/200 land vs
      270/40 land; retarget fail-closed domain onto Nevada; Channel goldens
      unchanged
- [x] 3.2 Schema/invent tests: Syria GA allowed; recon still refused; strike
      list includes Ural-375 not Blitz
- [x] 3.3 Update BACKLOG F3f, README, LESSONS (`agent-tooling` / `channel-ids`),
      matching skills + orchestrator baseline
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
