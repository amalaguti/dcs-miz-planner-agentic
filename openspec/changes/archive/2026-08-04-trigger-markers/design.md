## Context

After `#27`, Specs can detect partial group damage and already place airfield-relative
zones. Strike / FAC-style Channel missions still cannot put an F10 map mark or colored
smoke pillar on a zone. Stock IA uses those constantly. PyDCS 0.15.0 already exposes
`MarkToAll` (`a_mark_to_all`) and `ExplodeWPMarker` (`a_explosion_marker`, ME Smoke
Marker). Spec vocabulary and validation are the gap.

## Goals / Non-Goals

**Goals:**

- Spec actions `mark` and `smoke` that reference an existing Spec zone by name.
- Validate zone refs + smoke color enum; emit MarkToAll / ExplodeWPMarker.
- Example (prefer ground-attack over strike zone) + tests; ME shows the actions.

**Non-Goals:**

- Altitude/speed gates; flares; MarkToCoalition/Group; remove-mark; big fire smoke
  (`a_effect_smoke`); unit-attached markers.
- Narrative pack rewiring; Lua / Mist / MOOSE.

## Decisions

1. **Two actions, zone-by-name:** `mark` and `smoke` both take `zone` (Spec zone `name`),
   same reference style as `coalition_in_zone`. Alternative rejected: raw map x/y or free
   ME zone ids (LLM-unsafe / non-portable).

2. **`mark` → MarkToAll:** Fields: `zone`, non-empty `text`. Optional `readonly` (default
   true). Compiler assigns a unique integer mark `value` (id) per `mark` action in Spec
   order (starting at 1) so authors never invent mark ids. Comment left empty. Emit with
   `mission.string(text)` like messages.

3. **`smoke` → ExplodeWPMarker (Smoke Marker):** Fields: `zone`, `color` enum
   `green|red|white|orange|blue` mapped to ME color ints 0–4. Optional `altitude_m`
   (default 1, ME meters ASL for the marker). Prefer ExplodeWPMarker over `Smoke`
   (`a_effect_smoke`) because FAC/target marking wants the colored pillar, not big
   fire/smoke effects.

4. **Zone resolve at emit:** `MarkToAll` needs zone **id** (int from `zone_ids`).
   `ExplodeWPMarker` takes zone as ME expects (zone **name** string per PyDCS). Both
   resolve through the Spec zone list already emitted earlier in `apply_zones_and_triggers`.

5. **Example:** Ground-attack Spec with a zone over the strike/target area; `time_more`
   (or similar) → `smoke` + `mark` + `message` so ME acceptance is obvious without flying
   a full strike.

6. **Narrative packs unchanged:** Vocabulary allows the new types; packs do not auto-emit
   mark/smoke in this change.

## Risks / Trade-offs

- [Risk] Authors confuse Smoke Marker vs big smoke effect → Mitigation: Spec type is
  `smoke` with curated colors; docs/notes say ME Smoke Marker / colored pillar.
- [Risk] Mark id collisions if later remove-mark is added → Mitigation: compiler-owned
  sequential ids; document; remove-mark deferred.
- [Risk] ExplodeWPMarker zone name vs id mismatch in some DCS builds → Mitigation:
  golden asserts predicate presence; ME acceptance confirms; fix emit if needed.

## Migration Plan

- Additive Spec types. Rollback: ignore `mark` / `smoke` actions.

## Open Questions

- None blocking. Follow-ups: altitude/speed gates, flares, MarkToCoalition, narrative
  “mark target” radio recipes.
