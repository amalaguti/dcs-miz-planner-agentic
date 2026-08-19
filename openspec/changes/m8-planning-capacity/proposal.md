## Why

Channel/Normandy Spitfire planning already compiles six mission types, but the
catalog is thin: two WWII countries, five aircraft, Manston/Needs Oar Point
invent homes, empty artillery, no scenery, and the agent rarely chooses
solo vs a 2–4 ship section. M8 densifies WWII resources and a few
high-leverage behaviours so vague asks yield more distinct flyable sorties
without new Spec mission types. Modern maps stay parked.

## What Changes

- WWII era countries include verified PyDCS `USA` (dual-era; `usaaf` remains voice).
- First extra aircraft: `P-51D` radio 124.0, payload `p51d_2x_anm64`
  (`{AN-M64}` pylons 4 and 7). No Typhoon in PyDCS `plane_map`.
- Channel invent extras Hawkinge / Detling / BigginHill with per-home
  CAP/GA/escort recipes (not Manston 135/25 or 125/76). Parking notes;
  four-ship prefers Manston.
- Normandy extras Chailey / Tangmere / FordAF (not NeedsOarPoint 180/63 or
  180/133). Tangmere `max_flight_size` 3.
- Artillery class: `LeFH_18-40-105`, `Wespe124`, `M2A1-105`; static; soft AI.
- Spec `scenery[]` from ranked `fortification_map` keys; Channel smoke.
- Agent chooses `player.flight` size 2 lead on pair/section/Rhubarb; omits
  the block when the ask is clearly solo. Do not rebuild the compiler.
- Recon `narrative.enabled` prepends ops colour then the find beat.
- Behaviour/inspiration cards: `aircraft_failures`, `airfield_scenery`,
  `rhubarb_pair`, `dawn_recce_narrative`, `mustang_channel_strafe`.

## Non-goals

- New Spec types (SEAD, AAR, helo, carrier, FAC).
- Deepening Caucasus / Syria / Nevada / Falklands / Kola.
- Binding GermanyCW (gated: only if installed later).
- `#19` radio A–E bank, `#22` Lua library, `#24` cockpit-arg training.
- Inventing DCS ids or harvesting CLSIDs from a live install.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: USA in WWII; P-51D; statics table; artillery units.
- `mission-validation`: Channel accepts USA; unknown_static.
- `mission-spec`: optional `scenery[]`; recon narrative allowed.
- `mission-narrative`: recon pack defers to find-beat expander.
- `miz-compiler`: scenery static groups.
- `mission-options`: artillery class; extra homes; narrative_pack includes recon.
- `nl-agent`: extra homes; sortie-size assertiveness.
- `agent-catalog`: WWII countries include USA.

## Impact

Era YAML, planning_options, Spec/validate/compile, invent prompts/schema,
examples, tests. Channel goldens stay green. Acceptance: hermetic pytest +
compile M8 examples. ME Instant Action is human do-soon after merge.
