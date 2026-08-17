## Why

Syria invent can CAP, intercept, and escort on the Gulf of Iskenderun (180° /
40 km sea), but ground_attack still fail-closes. Land/sea domain is still
unsupported on Syria, and `list_strike_targets(theatre="Syria")` is empty. This
is the GA combat slice: Incirlik inland strike past Aleppo, reusing verified
modern trucks and `su25t_2x_fab250`. Do not copy CAP 180/40 onto trucks.

## What Changes

- Allow invent/chat **ground_attack** on Syria (Incirlik, Su-25T, Turkey blue).
  Recon stays every-turn refuse.
- Add a Syria land/sea domain recipe (coastal vs inland curated ids; Incirlik
  seaward 165–195°). Do not run Channel, Normandy, or Caucasus chords on Syria
  x,y. Do not apply Caucasus 270±45 to Incirlik (Adana Şakirpaşa id 2).
- Ship `examples/incirlik_aleppo_ground_attack.yaml`: strike 121° / 200 km /
  2000 m from Incirlik (~15 km past Aleppo). Soft trucks `Ural-375` (and
  companions) country **Syria** red. Payload `su25t_2x_fab250`.
- Add `channel_place` row `aleppo_inland_strike`. Family stays `channel_place`.
  Extend `incirlik_home` with `ground_attack`. Do not add GA to
  `incirlik_iskenderun_cap`.
- Offer modern **land** strike units on `list_strike_targets(theatre="Syria")`
  via query-time dual-offer (stored `theatre_id` stays Caucasus). Channel WWII
  trucks stay Channel; Nevada/Falklands stay empty.
- Schema `theatre=Syria` + `ground_attack` loads the new example with dedicated
  notes (no Manston french-coast concatenation).

## Non-goals

- Recon invent, new unit ids, QAG scrape, `theatre_place` rename, extra
  airfields, Nevada/Falklands combat, promoting Adana Şakirpaşa id 2.
- Copying CAP 180/40, Kutaisi 43/110, or Maupertus 180/133 onto Syria GA.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Syria invent includes ground_attack; recon still refuses.
- `agent-tools`: schema Syria+GA example; `list_strike_targets(theatre=Syria)`
  returns modern land trucks.
- `mission-options`: `aleppo_inland_strike` place recipe.
- `agent-catalog`: modern land strike units offered on Syria after query match.
- `mission-validation`: Syria land/sea domain; well-formed Syria GA validates.
- `miz-compiler`: Syria GA compiles; Channel goldens unchanged.

## Impact

`channel_domain.py`, invent allow-table / schema / prompts, strike-list dual-offer,
`planning_options.yaml`, new GA example + tests. Channel intercept goldens stay
bit-identical. Acceptance: ruff + pytest + compile the new example. ME Instant
Action is do-soon after merge.
