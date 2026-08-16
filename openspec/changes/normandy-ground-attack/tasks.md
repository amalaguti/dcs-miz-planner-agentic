## 1. Example, place, domain

- [x] 1.1 Add `examples/needs_oar_point_ground_attack.yaml` (NeedsOarPoint, Spitfire, `spitfire_2x250_slipper`, strike 180°/133 km/2000 m, Blitz + flak18 ThirdReich, document PyDCS measurement)
- [x] 1.2 Add `channel_place` `maupertus_inland_strike`; extend `needs_oar_point_home` mission_types with `ground_attack`
- [x] 1.3 Extend `channel_domain.py`: Normandy UK–Cotentin chord; `domain_supported` includes Normandy; Channel chord unchanged

## 2. Invent, schema, catalog

- [x] 2.1 Allow Normandy `ground_attack` in invent refuse table; intercept/escort/recon still refuse every turn
- [x] 2.2 Schema: Normandy+GA loads the new example; dedicated notes (no Channel concatenation); intercept/escort/recon still raise
- [x] 2.3 Update prompts, repair nudges, `SPEC_SHAPE_REMINDER`, `infer_theatre` (Maupertus)
- [x] 2.4 `list_strike_targets(theatre="Normandy")` returns WWII land units; sea stays Channel-only; other maps stay empty

## 3. Tests and docs

- [x] 3.1 Validate+compile example (airdromeId 28, Blitz, flak18, theatre Normandy); domain 180/63 sea vs 180/133 land; Channel GA still land
- [x] 3.2 Schema/invent tests: Normandy GA allowed; intercept still refused; strike list includes Blitz not U-boat; Channel intercept goldens unchanged
- [x] 3.3 Update BACKLOG M7, README, LESSONS (`channel-ids` / `agent-tooling`), matching skills; path clamp stays TheChannel-only
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
