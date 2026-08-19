---
name: dcs-dev-channel-ids
description: >-
  Channel / WWII DCS identity strings that must never be invented. Use when
  adding aircraft, countries, airfields, radio frequencies, spawn geometry, or
  validating Spec ids against the Channel registry.
---

# Channel / WWII identity strings

## Read first

[`docs/lessons/channel-ids.md`](../../../docs/lessons/channel-ids.md)

## Hard rules

1. **Never invent** DCS type ids, country names, airfield names, CLSID, failure ids.
   Source = packaged YAML / registry / stock `.miz` research.
2. **WWII Axis country:** `ThirdReich`, not `Germany`.
3. **Spitfire group frequency** must be in **VHF** band (e.g. 124.0) — not HF defaults.
   Channel cockpit A–E bank (stock Instant Action) is **124 / 40 / 41 / 42 / 108.9**.
   Do not use PyDCS `panel_radio` defaults (105/124/131/139). Dual-era YAML must
   keep identical `radio_channels_mhz` on wwii and modern Spitfire rows.
4. Intercept spawn geometry: packaged recipes in `intercept_spawn.py`.
   TheChannel: Hawkinge + Dover-approach offset. Do not recompute from
   `airport_list()`. Normandy: NeedsOarPoint + Cherbourg corridor
   (`-63000`, `0`) — same station as `cherbourg_channel_cap` (180°/63 km).
   Caucasus: Batumi + Black Sea corridor `(0, -40000)` — same station as
   `batumi_black_sea_cap` (270°/40 km). Syria: Incirlik + Iskenderun
   corridor `(-40000, 0)` — same station as `incirlik_iskenderun_cap`
   (180°/40 km).    Nevada: Nellis + north-range offset
   `(+39392.31012048834, −6945.927106677216)` — same station as
   `nellis_north_range_cap` (350°/40 km; **not** axis-aligned ±40000,0).
   Falklands: Mount Pleasant + South Atlantic offset
   `(−34641.016151377546, +20000.0)` — same station as
   `mount_pleasant_south_atlantic_cap` (150°/40 km; **not** axis-aligned
   ±40000,0). Other theatres fail `intercept_unsupported_theatre`.
   Derive the unsupported hint from `INTERCEPT_SPAWN_RECIPES` keys.
   Derive `domain_unsupported_theatre` hints from `DOMAIN_THEATRES` (include
   Nevada and Falklands).
5. Failure ids: exact stock strings (e.g. `ENG0_MAGNETO0`) from
   `data/era/wwii/aircraft_failures.yaml`.
6. **Normandy 2.0** Spec/inventory id is **`Normandy`**. Airfield lookup is
   theatre-scoped (`airdrome_id(name, theatre=)`); folder names under
   `data/theatres/` **are** Spec ids. Curated keys: `NeedsOarPoint` = 28,
   `Chailey` = 27, `Funtington` = 29, `Tangmere` = 30, `FordAF` = 31
   (PyDCS `Ford_AF`), `Maupertus` = 4, `SaintPierreduMont` = 1, `Carpiquet` = 19.
   Do not invent ids or dump all 38 fields.
7. Domain land/sea is TheChannel UK–FR chord, Normandy UK–Cotentin chord
   (NeedsOarPoint cluster vs Maupertus / SaintPierreduMont / Carpiquet),
   Caucasus west-of-coast seaward sector (coastal 22/24/18 vs inland
   23/25/29/31/28; heading 270°±45° from nearest coastal → sea), **or**
   Syria per-coastal seaward windows (coastal 16/21/6 vs inland 27/28/7/30/19;
   Incirlik 165–195°; Bassel/Beirut 225–315° those two fields only — never
   apply 270±45 to Incirlik), **or** Nevada desert-default land on curated
   ids `{4, 2, 1, 18, 15, 8, 6, 13}` (near AF 3 km → land; else land — do
   not promote Echo Bay id 7), **or** Falklands Syria-style seaward windows
   on classifier AFs `{1,2,3,24,29}` (near AF 3 km → land; else if nearest
   in that set and heading seaward → sea; else land; do not include
   mainland 5/6/7/9/11; MPA 2: 120–180°; Stanley 1: 45–135°; San Carlos 3:
   240–330°; Goose Green 24: 250–290°; Gull Point 29: 180–240° — do not
   promote Goose Green or Gull Point as Spec keys). Other
   theatres fail `domain_unsupported_theatre`. Hints MUST list every
   `DOMAIN_THEATRES` key (including Nevada and Falklands) — do not freeze
   Channel/Normandy/Caucasus/Syria/Nevada. `airfield_relative_map_point`
   MUST pass `theatre=spec.theatre`. Normandy inland strike from NeedsOarPoint
   is **180° / 133 km** (Maupertus is 180.22° / 125.29 km; 120 km is still sea).
   Caucasus inland strike from Batumi is **43° / 110 km** (Kutaisi is 43.14° /
   97.20 km; 100 km is near-field; CAP 270/40 is sea).    Syria inland strike/recon from
   Incirlik is **121° / 200 km** (Aleppo is 121.13° / 185.00 km; 121/185 is
   near-field; CAP 180/40 is sea). Nevada inland strike/recon from Nellis is
   **303° / 85 km** (Creech is 302.86° / 69.47 km; 303/70 is near-field; CAP
   350/40 is a different land station). Falklands inland strike/recon from Mount
   Pleasant is **269° / 21 km** (Goose Green is 268.80° / 36.01 km; 269/36 is
   0.13 km from GG — REJECT; 269/51 is Sound sea — REJECT as a station even
   if the seaward-window classifier still labels it land; CAP 150/40 is a
   different sea station). Known gap: 180/40 from MPA may classify land via
   Gull Point. Do not copy Manston
   125/76 or CAP 180/63 (sea) onto Cotentin land, do not copy CAP 270/40
   onto Caucasus GA, do not copy CAP 180/40 onto Syria GA or recon, do
   not copy CAP 350/40 onto Nevada GA or recon, and do not copy CAP 150/40
   onto Falklands GA or recon.
