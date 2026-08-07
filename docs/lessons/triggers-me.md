# Triggers, ME behaviour & failures

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Recon AOI find pack (`mission_type: recon`) (2026-08-07)

- **Date:** 2026-08-07
- **Lesson:** Recon Specs MUST keep `zones`/`triggers` empty in v1. After validate,
  `recon.expand_recon_find_pack` injects zone `recon_aoi` plus once-triggers
  `recon_aoi_mark` (T+1s → F10 mark) and `recon_area_observed` (player coalition in
  zone → message + flag **830**). Flag 830 sits above section orders (800+) and
  discipline (820+). Compiler uses PyDCS `Reconnaissance` + OptROE WeaponHold;
  optional `targets` are observe-only contacts (no Bombing).
- **Do not:** hand-author zones/triggers on recon v1; reuse strike/payload; treat
  contacts as destroy objectives.
- **Code:** `recon.py`, `compiler/pydcs_compiler.py` (`_apply_recon`),
  `examples/manston_recon.yaml`.

## Aircraft failures via ME Failures table (2026-08-07)

- **Date:** 2026-08-07
- **Symptom:** Compiled `a_set_failure` / ME Set Failure with Within=0 never
  failed Mag 1 in Instant Action; messages still fired; manual Mag switch worked.
- **Cause:** ME **Within (mm)** is **minutes**. Within `0` is a zero-width window
  (never fires); ED stock defaults `mmint=1`. Stock Spitfire missions arm failures
  via mission-root `failures` (`enable`/`hh`/`mm`/`mmint`/`prob`), not
  `a_set_failure` (none found in stock Mods). Options → Misc → **Random System
  Failures** is separate MTBF noise — not required for scripted Failures panel
  entries, and not a substitute for them.
- **Fix:** Emit Spec `failures` into `mission.failures` (PyDCS `mission.failures`);
  After = `start_after_s` floored to minutes; Within = max(1, ceil(random_pause_s/60)).
  Mag-cut drill: Mag 2 OFF + Mag 1 armed.
- **Debrief:** After the mission, Debriefing shows Event **failure** with Details
  like **Magneto No. 1 failure** when the Failures-panel cut actually applied
  (useful acceptance check beyond cockpit feel).
- **Code / notes:** `compiler/failures_emit.py`; example
  `manston_freeflight_magneto_failure.yaml`; backlog `#22b`.

## Aircraft failures via ME SetFailure triggers (2026-08-07)

- **Date:** 2026-08-07
- **Lesson:** Prefer Spec `failures[]` → mission Failures table (see entry above).
  Earlier assumption that ONCE `TimeAfter` + PyDCS `SetFailure` was the stock path
  was wrong for Spitfire; Within minutes semantics also bite if left at 0.
- **Code / notes:** superseded by Failures-table emit; backlog `#22b`.

## Spec dynamics expand XOR with narrative (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** `dynamics` and `narrative.enabled` both require empty zones/triggers
  and clear themselves after expand. Validate/compile runs narrative first — if XOR
  is only checked inside `apply_dynamics`, narrative expands first and the failure
  becomes `dynamics_conflict` (non-empty triggers) instead of the XOR code. Check
  XOR at the start of **both** expanders (and fail closed on missing
  `late_activation` for pooled enemies/targets).
- **Code:** `dynamics.py`, `narrative.py`, `validation.py`.

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

## Stock Channel Spitfire: native triggers, almost no Lua

- **Date:** 2026-07-26
- **Lesson:** ED Channel Spitfire Instant Action missions audited in R5 use **native ME triggers** (zones, flags, radio menus, unit-dead, messages/VO). **No Mist, no MOOSE, no zip-root `.lua`** in that corpus. Prefer native trigger compile (M6 `#20`–`#21`) for Channel combat behaviour.
- **Training exception:** `1-Startup.miz` uses short `a_do_script` payloads stored as **dictionary ActionText** keys (Mission Scripting API / event handlers), not separate zip `.lua` files — template for optional M6 `#22` snippets.
- **Beware! Beware!** Channel campaign missions can ship with **empty** trigger tables; immersion is briefing/kneeboard/VO/AI routes, not triggers.
- **Source:** `research/lua-usage-patterns.md` (gitignored). Revisit after R1–R2 user-file audits.
- **Do not:** assume free flight ⇒ zero triggers (stock Cold/Free Flight still have zone→VO scaffolding).

## Spitfire cockpit arguments: triggers only, not compile input

- **Date:** 2026-07-25
- **Lesson:** Community list [DCS User Files 3349460](https://www.digitalcombatsimulator.com/en/files/3349460/) (ModelViewer2 args for Spitfire LF Mk.IX) is for Mission Editor **triggers** that watch cockpit state (e.g. switch/gauge animation args). It does **not** set cold-start / parking state and is **not** needed for free-flight `.miz` compile.
- **Caveats:** Tied to DCS **2.9.25.21402**; some rows marked incomplete (red text in the sheet). Animation argument numbers are not the same as clickable command IDs — re-verify in-game before promoting into a registry.
- **Local copy:** `research/spitfire-cockpit-arguments/` (PDF + Excel; gitignored under `research/`). Do not commit the RAR or dump raw args into the product registry until an interactive/training-mission change needs them.
