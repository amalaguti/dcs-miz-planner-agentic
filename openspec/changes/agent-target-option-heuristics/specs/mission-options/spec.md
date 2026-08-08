## ADDED Requirements

### Requirement: Strike class and AI preset invent heuristics
Packaged planning options for `strike_target_class` and `ground_ai_preset` SHALL
expose invent-oriented meta so agents can map pilot cues to preferred motion and
AI presets without free-form ME option names. Soft vehicles MUST prefer path (or
patrol) with `convoy_transit`; AAA MUST prefer static with `aaa_alert`; sea under
way MUST prefer patrol with `ship_under_way`; harbour/dock MUST prefer static with
`harbour_static` (or equivalent documented meta).

#### Scenario: Soft vehicles meta carries convoy heuristics
- **WHEN** catalog sync loads `strike_target_class` `soft_vehicles` and
  `ground_ai_preset` `convoy_transit`
- **THEN** soft_vehicles meta MUST include preferred_motion path (or patrol) and
  a preferred_ai_preset pointing at convoy_transit (or convoy_transit meta MUST
  document preferred_motion path/patrol)

#### Scenario: AAA meta carries alert heuristics
- **WHEN** catalog sync loads `aaa_guns` and `aaa_alert`
- **THEN** aaa_guns MUST prefer static motion and aaa_alert (via preferred_* meta)

#### Scenario: Sea under-way and harbour meta
- **WHEN** catalog sync loads `sea_craft`, `ship_under_way`, and `harbour_static`
- **THEN** under-way MUST prefer patrol (or path) + ship_under_way; harbour MUST
  prefer static + harbour_static
