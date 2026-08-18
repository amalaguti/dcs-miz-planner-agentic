## 1. Example and place

- [x] 1.1 Add `examples/mount_pleasant_east_falkland_recon.yaml` (clone
      `examples/nellis_creech_recon.yaml`: MountPleasant, Su-25T, UK blue, no
      payload, Ural-375 observe country Argentina, 269/21/2000, radius_m 3000,
      mark true, weapons-hold copy, date 2024-06-06 09:00 sunny_clear;
      document PyDCS: GG 268.80°/36.01 km; 269/36 REJECT 0.13 km; 269/51
      REJECT Sound; 269/21 ACCEPT 15.02 km short of GG; station
      x=72951.81977681704 y=26171.946448715786; CAP 150/40 is
      x=38677.30416062245 y=67168.748047)
- [x] 1.2 Extend `east_falkland_inland_strike` and `mount_pleasant_home`
      mission_types with `recon` (do not add recon to
      `mount_pleasant_south_atlantic_cap`; family stays `channel_place`; no
      new unit YAML; dual-offer untouched)

## 2. Invent and schema

- [x] 2.1 Allow Falklands `recon` in invent table (all six types:
      empty `_FALKLANDS_UNSUPPORTED_COMBAT`; `_THEATRE_ALLOWED_TYPES["Falklands"]`
      = `frozenset(MissionType)`; flip host/chat/accept/planner refuse
      strings in `immersion.py`)
- [x] 2.2 Schema: Falklands+recon loads the new example; dedicated
      `_FALKLANDS_RECON_NOTES` (no french_coast concatenation); FF/CAP/
      intercept/escort/GA example files unchanged; lightly edit those notes
      so they no longer say refuse recon; stub LLM stays Manston
- [x] 2.3 Update prompts, repair nudges (East Falkland 269/21 for land strike
      **or recon**, not CAP 150/40), `SPEC_SHAPE_REMINDER`, `tool_bridge`
      schema description

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel recon goldens unchanged;
      compile MUST NOT contain CAP station coords, Hawkinge `30989.935547`,
      FAB-250, or french-coast tokens; do not edit `intercept_spawn.py` or
      `channel_domain.py`
- [x] 3.2 Schema/invent tests: Falklands recon allowed (flip
      `test_schema_theatre_falklands_combat_no_manston_skeleton` and
      `test_falklands_cap_invent_nudge`); unbound Kola still fail-closed
- [x] 3.3 `test_validate_mount_pleasant_recon` +
      `test_compile_mount_pleasant_recon_contracts` in
      `test_falklands_freeflight.py`; `fixtures_support` `FALKLANDS_RECON`
      helpers (airdromeId 2, 32400, 251.0, Reconnaissance, recon_aoi,
      Ural-375, UK, Argentina, station pair present; CAP coords / FAB-250 /
      ThirdReich / Hawkinge absent)
- [x] 3.4 Chat/planner write tests: `test_chat_falklands_recon_is_captured`,
      `test_planner_falklands_recon_is_written` (clone Nevada recon tests);
      repair nudge uses East Falkland 269/21 for recon mismatch
- [x] 3.5 Update BACKLOG F5g, README, LESSONS (`agent-tooling` / `channel-ids`
      + index), matching skills + orchestrator baseline (Falklands invent all
      six types; next promote unbound stay discovered-only)
- [x] 3.6 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
