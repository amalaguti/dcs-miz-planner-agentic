## Why

Caucasus invent can fly CAP over the Black Sea but cannot place modern ground
targets. Stage C shipped Batumi places and CAP; land/sea domain still fail-closes
on Caucasus, and `list_strike_targets(theatre="Caucasus")` is empty. This is the
GA combat slice: Batumi inland strike past Kutaisi, using verified modern trucks
and a Su-25T FAB-250 preset.

## What Changes

- Allow invent/chat **ground_attack** on Caucasus (Batumi, Su-25T, `sunny_clear`,
  Georgia blue). Intercept / escort / recon stay every-turn refuse.
- Add a Caucasus land/sea domain recipe (west-of-coast seaward sector). Do not
  run the Channel UK–FR or Normandy UK–Cotentin chords on Caucasus x,y. Do not
  copy CAP 270°/40 km onto land GA.
- Ship `examples/batumi_kutaisi_ground_attack.yaml`: strike 43° / 110 km / 2000 m
  from Batumi (~12.8 km past Kutaisi). Soft trucks `Ural-375` (and companions)
  country **Russia** red. Payload `su25t_2x_fab250` (inner pylons 5 and 7).
- Add `channel_place` row `kutaisi_inland_strike` (`meta.theatre: Caucasus`).
  Family name stays `channel_place`. Extend `batumi_home` with `ground_attack`.
- Package `era/modern/ground_units.yaml` and `era/modern/payloads.yaml`; registry
  unions them with WWII shelves (collision guards). Do **not** append Ural ids
  onto Channel `soft_vehicles` `unit_ids`.
- Offer modern **land** strike units on `list_strike_targets(theatre="Caucasus")`.
  Channel WWII trucks stay Channel; Normandy dual-offer stays WWII land.
- Schema `theatre=Caucasus` + `ground_attack` loads the new example with dedicated
  notes (no Channel french-coast concatenation).

## Non-goals

- Caucasus intercept spawn, escort, recon, path clamp, extra airfields, Shilka /
  AAA shelf, QAG scrape, `theatre_place` rename, Syria/Nevada/Falklands combat.
- Copying Blitz / flak18 / ThirdReich onto Caucasus, or Ural-375 onto Channel.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Caucasus invent is free_flight, CAP, **or ground_attack**;
  intercept/escort/recon still refuse; do not copy Channel/Normandy geometry onto
  Caucasus.
- `agent-tools`: schema Caucasus+GA example; `list_strike_targets(theatre=Caucasus)`
  returns modern land trucks.
- `mission-options`: `kutaisi_inland_strike` place recipe; modern soft class.
- `agent-catalog`: modern land strike units tagged Caucasus after sync.
- `mission-validation`: Caucasus land/sea domain; well-formed Caucasus GA validates.
- `miz-compiler`: Caucasus GA compiles (N1-style contracts).
- `reference-registry`: modern ground units + Su-25T FAB-250 payload union.

## Impact

`channel_domain.py`, invent allow-table / schema / prompts, catalog strike tagging,
`planning_options.yaml`, `era/modern` YAML, new GA example + tests. Channel Hawkinge
intercept goldens and Manston/Normandy GA stay bit-identical. Acceptance: ruff +
pytest + compile the new example. ME Instant Action at Batumi is do-soon after merge.
