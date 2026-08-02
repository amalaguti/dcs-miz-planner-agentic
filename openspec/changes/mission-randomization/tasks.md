## 1. Core randomize API

- [x] 1.1 Add `randomize.py` with `AXES`, `randomize_mission_spec(spec, seed, axes=None)` using `random.Random(seed)` and documented draw order
- [x] 1.2 Implement axis handlers: weather, time (±90 min / 5-min snap), geometry (cap/strike/escort bounds), opposition (count/aircraft/skill from registry)
- [x] 1.3 Preserve identity fields; raise clear errors for bad seed / unknown axes

## 2. CLI and agent surfaces

- [x] 2.1 Add `dcs-miz randomize` CLI (`--seed`, `--axes`, `-o`, validate-by-default, optional `--annotate` / `--no-validate`)
- [x] 2.2 Add `randomize_mission` tool on the tools surface; export from `tools/__init__.py`
- [x] 2.3 Wire tool into agent tool list / prompts if there is an explicit registry of tool names

## 3. Planning options and catalog

- [x] 3.1 Add `randomization` / `seeded_reroll` advisory row to `planning_options.yaml`
- [x] 3.2 Bump catalog schema version if needed so sync picks up the new option; update catalog/tools tests

## 4. Tests and docs

- [x] 4.1 Unit tests: seed stability, different seeds differ, identity preserved, unknown axis fails, each axis behaviour
- [x] 4.2 Integration: CLI randomize → validate; tool `randomize_mission` ok path; free-flight + one combat example
- [x] 4.3 Update README / BACKLOG / ARCHITECTURE briefly; note LESSONS only if a non-obvious pitfall appears
- [x] 4.4 Compile two seeds from the same base to `out/` for in-game compare; note accept result in tasks when done
  - Accepted 2026-08-02: seeded CAP rerolls (`out/manston_cap_seed42.miz` vs
    `seed99.miz`) — weather/time/geometry/opposition differ; player Manston cold
    Spitfire preserved. Seed is build-scoped (keep YAML/.miz to lock a sortie).
