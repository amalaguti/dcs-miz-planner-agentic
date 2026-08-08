## ADDED Requirements

### Requirement: Channel place geometry recipes
Packaged `channel_place` planning options for French-coast inland and mid-Channel
shipping SHALL expose numeric Manston-relative geometry recipes (bearing and
distance) suitable for strike/AOI invent, derived from accepted Channel examples.
Land inland recipes MUST use distances that place targets on Axis-held land (not
Channel water). Mid-Channel recipes MUST place AOI/strike over water.

#### Scenario: French coast place has inland recipe
- **WHEN** catalog sync loads `channel_place` french_coast_strike_belt (or
  equivalent inland place)
- **THEN** meta MUST include strike-bearing and strike-distance values consistent
  with accepted inland GA examples (approximately 125° / 76 km from Manston)

#### Scenario: Mid-Channel place has water recipe
- **WHEN** catalog sync loads mid_channel_shipping
- **THEN** meta MUST include bearing/distance suitable for mid-Channel water
  (approximately 140° / 40 km from Manston)
