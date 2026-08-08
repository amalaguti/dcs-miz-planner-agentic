## Why

Channel Specs already support recon and sea-domain GA (`Uboat_VIIC` in `ships.yaml`),
but there is no checked-in **surfaced U-boat locate → hunt** story: mid-Channel recon
contacts, bomb-run Specs, inspiration cards, or briefs that warn bombs only work on the
surface. Pilots and the agent need that Channel “sub hunt” flavour without inventing
true ASW.

## What Changes

- Add checked-in **recon** example: mid-Channel AOI with `Uboat_VIIC` observe-only contacts
  (weapons hold, find beat) — no payload.
- Add checked-in **ground_attack** example: mid-Channel (or harbour-water) strike on
  surfaced `Uboat_VIIC` with a bomb payload (prefer slipper for Channel crossing).
- Extend planning options: `mission_inspiration` for U-boat recon/hunt; ensure
  `channel_place` / `strike_target_class` sea_craft guidance mentions U-boat + recon
  mission type where advisory.
- Agent schema/voice/prompts: surfaced-only language (“bomb on the surface / before
  crash-dive”); never claim submerged detect, depth charges, or ASW.
- Goldens / compile asserts for both examples; ME Instant Action accept for both `.miz`.
- Optional light drama via existing radio/late-act or dynamics (only if cheap; not required
  for v1 acceptance).

## Non-goals

- True ASW: submerged detection, depth charges, sonobuoys, hydrophones.
- New `asw` / `anti_sub` mission type; armed recon / find-then-kill in one Spec.
- LLM Lua; inventing ship ids beyond registry; land trucks in mid-Channel water.
- Changing core recon/GA compilers beyond what examples already need (placement already
  works via `ship_group`).

## Capabilities

### New Capabilities

- *(none — content + options + agent briefs on existing recon / ground_attack)*

### Modified Capabilities

- `golden-fixtures`: Mid-Channel U-boat recon + GA examples / structural asserts.
- `mission-options`: Inspiration (+ place/class notes) for surfaced U-boat recon/hunt.
- `nl-agent` / `squadron-voice` / `agent-tools` (light): surfaced-only U-boat guidance.
- `mission-spec` / `miz-compiler` / `mission-validation`: only if examples expose a gap
  (prefer no Spec schema change — reuse recon + GA).

## Impact

- New `examples/` Specs + goldens; `planning_options.yaml`; agent prompts/voice/schema;
  BACKLOG `#15f`.
- Acceptance: open both compiled `.miz` in DCS ME / Instant Action — surfaced U-boat
  group(s) in/near AOI or strike point; recon find beat; GA bombs present.
