## ADDED Requirements

### Requirement: Showers scattered weather recipe and family
Packaged Channel weather YAML SHALL include `showers_scattered` with a
pilot-facing description and a gallery recipe whose default `cloud_preset` is a
light-rain ME gallery id (`RainyPreset4`, `NEWRAINPRESET4`, `RainyPreset5`, or
`RainyPreset6`). The pattern MUST declare a `gallery_family` that includes those
light-rain ids (and MUST NOT silently merge into `rain_overcast`’s
`RainyPreset1`–`3` family).

#### Scenario: Showers recipe declared
- **WHEN** the Channel registry loads weather presets after this change
- **THEN** `showers_scattered` MUST expose a non-empty gallery family containing
  at least `RainyPreset4` and MUST list a default `cloud_preset` from that family

### Requirement: Packaged gallery decode for synthetic METAR
Packaged Channel weather data SHALL provide a decode map from ME gallery
`cloud_preset` ids to METAR cloud coverage groups (and secondary layer bases)
sufficient to build offline synthetic METARs. The map MUST cover at least all
gallery ids used by packaged `gallery_family` lists, including rainy light ids.

#### Scenario: Decode covers rainy light presets
- **WHEN** the METAR decode map is loaded
- **THEN** entries for `RainyPreset4`, `RainyPreset5`, `RainyPreset6`, and
  `NEWRAINPRESET4` (if packaged in any family) MUST be present
