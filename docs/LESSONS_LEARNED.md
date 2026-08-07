# Lessons Learned

Living agent notes. **Read before** PyDCS / compiler / DCS integration work.
**Append** when a non-obvious bug or wrong assumption is fixed so we do not repeat it.

Format per entry: short title, date, symptom → cause → fix/workaround, optional “code touchpoint”.

---

## Player flight: SP Player must be group unit #1 (2026-08-07)

- **Date:** 2026-08-07
- **Symptom:** Wingman Spec put `Skill=Player` on `units[1]` of a 2-ship group;
  in Instant Action the human only got F7 cameras / hangar roof view, no cockpit
  control; both aircraft taxied under AI.
- **Cause:** DCS single-player only hands the controllable aircraft to
  `Skill=Player` on the **first unit of a group**. Player on unit 2+ is ignored
  for control (spectator).
- **Fix:** `role: lead` → one multi-unit group, Player on `units[0]`.
  `role: wingman` → **separate** AI lead group (`"{name} Lead"`, size−1) plus a
  size-1 Player group. No same-group Player-on-slot-2. Formation Follow / join-up
  deferred. Prefer Manston for size-4 parking.
- **Code / notes:** `player_flight_is_wingman`, `player_ai_lead_group_size`,
  `compiler/pydcs_compiler.py`; examples lead/wingman; backlog `#15b`.

## In-flight weather: fog yes, clouds/rain no (2026-08-06)

- **Date:** 2026-08-06
- **Lesson:** DCS mission scripting `world.weather` (2.9.10+) can animate **fog**
  thickness/visibility mid-sortie (`setFogAnimation`). It cannot change cloud
  presets, precip, or wind while the mission is running — those are fixed in the
  `.miz` weather table. Invent-time randomness among campaign-seeded patterns is
  fine (`#17a` + `#17e` invent jitter); sunny→rainy *during* flight is not
  productizable without ED APIs. Foggy↔clear belongs in `#17c` + curated
  snippets, never LLM Lua. `#17c` ships a fog-only slice: Spec `fog_dynamics` →
  PyDCS `DoScriptFile` + `l10n/DEFAULT/fog_dynamics.lua` with human template
  `world.weather.setFogAnimation({{duration}, vis, thick})` on ONCE `TimeAfter`.
  **Do not** use `DoScript(mission.string(lua))` for this: ME shows
  `DictKey_Translation_N`, and if the dict value is empty/missing DCS executes
  the key name → ` '=' expected near '<eof>'` (pydcs#179). Prefer
  `DoScriptFile` / map resources for curated snippets.
  Starting weather matters: `dawn_clear` is only ~8 km / 80 m haze — burn-off
  looks invisible. Use `sea_fog` (~1 km / 400 m) for ME demos; watch from the
  ramp or stay low (above the layer the change is easy to miss).
- **Code / notes:** `fog_dynamics.py`, `compiler/fog_emit.py`; ED FAQ weather
  singleton; backlog `#17c` / `#22`.

## Weather invent seed vs golden stability (2026-08-06)

- **Date:** 2026-08-06
- **Lesson:** Always-on invent jitter (`weather_invent.resolve_weather_snapshot`)
  must not break structural goldens on the legacy density trio. Skip cloud-base
  jitter (and inventing temperature) when there is no gallery preset; use a
  **stable derived seed** from weather+date+time when `weather_opts` is omitted
  at compile; use `draw=True` only when writing Spec YAML so sidecars get a
  persisted random seed. Pin explicit seeds in invent hermetic tests.
- **Code:** `weather_invent.py`, `write_spec_yaml`, `_apply_weather`.

## PyDCS cloud presets vs legacy density weather (2026-08-06)

- **Date:** 2026-08-06
- **Lesson:** Modern ME static weather uses a **cloud preset gallery**
  (`clouds.preset` = `PresetN` / `RainyPresetN`). PyDCS exposes this as
  `Weather.clouds_preset = CloudPreset.by_name(...)` via `dcs.cloud_presets`
  (30 presets in 0.15.x; each has min/max `clouds_base` metres — validate or
  clamp). `#17a` recipes set `cloud_preset` + numerics for expanded Spec ids;
  the original trio (`sunny_clear` / `dawn_clear` / `marginal_vfr`) keeps the
  legacy density/thickness path (`clouds_preset = None`). Clamp base into
  gallery min/max. Campaign rainy gallery often leaves `iprecptns=0` — rain look
  from the preset, not the precip enum. **Best reference corpus:** installed
  Spitfire campaign `.miz` weather tables (Beware / Fight or Die / Epsom / Big
  Show) — not empty ME weather-template folders. Mission `weather.name` is often
  a stale `"Winter, clean sky"` string; trust `clouds.preset` + numerics.
- **Code:** `compiler/pydcs_compiler._apply_weather`, `weather_presets.yaml`,
  `dcs.cloud_presets`, research notes in gitignored `research/weather.md`.

## Spec dynamics expand XOR with narrative (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** `dynamics` and `narrative.enabled` both require empty zones/triggers
  and clear themselves after expand. Validate/compile runs narrative first — if XOR
  is only checked inside `apply_dynamics`, narrative expands first and the failure
  becomes `dynamics_conflict` (non-empty triggers) instead of the XOR code. Check
  XOR at the start of **both** expanders (and fail closed on missing
  `late_activation` for pooled enemies/targets).
- **Code:** `dynamics.py`, `narrative.py`, `validation.py`.

## GitHub CLI + hermetic CI (no Windows/DCS on runners) (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Product CI does **not** need a Windows runner or DCS installed.
  Hermetic pytest (fake Channel inventory + golden normalizers) runs on
  `ubuntu-latest`. Install `gh` via winget (`GitHub.cli`); auth with
  `gh auth login` (HTTPS device flow) as the GitHub user that owns the remote.
  On PowerShell, do **not** use bash heredoc for `git commit` — use multiple
  `-m` flags. Prefer `gh pr create` / `gh pr merge` / `gh run watch` for remote
  CI; first green suite needed: (1) `tests/conftest.py` patches
  `validation.get_inventory`, (2) strip `livery_id` from both sides of golden
  compare, (3) always call `_registry_dcs_paths()` so Linux can monkeypatch it.
  Keep PR/push CI for the hermetic suite; in-game / live LLM stay local.
- **Code:** `.github/workflows/ci.yml`, `tests/conftest.py`,
  `fixtures_support.normalize_mission`.

## CI needs hermetic inventory; strip install-local liveries (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** GitHub runners have no DCS install cache. Any test that calls
  `validate_mission_spec` / `PyDCSCompiler` / CLI `validate` without an explicit
  `inventory=` hits `get_inventory()` → `install_inventory_unavailable`. Autouse
  `tests/conftest.py` patches `validation.get_inventory` to
  `channel_available_inventory()`; tests that need empty/disabled inventory still
  pass `inventory=` explicitly. Golden mission dumps also embed
  `livery_id` from PyDCS’s local livery scan — normalize those lines away (like
  `onboard_num`) or CI diverges even when compile is correct. Registry discovery
  must still call `_registry_dcs_paths()` on all platforms so unit tests can
  monkeypatch it (real impl returns `[]` off Windows).
- **Code:** `tests/conftest.py`, `tests/fixtures_support.normalize_mission`,
  `install/discover.py`.

## R2 ED Spitfire campaigns: immersion without triggers (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** All 60 `.miz` in installed Spitfire campaigns (Beware, Fight or Die, Epsom,
  Big Show) audit as trigger-class **`none`**: no Mist, no `a_do_script`, empty/no ME
  trigger actions. Many groups still set `lateActivation` without radio/activate graphs.
  Campaigns teach **briefing / Doc / kneeboard / AI package** design, not Spec trigger
  recipes. Keep learning triggers from Channel IA + User Files singles; keep Spec
  late-act ↔ `activate_group` validation for *authored* missions.
