## Why

Slice 0b bound invent to Normandy **free_flight only** and fail-closed combat
helpers. Needs Oar Point is the only curated airfield. The NL agent still cannot
plan a Normandy CAP even though CAP is airfield-relative and already compiles.
F1 deepens the bound map with verified airfields, place recipes, and CAP invent.

## What Changes

- Curate eight Normandy airfields from live PyDCS `airport_list()` (keep
  `NeedsOarPoint=28`; add Chailey, Funtington, Tangmere, `FordAF`, Maupertus,
  `SaintPierreduMont`, Carpiquet). Never invent ids; never dump all 38 fields.
- Add `channel_place` rows `needs_oar_point_home` and `cherbourg_channel_cap`
  (`meta.theatre: Normandy`; CAP station 180° / 63 km from Needs Oar Point).
  Family name stays `channel_place` (no `theatre_place` rename).
- Ship `examples/needs_oar_point_cap.yaml` (Spitfire at NeedsOarPoint, light
  Bf-109K-4, 1944-06-06 `sunny_clear`).
- Lift invent refuse for **CAP only**. Intercept / ground_attack / escort /
  recon stay every-turn refuse (never capture refused drafts). Schema
  `theatre=Normandy` + `cap` uses the new example (no Manston skeleton).
- `list_mission_options` optional `theatre=` filters `channel_place` by
  `meta.theatre` so Channel invent cannot pick Normandy places (and vice versa).

## Non-goals

- Normandy intercept spawn, land/sea domain classifier, path clamp, GA/recon
  examples, strike-catalog dual-tag, extra countries (USA), extra unit YAML,
  fake ICAO, `Normandy2`, all 38 airfields, `theatre_place` rename.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: eight curated Normandy airfields; `FordAF` → 31.
- `nl-agent`: Normandy invent is free_flight **or CAP**; other combat types
  still refuse; do not copy Channel geometry onto Normandy.
- `agent-tools`: schema Normandy+CAP example; `list_mission_options(theatre=)`.
- `mission-options`: two Normandy `channel_place` rows.
- `agent-catalog`: catalog lists the new airfields and places after sync.
- `miz-compiler`: Normandy CAP compiles (N1-style contracts).
- `mission-validation`: Normandy CAP validates; intercept still
  `intercept_unsupported_theatre`.

## Impact

`data/theatres/Normandy/airfields.yaml`, `planning_options.yaml`, invent
nudge/schema/prompts, `list_mission_options`, new CAP example + tests. Domain,
intercept spawn, path clamp, and strike `theatre_id=TheChannel` stay as Slice 0b.
Channel goldens stay green. Acceptance: hermetic pytest + compile the new CAP
example. ME Instant Action on Needs Oar Point CAP is do-soon after merge.
