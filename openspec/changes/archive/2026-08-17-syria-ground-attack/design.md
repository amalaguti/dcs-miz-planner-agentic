## Context

Syria Stage C shipped Incirlik CAP/intercept/escort at **180° / 40 km** (sea,
Gulf of Iskenderun). A land strike needs Levant inland geometry measured from
PyDCS, not copied CAP 180/40, Kutaisi 43/110, or Manston 125/76. Modern trucks
and `su25t_2x_fab250` already ship from Caucasus GA — reuse them; do not invent
ids. Domain still fail-closes on Syria until this slice.

## Goals / Non-Goals

**Goals:**

- Validate + compile an Incirlik ground_attack with Syria-red land trucks inland
  past Aleppo.
- Invent/chat may emit Syria `ground_attack` every turn; recon still refuses.
- Domain classifier for Syria using curated coastal vs inland airport ids.
- Catalog offers modern **land** units on Syria via query-time dual-offer.

**Non-Goals:**

- Recon invent, new unit YAML, QAG promote, path clamp on Syria, intercept_spawn
  edits, promoting Adana Şakirpaşa id 2, Instant Action as merge gate.

## Decisions

1. **Strike geometry 121° / 200 km / 2000 m** (not 180/40, not 121/185).
   PyDCS `heading_between_point` Incirlik (16) → Aleppo (27) is **121.13° /
   185.00 km**. Integer 121° / 185 km is only ~0.41 km from Aleppo
   (near-airport land — reject). 121° / 200 km is ~15 km past Aleppo. Document
   the measurement in the example YAML comment. Do not invent lat/lon.

2. **Syria domain = per-coastal seaward sector**, not an Incirlik–Aleppo chord
   (that heading is over land) and not Caucasus 270±45 on Incirlik.
   Curated ids:
   - Coastal: Incirlik 16, Bassel Al-Assad 21, Beirut-Rafic Hariri 6.
   - Inland: Aleppo 27, Palmyra 28, Damascus 7, Ramat David 30, King Hussein 19.
   Near any curated AF (3 km) → land. Else if nearest curated is inland → land.
   Else nearest is coastal and heading from that AF is seaward → sea. Else land.
   Incirlik seaward: **165–195°** (180±15). Bassel/Beirut seaward: 225–315°
   (west Med) — those two fields only. CAP 180/40 **must** classify sea. GA
   121/200 **must** classify land. 270/40 from Incirlik **must** classify land
   (Adana pitfall). Never run Channel/Normandy/Caucasus airport ids on Syria
   x,y. Path clamp stays TheChannel-only. Do not promote id 2.

3. **Reuse `aleppo_inland_strike`.** New place; keep CAP example path on the
   sea row. Extend `incirlik_home` with `ground_attack`. Do not add GA to
   `incirlik_iskenderun_cap`. Do not invent a Palmyra strike place this slice.

4. **Modern aircraft + trucks:** player Su-25T Turkey blue, payload
   `su25t_2x_fab250`. Targets Ural-375 / GAZ-66 / ZIL-135 country **Syria** red
   (`GroundTarget.country` defaults to ThirdReich). Date 2024-06-06, 09:00,
   `sunny_clear`.

5. **Dedicated `_SYRIA_GA_NOTES`.** Do not concatenate Channel `_TYPE_NOTES`.
   Schema loads `incirlik_aleppo_ground_attack.yaml`. Stub LLM stays Manston.
   Drop `ground_attack` from `_SYRIA_UNSUPPORTED_COMBAT` (recon stays).

6. **Strike list dual-offer:** `_strike_theatre_match` theatre=Syria matches
   stored `theatre_id=Caucasus` AND `era_id=modern` AND `domain=land`. Do not
   retag stored rows. Nevada/Falklands stay empty. Channel excludes Urals.

## Risks / Trade-offs

- [CAP 180/40 classified land] → Incirlik must be coastal; seaward window 165–195
  (not 180±45, which would swallow Palmyra 137°).
- [270±45 on Incirlik] → Adana id 2 land; lock a test that 270/40 is land.
- [Omitted country defaults] → example MUST set country Syria.

## Migration Plan

Implement on `syria-ground-attack`. Rollback = revert the branch. Channel
goldens must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
