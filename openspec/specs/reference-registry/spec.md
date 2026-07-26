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
The system SHALL expose a Python lookup API over the Channel registry for airfield id resolution,
aircraft/radio lookup, static planner theatre support, and weather preset existence so the compiler
and later tools share one source of truth. Static theatre membership MUST remain separate from the
user-local SQLite installation inventory; callers that offer mission options MUST require both
planner support and a currently available local theatre (from the cached inventory, refreshed on
demand).

#### Scenario: Unknown airfield fails clearly
- **WHEN** a caller requests an airfield name not present in the Channel registry
- **THEN** the API MUST raise an error that identifies the unknown name and lists known airfields
  (or equivalent clear diagnostics)

#### Scenario: Supported theatre
- **WHEN** a caller checks theatre `TheChannel`
- **THEN** the registry MUST treat it as supported

#### Scenario: Supported but not locally available
- **WHEN** `TheChannel` is supported by the packaged registry but the (cached or freshly
  refreshed) installation inventory does not report it as available
- **THEN** callers MUST NOT offer `TheChannel` as currently compilable for that installation

#### Scenario: Installed but unsupported
- **WHEN** the installation inventory reports a theatre that is absent from the packaged registry
- **THEN** callers MUST identify it as locally available but planner-unsupported

### Requirement: No invented DCS identifiers
The Channel registry SHALL NOT invent alternate spellings for theatres, aircraft, or airfields. Only verified ids already established for this project (and documented expansions via explicit data updates) MAY appear.

#### Scenario: Known WWII aircraft set
- **WHEN** the registry lists aircraft
- **THEN** it MUST include at least `SpitfireLFMkIX`, `Bf-109K-4`, `FW-190A8`, and `FW-190D9` with exact DCS type strings
