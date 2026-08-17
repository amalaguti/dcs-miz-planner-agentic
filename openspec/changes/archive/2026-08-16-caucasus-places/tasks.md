## 1. Places and example

- [x] 1.1 Add `channel_place` rows `batumi_home` and `batumi_black_sea_cap` to
      `data/shared/planning_options.yaml` with `meta.theatre: Caucasus`. CAP
      meta: bearing 270, distance 40 km, altitude 4000 m, domain sea, example
      `examples/batumi_black_sea_cap.yaml`. Keep family `channel_place`.
- [x] 1.2 Add `examples/batumi_black_sea_cap.yaml`: theatre Caucasus, 2024-06-06
      09:00 `sunny_clear`, player `Su-25T` / `Batumi` / Georgia blue /
      cold_parking, CAP 270/40/4000 circle weapons_free, two Average `Su-25T`
      Russia red, `objectives: [{type: patrol}]`.

## 2. Tests and compile contracts

- [x] 2.1 Add N1-style validate + compile contracts (extend
      `test_caucasus_freeflight.py` + `fixtures_support`): zip members, theatre
      `Caucasus`, `airdromeId=22`, `Su-25T`, start_time 32400, TakeOffParking,
      Player, frequency 251.0, CAP Orbit Circle, `Russia`. Assert player
      `["type"]="Su-25T"`. No full golden dump. Channel CAP goldens unchanged.
- [x] 2.2 Flip Caucasus CAP invent/schema tests to accept; use intercept as the
      still-refused type. Add positives: CAP nudge is None; chat/planner may
      capture/write CAP; `list_mission_options(theatre=Caucasus)` includes
      Batumi places and omits Cherbourg/Manston places.

## 3. Invent, schema, prompts

- [x] 3.1 Allow Caucasus CAP in `_THEATRE_ALLOWED_TYPES` and refuse copy.
      Intercept / GA / escort / recon stay every-turn refuse.
- [x] 3.2 Schema: `build_spec_schema("cap", theatre="Caucasus")` loads the new
      example; intercept/GA/escort/recon still raise. Dedicated Caucasus CAP
      notes (no `_COMMON_NOTES` concatenation). Update prompts, `SPEC_SHAPE_REMINDER`,
      `tool_bridge`. Stub LLM stays Manston.

## 4. Docs

- [x] 4.1 BACKLOG F2d / Stage C status; README Status (Caucasus CAP invent).
- [x] 4.2 Lessons + skills: CAP 270/40 from Batumi; enemies Russia+Su-25T;
      domain/intercept/path clamp still fail-closed; do not copy Cherbourg 180/63.

## 5. Merge gate

- [x] 5.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 5.2 `uv run pytest -q`
- [x] 5.3 Compile `examples/batumi_black_sea_cap.yaml`
- [ ] 5.4 ME Instant Action on Batumi CAP (human do-soon after merge — not a merge blocker)