- **Source:** `research/spitfire-campaigns.md`; harness `research/audit_campaigns_r2.py`.

## R1 Channel User Files: native dynamic > Mist (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Audited community Channel Spitfire singles (`research/spitfire-user-missions.md`).
  A full F10 + late-activate “dynamic BoB” works with **native triggers only**
  (`BATTLE_OF_BRITAIN_MASTERV2.miz`). Another variant embeds Mist for zone unit
  queries / scheduled RTB, but still uses **native `a_set_flag_random`** for raid
  dice and large `a_activate_group` pools. Do **not** treat “dynamic” as a reason to
  pin Mist; prefer Spec `radio`/`late_activation` (have) and Spec `set_flag_random`
  (`#22a`, PyDCS `SetFlagRandom`) before `#22` Lua. Ignore ME-exported Avionics/Config
  `.lua` zip members (Dunkirk) — they are not mission scripts.
- **Source:** R1 Priority Channel downloads under `research/samples/user-singles/`.
- **Code:** `models.SetFlagRandomAction`, `compiler/triggers_emit.py`; example
  `examples/manston_freeflight_flag_random.yaml`.

## Weather SoT parity (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Weather ids must stay equal across `WeatherPreset` enum,
  `weather_presets.yaml`, planning_options `weather` family, and
  `PyDCSCompiler._apply_weather` branches. Use `weather_sot.collect_weather_sot()` /
  `test_weather_sot_parity` when adding a preset — do not update only one surface.
- **Code:** `weather_sot.py`, `tests/test_weather_presets.py`.

## Campaign Doc PDF excerpts are cached (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Opt-in `include_doc_text` on `list_installed_campaigns` extracts short
  Doc PDF text via `pypdf`, capped (size/pages/chars). Cache in inventory SQLite
  (`campaign_doc_cache`) by absolute path + mtime_ns + size so unchanged campaign Docs
  are not re-parsed. Default remains filenames-only for fast listing.
- **Code:** `install/doc_extract.py`, `tools/surface.py`.

## Spec theatre → PyDCS terrain binding (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Never `Mission(terrain=TheChannel())` while ignoring `spec.theatre`. Use
  `theatre_terrain.terrain_for_theatre(spec.theatre)`; unbound ids fail compile and
  validate (`theatre_terrain_unbound`). Registry theatres must stay ⊆ binding keys
  before adding a second theatre.
- **Code:** `theatre_terrain.py`, `pydcs_compiler.py`, `channel_domain.py`.

## Soft immersion floor for vague invent (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** After `#30c`, live eval still under-emitted on “interesting” FF / marked
  GA / Big Show. Host `host_immersion_repair_nudge` once when prompt cues immersion
  but Spec is bare; `get_mission_spec_schema` prefers immersion examples (gates,
  markers, radio, narrative); invent tools omit `randomize_mission` (CLI randomize
  remains). Soft floor — bare Spec may still accept after one nudge.
- **Code:** `agent/immersion.py`, `planner.py`, `session.py`, `spec_schema.py`,
  `tool_bridge.py`.

## Soft-warn: known aircraft module missing from install (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Theatre inventory does not prove Spitfire/Mosquito/109 packs are
  installed. Spec type ids ≠ updater ids (`SPITFIRE-MKIX`); check folders under
  `Mods/aircraft/` and `CoreMods/WWII Units/` (FW-190 Spec `A8`/`D9` → folders
  `FW-190A-8` / `FW-190D-9`). Soft-warn only (`aircraft_module_missing`); never
  auto-promote into YAML.
- **Code:** `install/aircraft_modules.py`, `ValidationResult.warnings`.

## Aircraft module discovery cache (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Harvest folders on `theatres --refresh` into `aircraft_modules` SQLite
  (schema v2) alongside theatres — installs rarely change. Scan
  `Mods/aircraft` + `CoreMods/aircraft` (require `entry.lua`) and
  `CoreMods/WWII Units` (skip shared dirs like `Weapons`/`l10n`). Catalog
  `list --type aircraft` joins known vs discovered-only; never promote into YAML.
  Catalog list does **not** auto-rescan — refresh theatres first.
