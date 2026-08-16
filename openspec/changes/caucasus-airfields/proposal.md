## Why

Caucasus Stage A bound the map with Batumi only. The NL agent cannot name other
verified Caucasus fields, and modern identity has no Russia host for the
north-of-ridge side. Stage B deepens geography and identity without combat.

## What Changes

- Curate eight Caucasus airfields from live PyDCS `airport_list()` (keep
  `Batumi=22`; add Kobuleti, `SenakiKolkhi`, Kutaisi, `TbilisiLochini`,
  Vaziani, `SochiAdler`, Mozdok). Never invent ids; never dump all 21 fields.
- Add PyDCS country `Russia` to `era/modern` only (not WWII). Player aircraft
  stays `Su-25T` at 251.0 MHz. Invent/schema remain Batumi, Georgia blue,
  free_flight only.
- Ship `examples/mozdok_cold_freeflight.yaml` (Mozdok, Russia red, Su-25T) so
  extra-AF + Russia compile. Theatre-scoped lookup: Mozdok 28 is not
  NeedsOarPoint.
- Extend `infer_theatre` to the new Spec keys. Catalog lists the new airfields
  and Russia after sync.

## Non-goals

- Places, CAP/GA/intercept/escort/recon, domain classifier, intercept spawn,
  path clamp, strike dual-tag, paid FC3 jets, Abkhazia/SouthOssetia/Ukraine,
  all 21 airfields, `theatre_place` rename, modern payloads/failures.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: eight curated Caucasus airfields; `Russia` in modern.
- `agent-catalog`: catalog lists the new airfields and Russia after sync.
- `mission-validation`: extra Caucasus AFs and Russia (era-filtered) validate.
- `miz-compiler`: Mozdok cold FF compiles (N1-style contracts).
- `nl-agent`: infer theatre from new AF keys; invent still FF-only at Batumi.
- `agent-tools`: lookup of new keys; schema example stays Batumi.

## Impact

`data/theatres/Caucasus/airfields.yaml`, `data/era/modern/countries.yaml`,
`infer_theatre`, Mozdok example + tests. Invent stay FF-only. Channel goldens
stay green. Acceptance: hermetic pytest + compile Mozdok. ME Instant Action is
do-soon after merge.
