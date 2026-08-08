## Why

GA and recon `targets[]` are always placed once (static). Mid-Channel ships and
road convoys should usually move; harbour docks and emplaced AAA should stay put.
Without optional motion, U-boat/truck sorties feel parked and the agent cannot
express under-way vs docked contacts.

## What Changes

- Extend `GroundTarget` (GA + recon contacts) with optional **motion**: default
  `static` (omit-compatible); `patrol` + radius; or short looping `path` of
  airfield-relative waypoints.
- Compiler: native ME waypoints / go-to loop on ship **and** vehicle groups
  (curated speeds by domain). Static = today’s placement only. No Lua.
- Validation: motion params sane; path points stay on matching land/sea domain
  when practical; omit/static never required.
- Examples: update mid-Channel U-boat recon/hunt to **patrol**; add or update a
  soft-vehicle GA example with a short **path** (convoy). Existing AAA / static
  Specs unchanged.
- Agent / planning: prefer motion for mid-Channel shipping and soft vehicles;
  static for harbour / AAA. Briefs may say contact is under way.
- Tests + ME accept for moving sea + land targets.

## Capabilities

### New Capabilities

- *(none — extends existing target placement)*

### Modified Capabilities

- `mission-spec`: optional per-target motion fields on `targets[]`.
- `mission-validation`: motion shape + domain sanity.
- `miz-compiler`: emit ship/vehicle waypoints for patrol/path.
- `golden-fixtures`: U-boat patrol + truck path examples / asserts.
- `mission-options` / `nl-agent` / `agent-tools` / `squadron-voice` (light):
  heuristics and brief language for under-way vs static contacts.

## Impact

- `models.py` (`GroundTarget`), `validation.py`, `compiler/pydcs_compiler.py`
  (GA + recon placement), examples, planning_options / prompts / voice,
  tests, BACKLOG `#15g`.
- **Non-goals v1:** ASW/crash-dive; auto rail-mesh trains; LLM free-form routes;
  Mist/MOOSE; new unit classes (tanks/troops/trains stay future registry).
- Acceptance: ME shows U-boat moving on water and a truck group on a short path;
  Specs without motion stay static.
