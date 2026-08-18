# Channel / WWII identity strings

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Falklands intercept 150/40 South Atlantic; store Mount Pleasant offset literals (2026-08-18)

- **Date:** 2026-08-18
- **Lesson:** Falklands intercept reuses the packaged CAP station: Mount
  Pleasant (id 2, x=73318.320312, y=47168.748047) + live PyDCS
  `point_from_heading(150, 40000)` offset **−34641.016151377546,
  +20000.0** (station x=38677.30416062245 y=67168.748047). **150° is not
  axis-aligned** — do not store ±40000,0 (that is Incirlik 180/40 or Batumi
  270/40). Do not copy Nellis 350/40, Incirlik 180/40, Batumi 270/40,
  Cherbourg 180/63, or Hawkinge onto Mount Pleasant. Do not recompute
  Channel Hawkinge from `airport_list()` (golden `x=30989.935547` stays
  bit-identical). Player UK + Su-25T blue at 251.0 MHz; enemies country
  **Argentina** + Su-25T red. Do not put UK on red. Chile is deferred.
  Domain stays fail-closed (`channel_domain.py` untouched). Places:
  `mount_pleasant_home` and `mount_pleasant_south_atlantic_cap` now include
  `intercept` (keep advisory `domain: sea`). Do not dump all 27 Falklands
  fields or invent ids 4 or 28.
- **Code:** `intercept_spawn.py` (`FALKLANDS_THEATRE` literals),
  `examples/mount_pleasant_dawn_intercept.yaml`.

## Falklands CAP 150/40 South Atlantic; Argentina opposition (2026-08-18)

- **Date:** 2026-08-18
- **Lesson:** Mount Pleasant CAP station is **150° / 40 km / 4000 m** from
  Mount Pleasant (id 2, x=73318.320312, y=47168.748047) SSE into the South
  Atlantic. Live PyDCS `point_from_heading` → x=38677.3 y=67168.7, nearest
  Mount Pleasant 40.00 km (Gull Point 47.12, Port Stanley 56.99). **Do not
  copy** Nellis 350/40, Incirlik 180/40, Batumi 270/40, Cherbourg 180/63,
  Manston 135/25. 090/40 is nearer Port Stanley; 180/40 is nearer Gull
  Point; 270/40 is nearer Goose Green; 350/40 is nearer San Carlos. Player
  UK + Su-25T blue at 251.0 MHz; enemies country **Argentina** + Su-25T red
  (MUST set `enemies[].country: Argentina`; default is ThirdReich). Do not
  put UK on red. Chile is deferred. Port Stanley is not a CAP home. Domain
  and intercept spawn stay fail-closed this slice. Places:
  `mount_pleasant_home` (FF+CAP) and `mount_pleasant_south_atlantic_cap`
  (CAP only, advisory `domain: sea`). Family stays `channel_place`. Do not
  dump all 27 Falklands fields or invent ids 4 or 28.
- **Code:** `examples/mount_pleasant_south_atlantic_cap.yaml`,
  `planning_options.yaml` (`mount_pleasant_home`,
  `mount_pleasant_south_atlantic_cap`).

## Falklands eight airfields; Argentina modern; RioGallegos 5 (2026-08-18)

- **Date:** 2026-08-18
- **Lesson:** Falklands Stage B curates **eight** airfields from
  `Falklands.airport_list()` (27 fields — do not dump; ids **4 and 28 are
  absent**, do not invent them): `MountPleasant` 2 (PyDCS name
  `Mount Pleasant`, class `Mount_Pleasant`; invent home), `PortStanley` 1
  (`Port Stanley` / `Port_Stanley`; lookup-only heli — do not compile
  Su-25T there), `SanCarlosFOB` 3 (`San Carlos FOB` / `San_Carlos_FOB`),
  `RioGallegos` 5 (`Rio Gallegos` / `Rio_Gallegos`), `RioGrande` 6
  (`Rio Grande`), `Ushuaia` 7, `PuntaArenas` 9 (`Punta Arenas`),
  `SanJulian` 11 (`San Julian`). Spec keys are camelCase **without
  underscores**: `RioGallegos` ≠ `Rio_Gallegos` (registry must reject the
  underscore form — same pitfall as `GroomLake` ≠ `Groom_Lake` and
  `MountPleasant` ≠ `Mount_Pleasant`). Infer keeps the `Mount_Pleasant`
  alias only; `Rio_Gallegos` / `Port_Stanley` infer None.
  **RioGallegos 5 ≠ Manston 5**; **MountPleasant 2 ≠ GroomLake 2 ≠
  MervilleCalonne 2** — lookup is theatre-scoped. Country **`Argentina`**
  is modern-only (PyDCS `countries.Argentina` id 83; red default — extra-AF
  smoke uses coalition red). Channel+Argentina is unknown. Chile is
  deferred. Extra-AF smoke is Argentina red at Rio Gallegos; invent/schema
  home stays MountPleasant + UK + Su-25T 251.0 MHz, free_flight only.