8. Packaged WWII countries: `UK`, `ThirdReich`, and `USA`
   (`data/era/wwii/countries.yaml`). `usaaf` is voice only. `Germany` is a hint,
   not a known id in **any** era. WWII aircraft include `P-51D` (radio 124.0;
   payload `p51d_2x_anm64` `{AN-M64}` pylons 4+7). There is **no** Typhoon
   PyDCS type. Extra Channel invent homes: Hawkinge CAP 76/32 strike 104/78;
   Detling CAP 102/71 strike 110/122; BigginHill CAP 100/111 strike 106/160
   — do not copy Manston 135/25 or 125/76. Extra Normandy homes: Chailey
   CAP 228/130 inland 212/184; Tangmere CAP 215/89 inland 200/152 (max
   flight size 3); FordAF CAP 220/92 inland 203/152 — do not copy
   NeedsOarPoint 180/63 or 180/133. Artillery: `LeFH_18-40-105`, `Wespe124`,
   `M2A1-105`. Scenery: `Hangar A`, `Revetment_x4`, `Tent01`, `Belgian gate`,
   `Shelter` (exact `fortification_map` keys).
9. **Caucasus** Spec id is **`Caucasus`** (era `modern`). Curated AFs (8 of 21):
   `Batumi` = 22, `Kobuleti` = 24, `SenakiKolkhi` = 23 (PyDCS `Senaki-Kolkhi`),
   `Kutaisi` = 25, `TbilisiLochini` = 29 (`Tbilisi-Lochini`), `Vaziani` = 31,
   `SochiAdler` = 18 (`Sochi-Adler`), `Mozdok` = 28 (not NeedsOarPoint).
   Invent home: `Georgia` + `Su-25T` at **251.0 MHz** at Batumi.    Invent is
   **all six types** (CAP/intercept/escort 270° / 40 km
   west over the Black Sea — not Manston 135/25, not Cherbourg 180/63, not
   Hawkinge, not escort 120/55; GA/recon AOI 43° / 110 km inland past Kutaisi —
   not CAP 270/40).
   Modern trucks: `Ural-375`, `GAZ-66`, `ZIL-135` (not Channel `soft_vehicles`).
   Payload `su25t_2x_fab250` (FAB-250 on pylons 5 and 7). `Russia` is
   modern-only (PyDCS red default — do not place Russia on blue). Channel+Russia
   is unknown. CAP enemies: Russia + Su-25T (set `enemies[].country: Russia`;
   default is ThirdReich). **SpitfireLFMkIX is dual-era** (same 124.0 ref in wwii + modern)
   because DCS flies it on modern maps; Channel still rejects `Su-25T`. UK is
   dual-era. Catalog listing may union eras. Do not dump all 21 fields.
10. **Syria** Spec id is **`Syria`** (era `modern`). Curated AFs (8 of 59):
    `Incirlik` = 16, `RamatDavid` = 30 (`Ramat David`), `Damascus` = 7,
    `BeirutRaficHariri` = 6 (`Beirut-Rafic Hariri`), `Aleppo` = 27,
    `BasselAlAssad` = 21 (`Bassel Al-Assad`), `Palmyra` = 28 (not Mozdok,
    not NeedsOarPoint), `KingHusseinAirCollege` = 19. Do not dump 59 fields.
    Invent home: `Turkey` + `Su-25T` at **251.0 MHz** at Incirlik (all six types;
    CAP/intercept/escort 180° / 40 km south Iskenderun — not Cherbourg 180/63, not Batumi 270/40,
    not escort 120/55; GA/recon AOI 121° / 200 km inland past Aleppo — not CAP 180/40).
    Country **`Syria`** is modern-only (PyDCS red default — Palmyra smoke
    uses coalition red; GA trucks must set `targets[].country: Syria`). Theatre id `Syria` ≠ country `Syria`. Channel+country-Syria
    is unknown. Add Syria-the-country only to `era/modern` — never `era/wwii`.
    Spitfire is dual-era.
