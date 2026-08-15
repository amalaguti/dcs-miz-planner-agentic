## Why

Slice 0 split YAML packages, but invent, domain, intercept spawn, path clamp,
METAR, countries, and strike tags still assume TheChannel. A Normandy combat
Spec would get Channel Hawkinge coords and the UK–FR chord. Unlock offerable
theatres for invent and fail closed where Channel recipes do not apply.

## What Changes

- Invent/chat may use any offerable theatre (`known ∧ available ∧
  planner_supported`). Normandy invent is **free_flight only** (NeedsOarPoint,
  Spitfire, `sunny_clear`, UK blue). Combat types refuse until F1 places.
- Domain, intercept spawn, and Channel path clamp become theatre-keyed.
  Non-Channel land/sea combat → `domain_unsupported_theatre`. Non-Channel
  intercept → `intercept_unsupported_theatre`. Path clamp skips on
  non-Channel. Channel Hawkinge/Dover literals stay bit-identical.
- Join-up 120° stays generic airfield-relative.
- Packaged `data/era/wwii/countries.yaml` (`UK`, `ThirdReich` only).
- Strike catalog: `era_id=wwii`, keep `theatre_id=TheChannel`. Do not tag
  Normandy combat. Schema v6.
- `channel_place` rows get `meta.theatre: TheChannel` (no rename).
- METAR ICAO `EGMH` is Channel-only; Normandy briefs omit a fake ICAO.
- Miz-patch reweather fail-closed unless theatre is TheChannel.

## Non-goals

- Normandy places, intercept recipe, extra AFs, combat examples (F1).
- `theatre_place` rename; modern countries; invented ICAO; PyDCS `Normandy2`.
- Bind unbound terrains. ME Instant Action as a merge gate.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: offerable theatres; Normandy free_flight only; Channel geometry
  cues stay Channel-only.
- `mission-validation`: `domain_unsupported_theatre` and
  `intercept_unsupported_theatre`.
- `miz-compiler`: intercept spawn Channel-only; no Hawkinge dump on Normandy.
- `agent-catalog`: countries from era YAML; strike `era_id`; keep Channel
  combat tag.
- `agent-tools`: schema `theatre=`; `list_strike_targets(theatre=)`.
- `mission-options`: `channel_place` tagged TheChannel.
- `mission-briefing`: synthetic METAR ICAO Channel-only.
- `reference-registry`: WWII countries package.
- `weather-reweather`: miz-patch fail-closed unless TheChannel.

## Impact

`channel_domain.py`, `validation.py`, `pydcs_compiler.py`, invent prompts/
schema/path_clamp, `registry.py`, catalog sync/store, `weather_metar.py`,
`reweather.py`, `planning_options.yaml`, new `countries.yaml`. Channel goldens
including intercept stay green. Acceptance: hermetic pytest + compile Manston
and Needs Oar Point. ME Instant Action is do-soon after merge.
