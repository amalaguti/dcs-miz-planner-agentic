## Context

`#15a` recon places optional `targets` as contacts (land or sea) near an AOI via
registry `get_strike_unit` → `vehicle_group` / `ship_group`. Ground attack already places
sea-domain ships the same way. Channel registry includes `Uboat_VIIC` (`ships.yaml`,
PyDCS `ship_map`). Catalog already lists `sea_craft` with `Uboat_VIIC` and advisory
`mid_channel_shipping`. Missing pieces are **examples**, **inspiration**, and **brief
copy** that teach surfaced-only U-boat hunt (DCS bombs do not work on submerged subs).

## Goals / Non-Goals

**Goals:**

- Two flyable Manston Specs: recon (locate surfaced U-boat) + GA (bomb surfaced U-boat).
- Mid-Channel **water** geometry (strike-domain validate must pass — no land trucks at sea).
- Catalog inspiration + agent/voice language for surfaced-only hunt.
- Goldens + ME accept.

**Non-Goals:**

- New mission type; submerged ASW; single Spec find-then-kill; compiler rewrites unless a
  bug appears.

## Decisions

1. **No new `mission_type`**
   - Reuse `recon` + `ground_attack`. Alternative rejected: `asw` enum — implies
     capabilities DCS Spitfire cannot deliver.

2. **Placement: existing sea path**
   - Spec `targets: [{ unit: Uboat_VIIC, ... }]` on recon or GA with AOI/strike over
     **water**. Compiler already emits `mission.ship_group` near the point.
   - Confirmed: PyDCS `ship_map['Uboat_VIIC']` and registry domain `sea`.

3. **Geometry: mid-Channel water from Manston**
   - Prefer shorter Channel water than the Dunkirk inland GA example (125°/76 km is land).
   - Seed example: ~120–130° bearing, ~45–55 km (still water per prior Channel notes;
     validate with `strike_domain` / ME smoke). Adjust if domain validate fails.
   - Harbour-water variant optional later; v1 = mid-Channel corridor.

4. **Two Specs, not one**
   - `examples/manston_uboat_recon.yaml` — `mission_type: recon`, contacts `Uboat_VIIC`,
     empty payload, find beat.
   - `examples/manston_uboat_hunt.yaml` — `mission_type: ground_attack`, targets
     `Uboat_VIIC`, payload `spitfire_2x250_slipper` (or `spitfire_1x500` if brief prefers
     heavier), `attack_ground`.
   - Armed recon deferred (backlog non-goal).

5. **Catalog / agent**
   - New `mission_inspiration` id e.g. `uboat_surfaced_hunt` → behaviours hint recon AOI
     mark + optional GA follow-up (advisory; agent may emit two Specs over turns).
   - Extend `mid_channel_shipping` `mission_types` to include `recon`.
   - Voice: both Specs mention surfaced / crash-dive / no depth charges.

6. **Optional drama (stretch)**
   - Late-activated U-boat + F10 “report contact” only if tasks stay small; otherwise
     defer to `#25`/`#30f` reuse in a follow-up.

## Risks / Trade-offs

- [U-boat sits on land if geometry wrong] → Use mid-Channel km; run domain validate; ME
  check water.
- [Bombs ineffective if AI dives] → Brief “attack while surfaced”; accept DCS AI behaviour.
- [Agent invents ASW] → Explicit non-goals in schema notes + prompts.

## Migration Plan

- Additive examples/options only. Rollback: revert branch.

## Open Questions

- Exact mid-Channel bearing/distance for goldens (confirm at apply via domain + ME).
- Whether hunt example uses 2×250 slipper vs 1×500 — prefer slipper for Channel default.
- Agent “suggest available targets” from a full unit list is **out of this change** —
  backlog **`#8c` `agent-strike-target-catalog`** (SQLite sync offline; query at invent).
  `#15f` may only add inspiration/prompt hints; do not build the unit table here.