- **Code:** `data/theatres/Falklands/airfields.yaml`,
  `data/era/modern/countries.yaml`, `examples/rio_gallegos_cold_freeflight.yaml`.

## Nevada recon AOI 303/85; Ural-375 observe (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Nevada recon AOI is **303° / 85 km / 2000 m** from Nellis
  (airdromeId 4) — same desert land station as GA, not CAP/escort 350/40
  (x=-358803.06487951166 y=-24179.163922677217), not Aleppo 121/200, not
  Manston 125/76. PyDCS Nellis (4) → Creech (1) is 302.86° / 69.47 km;
  integer 303/70 is near-field reject. 303/85 ACCEPT station
  **x=-351901.05702 y=-88520.23509**. Observe-only contacts are modern trucks
  (`Ural-375` count 3) with country **Russia** red (not USA-on-red, not
  country Syria, not ThirdReich). Player Su-25T, USA blue, 251.0 MHz. Date
  2024-06-06, 09:00 (`start_time` 32400), `sunny_clear`. Weapons hold; no
  payload. Reuse place `creech_range_strike`; extend `nellis_home` with
  `recon`. Do not put recon on `nellis_north_range_cap`. Compiler recon is
  already airfield-relative.
- **Code:** `examples/nellis_creech_recon.yaml`,
  `planning_options.yaml` (`creech_range_strike` `mission_types` includes
  `recon`).

## Nevada GA 303/85 Creech; desert-default land (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Nellis → Creech PyDCS heading is **302.86° / 69.47 km**. Integer
  303° / 70 km is ~0.56 km from Creech (near-airport land — reject). Packaged
  strike is **303° / 85 km / 2000 m** (~15.53 km past Creech, nearest Creech,
  land). Station **x=-351901.05702 y=-88520.23509**. Do not copy CAP 350/40
  (x=-358803.06487951166 y=-24179.163922677217) onto trucks. Domain is
  desert-default land on curated ids `{4, 2, 1, 18, 15, 8, 6, 13}` only —
  near AF 3 km → land; else land. Do not promote Echo Bay id 7. Do not run
  Channel/Normandy/Caucasus/Syria chords on Nevada x,y. Player USA + Su-25T
  blue; targets country **Russia** red (`GroundTarget` defaults to ThirdReich).
  Not USA-on-red. Not country Syria. Payload `su25t_2x_fab250`. Place
  `creech_range_strike` (GA only). Extend `nellis_home` with `ground_attack`.
  Do not add GA to `nellis_north_range_cap`.
- **Code:** `channel_domain.py` (`classify_nevada_domain`),
  `examples/nellis_creech_ground_attack.yaml`,
  `planning_options.yaml` (`creech_range_strike`).

## Nevada escort 350/40 north-range; package USA, bounce Russia (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Nevada escort reuses the packaged CAP/intercept station: Nellis
  (id 4, x=-398195.375, y=-17233.236816) + 350° / 40 km / 4000 m
  (station x=-358803.06487951166 y=-24179.163922677217). Compiler escort is
  already airfield-relative — do not store raw map x/y in the Spec. **Do not
  copy** Channel escort 120/55, Incirlik 180/40, Batumi 270/40, or Cherbourg
  180/63. Player + package: USA + Su-25T blue at 251.0 MHz (`PackageFlight`
  defaults to UK — MUST set `package[].country: USA`). Bounce: country
  **Russia** + Su-25T red (`EnemyFlight` defaults to ThirdReich). Do not put
  USA on red. `usaaf` is voice only. Domain stays fail-closed
  (`channel_domain.py` untouched). Places: `nellis_home` and
  `nellis_north_range_cap` now include `escort`. Do not dump all 17 Nevada
  fields or invent id 12. Do not start Nevada GA this slice.
- **Code:** `examples/nellis_north_range_escort.yaml`,
  `planning_options.yaml` (`nellis_home`, `nellis_north_range_cap`).

