## Context

After `#15g`, targets can move and moving land groups get Disperse Under Fire.
R12 ME smoke (2026-08-08) showed WP Options differ by **domain and unit class**:
soft truck ≠ Flak 18 ≠ U-boat ≠ Spitfire; ME can list useless rows (Spit ECM).
`#15h` adds a curated Spec → PyDCS Opt* / PointAction shelf for GA/recon targets
only. Notes: `research/ai-options-domain.md` (gitignored). Broader matrix = R12b.

## Goals / Non-Goals

**Goals:**

- Allowlisted optional AI + move knobs on `targets[]` (GA + recon).
- Class-aware validation (soft / AAA / sea) matching R12 ME visibility.
- Compiler emit via existing PyDCS Opt* + PointAction; no LLM Lua.
- Presets that expand to allowlisted fields; examples + ME accept.

**Non-Goals:**

- Air/helo Option shelves; R12b full unit matrix.
- Wrappers for PyDCS-missing ids 27/29/30/31 (AAA alt, formation interval, ARM)
  unless a thin tested path appears mid-apply — default defer.
- Assuming ME list = capability.

## Decisions

1. **Spec shape — flat optional fields + optional preset**
   Prefer `targets[].ai_preset` (named) and/or explicit fields under `targets[].ai`
   (`roe`, `alarm_state`, `engage_air_weapons`, `restrict_targets`,
   `interception_range_km` or bool/range as PyDCS allows) plus
   `move_formation` (`off_road`|`on_road`|`rank`|`cone`|`vee`|…) for land.
   Keep `disperse_under_fire_s` on the target (already `#15g`) rather than
   duplicating. Preset expands first; explicit fields override preset keys.
   *Alt considered:* only presets — rejected (too coarse for agent/tests).

2. **Allowlists by class (R12)**

   | Class heuristic | Allowed |
   |-----------------|---------|
   | Land soft (default land non-AAA) | roe, alarm, engage_air, restrict_targets, disperse, move_formation |
   | Land AAA (`flak*` / `Pak*` / planning aaa class) | soft set + interception_range; no soft-only bans |
   | Sea | roe, alarm, engage_air?, interception_range?; **no** disperse, restrict_targets, move_formation |

   Unknown unit → soft land or sea by registry domain; AAA ids from packaged
   class list / registry tags.

3. **Emit site**
   Extend `target_motion.py` (or sibling `target_ai.py`) called from GA/recon
   placement after group create: apply Opt* on `points[0]`; set `PointAction` on
   all motion waypoints (and static single point if move_formation set).
   Static + no ai → unchanged.

4. **ROE values**
   Ground/sea: `open_fire` | `return_fire` | `weapons_hold` only (no WeaponFree).
   Map to existing `OptROE.Values`.

5. **Alarm**
   `auto` | `green` | `red` → `OptAlarmState`.

6. **Catalog**
   Planning family e.g. `ground_ai_preset` / `target_move_formation` cards;
   schema notes document allowlists + class rules.

## Risks / Trade-offs

- [Class heuristic wrong for a unit] → Validation allowlist + R12b later; prefer
  reject over silent no-op when Spec sets forbidden key.
- [OptAlarmState on ships untested in `.miz` reload] → ME accept on U-boat;
  if emit fails, document and narrow sea set.
- [On Road ignores sparse road mesh] → Document; Off Road remains default;
  accept ME Action label even if path is imperfect.
- [Preset vs disperse interaction] → Preset may set disperse; explicit
  `disperse_under_fire_s` wins.

## Migration Plan

- Additive Spec fields; omit = today’s behaviour.
- Update convoy / add AAA / tweak U-boat examples; goldens/asserts as needed.
- Rollback: omit new fields.

## Open Questions

- Exact AAA unit id list for class (flak18/36, Pak40 vs label heuristic).
- Whether soft trucks **reject** or **ignore** interception_range if agent emits it
  (prefer **reject** for honesty).
- Include `engage_air_weapons` default true for `aaa_alert` preset?
