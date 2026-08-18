## Context

Nevada Stage C shipped Nellis CAP/intercept/escort at **350° / 40 km** (desert
north-range **land**). A land strike must not reuse that station. Geometry is
measured from PyDCS Nellis → past Creech, not copied CAP 350/40, Aleppo 121/200,
or Manston 125/76. Modern trucks and `su25t_2x_fab250` already ship from
Caucasus/Syria GA — reuse them; do not invent ids. Domain still fail-closes on
Nevada until this slice.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Nellis ground_attack with Russia-red land trucks inland
  past Creech.
- Invent/chat may emit Nevada `ground_attack` every turn; recon still refuses.
- Domain classifier for Nevada using desert-default land on eight curated AFs.
- Catalog offers modern **land** units on Nevada via query-time dual-offer.

**Non-Goals:**

- Recon invent, new unit YAML, QAG promote, path clamp on Nevada,
  intercept_spawn edits, promoting Echo Bay id 7, Instant Action as merge gate.

## Decisions

1. **Strike geometry 303° / 85 km / 2000 m** (not 350/40, not 303/70, not
   303/40). PyDCS `heading_between_point` Nellis (4) → Creech (1) is **302.86° /
   69.47 km**. Integer 303° / 70 km is only ~0.56 km from Creech (near-airport
   land — reject). 303° / 85 km is ~15.53 km past Creech. Station
   **x=-351901.05702 y=-88520.23509**. Document the measurement in the example
   YAML comment. Do not invent lat/lon. Do not reuse CAP 350/40 for trucks.

2. **Nevada domain = desert-default land**, not a Nellis–Creech chord and not
   Channel/Normandy/Caucasus/Syria recipes. Curated ids only: Nellis 4,
   GroomLake 2, Creech 1, TonopahTestRange 18, NorthLasVegas 15,
   HendersonExecutive 8, BoulderCity 6, Mesquite 13. Spec keys **camelCase
   without underscores**. Near any curated AF (3 km) → land. Else land. Lake
   Mead / Echo Bay id 7 is a **known gap** — do not promote. CAP 350/40 **must**
   classify land. GA 303/85 **must** classify land. 79/40 **may** stay land.
   Never run other-theatre airport ids on Nevada x,y. Path clamp stays
   TheChannel-only. Falklands stays `domain_unsupported_theatre`.

3. **New place `creech_range_strike`.** Keep CAP example path on
   `nellis_north_range_cap`. Extend `nellis_home` with `ground_attack`. Do **not**
   add GA to `nellis_north_range_cap`. Place `mission_types: [ground_attack]`
   only (do not pre-add recon). Family stays `channel_place`.

4. **Modern aircraft + trucks:** player Su-25T USA blue, payload
   `su25t_2x_fab250`. Targets Ural-375 / GAZ-66 / ZIL-135 country **Russia** red
   (`GroundTarget.country` defaults to ThirdReich). Not USA-on-red. Not country
   Syria. Date 2024-06-06, 09:00, `sunny_clear`.

5. **Dedicated `_NEVADA_GA_NOTES`.** Do not concatenate Channel `_COMMON_NOTES`
   / `_TYPE_NOTES`. Schema loads `nellis_creech_ground_attack.yaml`. Stub LLM
   stays Manston. Drop `ground_attack` from `_NEVADA_UNSUPPORTED_COMBAT` (recon
   stays). Add `GROUND_ATTACK` to `_THEATRE_ALLOWED_TYPES["Nevada"]`. Lightly
   edit FF/CAP/intercept/escort notes so they no longer say refuse GA (recon
   still refused). FF/CAP/intercept/escort example **files** unchanged.

6. **Strike list dual-offer:** `_strike_theatre_match` theatre=Nevada matches
   stored `theatre_id=Caucasus` AND `era_id=modern` AND `domain=land` (same
   predicate as Syria). Do not retag stored rows. Do not invent unit YAML.
   Falklands stay empty. Channel excludes Urals. Extend `modern_soft_vehicles`
   cues for Nevada/Creech (country Russia, same as Caucasus).

7. **Repair:** `motion_domain_mismatch` / `strike_domain_mismatch` on Nevada
   MUST nudge `creech_range_strike` 303/85, not CAP 350/40, not french_coast
   125/76, not Aleppo 121/200. Split Nevada out of the `{Nevada, Falklands}`
   “domain not classified” fallback. `domain_unsupported_theatre` on Nevada
   (legacy) may still infer Nellis; Falklands stay Mount Pleasant FF.

## Risks / Trade-offs

- [303/70 classified as near-Creech] → lock 85 km; document 70 km reject in
  the example comment.
- [CAP 350/40 reused for trucks] → separate place; compile must not contain
  north-range CAP station coords.
- [Omitted country defaults to ThirdReich] → example MUST set country Russia.
- [USA-on-red or country Syria] → player USA blue; targets Russia red only.
- [Echo Bay / Lake Mead] → do not promote id 7; 79/40 may stay land.
- [Notes concat Manston] → dedicated `_NEVADA_GA_NOTES` only.

## Migration Plan

Implement on `nevada-ground-attack`. Rollback = revert the branch. Channel
goldens must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
