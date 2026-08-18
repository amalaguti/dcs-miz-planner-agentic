## 1. Example, place, domain

- [x] 1.1 Add `examples/mount_pleasant_east_falkland_ground_attack.yaml` (MountPleasant, Su-25T, `su25t_2x_fab250`, strike 269°/21 km/2000 m, Ural-375/GAZ-66 Argentina red; document PyDCS: GG 268.80°/36.01 km; 269/36 REJECT 0.13 km; 269/51 REJECT Sound; 269/21 ACCEPT 15.02 km short of GG; station x=72951.81977681704 y=26171.946448715786; CAP 150/40 is x=38677.30416062245 y=67168.748047)
- [x] 1.2 Add `channel_place` `east_falkland_inland_strike`; extend `mount_pleasant_home` with `ground_attack`; extend `modern_soft_vehicles` cues (`falklands`, `mount pleasant`, `argentina`). Do not add GA to `mount_pleasant_south_atlantic_cap`; place mission_types GA only
- [x] 1.3 Extend `channel_domain.py`: Falklands Syria-style seaward windows on `{1,2,3,24,29}`; MPA 120–180°; near AF 3 km → land; `domain_supported` includes Falklands; other chords unchanged; do not invent 4/28; do not dump 27 AFs

## 2. Invent, schema, catalog

- [x] 2.1 Allow Falklands `ground_attack` in invent refuse table; recon still refuses every turn
- [x] 2.2 Schema: Falklands+GA loads the new example; dedicated `_FALKLANDS_GA_NOTES` (no Manston french-coast concatenation); FF/CAP/intercept/escort example files unchanged
- [x] 2.3 Update prompts, `SPEC_SHAPE_REMINDER`, tool_bridge, repair nudges (East Falkland 269/21 not CAP 150/40)
- [x] 2.4 `list_strike_targets(theatre="Falklands")` dual-offers the three modern trucks; Channel list excludes them; do not retag stored `theatre_id`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; `test_falklands_strike_domain_classified` (150/40 sea, 269/21 land); flip fail-closed/hint tests onto Kola; Channel goldens unchanged; do not edit `intercept_spawn.py`
- [x] 3.2 Schema/invent/catalog flips: GA loads; recon still raises; strike list includes Ural-375; CAP place does not list GA
- [x] 3.3 `test_validate_mount_pleasant_ground_attack` + compile contracts in `test_falklands_freeflight.py`; `fixtures_support` helpers
- [x] 3.4 Chat/planner write tests; repair nudge uses East Falkland 269/21
- [x] 3.5 Update BACKLOG F5f, README, LESSONS, matching skills + orchestrator (next promote: Falklands recon)
- [x] 3.6 `uv run ruff check` + `ruff format --check` + `uv run pytest -q` + compile the new example
