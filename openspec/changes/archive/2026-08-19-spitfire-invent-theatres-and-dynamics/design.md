## Context

The owner flies only Spitfire LF Mk IX. Compiler already accepts that type on bound modern maps (dual-era). Invent schema still copies Su-25T from packaged map-smoke YAML into `player.aircraft`. Dynamics (`dynamics.mode` live|choose|hybrid) and target `motion` already compile; invent was taught not to use CLI randomize as authoring, so vague “surprise me” asks stay static.

Planner one-shot repairs share `immersion_repair_used`. Separate Spitfire then dynamics nudges would drop the second cue. Chat already uses per-nudge flags.

## Goals / Non-Goals

**Goals:**

- Schema/prompts for Caucasus, Syria, Nevada, Falklands, Kola emit Spitfire in the player slot; keep station geometry and map-smoke YAML for compile.
- WWII/Luftwaffe/1944 cues swap Su-25T *enemies* to Bf-109K-4 / FW-190A8 ThirdReich (not Kola combat).
- One combined host nudge for player, opposition, dynamics, and moving targets.
- Hermetic tests + two eval catalog prompts.

**Non-Goals:**

- Instant Action, R4, `#24`, extra player modules, Kola combat, new Lua, rewriting compile goldens.

## Decisions

1. **Schema rewrite, not new YAML.** `_finish_schema` rewrites `Su-25T` → `SpitfireLFMkIX` (and `su25t*` payload → `spitfire_2x250_slipper`) after extra-home apply. Compile examples stay Su-25T map-smoke. Country stays Georgia/Turkey/USA/UK/Norway.

2. **Shared prefix note** on modern-theatre schema notes so we do not copy Channel 135/25. First-line envelopes also say player Spitfire; Su-25T remains valid for red AI.

3. **Combined nudge** `host_invent_product_nudge` joins all applicable parts in one user message. Planner fires it on the shared one-shot slot after M8, before immersion. Chat uses `_invent_product_nudge_used`.

4. **Cue table (regex, prompt-only):** Frogfoot/Mustang named → do not steal player. WWII colour → 109/190. Unpredictable/dice/different-each-load → `live`; F10/I-choose → `choose`; both → `hybrid`. Skip dynamics if `narrative.enabled`. GA/recon all-static + moving-convoy/under-way/patrol → `motion` patrol or path.

5. **No CLI randomize** as invent authoring. Point at `examples/manston_dawn_intercept_dynamics_live.yaml` / hybrid.

## Risks / Trade-offs

- [Schema example no longer matches compile YAML] → tests distinguish schema player vs `.miz` goldens; notes still cite the YAML for geometry ids.
- [Spitfire + Georgia/Turkey country] → dual-era already allows it; Batumi Spitfire smoke uses UK if we ever retarget FF YAML.
- [One-shot misses a later cue] → combined message includes every applicable part.

## Migration Plan

Ship on `spitfire-invent-theatres-and-dynamics`, archive, FF-merge to local master. No data migration.

## Open Questions

None. Player country stays the theatre default (not forced UK).