- **Code:** `harvest_aircraft_modules`, `InventoryStore`, `join_aircraft_views`.

- **Date:** 2026-08-05
- **Lesson:** First `eval-agent-creativity` live run showed catalog tools are *consulted*
  but immersion often not *emitted*: vague free_flight stayed bare; “keeps me honest”
  skipped altitude/speed gates; “choose difficulty” set `late_activation` + narrative
  without F10/`activate_group` (dormant bandits); “Big Show” never called
  `list_installed_campaigns`. Track as BACKLOG `#30c` — prefer prompt/tool/validation
  hardenings over new Spec predicates. Half-recipes (late-act without activate) are
  worse than narrative-only. **Validation (`#32`):** late_activation without
  `activate_group` (and activate without late_act) now **errors** at validate — empty
  sky Specs are no longer green.
- **Code / process:** `.cursor/skills/eval-agent-creativity/`; `validation.py`
  (`late_activation_no_activate` / `activate_not_late`); `#30c` fixes sticky
  `SPEC_SHAPE_REMINDER` empty-triggers conflict, complete-recipe `infer_creative`, and
  stronger prompt/schema immersion pointers.

## Creative decision memory (`detail.creative`)

- **Date:** 2026-08-04
- **Lesson:** Persist creative picks under `generation_history.detail_json` as
  `{"creative": {"behaviours": [...], "inspirations": [...], "sources": [...]}}`.
  Hosts merge light Spec infer when `creative` is absent (`infer_creative_from_spec`).
  Bias via `creative_bias_from_history` + optional prefs
  (`preferred_behaviours` / `avoid_behaviours` / `creativity_level`); inject
  `format_creative_bias_fragment` into the system prompt. Feedback tags
  `liked:…` / `avoid:…` strengthen taste. Do not auto-rewrite packaged cards.
- **Code:** `memory/creative.py`, `agent/planner.py`, `agent/session.py`, `prompts.py`.

## Local campaign inspiration (`.cmp` vs `Doc/`)

- **Date:** 2026-08-04 (honesty update 2026-08-05)
- **Lesson:** `Mods/campaigns/*.cmp` is the campaign **playlist** (stages → `.miz`
  filenames, optional description) — not mission narrative. Real per-sortie colour
  often lives in each pack’s `Doc/*.pdf`, but the agent tool only indexes **PDF
  filenames** (no body extract until backlog `#40`). Prefer Doc filenames/titles over
  raw `.cmp` stage lists when inventing; map onto packaged behaviours; never import
  `.miz` as Spec. Hermetic tests use a fake campaigns tree (`campaigns_dir=`), not
  `S:\DCS World`.
- **Code:** `install/campaigns.py`, `tools/surface.py` (`list_installed_campaigns`).

## Player altitude / speed gates

- **Date:** 2026-08-04 (re-warn polish 2026-08-05)
- **Lesson:** Spec `unit_altitude_higher|lower` (`altitude_m`, `agl` default true →
  PyDCS `UnitAltitude*AGL` or MSL) and `unit_speed_higher|lower` (`speed_kmh` → m/s
  at emit). Always bind to the player unit id from `pydcs_compiler` (no Spec unit
  ids). Prefer flag cooldown + `time_since_flag` re-warn while still violating
  (not bare continuous message spam every ME tick); clear flag when back in limits;
  keep `time_more` so parking does not spam. Emit uses `int(altitude_m)` /
  speed conversion — non-integers soft-warn (`gate_threshold_truncated`). Example:
  `manston_freeflight_altitude_speed_gates.yaml`.
- **Code:** `models.py`, `validation.py`, `compiler/triggers_emit.py`,
  `pydcs_compiler.py`.

## Mark + smoke zone markers

- **Date:** 2026-08-04
- **Lesson:** Spec `mark` (zone name + text → PyDCS `MarkToAll` / `a_mark_to_all`;
  compiler assigns sequential mark ids) and `smoke` (zone + curated color →
  `ExplodeWPMarker` / `a_explosion_marker`, ME Smoke Marker). Colors:
  green/red/white/orange/blue → ME 0–4. Example:
  `manston_ground_attack_markers.yaml`.
- **Code:** `models.py`, `validation.py`, `compiler/triggers_emit.py`.

## Group life less (partial damage)

- **Date:** 2026-08-04
- **Lesson:** Spec `group_life_less` uses exactly one of `enemy_index` /
  `target_index` plus `percent` 1–100 (remaining group life). Emit via PyDCS
  `GroupLifeLess` → `c_group_life_less`. Additive beside `unit_dead` /
  `target_dead` (full GroupDead). Example:
  `manston_ground_attack_life_less.yaml`.
- **Code:** `models.py`, `validation.py`, `compiler/triggers_emit.py`.

## F10 radio items + late activation emit

- **Date:** 2026-08-04
- **Lesson:** Spec `radio_item_add` / `radio_item_remove` + `activate_group` /
  `deactivate_group` map via PyDCS to F10 radio and group activate. Enemy/target
  `late_activation: true` must be set on the placed group or Activate does nothing useful.
  ME: Set Rules for Triggers for radio/activate actions; group panel **Late Activation**
  checkbox; F10 Other menu is in-flight only. Example: `manston_dawn_intercept_radio.yaml`.
- **Code:** `models.py`, `compiler/triggers_emit.py`, `pydcs_compiler.py`.

## Sound assets + numeric flags

- **Date:** 2026-08-04
- **Lesson:** Spec `sound` uses curated `asset_id` only (`data/sounds/` registry); compile
  materializes the file and embeds via `mission.map_resource` + `SoundToAll` (`a_out_sound`).
  Numeric flags are additive beside bool `flag_is`/`set_flag`: `flag_equals` /
  `flag_more`/`flag_less`/`time_since_flag`, `inc_flag`/`set_flag_value`. PyDCS predicates:
  `c_flag_more`, `c_flag_less`, `c_time_since_flag`, `a_inc_flag`, `a_set_flag_value`.
  Example: `manston_freeflight_sound_flags.yaml`.
