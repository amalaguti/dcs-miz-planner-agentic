## Why

Nevada Stage A bound the map with Nellis only. The NL agent cannot name other
verified Nevada fields. Stage B deepens geography without combat. Country USA
and Su-25T already ship from Stage A — no new identity rows.

## What Changes

- Curate eight Nevada airfields from live PyDCS `airport_list()` (keep
  `Nellis=4`; add `GroomLake`, `Creech`, `TonopahTestRange`, `NorthLasVegas`,
  `HendersonExecutive`, `BoulderCity`, `Mesquite`). Never invent ids; never
  dump all 17 fields. Spec keys camelCase without underscores (`GroomLake` ≠
  `Groom_Lake`).
- Ship `examples/groom_lake_cold_freeflight.yaml` (GroomLake, USA blue,
  Su-25T) so extra-AF compile is proven. Theatre-scoped lookup: GroomLake 2
  is not MountPleasant and not MervilleCalonne. Invent/schema remain Nellis,
  USA blue, free_flight only.
- Extend `infer_theatre` to the new Spec keys. Catalog lists the new
  airfields after sync.

## Non-goals

- Places, CAP/GA/intercept/escort/recon, domain classifier, intercept spawn,
  path clamp, dump of 17 fields, new countries/aircraft/payloads, `usaaf` as
  a country, `theatre_place` rename, Falklands Stage B.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: eight curated Nevada airfields.
- `agent-catalog`: catalog lists the new airfields after sync.
- `mission-validation`: extra Nevada AFs validate.
- `miz-compiler`: Groom Lake cold FF compiles (N1-style contracts).
- `nl-agent`: infer theatre from new AF keys; invent still FF-only at Nellis.
- `agent-tools`: lookup of new keys; schema example stays Nellis.

## Impact

`data/theatres/Nevada/airfields.yaml`, `infer_theatre`, Groom Lake example +
tests. Invent stay FF-only. Channel goldens stay green. Acceptance: hermetic
pytest + compile Groom Lake. ME Instant Action is do-soon after merge.