11. **Nevada** Spec id is **`Nevada`** (era `modern`). Curated AFs (8 of 17):
    `Nellis` = 4 (PyDCS name `Nellis`), `GroomLake` = 2 (`Groom Lake` / class
    `Groom_Lake` — Spec key MUST be `GroomLake`, not `Groom_Lake`; id 2 is
    not Falklands `MountPleasant` and not Channel `MervilleCalonne`),
    `Creech` = 1, `TonopahTestRange` = 18 (`Tonopah Test Range`),
    `NorthLasVegas` = 15 (`North Las Vegas`), `HendersonExecutive` = 8
    (`Henderson Executive`), `BoulderCity` = 6 (`Boulder City`),
    `Mesquite` = 13. Do not invent id 12 or dump all 17 fields. Nellis 4 is
    not Maupertus and not Dunkirk. Modern smoke: country `USA` (not `usaaf`,
    not Georgia, not Turkey), aircraft `Su-25T` at **251.0 MHz**.     Invent home
    stays Nellis (**all six types**;
    CAP/intercept/escort station **350° / 40 km / 4000 m**
    desert north-range land — not Incirlik 180/40, not Batumi 270/40, not
    Cherbourg 180/63, not Channel escort 120/55, not Manston 135/25, not Creech
    303/40, not 180/40 Henderson, not 270/40 NLV, not 79/40 Echo Bay water;
    GA/recon AOI **303° / 85 km / 2000 m** inland past Creech — not CAP 350/40,
    not 303/70 near-field).
    CAP/intercept/escort enemies: Russia + Su-25T (set `enemies[].country:
    Russia`; default is ThirdReich). Escort package country **USA** (default UK).
    GA/recon trucks country **Russia** red (default ThirdReich). Do not put USA on red.
    Add USA only
    to `era/modern` next to
    Georgia and Turkey — never `era/wwii`. `usaaf` is voice only, not a
    country. Channel+USA/Su-25T is unknown. Spitfire is dual-era. UK is
    dual-era (wwii + modern).
12. **Falklands** Spec id is **`Falklands`** (product name South Atlantic;
    era `modern`). Curated AFs (8 of 27): `MountPleasant` = 2 (PyDCS name
    `Mount Pleasant`; class `Mount_Pleasant` — Spec key MUST be
    `MountPleasant`, not `Mount_Pleasant`), `PortStanley` = 1 (`Port Stanley`
    / `Port_Stanley`; lookup-only heli), `SanCarlosFOB` = 3
    (`San Carlos FOB` / `San_Carlos_FOB`), `RioGallegos` = 5
    (`Rio Gallegos` / `Rio_Gallegos`; not Channel Manston), `RioGrande` = 6,
    `Ushuaia` = 7, `PuntaArenas` = 9 (`Punta Arenas`), `SanJulian` = 11
    (`San Julian`). Do not invent ids 4 or 28 or dump all 27 fields.
    Underscore forms (`Rio_Gallegos`, `Port_Stanley`) MUST be unknown
    (same pitfall as `GroomLake` ≠ `Groom_Lake`); infer keeps
    `Mount_Pleasant` only. Modern smoke: country `UK` (keep UK in
    `era/wwii` as well), aircraft `Su-25T` at **251.0 MHz** at MountPleasant.
    Extra-AF smoke: country **`Argentina`** modern-only (PyDCS id 83; red —
    `examples/rio_gallegos_cold_freeflight.yaml`). Channel+Argentina is
    unknown. Chile is deferred. Spitfire is dual-era (same 124.0 in wwii +
    modern). Channel+UK still ok (wwii); Channel+Su-25T is unknown.     Invent
    home stays MountPleasant UK blue, **all six types**
    (station **150° / 40 km / 4000 m** SSE over the South Atlantic — not
    Nellis 350/40, not Incirlik 180/40, not Batumi 270/40, not Cherbourg
    180/63, not Manston 135/25, not Hawkinge, not Channel escort 120/55;
    GA/recon AOI **269° / 21 km / 2000 m** inland short of Goose Green — not
    CAP 150/40, not 269/36, not 269/51, not Nevada 303/85).
    CAP/intercept/escort enemies:
    Argentina + Su-25T (set `enemies[].country: Argentina`; default is
    ThirdReich). Escort package country **UK** (default UK — still set
    explicitly). GA/recon trucks country **Argentina** red (default ThirdReich).
    Port Stanley is not a CAP home.
13. **Kola** Spec id is **`Kola`** (era `modern`). Curated AF (1 of 37):
    `Bodo` = 7 (PyDCS name `Bodo`). Do not dump all 37 fields. Modern smoke:
    country `Norway` (modern-only; PyDCS id 12), aircraft `Su-25T` at
    **251.0 MHz**. Invent is **free_flight only**. Channel+Norway is unknown.
    Unbound stand-in after this bind: Iraq (no pydcs) / GermanyCW (pydcs
    class `Germany`, name `GermanyCW`). Do not bind Iraq or GermanyCW.

## Code touchpoints

`data/era/wwii/*.yaml`, `data/era/modern/*.yaml`, `data/shared/*.yaml`, `data/theatres/<SpecId>/`,
`registry.py`, `validation.py`, `channel_domain.py`, `intercept_spawn.py`,
spawn helpers in compiler.