- **Code:** `sounds.py`, `models.py`, `compiler/triggers_emit.py`.

## R9 ME enrichment candidates (radio / late-act first)

- **Date:** 2026-08-04
- **Lesson:** After narrative packs, the biggest Channel richness gap vs stock IA is
  **layer 3 interactivity**: F10 radio menus + late-activated groups (Dawn Raid pattern),
  not more message-only narrative. PyDCS already exposes `AddRadioItem*`,
  `ActivateGroup`/`DeactivateGroup`, sounds, `GroupLifeLess`, altitude/speed gates — Spec
  vocab is the bottleneck. Prefer native emit over `#22` unless world-event Lua is required.
  Ranked list: `research/me-enrichment-candidates.md` (gitignored).
- **Next product slice:** TBD after `#29` `altitude-speed-gates` (prefer native ME
  over `#22` unless world-event Lua is required).

## R7 PyDCS open-issue triage (2026-08-04)

- **Date:** 2026-08-04
- **Lesson:** Open [pydcs/dcs](https://github.com/pydcs/dcs/issues) triage vs Channel compiler:
  nothing blocks current combat emit beyond workarounds we already keep
  (`_disable_payload_scan`, `_ensure_theatre_member`, explicit waypoint speeds,
  plain `group.frequency`). Payload KeyError fix is on upstream **master**
  (#439/#440, Jun 2026) but **not** in PyPI `0.15.0` — do not remove the disable
  until a released wheel includes `.get(payload_path)`. Trigger vocab gaps (#62)
  and DoScript DictKey quirks (#179) matter for R9 / `#22`. Load→save action
  reordering (#369) matters only if we rewrite foreign `.miz` files.
- **Notes:** `research/pydcs-issues.md` (gitignored). Revisit on R8 bumps.

## Opt-in CAP narrative expands before validate/compile

- **Date:** 2026-08-03
- **Lesson:** `narrative.enabled: true` (CAP / intercept / escort / ground_attack)
  materialises curated zones/triggers via `apply_narrative`, then clears the flag so a
  second expand is a no-op. Conflicts with non-empty hand-written zones/triggers; requires
  enemies (CAP also needs `cap`; escort needs `escort` + package; GA needs `strike` +
  targets and uses `target_dead`, not air `unit_dead`). Message copy follows briefing
  voices (`raf`/`usaaf`/`neutral`). ME: view rules under **Set Rules for Triggers**,
  not group Triggered Actions.
- **Code:** `narrative.py`, `validation.py`, `examples/manston_*_narrative.yaml`.

## Trigger Spec compiles to native ME tables


- **Date:** 2026-08-02
- **Lesson:** Validated Spec `zones`/`triggers` map via PyDCS:
  `TimeAfter`, `FlagIsTrue`/`False`, `GroupDead`, `PartOfCoalitionInZone`,
  `MessageToAll` (`mission.string`), `SetFlag`/`ClearFlag`, `EndMission` (winner =
  player coalition for win, opposing for lose). Zones use
  `airport.position.point_from_heading` + `triggers.add_triggerzone`. Append
  `TriggerOnce`/`TriggerContinious` to `mission.triggerrules.triggers`. Spec string
  flags map to ints in first-seen order starting at 1. Keep enemy group ids in Spec
  `enemies[]` order for `unit_dead`.
- **Code:** `compiler/triggers_emit.py`, `pydcs_compiler.py` (`_apply_zones_and_triggers`).

## Trigger Spec is typed; .miz emit is a separate change

- **Date:** 2026-08-02
- **Lesson:** `zones` / `triggers` on Mission Spec are discriminated Pydantic models (no
  Lua). Shared validation checks refs; the compiler emits native ME tables
  (`trigger-compiler-native`). Do not invent Lua in the Spec. v1 conditions:
  time_more, flag_is, unit_dead, coalition_in_zone; actions: message, set_flag,
  mission_end. Zones are airfield-relative.
- **Code:** `models.py`, `validation.py`, `compiler/triggers_emit.py`,
  `examples/manston_freeflight_trigger_sample.yaml`.

## Mission randomization: seed is build-scoped, not forever-stable

- **Date:** 2026-08-02
- **Lesson:** `randomize_mission_spec` uses `random.Random(seed)` with a fixed draw order
  (weather → time → geometry → opposition). Same seed is reproducible **only for the
  current axis set and choice pools**. Adding WeatherPreset values, opposition fighters,
  new default axes, or changing jitter math will change Specs for old seeds. Lock a
  sortie by keeping the randomized YAML / `.miz`, not the seed alone. Never put RNG in
  the compiler — goldens stay on concrete Specs.
- **Code:** `randomize.py`, `dcs-miz randomize`, tools `randomize_mission`.

## Weather presets: dawn_clear / marginal_vfr mappings

- **Date:** 2026-08-02
- **Lesson:** Beyond `sunny_clear` (80 km, no fog): `dawn_clear` uses density 1, light fog
  (`enable_fog`, thickness 80, fog_visibility 8000) and visibility 45 km — pair with
  `start_time` ~06:00. `marginal_vfr` uses density 8, base 700, thickness 1500, visibility
  6000 m, no fog. Always set `clouds_iprecptns` via `Weather.Preceptions` enum. Catalog
  schema bumped to 3 so `ensure_synced` rebuilds planning options after YAML adds.
  Commander briefs and `.miz` l10n MUST use registry weather **descriptions** (meteo
  English), never raw Spec ids like `marginal_vfr`.
- **Code:** `compiler/pydcs_compiler.py` (`_apply_weather`), `weather_presets.yaml`,
  `agent/voice.py` (`_weather_phrase`), `examples/manston_dawn_freeflight.yaml`,
  `examples/manston_marginal_vfr.yaml`.

## Briefing l10n: PyDCS setters + lazy import (no compiler↔agent cycle)

- **Date:** 2026-08-02
- **Lesson:** Populate Sortie / Description / Blue|Red Task via
  `Mission.set_sortie_text` / `set_description_*` (writes `l10n/DEFAULT/dictionary`).
  Dictionary strings use Lua line-continuation `\` for newlines, not `\n` escapes — prefer
  substring asserts over naive regex parsers. Do **not** import `agent.voice` at
  `compiler` module top-level (or via a top-level `briefing`→`agent` import): that pulls
  `agent` → `tools` → `compiler` and raises a circular `ImportError`. Lazy-import
  `build_mission_briefing_texts` inside `_apply_briefing`. Sortie = `spec.name`; Description
  = Spec description + Situation + Watch-outs; player coalition task = Tactics + Procedures
  + closing; opposing task empty in v1. Pin goldens to `voice="raf"`. Free-flight groups still
  show ME main task `CAP` (PyDCS default) — unrelated to briefing Sortie title.
- **Code:** `briefing.py`, `compiler/pydcs_compiler.py` (`_apply_briefing`),
  `tests/fixtures_support.py` (dictionary golden member).

## Escort: package first, then EscortTaskAction + ROE

- **Date:** 2026-08-02
- **Lesson:** Escort compile must place the friendly `package` group **before** attaching
  `EscortTaskAction(group_id=…)` on the player. Destination is airfield-relative
  (`bearing_deg` / `distance_km`) like CAP/strike. Package starts inflight near the
  airfield along the escort bearing (`~8 km`), task `CAS`, waypoint to destination.
  Player task `Escort` + climb / Escort / Cover waypoints; `OptROE` from
  `escort.engagement`. Optional bounce spawns near the destination neighbourhood
  (`+2500`, `-1500` m), not the intercept Hawkinge corridor. Package coalition MUST match
  the player; enemies oppose. Example: Manston → 120° / 55 km, 2× `MosquitoFBMkVI`,
  2× `Bf-109K-4`.
- **Code:** `compiler/pydcs_compiler.py` (`_apply_escort`, `_place_escort_enemies`),
  `examples/manston_escort.yaml`, `models.Escort` / `PackageFlight`.

## Ground-attack: always verify strike position (land vs water, enemy vs practice)

- **Date:** 2026-08-02 (validate enforced 2026-08-05)
- **Lesson:** Before accepting any ground-attack example or compile, **check target
  geography in ME / against PyDCS airport math** — do not trust bearing/distance intuition.
  Shared validation now fails `strike_domain_mismatch` when the compile-equivalent strike
  Point’s Channel land/sea class disagrees with target unit domain (`channel_domain.py`
  UK–FR airport chord heuristic). `randomize` geometry redraws strike until domain matches.
- **Checks (every GA Spec):**
  1. Resolve strike Point from player airfield (`point_from_heading`); compare to known
     Channel airports (e.g. Dunkirk ≈ 120° / 72 km from Manston).
  2. **Land vehicles:** strike must be on land in enemy-held territory for combat (Axis
     French/Belgian coast for Channel WWII blue). Stopping *short* of a coastal airfield
     along a Channel crossing is usually **still water** (e.g. Manston→Dunkirk at 65 km).
     Prefer at/past the coast or an inland offset (example: ≈125° / 76 km inland of Dunkirk).
  3. **Water:** mid-Channel / offshore → `ships.yaml` sea-domain units only, never trucks.
  4. **Practice** (`strike.practice: true`): same-coalition / UK-side land OK; still verify
     the Point is actually on land, not the Strait.
  5. Confirm ME mission planner Target / Bombing waypoint and placed units agree (same
     land/sea domain).
- **Code:** `channel_domain.py`, `validation.py`, `randomize.py`,
  `examples/manston_ground_attack.yaml`, `compiler/pydcs_compiler.py`
  (`_apply_ground_attack`).

## Ground-attack: registry CLSID loadout + Bombing (not install payload scan)

- **Date:** 2026-08-02
- **Symptom / constraint:** Spitfire bomb + slipper loadouts must appear in `.miz` without
  re-enabling PyDCS `UnitPayloads` scanning (KeyError on some install files).
- **Cause:** Centreline pylon is tank **or** 500 lb — not both. Channel-crossing needs
  wing 250s + `SPITFIRE_45GAL_SLIPPER_TANK`. Player jettisons in cockpit; do not set
  `OptRestrictJettison`. A short SE offset (e.g. 140°/40 km) from Manston lands **in the
  sea** — land vehicles must use a bearing/distance that reaches enemy-held French/Belgian
  coast (example: ≈125° / 76 km inland near Dunkirk — **not** 65 km short of the coast,
  which is still water). Mid-Channel water strikes use `ships.yaml`
  ids (`Schnellboot_type_S130`, etc.) via `ship_group`, never trucks. Same-coalition /
  UK-side targets are allowed only when `strike.practice` is true (bombing-practice
  narrative); DCS gladly places friendly units as ME targets.
- **Fix:** Named presets in `payloads.yaml`; compiler `_disable_payload_scan` then
  `group.load_pylon((pylon, {"clsid": ...}))`. Strike uses airfield-relative
  bearing/distance; `get_strike_unit` chooses `vehicle_group` vs `ship_group` by domain;
  enemy coalition only.
- **Code:** `compiler/pydcs_compiler.py` (`_apply_ground_attack`), `data/channel/payloads.yaml`,
  `ground_units.yaml`, `ships.yaml`, `examples/manston_ground_attack.yaml`.

## Live research: Instant Answer alone is not enough

- **Date:** 2026-08-02
- **Symptom:** `/research Manston spitfire` printed only `fixture:…` notes that looked
  like a successful live lookup; Instant Answer JSON was often empty for multi-word
  aviation queries.
- **Cause:** DuckDuckGo Instant Answer is entity/definition oriented, not a full search
  API; it also sometimes returns an empty HTTP body (JSON decode fails). Soft-fail used
  to abort before any HTML fallback and returned fixtures with a warning chat did not
  label clearly. DDG HTML also serves an anomaly/challenge page for non-browser
  User-Agents (empty `result__a` parse).
- **Fix:** Cascade Instant Answer → `html.duckduckgo.com` result parse (stdlib); treat
  empty/invalid Instant Answer as continue-to-HTML; use a browser User-Agent for HTML;
  detect anomaly pages; enrich query with mission_type/theatre/aircraft; on empty/error
  always warn and label `/research` as offline fixture fallback. Research remains
  non-authoritative for Spec ids.
- **Code:** `tools/research.py`, `agent/session.py` (`/research`).

## Agent Spec JSON needs a derived example (not hand skeletons)

- **Date:** 2026-08-01
- **Symptom:** Live chat emitted flat Spec JSON (`airfield`/`aircraft` top-level, ISO
  `date` string, wrong `enemies`, `cap.objectives`) that Pydantic rejected; `/accept`
  had nothing to write.
- **Cause:** System prompt described rules in prose; models invent plausible shapes.
  Hand-maintained CAP skeletons in the prompt drift as mission types grow.
- **Fix:** `get_mission_spec_schema(mission_type)` + `agent/spec_schema.py` load
  validating examples from `examples/*.yaml`. Thin always-on anti-pattern reminder in
  the prompt; host repair nudge injects the derived example (infer `mission_type` from
  rejected JSON). Commander brief must use enum `.value` (weather → `sunny_clear`).
  `gpt-5.6-luna` rejects function tools on Chat Completions unless `reasoning_effort=none`
  or Responses API — stay on `gpt-4o-mini` until the live client is upgraded.
- **Code:** `agent/spec_schema.py`, `tools/surface.py` (`get_mission_spec_schema`),
  `agent/prompts.py`, `agent/session.py`, `agent/voice.py`.

## CAP station is airfield-relative; ROE is Spec-backed

- **Date:** 2026-08-01
- **Lesson:** CAP Spec uses `bearing_deg` + `distance_km` from the player airfield
  (PyDCS `point_from_heading`, metres), not raw map x/y or WGS84. Example Manston CAP:
  135° / 25 km / 4000 m / circle. Engagement maps to PyDCS `OptROE` on the CAP waypoint
  (`weapons_free`→0, `open_fire`→2, `return_fire`→3, `weapons_hold`→4). Optional enemies
  spawn near the station (`+3000`, `-2000` m), not the intercept Hawkinge corridor.
  Optional `duration_min` wraps Orbit in `ControlledTask.stop_after_duration`. Group
  `task` must be `"CAP"`.
- **Code:** `models.Cap`, `compiler/pydcs_compiler.py` (`_apply_cap`, `_place_cap_enemies`);
  example `examples/manston_cap.yaml`.

## Squadron voice is USAAF (not USAF); CLI brief vs `.miz` l10n

- **Date:** 2026-08-01 (updated 2026-08-02)
- **Lesson:** WWII Channel persona id is `usaaf` (Army Air Forces). `usaf` is post-1947 —
  do not rename the voice id. Default voice is `raf`. Commander briefs (tactics /
  procedures / watch-outs) are CLI/`PlanResult.brief` **and**, since `briefing-generation`,
  the same builder feeds compile-time `.miz` `l10n` — Spec fields still stay plain.
  `research_guidance` soft-fails to fixtures with a
  clear warning; chat `/research` labels offline fallback. Live uses Instant Answer then
  HTML results (`DCS_MIZ_RESEARCH_LIVE=1` or chat). Research is not DCS-id authority.
- **Code:** `agent/voice.py`, `agent/prompts.py`, `tools/research.py`, `agent/planner.py`,
  `briefing.py`, `compiler/pydcs_compiler.py`.

## User memory tables are not catalog_*

- **Date:** 2026-08-01
- **Lesson:** Prefs, generation history, and feedback live in the same
  `inventory.sqlite` as install + catalog, but under `user_meta` / `user_prefs` /
  `generation_history` / `satisfaction_feedback`. Never name them `catalog_*` —
  catalog sync and catalog schema bumps wipe those tables. User schema bumps may
  clear only user-memory tables; they must leave install + catalog intact.
  Host `plan_mission` records history; do not rely on the LLM calling
  `record_generation`. Never store API keys in SQLite.
- **Code:** `memory/store.py`, `agent/planner.py`, `tools/surface.py`.

## Catalog schema bump must clear synced_at

- **Date:** 2026-08-01
- **Symptom:** After bumping `CATALOG_SCHEMA_VERSION`, agent tools return empty catalog
  (`find_airfield` not_found) even though packaged YAML is fine.
- **Cause:** Version mismatch wiped `catalog_*` tables but left `catalog_meta.synced_at`,
  so `ensure_synced()` treated the empty DB as already synced.
- **Fix:** On schema mismatch, also delete `synced_at` / `source` so the next ensure/sync
  rebuilds from packaged YAML. Users with a stuck empty catalog can run
  `dcs-miz catalog sync`.
- **Code:** `catalog/store.py` (`CatalogStore._connect`).

## NL planner: stub offline, live via env key only

- **Date:** 2026-08-01
- **Lesson:** `dcs-miz plan` uses `agent/` with tool calling. `--stub` needs no network (canned
  Manston free flight). Live mode reads `OPENAI_API_KEY` (optional `DCS_MIZ_LLM_MODEL`,
  `OPENAI_BASE_URL`) — never store the key in SQLite or the repo. Always validate before
  writing YAML; one repair turn on failure. LLM must not write `.miz`/Lua.
- **Date / era:** Prefer a date that fits the mission’s historical backdrop (WWII for
  current Channel Spitfire/Axis content; later eras or modern day when the user wants).
  Channel years outside ~1939–1945 still succeed but warn (`agent/realism.py` / CLI stderr).
- **Code:** `agent/planner.py`, `agent/llm.py`, `agent/realism.py`; CLI `plan`.

## Agent tools: structured dicts, no dedicated CLI

- **Date:** 2026-08-01
- **Lesson:** Agent callables live in `dcs_miz_planner.tools` and return JSON-friendly
  `{ok: …}` dicts. Lookups use catalog; validate/compile wrap existing engines (inject
  `inventory=` in tests). Browse known data with `dcs-miz catalog list`; there is no
  `dcs-miz tools` CLI in v1 — pytest / Python REPL is the acceptance path.
- **Code:** `tools/surface.py`; `tests/test_tools.py`.

## Agent catalog shares `inventory.sqlite` (query layer, not SoT)

- **Date:** 2026-07-26
- **Lesson:** Known agent rows live in `catalog_*` tables in the same
  `%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite` as install inventory. YAML under
  `data/channel/` + Spec enums remain the product SoT; `dcs-miz catalog sync` replaces
  `catalog_*` from that package. Theatre **offerable** = known ∧ available ∧
  planner_supported. Never auto-promote discovered install theatres into known YAML.
- **Code:** `catalog/`; CLI `dcs-miz catalog sync|list`.

## Channel WWII Axis: use `ThirdReich`, not `Germany`

- **Date:** 2026-07-26 (validate allowlist 2026-08-05)
- **Symptom:** Intercept `.miz` shows “Allies flight: Bf 109 K-4” in the Mission Editor.
- **Cause:** PyDCS Channel defaults put modern **Germany** on **blue** (Allies). Looking up
  `Germany` reuses that blue country even when the Spec says `coalition: red`.
- **Fix:** Spec/compiler use PyDCS country id **`ThirdReich`** (DCS name “Third Reich”) on
  **red**. `_ensure_country` resolves by class attribute name, looks up by DCS display name,
  and refuses a country already parked on the wrong coalition. Shared validate allowlist
  (`allowlists.KNOWN_COUNTRIES` = UK / ThirdReich) rejects unknown countries with a
  Germany→ThirdReich hint before compile.
- **Code:** `allowlists.py`, `validation.py`, `compiler/pydcs_compiler.py`
  (`_ensure_country`); example `examples/manston_dawn_intercept.yaml`.

## Intercept spawn: Hawkinge anchor + Dover-approach offset

- **Date:** 2026-07-26
- **Lesson:** First intercept enemy flight is spawned inflight from PyDCS `TheChannel` **Hawkinge** (airdromeId 6) map x/y, plus a fixed SE offset toward the Strait as a Dover-approach corridor relative to Manston. Do not invent WGS84 lat/lon; stay in Channel terrain units.
- **Radio:** Enemy `Bf-109K-4` group frequency from registry (**40.0** MHz), same VHF rule as Spitfire 124.
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py` (`_place_enemies`); example `examples/manston_dawn_intercept.yaml`.

## Golden fixtures: normalize random `onboard_num`

- **Date:** 2026-07-26
- **Symptom:** Full `mission` member comparison fails across processes even when the Spec is unchanged.
- **Cause:** PyDCS assigns a random `["onboard_num"]` per process; other Manston free-flight fields stay stable.
- **Fix:** Store a normalized golden (`onboard_num` → `"<num>"`) and compare after the same normalization; keep explicit substring contracts (Manston, frequency, etc.).
- **Code:** `tests/fixtures_support.py`, `tests/fixtures/manston_cold_freeflight/`; refresh with `uv run python tests/refresh_manston_golden.py`.

## Install inventory: SQLite cache, never execute DCS Lua

- **Date:** 2026-07-26
- **Lesson:** Local theatre availability lives in `%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite` (override with `DCS_MIZ_INVENTORY_DB` / `--db`). Ordinary `dcs-miz theatres` reads the cache; `--refresh` rescans. Packaged Channel YAML stays the product SoT — do not treat install inventory rows as known catalog. Known agent rows are separate `catalog_*` tables in the same file, filled only by `dcs-miz catalog sync`.
- **Parse only:** `autoupdate.cfg` (JSON), terrain `entry.lua` / `pluginsEnabled.lua` via constrained regex for quoted fields. Never `exec` / import DCS Lua.
- **Discovery:** on Windows, prefer `HKCU/HKLM\SOFTWARE\Eagle Dynamics\DCS World` `Path` (covers non-Program-Files installs like `S:\DCS World`), then common Program Files / Steam locations; override with `--dcs-root` / `DCS_MIZ_DCS_ROOT`.
- **Code:** `src/dcs_miz_planner/install/`.

## Stock Channel Spitfire: native triggers, almost no Lua

- **Date:** 2026-07-26
- **Lesson:** ED Channel Spitfire Instant Action missions audited in R5 use **native ME triggers** (zones, flags, radio menus, unit-dead, messages/VO). **No Mist, no MOOSE, no zip-root `.lua`** in that corpus. Prefer native trigger compile (M6 `#20`–`#21`) for Channel combat behaviour.
- **Training exception:** `1-Startup.miz` uses short `a_do_script` payloads stored as **dictionary ActionText** keys (Mission Scripting API / event handlers), not separate zip `.lua` files — template for optional M6 `#22` snippets.
- **Beware! Beware!** Channel campaign missions can ship with **empty** trigger tables; immersion is briefing/kneeboard/VO/AI routes, not triggers.
- **Source:** `research/lua-usage-patterns.md` (gitignored). Revisit after R1–R2 user-file audits.
- **Do not:** assume free flight ⇒ zero triggers (stock Cold/Free Flight still have zone→VO scaffolding).

## Mission Scripting API defs ≠ ME trigger predicates

- **Date:** 2026-07-26
- **Lesson:** EmmyLua / `dcs-world-schema` helps author **SSE** Lua (`trigger.action.*`, `world.addEventHandler`). It does **not** validate Mission Editor action names (`a_out_text_delay`, `c_part_of_coalition_in_zone`). Those need PyDCS emit + golden fixtures against stock extracts.
- **Source:** `research/lua-ide-tooling.md`. Vendor LuaLS lab only when M6 `#22` starts; VEAF MCP is a lab microscope, never the product compiler.

## Spitfire / WWII: group frequency must be in VHF band

- **Date:** 2026-07-26
- **Symptom:** Compiled Manston free-flight `.miz` opens in the Mission Editor, but launching the flight warns the radio frequency is invalid for the Spitfire. PyDCS defaults every group to `["frequency"]=251`.
- **Cause:** 251 MHz is a modern UHF value. WWII radios cannot tune it: Allied VHF is ~**100–156 MHz**, German VHF ~**38.4–42.4 MHz**.
- **Fix:** Set the group frequency from the Channel registry radio table (Spitfire **124**, Bf-109K-4 40, FW-190 38.4) — the values every stock ED Channel mission uses. Assigning `group.frequency` is enough; DCS tunes the aircraft's first radio channel from it, and stock missions leave `radioSet = false`.
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py`; data in `data/channel/aircraft.yaml` via `registry.py`.
- **Do not:** use the airfield ATC frequency as the flight frequency. It is in-band and works (Channel ATC VHF-high runs 118.05–118.6, Manston = 118.45), but it is the tower channel, not the flight's, and diverges from every stock mission.
- **Note:** PyDCS `set_frequency()` also flips `radio_set` and writes channel presets — more than ME does. Plain attribute assignment matches stock output.

## Spitfire cockpit arguments: triggers only, not compile input

- **Date:** 2026-07-25
- **Lesson:** Community list [DCS User Files 3349460](https://www.digitalcombatsimulator.com/en/files/3349460/) (ModelViewer2 args for Spitfire LF Mk.IX) is for Mission Editor **triggers** that watch cockpit state (e.g. switch/gauge animation args). It does **not** set cold-start / parking state and is **not** needed for free-flight `.miz` compile.
- **Caveats:** Tied to DCS **2.9.25.21402**; some rows marked incomplete (red text in the sheet). Animation argument numbers are not the same as clickable command IDs — re-verify in-game before promoting into a registry.
- **Local copy:** `research/spitfire-cockpit-arguments/` (PDF + Excel; gitignored under `research/`). Do not commit the RAR or dump raw args into the product registry until an interactive/training-mission change needs them.

## PyDCS: payload loader KeyError when DCS install is present

- **Date:** 2026-07-25 (updated 2026-08-04)
- **Symptom:** `KeyError` on a path under `S:/DCS World/.../UnitPayloads/*.lua` while creating aircraft via `Mission.flight_group_from_airport` / `Plane.__init__` → `FlyingType.load_payloads`.
- **Cause:** With a real DCS install detected, PyDCS scans payload dirs. `scan_payload_dir` skips files with no `["unitType"]` line (never caches them). `load_payloads` then does `_payload_cache[payload_path]` → KeyError. Upstream bug in PyDCS `unittype.py`; free-flight missions do not need payloads.
- **Fix / workaround:** In our compiler only, call `_disable_payload_scan(...)` before creating units: seed `_payload_cache` so the install is not scanned, and set `aircraft_type.payloads = {}` so `load_payloads` returns early. Do **not** edit files under `.venv`.
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py` (`_disable_payload_scan`).
- **Do not:** Re-enable full install payload scanning without fixing the KeyError path (`.get` / skip missing keys) or pinning a fixed PyDCS.
- **Upstream (R7):** `.get()` fix merged on pydcs `master` (#439/#440, 2026-06); **not** in PyPI `0.15.0`. Keep the monkeypatch until R8 bumps to a release that includes it, then re-test with scan on.

## PyDCS: no standalone `theatre` zip member

- **Date:** 2026-07-25
- **Symptom:** Compiled `.miz` has `mission` / `options` / `warehouses` but no `theatre` file; theatre only appears as `["theatre"]="TheChannel"` inside `mission`.
- **Cause:** PyDCS `Mission.save` does not write a top-level `theatre` member (real ME-exported missions usually do).
- **Fix:** After `mission.save`, append a `theatre` member with the theatre id string if missing (`_ensure_theatre_member`).
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py`.
- **Note:** DCS often still loads without the file; we keep it for fidelity and our compiler acceptance contract.

## PyDCS weather: `clouds_iprecptns` is an enum

- **Date:** 2026-07-25
- **Symptom:** `AttributeError: 'int' object has no attribute 'value'` in `Weather._make_cloud_dict` during `mission.save`.
- **Cause:** Assigning `clouds_iprecptns = 0` (int). PyDCS expects `Weather.Preceptions` (e.g. `Preceptions.None_`).
- **Fix:** Use `Weather.Preceptions.None_` (and other enum members) for clear / precip settings.
- **Code:** `PyDCSCompiler._apply_weather`.

## DCS identity strings: never invent

- **Date:** 2026-07-24 (research) / reinforced in M1
- **Symptom:** Mission fails to load or units missing if type / airfield ids are wrong.
- **Cause:** Guessing spellings (`Spitfire IX`, wrong `airdromeId`, etc.).
- **Fix:** Use verified ids only (`SpitfireLFMkIX`, Manston → `airdromeId` 5, theatre `TheChannel`, …). Prefer `registry.py` / `data/channel/*.yaml` over memory. Expand the registry via data PRs, not ad-hoc in prompts.

## Mission Spec vs PyDCS boundary

- **Date:** 2026-07-25
- **Lesson:** Keep `MissionSpec` / loader / CLI free of PyDCS imports. All PyDCS usage stays behind `CompilerInterface` / `pydcs_compiler.py` so a future native compiler can replace the backend.

## OpenSpec / git process

- **Date:** 2026-07-24
- **Lesson:** Never implement or commit OpenSpec work on `master`/`main`. Branch name = change name. Enforced by Cursor hook `protect-master.py` and pre-commit `no-commit-to-branch`.

---

## How to add an entry

1. Put new lessons **at the top** of the list (newest first), under a `##` heading.
2. Prefer one concrete failure over long narrative.
3. Link the code path or OpenSpec change if it exists.
4. If the lesson changes product behavior, also update specs/design as needed — this file is not a substitute for OpenSpec.
