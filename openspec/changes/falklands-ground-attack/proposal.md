## Why

Falklands invent can CAP, intercept, and escort over the South Atlantic (150° /
40 km sea), but ground_attack still fail-closes. Land/sea domain is still
unsupported on Falklands, and `list_strike_targets(theatre="Falklands")` is
empty. This is the GA combat slice: Mount Pleasant inland strike **short of**
Goose Green on East Falkland camp land, reusing verified modern trucks and
`su25t_2x_fab250`. Do not copy CAP 150/40 onto trucks.

## What Changes

- Allow invent/chat **ground_attack** on Falklands (MountPleasant, Su-25T, UK
  blue). Recon stays every-turn refuse.
- Add a Falklands land/sea domain recipe: Syria-style seaward windows on island
  AFs `{1,2,3,24,29}` (near AF 3 km → land; MPA 120–180° so CAP 150/40 is sea).
  Do not run Channel/Normandy/Caucasus/Syria chords or Nevada desert-default on
  Falklands x,y. Do not dump 27 AFs. Do not invent ids 4/28. Do not promote
  Goose Green 24 or Gull Point 29 as Spec keys.
- Ship `examples/mount_pleasant_east_falkland_ground_attack.yaml`: strike
  **269° / 21 km / 2000 m** from Mount Pleasant (15 km SHORT of Goose Green).
  Soft trucks country **Argentina** red. Payload `su25t_2x_fab250`.
- Add `channel_place` row `east_falkland_inland_strike`. Family stays
  `channel_place`. Extend `mount_pleasant_home` with `ground_attack`. Do not
  add GA to `mount_pleasant_south_atlantic_cap`.
- Offer modern **land** strike units on `list_strike_targets(theatre="Falklands")`
  via query-time dual-offer (stored `theatre_id` stays Caucasus). Channel WWII
  trucks stay Channel.
- Schema `theatre=Falklands` + `ground_attack` loads the new example with
  dedicated notes (no Manston french-coast concatenation).

## Non-goals

- Recon invent, new unit ids, QAG scrape, extra airfields, Chile, promoting
  Goose Green/Gull Point, `intercept_spawn.py` edits.
- Copying CAP 150/40, 269/36, 269/51, Nevada 303/85, Aleppo 121/200, or
  Kutaisi 43/110 onto Falklands GA.
- UK-on-red or country Russia/Syria/ThirdReich on Falklands trucks.
- ME Instant Action as a merge gate.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Falklands invent includes ground_attack; recon still refuses.
- `agent-tools`: schema Falklands+GA example; `list_strike_targets(theatre=Falklands)`
  returns modern land trucks.
- `mission-options`: `east_falkland_inland_strike` place recipe.
- `agent-catalog`: modern land strike units offered on Falklands after query match.
- `mission-validation`: Falklands seaward-window domain; well-formed Falklands GA
  validates; unbound theatres still fail-closed.
- `miz-compiler`: Falklands GA compiles; Channel goldens unchanged.

## Impact

`channel_domain.py`, invent allow-table / schema / prompts, strike-list
dual-offer, `planning_options.yaml`, new GA example + tests. Channel intercept
goldens stay bit-identical.
