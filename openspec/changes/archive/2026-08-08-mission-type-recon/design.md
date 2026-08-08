## Context

M4 combat types are done through escort + player-flight polish. Backlog `#15a` is the only
remaining mission-type idea: locate/observe without strike. Ground attack already owns
airfield-relative geometry, `targets`, and registry ground/ship ids; recon must reuse that
placement math but swap tasking, payload rules, and success semantics. PyDCS exposes
`Reconnaissance` as a group task. Native zones/marks/`coalition_in_zone`/messages already
exist — no new Lua and no new trigger kinds.

## Goals / Non-Goals

**Goals:**

- Spec + validate + compile one Channel recon: cold Spit at Manston, fly to an AOI, optional
  visual contacts, observe (weapons hold), find message, RTB implied by brief — no bombs.
- Golden + example; agent/options/voice awareness; free_flight / intercept / CAP / GA /
  escort unchanged.

**Non-Goals:**

- Armed recon, payload presets, destroy/`group_life_less` wins, photo scoring.
- Air bounce enemies on recon v1; full narrative-pack parity; Mist/MOOSE / LLM Lua.
- New registry unit families (reuse strike unit SoT for contacts).
- Overloading `ground_attack` with empty payload (rejected).

## Decisions

1. **`mission_type: recon` (distinct enum)**
   - Same short style as other types.
   - Alternative rejected: GA + no payload / weapons_hold — still requires `strike` +
     `attack_ground` + GroundAttack tasking; wrong objective and brief.

2. **Nested `recon` block (required for recon; forbidden otherwise)**
   - Fields:
     - `bearing_deg` (0–360), `distance_km` (>0): AOI centre relative to player airfield
       (same CAP/strike math).
     - `altitude_m` (>0): ingress / observe altitude.
     - `radius_m` (default ~3000, bounded e.g. 500–15000): AOI trigger zone radius.
     - `mark` (bool, default true): emit F10 map mark on the AOI zone at mission start (or
       via a once trigger) using existing mark action vocabulary.
   - Do **not** reuse the `strike` key — semantics differ (observe vs attack).

3. **Optional `targets` as visual contacts**
   - Empty `targets` = area recon (empty AOI).
   - Non-empty = enemy land/sea units placed near AOI centre via existing strike-unit
     registry + opposing-coalition rules (no `strike.practice` path on recon).
   - Air `enemies` MUST be empty in v1.
   - Compiler MUST NOT attach Bombing / AttackGroup / GroundAttack tasks for contacts.

4. **No `player.payload`**
   - Omit / reject on recon (guns-only Spit default). ROE: `weapons_hold` (or return_fire
     only if we need self-defence — prefer `weapons_hold` for observe discipline).

5. **Objective `recon_area`**
   - Required in non-empty `objectives`; reject `attack_ground` / `intercept_enemy` /
     `patrol` / `escort_package` on recon unless a later change allows mixes.
   - Schema/validate marker; win messaging comes from compiler-emitted find beat.

6. **Compiler path**
   - `group.task = Reconnaissance.name`.
   - Ingress waypoint(s) to AOI; optional short Orbit or Hold over AOI (prefer simple
     waypoint + Reconnaissance task; add Orbit only if ME smoke shows AI wanders off).
   - Add Spec zone (reserved name e.g. `recon_aoi`) at AOI; optional mark text
     “Recon AOI”.
   - Place contact groups when `targets` non-empty (same placement helper as GA, no attack
     tasking).
   - Emit TriggerOnce (or Continuous once-flagged): `coalition_in_zone` for player
     coalition in `recon_aoi` → MessageToAll (“Area observed — RTB when ready”) + set a
     reserved flag (e.g. 830) for future chaining. No `mission_end` / force-land in v1.
   - If Spec already has hand-written `zones`/`triggers`, either: (a) require empty and
     inject (like narrative), or (b) inject only when empty and otherwise skip find pack
     with validate warn. Prefer **(a) require empty zones/triggers for recon v1** so the
     find beat is deterministic — same pattern as `dynamics` / narrative conflict rules.
     Document clearly; pilots who want custom triggers disable auto-find later.

7. **Example**
   - `examples/manston_recon.yaml`: Manston morning sunny; AOI inland toward Dunkirk
     (~125° / 76 km) or a shorter coastal look; 2–3× soft trucks as contacts; no payload;
     `recon_area` objective.
   - Golden asserts: Reconnaissance task, zone present, no bomb CLSIDs, contact unit type
     if present, find-message / zone comment strings.

8. **Planning / agent**
   - `mission_type` / `recon` → `supported`.
   - Schema + voice: observe discipline, jettison N/A, RTB after find message; recommend
     empty payload and optional contacts.

## Risks / Trade-offs

- [Reconnaissance AI wanders] → Prefer explicit ingress WP + OptROE hold; ME smoke; add
  Orbit if needed.
- [Zone/trigger conflict with narrative/dynamics] → Forbid non-empty zones/triggers on
  recon v1 (or conflict like narrative); expand later.
- [Contacts look like strike targets to agent] → Schema/prompt: contacts are observe-only;
  reject payload/`attack_ground`.
- [Find beat too quiet / spammy] → Single once message; reserved flag for later narrative.

## Migration Plan

- Additive enum + fields; no breaking change to existing Specs.
- Update BACKLOG `#15a` proposed → building → done on accept.
- Rollback: revert branch; no data migration.

## Open Questions

- Exact default `radius_m` and reserved find-flag id (propose 3000 m / flag 830) — confirm
  at apply if discipline/orders ranges collide (orders 800+, discipline 820+ → use **830+**).
- Whether optional Orbit over AOI is needed after first ME smoke.
