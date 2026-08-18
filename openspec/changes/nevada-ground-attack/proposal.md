## Why

Nevada invent can CAP, intercept, and escort on desert north-range land
(350° / 40 km), but ground_attack still fail-closes. Land/sea domain is still
unsupported on Nevada, and `list_strike_targets(theatre="Nevada")` is empty.
This is the GA combat slice: Nellis inland strike past Creech, reusing verified
modern trucks and `su25t_2x_fab250`. Do not copy CAP 350/40 onto trucks.

## What Changes

- Allow invent/chat **ground_attack** on Nevada (Nellis, Su-25T, USA blue).
  Recon stays every-turn refuse.
- Add a Nevada land/sea domain recipe: desert-default **land** using only the
  eight curated AFs (near AF 3 km → land; else land). Do not run Channel,
  Normandy, Caucasus, or Syria chords on Nevada x,y. Do not promote Lake Mead /
  Echo Bay id 7. Falklands stays fail-closed.
- Ship `examples/nellis_creech_ground_attack.yaml`: strike **303° / 85 km /
  2000 m** from Nellis (~15.5 km past Creech). Soft trucks `Ural-375` (and
  companions) country **Russia** red. Payload `su25t_2x_fab250`.
- Add `channel_place` row `creech_range_strike`. Family stays `channel_place`.
  Extend `nellis_home` with `ground_attack`. Do not add GA to
  `nellis_north_range_cap`.
- Offer modern **land** strike units on `list_strike_targets(theatre="Nevada")`
  via query-time dual-offer (stored `theatre_id` stays Caucasus). Channel WWII
  trucks stay Channel; Falklands stay empty.
- Schema `theatre=Nevada` + `ground_attack` loads the new example with dedicated
  notes (no Manston french-coast concatenation). FF/CAP/intercept/escort
  example files unchanged. Stub LLM stays Manston.

## Non-goals

- Recon invent, new unit ids, QAG scrape, `theatre_place` rename, extra
  airfields, Falklands combat, promoting Echo Bay id 7.
- Copying CAP 350/40, Creech 303/70, Aleppo 121/200, or Kutaisi 43/110 onto
  Nevada GA.
- USA-on-red or country Syria on Nevada trucks.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Nevada invent includes ground_attack; recon still refuses.
- `agent-tools`: schema Nevada+GA example; `list_strike_targets(theatre=Nevada)`
  returns modern land trucks.
- `mission-options`: `creech_range_strike` place recipe.
- `agent-catalog`: modern land strike units offered on Nevada after query match.
- `mission-validation`: Nevada desert-default land domain; well-formed Nevada GA
  validates; Falklands still fail-closed.
- `miz-compiler`: Nevada GA compiles; Channel goldens unchanged.

## Impact

`channel_domain.py`, invent allow-table / schema / prompts, strike-list
dual-offer, `planning_options.yaml`, new GA example + tests. Channel intercept
goldens stay bit-identical. Acceptance: ruff + pytest + compile the new
example. ME Instant Action is do-soon after merge.
