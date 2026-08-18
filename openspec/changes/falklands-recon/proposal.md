## Why

Falklands invent can fly five of six mission types, but recon still refuse-closes
every turn. Recon AOI is already airfield-relative. The East Falkland inland
station (269° / 21 km) is packaged as `east_falkland_inland_strike` — the
analogue of Channel recon 125° / 76 km, Caucasus recon 43° / 110 km, Syria
recon 121° / 200 km, and Nevada recon 303° / 85 km. Do not copy french-coast
geometry or CAP 150/40 onto an East Falkland land observe.

## What Changes

- Ship `examples/mount_pleasant_east_falkland_recon.yaml` (MountPleasant,
  Su-25T UK blue, observe Ural-375 trucks country Argentina red at 269° /
  21 km / 2000 m, radius_m 3000, mark true, weapons hold, no payload).
- Allow invent/chat **recon** on Falklands (all six types).
- Schema `theatre=Falklands` + `recon` loads the new example with dedicated
  notes (no french_coast / Manston 125/76 concatenation). Stub LLM stays
  Manston.
- Extend `east_falkland_inland_strike` `mission_types` with `recon`. Extend
  `mount_pleasant_home` with `recon`. Family stays `channel_place`. Do not
  add recon to `mount_pleasant_south_atlantic_cap`.

## Non-goals

- Domain rewrite, intercept_spawn, path clamp, extra unit YAML, QAG scrape,
  `theatre_place` rename, dual-offer retag, Chile, promoting Goose Green 24
  or Gull Point 29 as Spec keys.
- Changing Channel/Caucasus/Syria/Nevada recon goldens or Falklands CAP 150/40.
- Adding recon to `mount_pleasant_south_atlantic_cap`.
- ME Instant Action as a merge gate (human do-soon after merge).
- Binding unbound maps (`Kola`, `Iraq`, `MarianaIslandsWWII`).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Falklands invent includes recon (all six types).
- `agent-tools`: schema Falklands+recon example.
- `mission-options`: East Falkland inland place also cues recon.
- `mission-validation`: well-formed Falklands recon validates.
- `miz-compiler`: Falklands recon compiles; Channel recon goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests.
Compiler already places recon via airfield-relative geometry. Domain already
classifies 269/21 land. Acceptance: ruff + pytest + compile the new example.
ME Instant Action is do-soon after merge.
