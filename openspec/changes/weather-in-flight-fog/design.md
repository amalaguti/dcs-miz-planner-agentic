## Context

ED `world.weather.setFogAnimation` (2.9.10+): keys `{time_s, visibility_m,
thickness_m}`; relative to call time. PyDCS has `DoScript(mission.string(lua))`.
Training `.miz` pattern: ActionText DictKey, not zip-root `.lua`. Full `#22`
deferred — this change is a **fog-only snippet slice**.

## Goals / Non-Goals

**Goals:** Declarative fog evolution; curated Lua only; compile inject; tests.

**Non-Goals:** Cloud/rain mid-flight; general snippet library; free-form script field.

## Decisions

1. **Spec `fog_dynamics`** — optional object:
   - `mode`: `burn_off` | `roll_in`
   - `start_after_s`: seconds after mission start when animation begins (ONCE `time_more`)
   - `duration_s`: animation span to end state
   - optional `end_visibility_m` / `end_thickness_m` (defaults by mode)
2. **Templates in code** (`fog_dynamics.py`) — fill numeric params into fixed Lua;
   never accept arbitrary script strings on the Spec.
3. **Emit** — append one ONCE trigger at compile (does not require empty
   zones/triggers; does not use narrative/dynamics expand XOR).
4. **Static weather** — invent/compile still sets initial fog; burn_off expects
   initial fog present (warn or require enable_fog / fog fields); roll_in may
   start thinner and animate thicker.
5. **DoScript** via `mission.string(lua)` → `action.DoScript`.

## Risks / Trade-offs

- [Risk] Map/version fog support varies → document Channel smoke; soft-warn in brief
- [Risk] Thickness clamped to cloud base → templates use safe thickness caps
- [Risk] DoScript DictKey round-trip → follow MessageToAll string pattern; golden assert substring

## Migration Plan

- Additive optional field; omit = prior behaviour

## Open Questions

- None blocking; full `#22` later can absorb these templates
