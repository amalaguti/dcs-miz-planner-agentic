## Context

After `#28` (mark/smoke), Specs can place visual aids and already have rich flag / life /
radio vocabulary. Channel missions still cannot warn or fail when the player busts an
ingress height or speed gate. Stock training and strike patterns use ME unit altitude and
speed conditions constantly. PyDCS 0.15.0 already exposes `UnitAltitudeHigher` /
`UnitAltitudeLower` (MSL), `UnitAltitudeHigherAGL` / `UnitAltitudeLowerAGL`,
`UnitSpeedHigher` / `UnitSpeedLower` (m/s). Spec vocabulary, player unit wiring, and
validation are the gap.

## Goals / Non-Goals

**Goals:**

- Spec conditions for player altitude higher/lower (AGL or MSL) and speed higher/lower.
- Validate positive thresholds; emit the matching PyDCS predicates against the player unit.
- Example (prefer free-flight for easy ME/in-flight check) + tests; ME shows the conditions.

**Non-Goals:**

- Enemy/AI unit gates; vertical-speed (`UnitVerticalSpeedWithin`); Lua / Mist / MOOSE.
- Narrative pack rewiring; automatic mission_end on gate bust.
- Cockpit args (`#24`).

## Decisions

1. **Four condition types, player-only subject:**
   - `unit_altitude_higher` / `unit_altitude_lower` with `altitude_m` (> 0) and
     `agl` (bool, default `true` — ingress discipline wants AGL).
   - `unit_speed_higher` / `unit_speed_lower` with `speed_kmh` (> 0).
   Alternative rejected: raw DCS unit ids or enemy_index in this slice (LLM-unsafe /
   out of scope). Compiler always binds the condition unit to the placed player aircraft
   unit id.

2. **Units match the rest of Spec:** Altitude stays meters (`altitude_m`). Speed uses
   `speed_kmh` (same convention as compiler waypoint speeds); emit converts to m/s for
   PyDCS `UnitSpeed*` (`speed / 3.6`). Alternative rejected: Spec-side m/s (harder for
   authors and inconsistent with existing km/h cruise numbers).

3. **AGL vs MSL via boolean:** `agl: true` → `UnitAltitude*AGL`; `agl: false` →
   `UnitAltitude*` (MSL). Prefer one pair of types over four altitude type names.

4. **Player unit id plumbing:** `pydcs_compiler` already has the player flight group when
   applying triggers; pass `player_unit_id` (e.g. `group.units[0].id`) into
   `apply_zones_and_triggers` → `_map_condition`. Do not invent unit ids in the Spec.

5. **Continuous rules for warnings:** Example SHOULD set `once: false` so the gate can
   re-fire while the condition holds (ME Continuous). Authors may still use `once: true`
   with flags. No new Spec field for continuous beyond existing `once`.

6. **Example:** Free-flight Spec with a continuous `unit_altitude_higher` (AGL) →
   `message` after a short `time_more` (or AND with time so cold-start parking does not
   spam). Optional second rule for speed. Keep it flyable from Manston for acceptance.

7. **Narrative packs unchanged:** Vocabulary allows the new types; packs do not auto-emit
   altitude/speed gates in this change.

## Risks / Trade-offs

- [Risk] Cold parking AGL near 0 falsely trips “below” gates → Mitigation: example uses
  higher-than / speed gates after `time_more`, or authors AND with `coalition_in_zone` /
  flags; document in example comments.
- [Risk] Speed IAS vs TAS confusion in ME → Mitigation: Spec documents km/h as ME unit
  speed threshold (PyDCS m/s); acceptance checks predicate presence, not exact IAS.
- [Risk] Player unit id missing if flight placement changes → Mitigation: compile fails
  clearly if player unit id is absent when a gate condition is present.

## Migration Plan

- Additive Spec types. Rollback: ignore new condition types (or reject until rolled back).

## Open Questions

- None blocking. Follow-ups: enemy unit gates, vertical speed, narrative “stay low”
  recipes.
