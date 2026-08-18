## Why

Falklands Stage A bound the map with MountPleasant only. The NL agent cannot
name other verified South Atlantic fields, and modern identity has no
Argentina-nation host for the extra-AF smoke. Stage B deepens geography and
identity without combat.

## What Changes

- Curate eight Falklands airfields from live PyDCS `airport_list()` (keep
  `MountPleasant=2`; add `PortStanley`, `SanCarlosFOB`, `RioGallegos`,
  `RioGrande`, `Ushuaia`, `PuntaArenas`, `SanJulian`). Never invent ids;
  never dump all 27 fields. Spec keys camelCase without underscores
  (`RioGallegos` ≠ `Rio_Gallegos`). Ids 4 and 28 are absent — do not invent.
- Add PyDCS country `Argentina` (id 83) to `era/modern` only (not WWII).
  Defer Chile. Player aircraft stays `Su-25T` at 251.0 MHz. Invent/schema
  remain MountPleasant, UK blue, free_flight only.
- Ship `examples/rio_gallegos_cold_freeflight.yaml` (RioGallegos, Argentina
  red, Su-25T) so extra-AF + Argentina-nation compile. Theatre-scoped lookup:
  RioGallegos 5 is not Manston 5. Port Stanley is lookup-only (heli) — do not
  compile Su-25T there.
- Extend `infer_theatre` to the eight Spec keys; keep `Mount_Pleasant` alias.
  Registry MUST reject `Port_Stanley`, `Rio_Gallegos`, etc. Catalog lists
  the new airfields and Argentina after sync.

## Non-goals

- Places, CAP/GA/intercept/escort/recon, domain classifier, intercept spawn,
  path clamp, dual-offer strike units, Chile, dump of 27 fields, payloads,
  `theatre_place` rename.
- ME Instant Action as a merge gate (human do-soon after merge).
- Next slice `falklands-places` (Stage C CAP) — 0b is on master, but not this
  change.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: eight curated Falklands airfields; `Argentina` in modern.
- `agent-catalog`: catalog lists the new airfields and Argentina after sync.
- `mission-validation`: extra Falklands AFs and Argentina (era-filtered) validate.
- `miz-compiler`: Rio Gallegos cold FF compiles (N1-style contracts).
- `nl-agent`: infer theatre from new AF keys; invent still FF-only at MountPleasant.
- `agent-tools`: lookup of new keys; schema example stays MountPleasant.

## Impact

`data/theatres/Falklands/airfields.yaml`, `data/era/modern/countries.yaml`,
`infer_theatre`, Rio Gallegos example + tests. Invent stay FF-only. Channel
goldens stay green. Acceptance: hermetic pytest + compile Rio Gallegos. ME
Instant Action is do-soon after merge. BACKLOG F5b; next promote
`falklands-places`.
