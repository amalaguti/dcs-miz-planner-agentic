## Context

`#20` defined typed Spec triggers. PyDCS exposes `mission.triggers.add_triggerzone`,
`mission.triggerrules.triggers` (`TriggerOnce`/`TriggerContinious`), and
`dcs.condition` / `dcs.action` predicates matching the v1 vocabulary.

## Goals / Non-Goals

**Goals:** Spec zones/triggers → native `.miz` trig/zones; empty graphs unchanged;
deterministic flag id mapping; structural tests + in-game sample accept.

**Non-Goals:** New Spec types; Lua snippets; OR conditions; cockpit/radio menus.

## Decisions

1. **Emit after groups exist** — resolve `unit_dead` to enemy `group.id`; zones from
   player airport `point_from_heading` (same as CAP).
2. **Flag strings → ints** — first-seen order starting at 1 within the Spec.
3. **Messages** — `mission.string(text)` + `MessageToAll(..., seconds=duration or 10)`.
4. **mission_end** — `win` → player coalition id string; `lose` → opposing.
5. **once=false** → `TriggerContinious`; default `TriggerOnce`.
6. **Remove `_refuse_uncompiled_triggers`.**

## Risks / Trade-offs

- [GroupDead vs per-unit] → whole enemy flight group (matches Spec `enemies[]`).
- [Flag collisions with ME defaults] → start at 1; document; raise if needed later.
- [Golden noise] → empty-trigger goldens unchanged; sample uses contract asserts.

## Migration Plan

- Additive compile path; sample YAML already checked in.

## Open Questions

- Whether continuous triggers need extra ME event wiring (start with NoEvent + conditions).