## Nevada intercept 350/40 north-range; store Nellis offset literals (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Nevada intercept reuses the packaged CAP station: Nellis
  (id 4, x=-398195.375, y=-17233.236816) + live PyDCS
  `point_from_heading(350, 40000)` offset **+39392.31012048834,
  −6945.927106677216** (station x=-358803.06487951166
  y=-24179.163922677217). **350° is not axis-aligned** — do not store
  ±40000,0 (that is Incirlik 180/40 or Batumi 270/40). Do not recompute
  Channel Hawkinge from `airport_list()` (golden `x=30989.935547` stays
  bit-identical). Player USA + Su-25T blue at 251.0 MHz; enemies country
  **Russia** + Su-25T red. Do not put USA on red. Do not use country Syria
  on Nevada. `usaaf` is voice only. Domain stays fail-closed
  (`channel_domain.py` untouched). Places: `nellis_home` and
  `nellis_north_range_cap` now include `intercept`. Do not dump all 17
  Nevada fields or invent id 12.
- **Code:** `intercept_spawn.py` (`NEVADA_THEATRE` literals),
  `examples/nellis_dawn_intercept.yaml`.

## Nevada CAP 350/40 desert north-range; country Russia opposition (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Nellis CAP station is **350° / 40 km / 4000 m** from Nellis
  (id 4, x=-398195.375, y=-17233.236816) north-by-west into Desert NWR /
  north range. Live PyDCS `point_from_heading` → x=-358803.06488
  y=-24179.16392, nearest Nellis 40 km (land). **Do not copy** Incirlik
  180/40, Batumi 270/40, Cherbourg 180/63, Manston 135/25, Creech 303/40.
  180/40 is nearer Henderson Executive (13.74 km from that station);
  270/40 is nearer North Las Vegas (25.65 km); 79/40 is Echo Bay water.
  Player USA + Su-25T blue at 251.0 MHz; enemies country **Russia** +
  Su-25T red (MUST set `enemies[].country: Russia`; default is ThirdReich).
  Do not put USA on red. Do not use country Syria on Nevada. `usaaf` is
  voice only. Domain and intercept spawn stay fail-closed this slice.
  Places: `nellis_home` (FF+CAP) and `nellis_north_range_cap` (CAP only,
  domain land). Family stays `channel_place`. Do not dump all 17 Nevada
  fields or invent id 12.
- **Code:** `examples/nellis_north_range_cap.yaml`,
  `planning_options.yaml` (`nellis_home`, `nellis_north_range_cap`).

## Nevada eight airfields; GroomLake 2 vs MountPleasant (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Nevada Stage B curates **eight** airfields from
  `Nevada.airport_list()` (17 fields — do not dump; id **12 is absent**, do
  not invent it): `Nellis` 4, `GroomLake` 2 (PyDCS name `Groom Lake`, class
  `Groom_Lake`), `Creech` 1, `TonopahTestRange` 18 (`Tonopah Test Range`),
  `NorthLasVegas` 15 (`North Las Vegas`), `HendersonExecutive` 8
  (`Henderson Executive`), `BoulderCity` 6 (`Boulder City`), `Mesquite` 13.
  Spec keys are camelCase **without underscores**: `GroomLake` ≠
  `Groom_Lake` (registry must reject the underscore form — same pitfall as
  `FordAF` ≠ `Ford_AF` and `MountPleasant` ≠ `Mount_Pleasant`).
  **GroomLake 2 ≠ MountPleasant 2 ≠ MervilleCalonne 2**; **Nellis 4 ≠
  Maupertus 4 ≠ Dunkirk 4** — lookup is theatre-scoped. Extra-AF smoke is
  USA blue at Groom Lake; invent/schema home stays Nellis + USA + Su-25T
  251.0 MHz, free_flight only. `usaaf` is voice only.
- **Code:** `data/theatres/Nevada/airfields.yaml`,
  `examples/groom_lake_cold_freeflight.yaml`.

## Syria recon AOI 121/200; Ural-375 observe (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Syria recon AOI is **121° / 200 km / 2000 m** from Incirlik
  (airdromeId 16) — same Levant land station as GA, not CAP/escort 180/40
  (sea), not Kutaisi 43/110, not Manston 125/76. PyDCS Incirlik (16) → Aleppo
  (27) is 121.13° / 185.00 km; integer 121/185 is near-field reject. Observe-only
  contacts are modern trucks (`Ural-375`) with country **Syria** red (not
  Russia, not ThirdReich). Player Su-25T, Turkey blue, 251.0 MHz. Date
  2024-06-06, 09:00 (`start_time` 32400), `sunny_clear`. Weapons hold; no
  payload. Do not put recon on `incirlik_iskenderun_cap`. Compiler recon is
  already airfield-relative.
