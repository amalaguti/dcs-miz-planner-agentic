## Why

After `#8f`, invent usually places strike/AOI on the right Channel band, but live
eval still fails **convoy path points** over water and **harbour** asks that keep
coastal geometry while inventing **land trucks**. Place recipes alone are not
enough — path invent and harbour→sea unit binding need hardening before shelf
expand.

## What Changes

- Harden invent guidance: land `path` MUST copy place `path_point_deltas` (or stay
  within a tight band of strike); invent prefers **2–3** path points, not long
  free routes.
- Enrich domain-mismatch repair with an **exact copy-paste path YAML** snippet for
  the French-coast belt (from accepted convoy example / place meta).
- Harbour harden: prompts/schema/repair insist harbour/dock → `list_strike_targets
  (domain=sea)` + `coastal_harbour` + static + `harbour_static` (never soft land
  units).
- Optional narrow **host path clamp** when land path fails domain: rewrite path
  points from place recipe relative to a land strike (no full Spec rewrite).
- Hermetic tests; live invent re-eval of convoy + harbour as accept (CLI/API).

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `mission-options`: path recipe invent contract; harbour→sea binding notes.
- `nl-agent`: path/harbour invent + repair; optional host path clamp.
- `mission-validation`: optional clearer path-point domain errors (if needed).
- `golden-fixtures`: tests for path/harbour harden behaviour.

## Impact

- `planning_options.yaml`, `agent/prompts.py`, `spec_schema.py`, possibly a small
  host helper near validate/repair; tests; BACKLOG `#8g`.
- Does not expand unit shelves (`#8e`); does not change compile motion emit.

## Non-goals

- Full terrain mesh / auto-snap to roads or bathymetry.
- Expanding Channel unit shelves (`#8e`).
- Host rewrite of unit ids (harbour wrong-unit stays repair/nudge + guidance).
- ME Instant Action accept (hermetic + live invent validate is enough).

## Acceptance

Convoy invent validates with land path points near strike (no mid-Channel path
waypoints). Harbour invent uses sea unit ids + coastal water geometry (or fails
repair with an explicit sea-unit nudge). Hermetic tests pin path recipe / harbour
guidance / clamp behaviour.
