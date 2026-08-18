## 1. Example and place

- [x] 1.1 Add `examples/nellis_creech_recon.yaml` (clone
      `examples/incirlik_aleppo_recon.yaml`: Nellis, Su-25T, USA blue, no
      payload, Ural-375 observe country Russia, 303/85/2000, radius_m 3000,
      mark true, weapons-hold copy, date 2024-06-06 09:00 sunny_clear;
      document PyDCS measurement: Creech 302.86°/69.47 km; 303/70 REJECT;
      303/85 ACCEPT 15.53 km; station x=-351901.05702 y=-88520.23509;
      do not copy CAP 350/40)
- [x] 1.2 Extend `creech_range_strike` and `nellis_home` mission_types with
      `recon` (do not add recon to `nellis_north_range_cap`; family stays
      `channel_place`; no new unit YAML; dual-offer untouched)

## 2. Invent and schema

- [x] 2.1 Allow Nevada `recon` in invent table (all six types:
      empty `_NEVADA_UNSUPPORTED_COMBAT`; `_THEATRE_ALLOWED_TYPES["Nevada"]`
      = `frozenset(MissionType)`; flip host/chat/accept/planner refuse
      strings in `immersion.py`)
- [x] 2.2 Schema: Nevada+recon loads the new example; dedicated
      `_NEVADA_RECON_NOTES` (no french_coast concatenation); FF/CAP/
      intercept/escort/GA example files unchanged; lightly edit those notes
      so they no longer say refuse recon; stub LLM stays Manston
- [x] 2.3 Update prompts, repair nudges (Creech 303/85 for land strike **or
      recon**, not CAP 350/40), `SPEC_SHAPE_REMINDER`, `tool_bridge`
      schema description

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel recon goldens unchanged;
      compile MUST NOT contain CAP station coords or french-coast tokens
- [x] 3.2 Schema/invent tests: Nevada recon allowed (flip
      `test_schema_theatre_nevada_combat_no_manston_skeleton` and
      `test_nevada_cap_invent_nudge`); Falklands still fail-closed
- [x] 3.3 `test_validate_nellis_recon` + `test_compile_nellis_recon_contracts`
      in `test_nevada_freeflight.py`; `fixtures_support` `NEVADA_RECON` helpers
- [x] 3.4 Chat/planner write tests: `test_chat_nevada_recon_is_captured`,
      `test_planner_nevada_recon_is_written` (clone Syria recon tests);
      repair nudge still uses Creech 303/85 (extend mismatch hint to recon)
- [x] 3.5 Update BACKLOG F4g, README, LESSONS (`agent-tooling` / `channel-ids`
      + index), matching skills + orchestrator baseline (Nevada invent all
      six types; next promote Falklands B)
- [x] 3.6 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