- **Code:** `examples/incirlik_aleppo_recon.yaml`,
  `planning_options.yaml` (`aleppo_inland_strike` `mission_types` includes
  `recon`).

## Syria GA 121/200 Aleppo; Incirlik seaward 165–195 (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Incirlik → Aleppo PyDCS heading is **121.13° / 185.00 km**. Integer
  121° / 185 km is ~0.41 km from Aleppo (near-airport land — reject). Packaged
  strike is **121° / 200 km / 2000 m** (~15.01 km past Aleppo, nearest Aleppo,
  land). Do not copy CAP 180/40 (sea) onto trucks. Domain is per-coastal seaward
  windows, not a chord and not Caucasus 270±45: Incirlik (id 16) seaward
  **165–195°**; Bassel (21) / Beirut (6) **225–315° those two fields only**.
  180/40 from Incirlik is sea; 270/40 from Incirlik is land (nearer Adana
  Şakirpaşa id 2 — do not promote id 2). Player Turkey + Su-25T blue; targets
  country **Syria** red (`GroundTarget` defaults to ThirdReich). Payload
  `su25t_2x_fab250`. Do not dump 59 airfields.
- **Code:** `channel_domain.py` (`classify_syria_domain`),
  `examples/incirlik_aleppo_ground_attack.yaml`,
  `planning_options.yaml` (`aleppo_inland_strike`).

## Syria escort 180/40; Turkey package / Syria bounce (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Syria escort package destination is **180° / 40 km / 4000 m** from
  Incirlik (airdromeId 16) — same Gulf of Iskenderun station as CAP/intercept, not
  Manston 120/55, not Cherbourg 180/63, not Batumi 270/40. Spec uses
  bearing/distance only; compiler escort is already airfield-relative
  (`airport.position.point_from_heading`). Do **not** copy intercept spawn
  literals into the Spec, and do **not** edit `intercept_spawn.py` for escort.
  Player, package, and bounce are **Su-25T** at 251.0 MHz. Package country
  **Turkey** blue (`PackageFlight` defaults to UK). Bounce country **Syria** red
  (`EnemyFlight` defaults to ThirdReich). Theatre id `Syria` ≠ country `Syria`.
  MosquitoFBMkVI / Bf-109K-4 / ThirdReich must not appear. Date 2024-06-06,
  09:00 (`start_time` 32400), `sunny_clear` (not intercept dawn 06:00). GA/recon
  still refuse.
- **Code:** `examples/incirlik_iskenderun_escort.yaml`,
  `planning_options.yaml` (`incirlik_iskenderun_cap` `mission_types` includes
  `escort`; keep CAP example path).

## Syria intercept spawn: Incirlik + Iskenderun 180/40 (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Syria intercept enemies spawn at Incirlik (id 16)
  `x=221207.773438`, `y=-35240.347656` plus PyDCS
  `point_from_heading(180, 40000)` → `181207.773438`, `-35240.347656`.
  Store those literals. Channel Hawkinge/Dover goldens stay
  `30989.935547`, `-35402.577148`. Same 180/40 station as CAP; not
  Cherbourg 180/63, not Batumi 270/40. Country **Syria** on enemies.
  Dawn example uses 06:00 (`start_time` 21600).
- **Code:** `intercept_spawn.py`, `examples/incirlik_dawn_intercept.yaml`.

## Syria CAP 180/40 Iskenderun; country Syria opposition (2026-08-17)

- **Date:** 2026-08-17
- **Lesson:** Incirlik CAP station is **180° / 40 km / 4000 m** from
  Incirlik (id 16, x=221207.773438, y=-35240.347656) due south into the
  Gulf of Iskenderun. Live PyDCS: 180/40 stays nearest Incirlik; **270/40
  west is nearer Adana Şakirpaşa (id 2, uncurated, land)** — do not copy
  Batumi 270/40. Same bearing as Cherbourg but **40 km not 63**. Player
  Turkey + Su-25T blue at 251.0 MHz; enemies country **Syria** + Su-25T
  red. Theatre id `Syria` ≠ country `Syria`. Domain and intercept spawn
  stay fail-closed this slice.
- **Code:** `examples/incirlik_iskenderun_cap.yaml`,
  `planning_options.yaml` (`incirlik_iskenderun_cap`).

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
