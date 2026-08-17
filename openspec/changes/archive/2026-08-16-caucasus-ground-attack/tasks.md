## 1. Example, place, domain, registry

- [x] 1.1 Add `examples/batumi_kutaisi_ground_attack.yaml` (Batumi, Su-25T,
      `su25t_2x_fab250`, strike 43°/110 km/2000 m, Ural-375 Russia red, document
      PyDCS measurement)
- [x] 1.2 Add `channel_place` `kutaisi_inland_strike`; extend `batumi_home`
      mission_types with `ground_attack`; add `modern_soft_vehicles` class (do not
      append Ural ids onto Channel `soft_vehicles`)
- [x] 1.3 Extend `channel_domain.py`: Caucasus west-of-coast recipe;
      `domain_supported` includes Caucasus; Channel/Normandy chords unchanged
- [x] 1.4 Add `era/modern/ground_units.yaml` (Ural-375, GAZ-66, ZIL-135) and
      `era/modern/payloads.yaml` (`su25t_2x_fab250` pylons 5+7 FAB-250 CLSID);
      registry unions with collision guards

## 2. Invent, schema, catalog

- [x] 2.1 Allow Caucasus `ground_attack` in invent refuse table; intercept/escort/recon
      still refuse every turn
- [x] 2.2 Schema: Caucasus+GA loads the new example; dedicated notes (no Channel
      concatenation); intercept/escort/recon still raise
- [x] 2.3 Update prompts, repair nudges, `SPEC_SHAPE_REMINDER`, tool descriptions
- [x] 2.4 `list_strike_targets(theatre="Caucasus")` returns the three modern trucks;
      Channel list excludes them; Normandy dual-offer stays WWII land; other maps
      stay empty

## 3. Tests and docs

- [x] 3.1 Validate+compile example (airdromeId 22, Ural-375, Russia, FAB-250,
      theatre Caucasus); domain 270/40 sea vs 43/110 land; Channel GA still land;
      retarget fail-closed domain onto Syria
- [x] 3.2 Schema/invent tests: Caucasus GA allowed; intercept still refused;
      strike list includes Ural-375 not Blitz; Channel intercept goldens unchanged
- [x] 3.3 Update BACKLOG F2e, README, LESSONS (`channel-ids` / `agent-tooling`),
      matching skills + orchestrator baseline; path clamp stays TheChannel-only
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
