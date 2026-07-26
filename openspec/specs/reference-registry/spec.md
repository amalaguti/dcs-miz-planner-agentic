# Reference Registry

## Purpose

Queryable Channel Map reference data (airfields, aircraft, weather presets, radio
defaults, optional payload CLSIDs) with a stable Python lookup API. Exact DCS
identifiers only — YAML tables under `data/channel/` are the source of truth.

## Requirements

### Requirement: Channel reference registry data
The system SHALL provide committed Channel reference data covering airfields (display name → `airdromeId`), aircraft type ids with default radio frequency (MHz), supported theatre id `TheChannel`, and named weather presets used by the Mission Spec. Data MUST use verified DCS identifiers only.

#### Scenario: Manston is registered
- **WHEN** the Channel registry is queried for airfield `Manston`
- **THEN** it MUST return `airdromeId` 5

#### Scenario: Spitfire radio default
- **WHEN** the Channel registry is queried for aircraft `SpitfireLFMkIX`
- **THEN** it MUST expose the default group radio frequency 124.0 MHz (Allied VHF, matching stock Channel missions)

### Requirement: Registry lookup API
The system SHALL expose a Python lookup API over the Channel registry for airfield id resolution, aircraft/radio lookup, theatre membership, and weather preset existence so the compiler and later tools share one source of truth.

#### Scenario: Unknown airfield fails clearly
- **WHEN** a caller requests an airfield name not present in the Channel registry
- **THEN** the API MUST raise an error that identifies the unknown name and lists known airfields (or equivalent clear diagnostics)

#### Scenario: Supported theatre
- **WHEN** a caller checks theatre `TheChannel`
- **THEN** the registry MUST treat it as supported

### Requirement: No invented DCS identifiers
The Channel registry SHALL NOT invent alternate spellings for theatres, aircraft, or airfields. Only verified ids already established for this project (and documented expansions via explicit data updates) MAY appear.

#### Scenario: Known WWII aircraft set
- **WHEN** the registry lists aircraft
- **THEN** it MUST include at least `SpitfireLFMkIX`, `Bf-109K-4`, `FW-190A8`, and `FW-190D9` with exact DCS type strings
