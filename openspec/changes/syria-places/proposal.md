## Why

Syria Stage B curated eight airfields and Palmyra smoke, but invent is still
free_flight only. CAP is already airfield-relative and compiles without a domain
classifier or intercept spawn. Stage C adds Incirlik place recipes and CAP invent
so the NL agent can plan a Gulf of Iskenderun CAP from Incirlik.

## What Changes

- Add `channel_place` rows `incirlik_home` and `incirlik_iskenderun_cap`
  (`meta.theatre: Syria`; CAP station 180° / 40 km / 4000 m south of Incirlik).
  Family name stays `channel_place`.
- Ship `examples/incirlik_iskenderun_cap.yaml` (Incirlik, Turkey, Su-25T,
  2024-06-06 `sunny_clear`, Syria Su-25T red opposition). Explicit
  `enemies[].country: Syria` (model default is `ThirdReich`).
- Lift invent/chat refuse for **CAP only**. Intercept / ground_attack / escort /
  recon stay every-turn refuse. Schema `theatre=Syria` + `cap` uses the new
  example (no Manston / Batumi / Cherbourg skeleton).

## Non-goals

- Domain classifier, intercept spawn, path clamp, GA/recon, extra unit YAML,
  Israel/Jordan countries, `theatre_place` rename, Nevada/Falklands combat.
- Copying Batumi 270/40 or Cherbourg 180/63 onto Incirlik.
- ME Instant Action as a merge gate.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Syria invent is free_flight **or CAP**.
- `agent-tools`: schema Syria+CAP example.
- `mission-options`: two Syria `channel_place` rows.
- `miz-compiler`: Incirlik CAP compiles.
- `mission-validation`: Incirlik CAP validates; intercept/domain still fail-closed.

## Impact

Places, invent, schema, example + tests. Domain and intercept spawn stay
fail-closed. Channel goldens stay green.
