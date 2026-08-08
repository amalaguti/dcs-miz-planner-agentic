## Context

Follow [`docs/THEATRE_TARGET_PROMOTE.md`](../../../docs/THEATRE_TARGET_PROMOTE.md)
section B. PyDCS ids verified: `Sd_Kfz_251`, `Sd_Kfz_7`, `M2A1_halftrack` in
`vehicle_map`. Motion profile `halftrack` already exists; unit maps were
commented stubs after `#8h`.

## Goals / Non-Goals

**Goals:** Promote halftracks_apc class + three verified ids; motion wiring;
invent cues; example + hermetic tests.

**Non-goals:** New AI Opt* / presets; armor/troops; ME scrape.

## Decisions

1. **Class row** — New `strike_target_class` `halftracks_apc` (not fold into
   soft_vehicles). Prefer path + `convoy_transit` (soft AI class already covers
   non-AAA land units).

2. **Ids** — Axis `Sd_Kfz_251`, `Sd_Kfz_7`; Allied practice `M2A1_halftrack`
   (label notes UK-side / practice, same pattern as Willys/Bedford).

3. **Motion** — Map all three to existing `halftrack` profile (15–40 km/h).

4. **Place / invent** — Add `halftracks_apc` to french_coast `related_classes`;
   cue line: halftrack/SPW/APC → halftracks_apc + path + convoy_transit.

5. **Accept** — Hermetic validate/compile + catalog; ME do-soon.

## Risks / Trade-offs

- [Era stretch Allied M2A1] → Label practice/UK-side; keep on shelf for invent
  variety.
- [Soft AI for halftracks] → Acceptable until R12b proves distinct ME options;
  no new preset this change.

## Migration Plan

- Additive YAML + one example; catalog sync; no schema bump.

## Open Questions

- None.
