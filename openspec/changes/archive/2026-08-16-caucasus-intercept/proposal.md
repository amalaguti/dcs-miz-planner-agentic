## Why

Caucasus invent can fly CAP and bomb inland of Kutaisi, but intercept still
fail-closes on Hawkinge/Dover literals. The Black Sea CAP station (270° / 40 km
west of Batumi) is already a packaged sea place. This slice adds that recipe so
modern intercept colour works on Caucasus without copying Channel or Normandy spawn.

## What Changes

- Add a Caucasus intercept spawn recipe: Batumi map position plus due-west 40 km
  offset (PyDCS `point_from_heading(270, 40000)`). Store literals; do not recompute
  Channel Hawkinge from `airport_list()`.
- Ship `examples/batumi_dawn_intercept.yaml` (Batumi, Su-25T, Russia Su-25T red,
  06:00, `sunny_clear`, 2024-06-06). Explicit `enemies[].country: Russia`.
- Allow invent/chat **intercept** on Caucasus. Escort / recon still refuse every turn.
- Schema `theatre=Caucasus` + `intercept` loads the new example with dedicated notes
  (no Hawkinge concatenation).
- Extend `batumi_black_sea_cap` `mission_types` to include `intercept` (same 270/40
  sea station). Extend `batumi_home` with `intercept`. Family stays `channel_place`.

## Non-goals

- Escort, recon, path clamp, extra unit YAML, QAG scrape, `theatre_place` rename,
  Syria/Nevada/Falklands combat.
- Changing Channel Hawkinge/Dover goldens or Normandy Cherbourg literals.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Caucasus invent is free_flight, CAP, ground_attack, **or intercept**;
  escort/recon still refuse.
- `agent-tools`: schema Caucasus+intercept example.
- `mission-options`: Batumi Black Sea place also cues intercept.
- `mission-validation`: well-formed Caucasus intercept validates; Syria still fail-closed.
- `miz-compiler`: Caucasus intercept compiles; Channel Hawkinge recipe unchanged.

## Impact

`intercept_spawn.py`, invent allow-table / schema / prompts, validation hint, new
example + tests. Channel intercept goldens stay bit-identical. Acceptance: ruff +
pytest + compile the new example. ME Instant Action is do-soon after merge.
