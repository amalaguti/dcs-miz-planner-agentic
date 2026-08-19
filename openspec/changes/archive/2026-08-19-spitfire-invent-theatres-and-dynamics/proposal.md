## Why

Invent schema and prompts still put Su-25T in the **player** slot on Caucasus, Syria, Nevada, Falklands, and Kola, so the owner’s only cockpit (Spitfire LF Mk IX) is not what vague asks emit. Play-time variation already compiles (`dynamics.mode` live|choose|hybrid, target `motion` patrol|path) but invent rarely turns it on. This change makes invent sit the player in the Spitfire on every bound map and assert dynamics/motion when the ask implies unpredictability or moving pieces.

## What Changes

- Invent schema examples for Caucasus / Syria / Nevada / Falklands / Kola rewrite `player.aircraft` to `SpitfireLFMkIX` (keep theatre airfield, country, and station geometry). Su-25T stays on enemies/package unless a WWII/Luftwaffe/1944 cue asks for Bf-109K-4 / FW-190A8 ThirdReich.
- Ground-attack schema examples swap Su-25T payloads for `spitfire_2x250_slipper`.
- Prompts and schema notes state Spitfire as the player; Frogfoot/P-51 only when named.
- One-shot host nudge (invent + chat) joins player/opposition/dynamics/motion repairs so a shared one-shot flag cannot drop later cues.
- Eval catalog: Caucasus Spitfire hop; intercept different each load.
- Compile goldens (`batumi_cold_freeflight.yaml` and other Su-25T map-smoke YAML) stay unchanged.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: modern-theatre invent player is Spitfire; WWII colour cue; dynamics/motion host nudge.
- `agent-tools`: `get_mission_spec_schema` examples for those theatres use Spitfire in `player.aircraft`.

## Impact

`spec_schema.py`, `prompts.py`, new `invent_nudges.py`, `planner.py`, `session.py`, theatre-agnostic schema tests, eval catalog, README/BACKLOG. No new Lua, no Mist, no CLI randomize as invent authoring. Kola remains free_flight only.

## Non-goals

- Instant Action fly matrix, R4 cockpit-arg verify, `#24` cockpit-state-triggers, freeze-docs.
- MiG-15 / F-86 ids, extra player modules, Kola combat, rewriting compile goldens to Spitfire.
- Combining narrative packs with dynamics.
