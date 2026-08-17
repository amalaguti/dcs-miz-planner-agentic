## Why

Nevada Stage B curated eight airfields and Groom Lake smoke, but invent is still
free_flight only. CAP is already airfield-relative and compiles without a domain
classifier or intercept spawn. Stage C adds Nellis place recipes and CAP invent
so the NL agent can plan a desert north-range CAP from Nellis.

## What Changes

- Add `channel_place` rows `nellis_home` and `nellis_north_range_cap`
  (`meta.theatre: Nevada`; CAP station 350° / 40 km / 4000 m north of Nellis,
  Desert NWR / north range land). Family name stays `channel_place`.
- Ship `examples/nellis_north_range_cap.yaml` (Nellis, USA, Su-25T,
  2024-06-06 `sunny_clear`, Russia Su-25T red opposition). Explicit
  `enemies[].country: Russia` (model default is `ThirdReich`).
- Lift invent/chat refuse for **CAP only**. Intercept / ground_attack / escort /
  recon stay every-turn refuse. Schema `theatre=Nevada` + `cap` uses the new
  example (no Manston / Batumi / Cherbourg / Incirlik skeleton).

## Non-goals

- Domain classifier, intercept spawn, path clamp, GA/recon, extra unit YAML,
  new countries, `theatre_place` rename, Falklands combat.
- Copying Incirlik 180/40, Batumi 270/40, Cherbourg 180/63, Manston 135/25,
  Creech 303/40, or Henderson/NLV/Echo Bay headings onto Nellis.
- USA-on-red (compile-illegal while USA is blue). Country `Syria` on Nevada.
  `usaaf` as a country (voice only).
- ME Instant Action as a merge gate.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Nevada invent is free_flight **or CAP**.
- `agent-tools`: schema Nevada+CAP example.
- `mission-options`: two Nevada `channel_place` rows.
- `miz-compiler`: Nellis CAP compiles.
- `mission-validation`: Nellis CAP validates; intercept/domain still fail-closed.

## Impact

Places, invent, schema, example + tests. Domain and intercept spawn stay
fail-closed. Channel goldens stay green.
