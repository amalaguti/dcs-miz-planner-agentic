# Channel / WWII identity strings

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Syria eight airfields; country Syria modern; Palmyra 28 (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Syria Stage B curates **eight** airfields from
  `Syria.airport_list()` (59 fields — do not dump): `Incirlik` 16,
  `RamatDavid` 30 (`Ramat David`), `Damascus` 7, `BeirutRaficHariri` 6
  (`Beirut-Rafic Hariri`), `Aleppo` 27, `BasselAlAssad` 21 (`Bassel Al-Assad`),
  `Palmyra` 28, `KingHusseinAirCollege` 19. **Palmyra 28 ≠ Mozdok 28 ≠
  NeedsOarPoint 28** — lookup is theatre-scoped. Country **`Syria`** is
  modern-only (PyDCS red default — do not place Syria on blue). Theatre id
  `Syria` ≠ country `Syria`. Invent home stays Incirlik + Turkey + Su-25T
  251.0 MHz, free_flight only. Channel+country-Syria is unknown.
- **Code:** `data/theatres/Syria/airfields.yaml`,
  `data/era/modern/countries.yaml`, `examples/palmyra_cold_freeflight.yaml`.

## Caucasus recon AOI 43/110; Ural-375 observe (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Caucasus recon AOI is **43° / 110 km / 2000 m** from Batumi
  (airdromeId 22) — same Colchis land station as GA, not CAP/escort 270/40
  (sea), not Manston 125/76, not Maupertus 180/133. Observe-only contacts are
  modern trucks (`Ural-375`) with country **Russia** red. Player Su-25T,
  Georgia blue, 251.0 MHz. Date 2024-06-06, 09:00 (`start_time` 32400),
  `sunny_clear`. Weapons hold; no payload. Do not put recon on
  `batumi_black_sea_cap`. Compiler recon is already airfield-relative.
- **Code:** `examples/batumi_kutaisi_recon.yaml`,
  `planning_options.yaml` (`kutaisi_inland_strike` `mission_types` includes
  `recon`).

## Caucasus escort 270/40; Georgia package / Russia bounce (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Caucasus escort package destination is **270° / 40 km / 4000 m**
  from Batumi (airdromeId 22) — same Black Sea station as CAP/intercept, not
  Manston 120/55, not Cherbourg 180/63, not Kutaisi inland 43/110. Spec uses
  bearing/distance only; compiler escort is already airfield-relative
  (`airport.position.point_from_heading`). Do **not** copy intercept spawn
  literals (`-355810.6875`, `577386.1875`) into the Spec, and do **not** edit
  `intercept_spawn.py` for escort. Player, package, and bounce are **Su-25T**
  at 251.0 MHz. Package country **Georgia** blue (`PackageFlight` defaults to
  UK). Bounce country **Russia** red (`EnemyFlight` defaults to ThirdReich).
  MosquitoFBMkVI / Bf-109K-4 / ThirdReich must not appear. Date 2024-06-06,
  09:00 (`start_time` 32400), `sunny_clear` (not intercept dawn 06:00).
  Recon still refuses.
- **Code:** `examples/batumi_black_sea_escort.yaml`,
  `planning_options.yaml` (`batumi_black_sea_cap` `mission_types` includes
  `escort`; keep CAP example path).

## Caucasus intercept spawn: Batumi + Black Sea 270/40 (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Caucasus intercept enemy spawn is Batumi map position
  (`-355810.6875`, `617386.1875`, airdromeId 22) plus due-west 40 km
  (`point_from_heading(270, 40000)` → offset `(0, -40000)`). Enemy
  `-355810.6875`, `577386.1875` — same station as `batumi_black_sea_cap`
  (sea). Store literals in `intercept_spawn.py`; do **not** copy Hawkinge /
  Dover (`30989.935547`, `-35402.577148`) or Cherbourg `(-63000, 0)`, and do
  **not** recompute Channel goldens from `airport_list()`. Enemies are
  **Russia + Su-25T** (explicit country — default is ThirdReich). Syria /
  Nevada / Falklands still fail `intercept_unsupported_theatre`.
- **Code:** `intercept_spawn.py` (`CAUCASUS_THEATRE` recipe),
  `examples/batumi_dawn_intercept.yaml`,
  `planning_options.yaml` (`batumi_black_sea_cap` `mission_types: [cap, intercept]`).

## Caucasus inland GA 43/110; west-of-coast domain (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Caucasus land strike from Batumi is **43° / 110 km / 2000 m**
  (~12.8 km past Kutaisi). Live `heading_between_point` Batumi (22) → Kutaisi
  (25) is 43.14° / 97.20 km; 43°/100 km is near-field — reject. Do **not** copy
  CAP 270/40 (sea), Manston 125/76, or Cherbourg 180/63. Domain is **not** a
  Batumi–Kutaisi chord (that's Colchis land). Coastal ids 22/24/18; inland
  23/25/29/31/28. Near-AF 3 km → land; nearest inland → land; nearest coastal
  and heading 270°±45° → sea; else land. CAP 270/40 must classify sea. Modern
  trucks `Ural-375` / `GAZ-66` / `ZIL-135` (pydcs `vehicle_map`); country
  **Russia** red. Do not append Ural ids onto Channel `soft_vehicles`. Su-25T
  FAB-250 CLSID `{3C612111-C7AD-476E-8A8E-2485812F4E5C}` on inner pylons **5
  and 7** (dumped from `Su_25T.PylonN`; do not invent stations). Mozdok 28 is
  still not NeedsOarPoint 28.
- **Code:** `channel_domain.py` (`classify_caucasus_domain`),
  `data/era/modern/ground_units.yaml`, `data/era/modern/payloads.yaml`,
  `examples/batumi_kutaisi_ground_attack.yaml`.

## Spitfire is dual-era; DCS map capability wins (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** If DCS can spawn the module on the map, the planner MUST allow
  the Spec. `SpitfireLFMkIX` / `SpitfireLFMkIXCW` are dual-era: same 124.0
  `AircraftRef` in `era/wwii` and `era/modern` (collision guard requires
  identical refs). Modern theatres accept Spitfire; **Su-25T stays
  modern-only** (Channel still rejects Frogfoot). Invent default on Caucasus
  remains Su-25T Georgia; users may emit UK+Spitfire at Batumi.
- **Code:** `data/era/modern/aircraft.yaml`,
  `examples/batumi_spitfire_freeflight.yaml`.

## Caucasus eight airfields; Russia modern; Mozdok 28 (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Caucasus Stage B curates **eight** Spec keys from live
  `Caucasus.airport_list()` (21 fields — do not dump): `Batumi` 22,
  `Kobuleti` 24, `SenakiKolkhi` 23 (PyDCS `Senaki-Kolkhi` / `Senaki_Kolkhi`),
  `Kutaisi` 25, `TbilisiLochini` 29 (`Tbilisi-Lochini`), `Vaziani` 31,
  `SochiAdler` 18 (`Sochi-Adler`), `Mozdok` 28. Lookup is theatre-scoped:
  Mozdok 28 is **not** Normandy NeedsOarPoint 28. Add **`Russia`** only to
  `era/modern` (PyDCS class `Russia` id 0; Mission defaults Russia to **red**
  — compile `_ensure_country` will refuse Russia-on-blue). Invent/schema stay
  Batumi Georgia blue, free_flight only. Player aircraft stays **Su-25T** at
  **251.0 MHz**. Do not add paid FC3 jets. Channel+Russia is unknown-country.
- **Code:** `data/theatres/Caucasus/airfields.yaml`,
  `data/era/modern/countries.yaml`, `examples/mozdok_cold_freeflight.yaml`.

## Normandy intercept spawn: NeedsOarPoint + Cherbourg 180/63 (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Normandy intercept enemy spawn is Needs Oar Point map position
  (`141296.390625`, `-84372.234375`, airdromeId 28) plus due-south 63 km
  (`point_from_heading(180, 63000)` → offset `(-63000, 0)`). Enemy
  `78296.390625`, `-84372.234375` — same station as `cherbourg_channel_cap`
  (sea). Store literals in `intercept_spawn.py`; do **not** copy Hawkinge /
  Dover (`30989.935547`, `-35402.577148`) and do **not** recompute Channel
  goldens from `airport_list()`. Caucasus/Syria/Nevada/Falklands still fail
  `intercept_unsupported_theatre`.
- **Code:** `intercept_spawn.py` (`NORMANDY_THEATRE` recipe),
  `examples/needs_oar_point_dawn_intercept.yaml`,
  `planning_options.yaml` (`cherbourg_channel_cap` `mission_types: [cap, intercept]`).

## Normandy domain chord; Maupertus inland 180/133 (2026-08-16)

- **Date:** 2026-08-16
- **Lesson:** Land/sea on Normandy uses a **UK–Cotentin** airport chord
  (NeedsOarPoint 28, Chailey 27, Funtington 29, Tangmere 30, FordAF 31 vs
  Maupertus 4, SaintPierreduMont 1, Carpiquet 19) — never Channel UK/FR ids.
  PyDCS `heading_between_point` NeedsOarPoint → Maupertus is **180.22° /
  125.29 km**. Integer 180° / 125 km is on the field; **180° / 120 km is
  still sea**; **180° / 133 km** is ~8 km inland (land), analogous to
  Channel 125/76 inland of Dunkirk. CAP 180/63 remains sea. Do not copy
  Manston 125/76 onto Needs Oar Point.
- **Code:** `channel_domain.py` (`classify_normandy_domain`),
  `examples/needs_oar_point_ground_attack.yaml`,
  `planning_options.yaml` (`maupertus_inland_strike`).

## Falklands MountPleasant key; UK dual-era (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Spec theatre `Falklands` (product name South Atlantic; era
  `modern`) curates **MountPleasant** = airdromeId **2** (PyDCS name
  `Mount Pleasant`; class `Mount_Pleasant`; 37 parking slots; do not dump
  all 27 Falklands fields). Spec key is **`MountPleasant`**, not
  `Mount_Pleasant` — same pitfall as Normandy `FordAF` ≠ `Ford_AF`. Host
  country is **UK** (blue). UK is dual-era: keep it in `era/wwii` and add
  it to `data/era/modern/countries.yaml` next to Georgia, Turkey, and USA
  so Falklands can use UK+Su-25T without putting Frogfoot on Channel.
  Reuse **Su-25T** at **251.0 MHz** (modern UHF default — not Mount
  Pleasant ATC 133.35 / 250.8). Do **not** add Spitfire to modern.
  `usaaf` is voice only, not a country. `Germany` is still not a known id
  in any era. Validate with `era_for_theatre(spec.theatre)`: Channel+UK
  still ok (wwii); Falklands+Spitfire is unknown; Channel+Su-25T is still
  unknown. Because countries are era-keyed, UK is now valid on every
  modern theatre (Caucasus/Syria/Nevada/Falklands).
- **Code:** `data/era/modern/countries.yaml`, `data/theatres/Falklands/`,
  `theatre_terrain.py` (`_falklands_terrain` → `Falklands()`).

## Nevada Nellis smoke; USA not usaaf (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Spec theatre `Nevada` (era `modern`) curates **Nellis** =
  airdromeId **4** (PyDCS name `Nellis`; 247 parking slots; do not dump all
  17 Nevada fields). Host country is **USA** (blue) — not `usaaf` (voice
  only), not Georgia, not Turkey. F2 rejected USA at Batumi because Batumi
  is a Georgia host; Nellis is a US host so USA is correct. Reuse **Su-25T**
  at **251.0 MHz** (modern UHF default — not Nellis ATC 132.55 / 327.0).
  Add USA only to `data/era/modern/countries.yaml` next to Georgia and
  Turkey; do **not** put USA in `era/wwii`. `Germany` is still not a known
  id in any era. Validate with `era_for_theatre(spec.theatre)`:
  Channel+USA or Channel+Su-25T is unknown; Nevada+UK or Nevada+Spitfire is
  unknown; Caucasus+Georgia and Syria+Turkey stay ok.
- **Code:** `data/era/modern/countries.yaml`, `data/theatres/Nevada/`,
  `theatre_terrain.py` (`_nevada_terrain` → `Nevada()`).

## Syria Incirlik smoke; Turkey not USAF (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Spec theatre `Syria` (era `modern`) curates **Incirlik** =
  airdromeId **16** (PyDCS name `Incirlik`; do not dump all 59 Syria fields).
  Host country is **Turkey** (blue) — not USA / `usaaf`, not Georgia, not
  Syria-on-red. Reuse **Su-25T** at **251.0 MHz** (modern UHF default — not
  Incirlik ATC 122.1 / 360.1). Add Turkey only to `data/era/modern/countries.yaml`
  next to Georgia; do **not** put Turkey in `era/wwii`. `Germany` is still not
  a known id in any era. Validate with `era_for_theatre(spec.theatre)`:
  Channel+Turkey or Channel+Su-25T is unknown; Syria+UK or Syria+Spitfire is
  unknown; Caucasus+Georgia stays ok.
- **Code:** `data/era/modern/countries.yaml`, `data/theatres/Syria/`,
  `theatre_terrain.py` (`_syria_terrain` → `Syria()`).

## Modern era + Caucasus Batumi smoke (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Era `modern` is a packaged shelf (`data/era/modern/`) walked by the
  registry for **countries + aircraft only**. WWII payloads / ground / ships /
  failures stay on `era/wwii/` this slice. **Georgia** is the Batumi host
  country (`dcs.countries.Georgia`) — not USAF / `usaaf`. **Su-25T** group radio
  is **251.0 MHz** (PyDCS/DCS modern UHF default) — not Spitfire VHF 124 and not
  Batumi ATC. Airfield **Batumi** = airdromeId **22** (PyDCS name `Batumi`; do
  not dump all 21 Caucasus fields). `Germany` is still not a known id in any era.
  Validate with `era_for_theatre(spec.theatre)`: Channel+Georgia or Channel+Su-25T
  is unknown; Caucasus+UK or Caucasus+Spitfire is unknown. Catalog listing may
  union eras; `list_countries(era="wwii")` stays UK / ThirdReich. Install harvest
  must map `Su-25T` → `CoreMods/aircraft/Su-25T` in `_AIRCRAFT_FOLDERS` or the
  catalog join emits a second discovered-only row with `known=False`.
- **Code:** `data/era/modern/`, `data/theatres/Caucasus/`, `registry.py`,
  `allowlists.py`, `validation.py`, `install/aircraft_modules.py`.

## Curated Normandy airfields; FordAF is not Ford_AF (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Packaged Normandy airfields are eight curated keys from
  `Normandy.airport_list()`, not all 38 fields. Spec key **`FordAF`** = 31
  (PyDCS name **`Ford_AF`** — do not use the underscore in Spec YAML).
  `Maupertus` = 4 on Normandy is **not** Channel Abbeville (also id 4 on
  TheChannel). Lookup stays theatre-scoped. Keys: NeedsOarPoint 28, Chailey 27,
  Funtington 29, Tangmere 30, FordAF 31, Maupertus 4, SaintPierreduMont 1
  (PyDCS “Saint Pierre du Mont”), Carpiquet 19.
- **Code:** `data/theatres/Normandy/airfields.yaml`, `registry.airdrome_id`.

## Theatre-keyed intercept and domain (fail closed off TheChannel)

- **Date:** 2026-08-15
- **Lesson:** Land/sea domain classification is the Channel UK–FR airport chord only.
  Non-Channel Specs with strike/recon/path geometry fail
  `domain_unsupported_theatre` — do not run the chord on Normandy (x,y). Intercept
  enemy spawn is a recipe table with **only** TheChannel Hawkinge
  `26989.935547` / `-29402.577148` plus Dover `+4000` / `-6000` (golden
  `30989.935547` / `-35402.577148`). Do **not** recompute from `airport_list()`.
  Other theatres fail `intercept_unsupported_theatre`. Join-up outbound 120° stays
  generic airfield-relative. WWII countries live in `data/era/wwii/countries.yaml`
  (`UK`, `ThirdReich`); Germany is a hint, not a known id. `airfield_relative_map_point`
  must pass `theatre=spec.theatre` into `airdrome_id`.
- **Code:** `channel_domain.py`, `intercept_spawn.py`, `allowlists.py`,
  `data/era/wwii/countries.yaml`, `validation.py`, `compiler/pydcs_compiler.py`.

## Theatre-scoped airfield lookup (replaces `airfield_theatres`)

- **Date:** 2026-08-15
- **Lesson:** Packaged SoT is `data/era/wwii/` + `data/shared/` +
  `data/theatres/<SpecId>/` (folder name **is** the Spec/PyDCS id:
  `TheChannel`, `Normandy`). `theatre.yaml` `id:` MUST match the folder;
  the loader fails closed if not. Airfield → `airdromeId` is
  **per-theatre** (`airdrome_id(name, theatre=)`). Validate/compile/reference
  MUST pass `spec.theatre`. Unscoped unique-name lookup remains for tests.
  Do not keep a combined `data/channel/` tree or a flat `airfield_theatres:`
  map. Channel curated keys are the 12 verified names (no airdromeIds 9 or 11).
  Normandy smoke is `NeedsOarPoint` = 28 only. Shared `weather_presets.yaml`
  covers `sunny_clear` for both maps (no Normandy weather file this slice).
- **Code:** `registry.py` (`from_packaged_packages`, `_airfields_by_theatre`),
  `data/theatres/TheChannel/`, `data/theatres/Normandy/`, `validation.py`,
  `compiler/pydcs_compiler.py`, `reference.py`.

## Normandy 2.0 Spec id is `Normandy`; tag AFs with `airfield_theatres`

- **Date:** 2026-08-09
- **Lesson:** Product name “Normandy 2.0” maps to inventory/Spec/PyDCS theatre id
  **`Normandy`** (not a separate `Normandy2` id). Smoke airfield Spec key
  **`NeedsOarPoint`** → airdromeId **28** (PyDCS name “Needs Oar Point”).
  *(Superseded for packaging: Slice 0 `theatre-registry-packages` replaced the
  combined `data/channel/` + `airfield_theatres:` map with per-theatre packages
  and `airdrome_id(name, theatre=)`. See the 2026-08-15 entry.)*
- **Code:** `data/theatres/Normandy/airfields.yaml`, `registry.airfield_theatre`,
  `catalog/sync.py`; example `examples/needs_oar_point_cold_freeflight.yaml`.

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

## Spitfire / WWII: group frequency must be in VHF band

- **Date:** 2026-07-26
- **Symptom:** Compiled Manston free-flight `.miz` opens in the Mission Editor, but launching the flight warns the radio frequency is invalid for the Spitfire. PyDCS defaults every group to `["frequency"]=251`.
- **Cause:** 251 MHz is a modern UHF value. WWII radios cannot tune it: Allied VHF is ~**100–156 MHz**, German VHF ~**38.4–42.4 MHz**.
- **Fix:** Set the group frequency from the Channel registry radio table (Spitfire **124**, Bf-109K-4 40, FW-190 38.4) — the values every stock ED Channel mission uses. Assigning `group.frequency` is enough; DCS tunes the aircraft's first radio channel from it, and stock missions leave `radioSet = false`.
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py`; data in `data/era/wwii/aircraft.yaml` via `registry.py`.
- **Do not:** use the airfield ATC frequency as the flight frequency. It is in-band and works (Channel ATC VHF-high runs 118.05–118.6, Manston = 118.45), but it is the tower channel, not the flight's, and diverges from every stock mission.
- **Note:** PyDCS `set_frequency()` also flips `radio_set` and writes channel presets — more than ME does. Plain attribute assignment matches stock output.

## DCS identity strings: never invent

- **Date:** 2026-07-24 (research) / reinforced in M1
- **Symptom:** Mission fails to load or units missing if type / airfield ids are wrong.
- **Cause:** Guessing spellings (`Spitfire IX`, wrong `airdromeId`, etc.).
- **Fix:** Use verified ids only (`SpitfireLFMkIX`, Manston → `airdromeId` 5, theatre `TheChannel`, …). Prefer `registry.py` / packaged `data/era/`, `data/shared/`, `data/theatres/<SpecId>/` over memory. Expand the registry via data PRs, not ad-hoc in prompts.
