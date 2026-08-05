## Context

A1 sticky empty-triggers reminder; A3 half-recipe infer; A4 bare schema examples; live eval
bare free_flight. `#32` validates late-act graphs.

## Goals / Non-Goals

**Goals:** Align reminder, schema notes, infer, and prompts so assertive immersion is consistent.

**Non-Goals:** Hard emission enforcement; PDF extract; tool sandbox.

## Decisions

1. Reminder: `triggers` list required but **may contain** immersion rules; only free_flight
   without behaviours needs empty triggers — say “use [] when unused; non-empty OK for behaviours”.
2. Schema: keep base example files; add notes listing immersion YAML paths per type.
3. Infer: `radio_late_activation` only if any late_act **and** any `activate_group` action.
4. Prompts: strengthen vague-ask 1–2 behaviours; “never use randomize_mission to invent mission
   content — only to reroll an accepted Spec”.

## Risks

- [Models still emit bare Specs] → Soft prompts only; re-run eval skill later.
- [Infer under-tags] → Prefer under-tag over false prefer.

## Open Questions

None blocking.
