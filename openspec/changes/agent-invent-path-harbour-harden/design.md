## Context

`#8f` shipped Manston-relative place recipes and domain repair nudges. Live invent
still fails when the model invents **path points** far from strike (into Channel
water) even when strike itself is inland, and when **harbour** cues keep coastal
geometry but land soft units. Validate already samples every path point for
domain (`motion_domain_mismatch`).

## Goals / Non-Goals

**Goals:**

- Make land path invent reliably stay on land near strike.
- Make harbour invent bind to sea units + coastal place (guidance + repair).
- Narrow deterministic host path clamp when land path domain fails.
- Hermetic coverage; live convoy/harbour invent as accept.

**Non-Goals:**

- Auto-snap to roads/coast mesh; rewrite unit ids; shelf expand; ME accept.

## Decisions

1. **Path invent contract (meta + prompts)** — Treat `french_coast_strike_belt`
   `path_point_deltas` as the only invent recipe for soft land paths. Prompts/
   schema: prefer **2–3** points; each point = strike bearing/distance + delta
   (or absolute copy of accepted convoy band). Cap free invent at 3 points in
   guidance (Spec still allows up to 6).

2. **Repair nudge includes pasteable path block** — On `motion_domain_mismatch`
   for path, append concrete YAML like the convoy example (125/76, 128/77,
  122/78) and “rewrite path only; keep strike inland.”

3. **Host path clamp (narrow)** — When invent/chat validate fails with
   `motion_domain_mismatch` and a land-domain target has `motion: path`, once
   rewrite that target’s `path` from strike + place `path_point_deltas` (default
   french-coast deltas if strike looks inland). Re-validate; if green, accept
   without LLM repair. Do **not** clamp sea paths or change units/strike.

   Alternatives considered: LLM-only (failed live); full Spec rewrite (too
   broad); reject invent (worse UX).

4. **Harbour harden (guidance + repair only)** — Strengthen cue table /
   `coastal_harbour` description / schema: harbour → `list_strike_targets
   (domain=sea)` only. Repair when error text or rejected Spec shows land units
   with harbour place geometry, or when prompt cues harbour and Spec has land
   soft units (host harbour nudge similar to immersion floor). No automatic
   unit swap.

5. **Validation** — Prefer existing `motion_domain_mismatch` path labels; only
   add a dedicated path-point code if clamp/tests need it (optional).

## Risks / Trade-offs

- [Clamp hides bad invent] → Log/detail that path was clamped; still require
  strike on land.
- [Wrong place deltas if strike mid-Channel with land trucks] → Clamp only when
  unit domain is land; if strike is sea, leave to LLM repair.
- [Harbour still wrong unit] → Explicit sea-unit nudge; shelf expand later (`#8e`).

## Migration Plan

- Additive YAML notes + prompt/repair + small clamp helper on invent validate
  path; catalog sync unchanged beyond planning_options text.

## Open Questions

- None blocking — clamp triggers only on invent/chat validate failure, not on
  CLI `dcs-miz validate` of author Specs (authors may want custom paths).
