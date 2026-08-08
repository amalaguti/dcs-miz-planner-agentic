## Why

Live invent after `#8d` picks units and AI presets well, but Specs often fail
validation on **geometry/domain**: land convoy paths over water, harbour strikes
~4 km from Manston, U-boat GA domain mismatches. Repair nudges are generic and
do not re-ground the model on Channel place recipes.

## What Changes

- Add numeric geometry recipes to `channel_place` meta (and/or strike class
  notes) from accepted Manston examples (inland / mid-Channel / harbour bands).
- Invent prompts + Spec schema: copy place geometry; keep land paths on land
  near strike; sea patrol/static on water.
- Strengthen validation repair nudges for `motion_domain_mismatch` /
  `strike_domain_mismatch` (include place recipe + example bearings).
- Optional thin helper or tool note — prefer meta-first (no new compile fields).
- Hermetic tests for place meta + repair nudge content; re-run live invent suite
  as accept (CLI/API; ME not required).

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `mission-options`: `channel_place` geometry recipes (bearing/distance bands).
- `nl-agent`: invent geometry guidance + domain-aware repair nudges.
- `agent-tools`: optional tool/schema notes pointing at place geometry meta.
- `golden-fixtures`: tests for place recipes / repair nudge strings.

## Impact

- `planning_options.yaml`, `agent/prompts.py` (repair), `spec_schema.py`,
  tests, BACKLOG `#8f`.
- Does not change validate/compile domain rules (already ship); invent must
  obey them.

## Non-goals

- Full terrain mesh / auto-snap; multi-theatre geometry.
- Expanding unit shelves (`#8e` / later).
- Deterministic host rewrite of Specs (defer unless LLM repair still fails).
- ME Instant Action accept (hermetic + live invent validate is enough).

## Acceptance

Place meta exposes inland ~125°/76 km and mid-Channel ~140°/40 km (or documented
bands); repair nudge mentions domain/geometry codes with recipes; invent
prompts/schema warn land-path-over-water. Live re-eval of convoy/flak/U-boat/
harbour prompts validates with coherent domain (optional same-session).
