## Context

M8 densified Channel/Normandy WWII catalog (USA/P-51D, extra homes, artillery,
scenery, sortie-size prompts). Invent still calls
`get_mission_spec_schema(mission_type, theatre)` and Channel always loads
Manston examples. Live eval cloned Manston CAP 135/25 onto a Hawkinge pair.

Place-card meta on `channel_place` `*_home` rows is the geometry SoT. Packaged
extra-home examples exist only for Hawkinge FF/CAP/pair and Chailey FF.

## Goals / Non-Goals

**Goals:** schema keyed by optional airfield; host clamp of cloned default-home
stations on extra homes; one-shot nudges for M8 knobs when the ask implies
them; eval catalog coverage.

**Non-Goals:** new YAML units/aircraft/types; modern-map depth; changing
Manston as Channel default; CLI validate clamp; stacking every M8 knob on a
bare pair ask.

## Decisions

1. **Optional `airfield` on schema, not a new tool.** Same derived-example
   projection. Omitted or Manston → today’s Manston immersion-first files.
   Hawkinge + matching type → packaged Hawkinge YAML. Other extras → theatre
   default example with `player.airfield` and station fields rewritten from
   place-card `cap_*` / `strike_*` / `escort_*`. No six-file matrix per field.

2. **Infer airfield like theatre.** `infer_airfield` from rejected JSON
   `player.airfield` (and known extra-home names). Repair nudge passes it so
   a Hawkinge parse failure is not repaired with Manston JSON.

3. **Host geometry clamp, invent/chat only.** If extra-home Spec CAP / escort
   dest / strike / recon AOI matches default-home numbers (Channel 135/25,
   125/76, 120/55; Normandy 180/63, 180/133), rewrite from the home card.
   Skip when the ask names a place (French coast, harbour, mid-Channel).
   Intercept has no Spec station; clamp does not invent intercept spawn.
   Land-path clamp unchanged. CLI validate does not clamp.

4. **One-shot M8 knob nudges.** Same session flag pattern as immersion floor.
   Cue → P-51 / artillery / scenery / failures / orders / discipline. Do not
   fire on a bare Hawkinge pair. Soft immersion floor stays Channel-only.

5. **Place cards remain SoT.** Schema rewrite and clamp read registry
   planning-option meta; do not duplicate bearings in a second table.

## Risks / Trade-offs

- [Hawkinge CAP still 135/25 after notes-only] → schema example + clamp.
- [Clamp overwrites a deliberate French-coast strike from Hawkinge] → skip
  when prompt has named-place cues; only rewrite default-home clones.
- [Stacking scenery+failures+orders on every hop] → cue-gated one-shot;
  pair-as-lead stays size 2 + geometry.
- [Detling/Tangmere lack example YAML] → rewrite from place-card meta.

## Migration Plan

Hermetic tests first. Live eval after implement. Rollback is revert of the
branch; no inventory schema bump.
