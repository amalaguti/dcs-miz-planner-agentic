## 1. WWII density

- [x] 1.1 Add `USA` to `data/era/wwii/countries.yaml` (dual-era). `usaaf` remains voice-only. Channel still rejects Georgia/Turkey/Russia/Syria/Argentina/Norway.
- [x] 1.2 Add `P-51D` radio 124.0 and payload `p51d_2x_anm64` (`{AN-M64}` pylons 4+7). Do not add Typhoon.
- [x] 1.3 Examples: `manston_p51_freeflight.yaml`, `manston_p51_ground_attack.yaml`.

## 2. Extra homes and artillery

- [x] 2.1 Channel places `hawkinge_home` / `detling_home` / `biggin_hill_home` with per-home CAP/GA/escort (not Manston 135/25 or 125/76). `max_flight_size` 4. Examples Hawkinge FF/CAP/pair.
- [x] 2.2 Normandy places `chailey_home` / `tangmere_home` / `ford_af_home` (not NeedsOarPoint 180/63 or 180/133). Tangmere `max_flight_size` 3. Example Chailey FF.
- [x] 2.3 Artillery class `LeFH_18-40-105`, `Wespe124`, `M2A1-105`; static; `convoy_transit`; example `manston_ground_attack_artillery.yaml`.

## 3. Behaviours, scenery, sortie size

- [x] 3.1 Recon `narrative.enabled` defers to `expand_recon_find_pack` (push then find beat). Example `manston_recon_narrative.yaml`.
- [x] 3.2 Spec `scenery[]` + `era/wwii/statics.yaml` + compile `Mission.static_group`. Example `manston_freeflight_scenery.yaml`. Cards `airfield_scenery`, `aircraft_failures`.
- [x] 3.3 Inspirations `rhubarb_pair`, `dawn_recce_narrative`, `mustang_channel_strafe`. Prompts/schema: pair → `player.flight` size 2 lead; solo omits the block; Tangmere max 3.
- [x] 3.4 Eval catalog scenarios `pair-as-lead`, `wingman-join-up`, `recon-ops-colour`. Live eval 2026-08-19: pair/wingman/recon fired; Hawkinge pair still cloned Manston CAP 135/25 (notes hardened).

## 4. Docs and merge gate

- [x] 4.1 BACKLOG M8 table; README Status; THEATRE_TARGET_PROMOTE artillery; lessons + dcs-dev-* skills. GermanyCW stays `idea` gated.
- [x] 4.2 Main OpenSpec specs updated (registry, validation, narrative, spec, compiler, options, nl-agent, catalog).
- [x] 4.3 `uv run ruff check` / `ruff format` and `uv run pytest -q`
- [x] 4.4 Compile M8 examples (pytest compile loop)
- [ ] 4.5 ME Instant Action on P-51 / extra-home / artillery / scenery (human do-soon after merge — not a merge blocker)
