## Why

Falklands Stage B curated eight airfields and Rio Gallegos smoke, but invent is still
free_flight only. CAP is already airfield-relative and compiles without a domain
classifier or intercept spawn. Stage C adds Mount Pleasant place recipes and CAP invent
so the NL agent can plan a South Atlantic CAP from Mount Pleasant.

## What Changes

- Add `channel_place` rows `mount_pleasant_home` and
  `mount_pleasant_south_atlantic_cap` (`meta.theatre: Falklands`; CAP station
  150° / 40 km / 4000 m SSE of Mount Pleasant, South Atlantic sea). Family
  name stays `channel_place`.
- Ship `examples/mount_pleasant_south_atlantic_cap.yaml` (MountPleasant, UK,
  Su-25T, 2024-06-06 `sunny_clear`, Argentina Su-25T red opposition). Explicit
  `enemies[].country: Argentina` (model default is `ThirdReich`).
- Lift invent/chat refuse for **CAP only**. Intercept / ground_attack / escort /
  recon stay every-turn refuse. Schema `theatre=Falklands` + `cap` uses the new
  example (no Manston / Batumi / Cherbourg / Incirlik / Nellis skeleton).

## Non-goals

- Domain classifier, intercept spawn, path clamp, GA/recon, extra unit YAML,
  new countries, `theatre_place` rename, Chile, extra-AF invent home.
- Copying Manston 135/25, Cherbourg 180/63, Incirlik 180/40, Batumi 270/40,
  Nellis 350/40, or rejected Falklands probes (090/40 nearer Stanley, 180/40
  nearer Gull Point, 270/40 nearer Goose Green, 350/40 nearer San Carlos).
- Port Stanley as CAP home. UK-on-red. `usaaf` as a country.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Falklands invent is free_flight **or CAP**.
- `agent-tools`: schema Falklands+CAP example.
- `mission-options`: two Falklands `channel_place` rows.
- `miz-compiler`: Mount Pleasant CAP compiles.
- `mission-validation`: Mount Pleasant CAP validates; intercept/domain still fail-closed.

## Impact

Places, invent, schema, example + tests. Domain and intercept spawn stay
fail-closed. Channel goldens stay green. Opening the compiled `.miz` in DCS
Mission Editor Instant Action is human do-soon, not a merge gate.
