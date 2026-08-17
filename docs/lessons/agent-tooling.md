# Agent, catalog, memory & research

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Nevada invent allows intercept; dedicated notes (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Nevada invent/chat may emit **free_flight, CAP, or intercept**
  at Nellis (Su-25T, USA blue). Intercept spawn is **350° / 40 km** north of
  Nellis over Desert NWR / north-range land — same station as
  `nellis_north_range_cap`; not Incirlik 180/40, not Batumi 270/40, not
  Cherbourg 180/63, not Hawkinge. Schema `theatre=Nevada` + `intercept`
  loads `nellis_dawn_intercept.yaml` with dedicated
  `_NEVADA_INTERCEPT_NOTES` — do **not** concatenate Channel
  `_COMMON_NOTES` / `_TYPE_NOTES`. Enemies: Su-25T, country **Russia** red.
  Do not put USA on red. GA/escort/recon still refuse every turn. Domain
  classifier stays fail-closed on Nevada. Path clamp and soft immersion
  floor stay TheChannel-only. Stub LLM stays Manston. FF schema example
  stays `nellis_cold_freeflight.yaml`; CAP schema stays
  `nellis_north_range_cap.yaml`.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`
  (`_NEVADA_INTERCEPT_NOTES`), `agent/prompts.py`,
  `examples/nellis_dawn_intercept.yaml`.

## Nevada invent allows CAP; 350/40 desert north-range (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Nevada invent/chat may emit **free_flight or CAP** at Nellis
  (Su-25T, USA blue). CAP station is **350° / 40 km / 4000 m** north of
  Nellis over Desert NWR / north-range land — not Incirlik 180/40, not
  Batumi 270/40, not Cherbourg 180/63, not Manston 135/25, not Creech 303/40.
  180/40 is nearer Henderson; 270/40 is nearer North Las Vegas; 79/40 is
  Echo Bay water. Schema `theatre=Nevada` + `cap` loads
  `nellis_north_range_cap.yaml` with dedicated `_NEVADA_CAP_NOTES` — do not
  concatenate Channel `_COMMON_NOTES` / `_TYPE_NOTES`. Enemies: Su-25T,
  country **Russia** red (`EnemyFlight` defaults to ThirdReich). Do not put
  USA on red. Intercept/GA/escort/recon still refuse every turn. Domain
  classifier and intercept spawn stay fail-closed on Nevada. Path clamp and
  soft immersion floor stay TheChannel-only. Stub LLM stays Manston. FF
  schema example stays `nellis_cold_freeflight.yaml`.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py` (`_NEVADA_CAP_NOTES`),
  `agent/prompts.py`, `planning_options.yaml` (`nellis_home`,
  `nellis_north_range_cap`), `examples/nellis_north_range_cap.yaml`.

## Syria invent allows recon; all six types (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Syria invent/chat may emit **all six types** at Incirlik
  (Su-25T, Turkey blue). Recon AOI is **121° / 200 km / 2000 m** inland past
  Aleppo — same land station as `aleppo_inland_strike` / GA, not CAP 180/40
  sea, not Kutaisi 43/110, not Manston 125/76. Schema `theatre=Syria` + `recon`
  loads `incirlik_aleppo_recon.yaml` with dedicated `_SYRIA_RECON_NOTES` — do
  **not** concatenate Channel `_TYPE_NOTES` (french_coast / U-boat / 125/76).
  Observe modern trucks from `list_strike_targets(theatre=Syria)` (`Ural-375`;
  country **Syria** red). Weapons hold; omit payload. Path clamp and soft
  immersion floor stay TheChannel-only. Stub LLM stays Manston. Fail-closed
  invent coverage moves to Nevada/Falklands combat.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py` (`_SYRIA_RECON_NOTES`),
  `agent/prompts.py`, `planning_options.yaml` (`aleppo_inland_strike`,
  `incirlik_home`), `examples/incirlik_aleppo_recon.yaml`.

## Syria invent allows ground_attack; Aleppo 121/200 (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Syria invent/chat may emit **free_flight, CAP, intercept, escort, or
  ground_attack** at Incirlik (Su-25T, Turkey blue). GA strike is **121° / 200 km /
  2000 m** inland past Aleppo — not CAP 180/40 (sea), not Kutaisi 43/110, not
  Maupertus 180/133. Schema `theatre=Syria` + `ground_attack` loads
  `incirlik_aleppo_ground_attack.yaml` with dedicated `_SYRIA_GA_NOTES` — do
  **not** concatenate Channel `_TYPE_NOTES` / `_COMMON_NOTES`. Targets: modern
  trucks from `list_strike_targets(theatre=Syria)` (`Ural-375`; country **Syria**
  red). Dual-offer is query-time: stored `theatre_id` stays `Caucasus` /
  `era_id=modern` / `domain=land`. Recon still refuses every turn. Path clamp
  stays TheChannel-only. Stub LLM stays Manston.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py` (`_SYRIA_GA_NOTES`),
  `agent/prompts.py`, `tools/surface.py` (`_strike_theatre_match`),
  `planning_options.yaml` (`aleppo_inland_strike`, `incirlik_home`),
  `examples/incirlik_aleppo_ground_attack.yaml`.

## Syria invent allows escort; 180/40 Iskenderun (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Syria invent/chat may emit **free_flight, CAP, intercept, or escort**
  at Incirlik (Su-25T, Turkey blue). Escort package destination is **180° / 40 km /
  4000 m** due south of Incirlik — same station as `incirlik_iskenderun_cap` /
  intercept, not Manston 120/55, not Cherbourg 180/63, not Batumi 270/40. Schema
  `theatre=Syria` + `escort` loads `incirlik_iskenderun_escort.yaml` with dedicated
  `_SYRIA_ESCORT_NOTES` — do not concatenate Channel `_TYPE_NOTES` (Manston 120/55)
  or `_COMMON_NOTES`. Package country **Turkey** (PackageFlight defaults to UK).
  Bounce country **Syria** red (`EnemyFlight` defaults to ThirdReich; theatre id
  `Syria` ≠ country `Syria`). Do **not** edit `intercept_spawn.py` for escort
  (compiler escort is already airfield-relative). GA/recon still refuse every
  turn. Stub LLM stays Manston.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`, `agent/prompts.py`,
  `planning_options.yaml` (`incirlik_home`, `incirlik_iskenderun_cap`),
  `examples/incirlik_iskenderun_escort.yaml`.

## Domain-mismatch repair is theatre-keyed (2026-08-17)

- **Date:** 2026-08-17
- **Symptom:** Batumi recon with CAP 270/40 sea AOI and land trucks failed
  `strike_domain_mismatch`, then `host_spec_repair_nudge` injected Channel
  `french_coast_strike_belt` 125°/76 km.
- **Cause:** The mismatch branch ignored inferred theatre.
- **Fix:** Channel (or unspecified) stays 125/76. Caucasus → Kutaisi 43/110.
  Normandy → Maupertus 180/133. Syria → Aleppo 121/200 (not CAP 180/40).
  Nevada/Falklands must not copy french-coast geometry.
- **Code:** `agent/prompts.py` `host_spec_repair_nudge`.

## Syria invent allows intercept; 180/40 Iskenderun spawn (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Syria invent/chat may emit **free_flight, CAP, or intercept** at
  Incirlik (Su-25T, Turkey blue). Intercept spawn is **180° / 40 km** due
  south of Incirlik — same station as `incirlik_iskenderun_cap`, not Hawkinge,
  not Cherbourg 180/63, not Batumi 270/40. Store literals
  (`221207.773438`, `-35240.347656` + offset `-40000, 0` → enemy
  `181207.773438`, `-35240.347656`). Do not recompute Channel Hawkinge from
  `airport_list()`. Schema `theatre=Syria` + `intercept` loads
  `incirlik_dawn_intercept.yaml` with dedicated `_SYRIA_INTERCEPT_NOTES`.
  Enemies: Su-25T, country **Syria** red. GA/escort/recon still refuse.
  Domain classifier stays fail-closed on Syria.
- **Code:** `intercept_spawn.py`, `agent/immersion.py`, `agent/spec_schema.py`,
  `examples/incirlik_dawn_intercept.yaml`.

## Syria invent allows CAP; 180/40 Iskenderun (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Syria invent/chat may emit **free_flight or CAP** at Incirlik
  (Su-25T, Turkey blue). CAP station is **180° / 40 km / 4000 m** due south
  of Incirlik over the Gulf of Iskenderun — not Cherbourg 180/**63**, not
  Batumi 270/40 (west of Incirlik is nearer Adana Şakirpaşa, land). Schema
  `theatre=Syria` + `cap` loads `incirlik_iskenderun_cap.yaml` with dedicated
  `_SYRIA_CAP_NOTES` — do not concatenate Channel `_TYPE_NOTES`. Enemies:
  Su-25T, country **Syria** red (`EnemyFlight` defaults to ThirdReich).
  Intercept/GA/escort/recon still refuse every turn. Domain classifier and
  intercept spawn stay fail-closed on Syria. Path clamp and soft immersion
  floor stay TheChannel-only. Stub LLM stays Manston.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`, `agent/prompts.py`,
  `planning_options.yaml` (`incirlik_home`, `incirlik_iskenderun_cap`),
  `examples/incirlik_iskenderun_cap.yaml`.

## Caucasus invent allows recon; all six types (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Caucasus invent/chat may emit **all six types** at Batumi
  (Su-25T, Georgia blue). Recon AOI is **43° / 110 km / 2000 m** inland past
  Kutaisi — same land station as `kutaisi_inland_strike` / GA, not CAP 270/40
  sea, not Manston 125/76. Schema `theatre=Caucasus` + `recon` loads
  `batumi_kutaisi_recon.yaml` with dedicated `_CAUCASUS_RECON_NOTES` — do not
  concatenate Channel `_TYPE_NOTES` (french_coast / U-boat / 125/76). Observe
  modern trucks from `list_strike_targets(theatre=Caucasus)` (`Ural-375`;
  country Russia). Weapons hold; omit payload. Path clamp and soft immersion
  floor stay TheChannel-only. Stub LLM stays Manston. Fail-closed invent
  coverage moves to Syria combat.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`, `agent/prompts.py`,
  `planning_options.yaml` (`kutaisi_inland_strike`, `batumi_home`),
  `examples/batumi_kutaisi_recon.yaml`.

## Caucasus invent allows escort; recon still refuses (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Caucasus invent/chat may emit **free_flight, CAP, ground_attack,
  intercept, or escort** at Batumi (Su-25T, Georgia blue). Escort package
  destination is **270° / 40 km / 4000 m** west of Batumi over the Black Sea —
  same station as `batumi_black_sea_cap` / intercept, not Manston 120/55, not
  Cherbourg 180/63. Schema `theatre=Caucasus` + `escort` loads
  `batumi_black_sea_escort.yaml` with dedicated `_CAUCASUS_ESCORT_NOTES` — do
  not concatenate Channel `_TYPE_NOTES` (Manston 120/55). Package country
  **Georgia** (PackageFlight defaults to UK). Bounce country **Russia**
  (`EnemyFlight` defaults to ThirdReich). Recon still refuses every turn.
  Compiler escort is already airfield-relative; do not copy intercept spawn
  x/y into the Spec. Path clamp and soft immersion floor stay TheChannel-only.
  Stub LLM stays Manston.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`, `agent/prompts.py`,
  `planning_options.yaml` (`batumi_black_sea_cap`, `batumi_home`),
  `examples/batumi_black_sea_escort.yaml`.

## Caucasus invent allows intercept; escort/recon still refuse (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Caucasus invent/chat may emit **free_flight, CAP, ground_attack,
  or intercept** at Batumi (Su-25T, Georgia blue). Intercept spawn is **270° /
  40 km** west of Batumi over the Black Sea — same station as
  `batumi_black_sea_cap`, not Hawkinge/Dover, not Cherbourg 180/63. Schema
  `theatre=Caucasus` + `intercept` loads `batumi_dawn_intercept.yaml` with
  dedicated `_CAUCASUS_INTERCEPT_NOTES` — do not concatenate Channel
  `_TYPE_NOTES` (Hawkinge / `manston_dawn_intercept_radio`). Enemies: Russia +
  Su-25T (set `enemies[].country: Russia`). Escort / recon still refuse every
  turn. Path clamp and soft immersion floor stay TheChannel-only. Stub LLM
  stays Manston.
- **Code:** `intercept_spawn.py`, `agent/immersion.py`, `agent/spec_schema.py`,
  `planning_options.yaml` (`batumi_black_sea_cap`, `batumi_home`).

## Caucasus invent allows ground_attack; modern trucks (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Caucasus invent/chat may emit **free_flight, CAP, or
  ground_attack** at Batumi (Su-25T, Georgia blue). GA strike is **43° / 110 km
  / 2000 m** inland past Kutaisi — not CAP 270/40. Schema
  `theatre=Caucasus` + `ground_attack` loads
  `batumi_kutaisi_ground_attack.yaml` with dedicated `_CAUCASUS_GA_NOTES` — do
  not concatenate Channel `_TYPE_NOTES` (french_coast / Manston). Catalog
  tags modern trucks `theatre_id=Caucasus` / `era_id=modern`;
  `list_strike_targets(theatre="Caucasus")` returns Ural-375 not Blitz.
  Channel `soft_vehicles` unit_ids stay WWII. Intercept/escort/recon still
  refuse every turn. Path clamp and soft immersion floor stay TheChannel-only.
  Stub LLM stays Manston.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`, `catalog/sync.py`,
  `planning_options.yaml` (`kutaisi_inland_strike`, `modern_soft_vehicles`).

## Caucasus invent allows CAP; 270/40 Black Sea (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Caucasus invent/chat may emit **free_flight or CAP** at Batumi
  (Su-25T, Georgia blue). CAP station is **270° / 40 km / 4000 m** west of
  Batumi over the Black Sea — live `heading_between_point` from Batumi: Kutaisi
  43.14°/97.20 km inland, Tbilisi 81.82°/282.11 km inland, Sochi 320.96°
  along-coast. Do **not** copy Manston 135/25 or Cherbourg 180/63. Enemies are
  **Russia + Su-25T** (explicit country — `EnemyFlight.country` defaults to
  `ThirdReich`, which modern era-filter rejects). Domain, intercept spawn, and
  path clamp stay fail-closed / Channel-only. Schema `theatre=Caucasus` + `cap`
  loads `batumi_black_sea_cap.yaml` with dedicated `_CAUCASUS_CAP_NOTES` — do
  not concatenate Channel `_COMMON_NOTES`. Stub LLM stays Manston.
- **Code:** `planning_options.yaml` (`batumi_home`, `batumi_black_sea_cap`),
  `agent/immersion.py`, `agent/spec_schema.py`, `examples/batumi_black_sea_cap.yaml`.

## Normandy invent allows recon; all six types (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Normandy invent/chat may emit **all six** mission types at
  NeedsOarPoint. Recon AOI is inland of Maupertus (180° / 133 km / 2000 m —
  same land station as GA `maupertus_inland_strike`, not Manston 125/76, not
  CAP/intercept/escort 180/63 sea). Schema `theatre=Normandy` + `recon` loads
  `needs_oar_point_recon.yaml` with dedicated `_NORMANDY_RECON_NOTES` — do
  **not** concatenate Channel `_TYPE_NOTES` (french_coast / U-boat / 125/76).
  Compiler recon is already airfield-relative; no intercept-spawn recipe.
  Stub LLM stays Manston. Soft immersion floor and path clamp stay
  TheChannel-only.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`, `agent/prompts.py`,
  `examples/needs_oar_point_recon.yaml`.

## Normandy invent allows escort; recon still refuses (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Normandy invent/chat may emit **free_flight, CAP, ground_attack,
  intercept, or escort** at NeedsOarPoint. Escort package destination is the
  Cherbourg corridor (180°/63 km / 4000 m — same as CAP/intercept, not
  Manston 120/55). Schema `theatre=Normandy` + `escort` loads
  `needs_oar_point_escort.yaml` with dedicated `_NORMANDY_ESCORT_NOTES` —
  do not concatenate Channel `_TYPE_NOTES`. Recon still refuses every turn.
  Compiler escort is already airfield-relative (`point_from_heading`); no
  intercept-spawn recipe is required. Stub LLM stays Manston.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`, `agent/prompts.py`,
  `examples/needs_oar_point_escort.yaml`.

## Normandy invent allows intercept; escort/recon still refuse (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Normandy invent/chat may emit **free_flight, CAP, ground_attack,
  or intercept** at NeedsOarPoint. Intercept uses the Cherbourg corridor
  (180°/63 km — same as CAP, not Hawkinge). Schema `theatre=Normandy` +
  `intercept` loads `needs_oar_point_dawn_intercept.yaml` with dedicated
  `_NORMANDY_INTERCEPT_NOTES` — do not concatenate Channel `_TYPE_NOTES`
  (Hawkinge / `manston_dawn_intercept_radio`). Escort / recon still refuse
  every turn. Soft immersion floor and path clamp stay TheChannel-only.
  Stub LLM stays Manston.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`, `agent/prompts.py`.

## Normandy invent allows ground_attack; land strike list (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Normandy invent/chat may emit **free_flight, CAP, or
  ground_attack** at NeedsOarPoint (GA strike 180°/133 km from
  `maupertus_inland_strike`, not Manston 125/76 and not CAP 180/63 sea).
  Intercept / escort / recon still refuse every turn. Schema
  `theatre=Normandy` + `ground_attack` loads
  `needs_oar_point_ground_attack.yaml` with dedicated notes — do not
  concatenate Channel `_TYPE_NOTES` (french_coast / Manston).
  `list_strike_targets(theatre="Normandy")` returns WWII **land** units
  (Blitz, flak18, …); sea_craft stay Channel-only; stored catalog
  `theatre_id` remains `TheChannel`. Path clamp and soft immersion stay
  TheChannel-only. Stub LLM stays Manston.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`,
  `tools/surface.py` (`_strike_theatre_match`), `agent/prompts.py`.

## QAG HTML is research colour, not catalog YAML (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Gitignored `research/DCS *` QAG HTML is a **local source** for
  `research_guidance`, not product data. A thin packaged index
  (`data/qag_fixtures/qag_index.yaml`) maps those paths; the HTML itself MUST
  NOT be copied into the wheel. Notes are `fixture:qag:<id>` when the dump is
  present; if `research/` is missing (CI, installed wheel) QAG notes are empty
  and canned Channel fixtures remain. QAG UI names, site templates
  (`FLAK36 BATTERY(Asset Pack Required)`), and `template.lua` strings are
  **not** Spec/`vehicle_map` ids. The Cold War Anti-Ship HTML was a copy of the
  WWII anti-ship page — index row `enabled: false`. QAG Dogfight / Anti-Ship SR /
  SEAD SR are generator families, not Spec `mission_type`s. QAG “Cold War
  1947–1970” is not a Spec era. Promote only via
  [`docs/THEATRE_TARGET_PROMOTE.md`](../THEATRE_TARGET_PROMOTE.md) §B.
- **Code:** `tools/qag_fixtures.py`, `tools/research.py`, `data/qag_fixtures/qag_index.yaml`.

## Falklands invent is free_flight only; schema notes must not concatenate (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Invent allow-table: TheChannel all six; Normandy free_flight +
  CAP; Caucasus **free_flight only**; Syria **free_flight only**; Nevada
  **free_flight only**; Falklands **free_flight only** (CAP refused every
  turn — never capture or write). Schema `theatre=Falklands` + free_flight
  loads `mount_pleasant_cold_freeflight.yaml`; combat types raise with no
  Manston/NeedsOarPoint/Batumi/Incirlik/Nellis skeleton. `_notes_for("Falklands")`
  returns dedicated `_FALKLANDS_FF_NOTES` only — do **not** concatenate
  `_COMMON_NOTES` / `_TYPE_NOTES` (those cite Manston YAML, Spitfire
  failures, `channel_place`). `infer_theatre` accepts JSON `Falklands` or
  airfield `MountPleasant` (and PyDCS-style `Mount_Pleasant` so a wrong key
  still repairs to Falklands, not Manston). Host repair of `domain_unsupported_theatre` /
  `intercept_unsupported_theatre` MUST use the inferred theatre — do not
  hardcode Nevada, Syria, Caucasus, or Normandy or a Falklands CAP repair
  becomes Nellis, Incirlik, Batumi, or NeedsOarPoint. Stub LLM stays
  Manston. `list_strike_targets(theatre="Falklands")` is empty. Hermetic
  inventory: Falklands AVAILABLE + `planner_supported=True`; retarget
  `test_unsupported_installed_map` onto Kola (installed, no PyDCS). Soft
  immersion floor (`host_immersion_repair_nudge`) is **TheChannel-only** —
  do not cite `manston_*.yaml` behaviour examples on
  Falklands/Nevada/Syria/Caucasus.
- **Code:** `agent/spec_schema.py` (`_FALKLANDS_FF_NOTES`, `_notes_for`),
  `agent/immersion.py`, `agent/prompts.py`, `agent/session.py`,
  `agent/planner.py`.

## Nevada invent is free_flight only; schema notes must not concatenate (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Invent allow-table: TheChannel all six; Normandy free_flight +
  CAP; Caucasus **free_flight only**; Syria **free_flight only**; Nevada
  **free_flight only** (CAP refused every turn — never capture or write).
  Schema `theatre=Nevada` + free_flight loads `nellis_cold_freeflight.yaml`;
  combat types raise with no Manston/NeedsOarPoint/Batumi/Incirlik skeleton.
  `_notes_for("Nevada")` returns dedicated `_NEVADA_FF_NOTES` only — do
  **not** concatenate `_COMMON_NOTES` / `_TYPE_NOTES` (those cite Manston
  YAML, Spitfire failures, `channel_place`). `infer_theatre` accepts JSON
  `Nevada` or airfield `Nellis`. Host repair of `domain_unsupported_theatre`
  / `intercept_unsupported_theatre` MUST use the inferred theatre — do not
  hardcode Syria, Caucasus, or Normandy or a Nevada CAP repair becomes
  Incirlik, Batumi, or NeedsOarPoint. Stub LLM stays Manston.
  `list_strike_targets(theatre="Nevada")` is empty. Hermetic inventory:
  Nevada AVAILABLE + `planner_supported=True`; retarget
  `test_unsupported_installed_map` onto Falklands. Soft immersion floor
  (`host_immersion_repair_nudge`) is **TheChannel-only** — do not cite
  `manston_*.yaml` behaviour examples on Nevada/Syria/Caucasus.
- **Code:** `agent/spec_schema.py` (`_NEVADA_FF_NOTES`, `_notes_for`),
  `agent/immersion.py`, `agent/prompts.py`, `agent/session.py`,
  `agent/planner.py`.

## Syria invent is free_flight only; schema notes must not concatenate (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Invent allow-table: TheChannel all six; Normandy free_flight +
  CAP; Caucasus **free_flight only**; Syria **free_flight only** (CAP refused
  every turn — never capture or write). Schema `theatre=Syria` + free_flight
  loads `incirlik_cold_freeflight.yaml`; combat types raise with no
  Manston/NeedsOarPoint/Batumi skeleton. `_notes_for("Syria")` returns
  dedicated `_SYRIA_FF_NOTES` only — do **not** concatenate `_COMMON_NOTES` /
  `_TYPE_NOTES` (F2 Bugbot: those cite Manston YAML, Spitfire failures,
  `channel_place`). `infer_theatre` accepts JSON `Syria` or airfield
  `Incirlik`. Host repair of `domain_unsupported_theatre` /
  `intercept_unsupported_theatre` MUST use the inferred theatre — do not
  hardcode Caucasus or Normandy or a Syria CAP repair becomes Batumi or
  NeedsOarPoint. Stub LLM stays Manston. `list_strike_targets(theatre="Syria")`
  is empty. Hermetic inventory: Syria AVAILABLE + `planner_supported=True`;
  retarget `test_unsupported_installed_map` onto Nevada.
  Soft immersion floor (`host_immersion_repair_nudge`) is **TheChannel-only** —
  do not cite `manston_*.yaml` behaviour examples on Syria/Caucasus.
- **Code:** `agent/spec_schema.py` (`_SYRIA_FF_NOTES`, `_notes_for`),
  `agent/immersion.py`, `agent/prompts.py`, `agent/session.py`,
  `agent/planner.py`.

## Caucasus schema notes must not concatenate Channel bundles (2026-08-15)

- **Date:** 2026-08-15
- **Symptom:** `theatre=Caucasus` schema/repair notes prepended a Batumi line
  then still appended `_COMMON_NOTES` + `_TYPE_NOTES`, so the model was told
  examples are Channel templates, cited `manston_*.yaml`, Spitfire failure
  shelves, and `channel_place`.
- **Cause:** `_notes_for` treated theatre extras as a prefix, not a replacement.
- **Fix:** Caucasus free_flight uses a dedicated `_CAUCASUS_FF_NOTES` tuple.
  Do not concatenate Channel/Normandy note bundles onto Stage A theatres.
- **Code:** `agent/spec_schema.py` (`_CAUCASUS_FF_NOTES`, `_notes_for`).

## Caucasus invent is free_flight only (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Invent allow-table is theatre-keyed: TheChannel all six; Normandy
  free_flight + CAP; else (Caucasus Stage A) **free_flight only** — CAP is
  refused every turn (never capture or write). Schema `theatre=Caucasus` +
  free_flight loads `batumi_cold_freeflight.yaml`; combat types raise with no
  Manston/NeedsOarPoint skeleton. `infer_theatre` accepts JSON `Caucasus` or
  airfield `Batumi`. Host repair of `domain_unsupported_theatre` /
  `intercept_unsupported_theatre` MUST use the inferred theatre — do not
  hardcode `theatre="Normandy"` or a Caucasus CAP repair becomes NeedsOarPoint
  CAP. Session/planner/accept user strings must say Batumi FF, not NeedsOarPoint
  CAP. Stub LLM stays Manston. `list_strike_targets(theatre="Caucasus")` is
  empty. Date realism no-ops when `era != wwii` (2024 Batumi is silent).
- **Code:** `agent/immersion.py` (`host_theatre_mission_refuse_nudge`;
  `host_normandy_combat_nudge` is an alias), `agent/spec_schema.py`,
  `agent/prompts.py`, `agent/session.py`, `agent/planner.py`.

## Normandy invent is free_flight or CAP (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Normandy invent/chat may emit **free_flight or CAP** at
  NeedsOarPoint (CAP station 180°/63 km from `cherbourg_channel_cap`, not
  Manston 135/25). Intercept / ground_attack / escort / recon still refuse
  **every turn** (never capture or write). `list_mission_options(theatre=)`
  filters `channel_place` by `meta.theatre` so Channel invent cannot copy
  Cherbourg geometry. Schema `theatre=Normandy` + `cap` loads
  `needs_oar_point_cap.yaml`. Host repair (`host_spec_repair_nudge`) MUST
  infer theatre from rejected JSON and pass it to `build_spec_schema` —
  omitting theatre injects the Manston CAP example (135°/25 km) onto a
  Normandy CAP parse/validation failure. The one-shot planner validation
  repair MUST pass `theatre=spec.theatre` (and the Spec JSON) into that
  nudge — `mission_type` alone is not enough.
- **Code:** `agent/immersion.py`, `agent/spec_schema.py`, `agent/prompts.py`,
  `tools/surface.py`, `data/shared/planning_options.yaml`.

## Invent offerable theatres; Normandy free_flight only (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Invent/chat may set Spec theatre from offerable theatres (not
  TheChannel-only). Normandy invent is **free_flight only** (NeedsOarPoint,
  SpitfireLFMkIX, `sunny_clear`, UK blue). Combat types refuse with a repair
  toward NeedsOarPoint or TheChannel. Host chat/planner MUST refuse every turn
  (never a one-shot `_used` flag that then captures `proposed_spec` or writes YAML;
  `/accept` must refuse a slipped combat draft). `get_mission_spec_schema` accepts optional
  `theatre=`; Normandy+combat must not return a Manston skeleton. Path clamp and
  harbour immersion skip unless `spec.theatre == TheChannel`. Keep family
  `channel_place` with `meta.theatre: TheChannel` (no Normandy place rows). Strike
  catalog schema v6: `era_id=wwii`, keep `theatre_id=TheChannel`;
  `list_strike_targets(theatre="Normandy")` is empty. WWII date realism follows
  theatre→era from `theatre.yaml`, not `if theatre != TheChannel: skip`.
- **Code:** `agent/prompts.py`, `agent/spec_schema.py`, `agent/path_clamp.py`,
  `catalog/store.py` (schema 6), `catalog/sync.py`, `tools/surface.py`,
  `agent/realism.py`, `data/shared/planning_options.yaml`.

## Theatre expand: Normandy first; Marianas WWII needs PyDCS (R11) (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** Multi-theatre promote order from install+PyDCS audit: **Normandy**
  next (PyDCS `Normandy`, 38 AF, WWII Units on disk). Syria is PyDCS-ready but
  modern shelves. `MarianaIslandsWWII` / Kola / Iraq may be on disk yet **lack**
  PyDCS 0.15 terrain modules — don’t Spec-bind until upstream or R8 bump.
  Inventory cache can lag new terrain folders — `--refresh` before product work.
  Notes: gitignored `research/theatres/`.
- **Code / notes:** `theatre_terrain.py` (Channel-only bind); harness
  `research/audit_theatres_r11.py`.

## Spitfire campaign unit inventory (R13) (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** Mine Channel Spitfire campaign `.miz` with zip + regex on
  `["type"]` (PyDCS `Mission.load_file` may KeyError on `zones`). Filter
  waypoint/action strings (`Turning Point`, TakeOff*, …). Helos: **none** in
  Beware/FoD/Epsom/Big Show. Promote from frequency shortlist via `#8e` only —
  never auto-YAML. Notes: gitignored `research/campaign-units.md`.
- **Code / notes:** `research/audit_campaign_units_r13.py` (local).

## Train corridor is curated path deltas, not rail-mesh snap (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** `#8m` ships `trains` class + `french_coast_rail_corridor` place with
  elongated `path_point_deltas` near the Dunkirk inland band. Invent must copy
  that recipe only — never free-form rail routes. Compiler still places vehicles
  on ordinary waypoints; there is **no** DCS rail-mesh snap. ME Instant Action
  may show trains off the visible track; that is expected for v1.
- **Code / notes:** `planning_options.yaml` (`trains`, `french_coast_rail_corridor`);
  `examples/manston_ground_attack_train.yaml`.

## Promote theatres/targets via checklist, not ME dump (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** Grow theatres and strike/recon shelves only via curated YAML +
  OpenSpec batches. Follow [`docs/THEATRE_TARGET_PROMOTE.md`](../THEATRE_TARGET_PROMOTE.md)
  (`#8e`). Catalog/`list_strike_targets` is not a full ME unit list; never
  auto-promote install discovery into known sources.
- **Code / notes:** checklist SoT; skill `dcs-dev-agent-tooling` Hard rule 3.

## Invent place recipes fix most domain misses; path points still drift (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** `#8f` ships Manston-relative `channel_place` recipes
  (`french_coast_strike_belt` ~125°/76 km, `mid_channel_shipping` ~140°/40 km,
  `coastal_harbour` ~120°/68 km — **not** 70 km: 120/70 classifies as land).
  `#8g` invent/chat clamps land paths that fail domain **or** diverge from strike
  (near-Manston path + inland strike was validating). Live invent suite 6/6 after
  those fixes. CLI validate does not auto-clamp.
- **Code / notes:** `planning_options.yaml` place meta; `agent/path_clamp.py`;
  `out/target_invent_eval/`.

## Strike unit catalog is curated YAML, not ME dump (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** `#8c` syncs `catalog_strike_units` from packaged `ground_units.yaml` +
  `ships.yaml` only (class tags inverted from `strike_target_class` meta). ME shows
  far more land/sea types; there is no epoch auto-filter or install scrape. Grow the
  shelf by promoting verified PyDCS ids into YAML, then `catalog sync`. Invent uses
  `list_strike_targets` (SQLite) — compile/validate stay registry SoT.
- **Code:** `catalog/sync.py`, `tools/surface.list_strike_targets`, schema v5.

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

## Campaign Doc PDF excerpts are cached (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Opt-in `include_doc_text` on `list_installed_campaigns` extracts short
  Doc PDF text via `pypdf`, capped (size/pages/chars). Cache in inventory SQLite
  (`campaign_doc_cache`) by absolute path + mtime_ns + size so unchanged campaign Docs
  are not re-parsed. Default remains filenames-only for fast listing.
- **Code:** `install/doc_extract.py`, `tools/surface.py`.

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
  `data/era/` + `data/shared/` + `data/theatres/<SpecId>/` + Spec enums remain the product SoT; `dcs-miz catalog sync` replaces
  `catalog_*` from that package. Theatre **offerable** = known ∧ available ∧
  planner_supported. Never auto-promote discovered install theatres into known YAML.
- **Code:** `catalog/`; CLI `dcs-miz catalog sync|list`.
