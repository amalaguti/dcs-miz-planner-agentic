## Why

Syria Stage A bound the map with Incirlik only. The NL agent cannot name other
verified Syria fields, and modern identity has no Syria-nation host for the
inland red side. Stage B deepens geography and identity without combat.

## What Changes

- Curate eight Syria airfields from live PyDCS `airport_list()` (keep
  `Incirlik=16`; add `RamatDavid`, `Damascus`, `BeirutRaficHariri`, `Aleppo`,
  `BasselAlAssad`, `Palmyra`, `KingHusseinAirCollege`). Never invent ids;
  never dump all 59 fields.
- Add PyDCS country `Syria` to `era/modern` only (not WWII). Player aircraft
  stays `Su-25T` at 251.0 MHz. Invent/schema remain Incirlik, Turkey blue,
  free_flight only.
- Ship `examples/palmyra_cold_freeflight.yaml` (Palmyra, Syria red, Su-25T) so
  extra-AF + Syria-nation compile. Theatre-scoped lookup: Palmyra 28 is not
  Mozdok and not NeedsOarPoint.
- Extend `infer_theatre` to the new Spec keys. Catalog lists the new airfields
  and Syria (country) after sync.

## Non-goals

- Places, CAP/GA/intercept/escort/recon, domain classifier, intercept spawn,
  path clamp, Israel/Jordan/Lebanon/Iran countries, all 59 airfields,
  `theatre_place` rename, modern payloads/failures, Caucasus Stage D.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: eight curated Syria airfields; `Syria` country in modern.
- `agent-catalog`: catalog lists the new airfields and Syria country after sync.
- `mission-validation`: extra Syria AFs and Syria country (era-filtered) validate.
- `miz-compiler`: Palmyra cold FF compiles (N1-style contracts).
- `nl-agent`: infer theatre from new AF keys; invent still FF-only at Incirlik.
- `agent-tools`: lookup of new keys; schema example stays Incirlik.

## Impact

`data/theatres/Syria/airfields.yaml`, `data/era/modern/countries.yaml`,
`infer_theatre`, Palmyra example + tests. Invent stay FF-only. Channel goldens
stay green. Acceptance: hermetic pytest + compile Palmyra. ME Instant Action is
do-soon after merge.
