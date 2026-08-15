## ADDED Requirements

### Requirement: Packaged registry packages
The packaged reference registry SHALL load from theatre packages under
`data/theatres/<SpecId>/` plus shared and era YAML (WWII aircraft, payloads,
failures, ground/sea units, weather presets, planning options). The loader MUST
walk packaged `theatre.yaml` files and treat each `id:` as a planner-supported
theatre. The registry MUST NOT invent DCS identifiers. The single
`data/channel/` package MUST NOT remain the source of truth.

#### Scenario: Both bound theatres load from packages
- **WHEN** the packaged registry is loaded
- **THEN** it MUST treat `TheChannel` and `Normandy` as supported theatres
  sourced from per-theatre packages (not a combined `data/channel/theatres.yaml`
  list)

#### Scenario: Shared weather still resolves
- **WHEN** the packaged registry is queried for weather preset `sunny_clear`
- **THEN** it MUST resolve that preset without a Normandy-local weather file

### Requirement: Theatre-scoped airfield lookup
Airfield → `airdromeId` lookup SHALL be scoped to a Spec theatre. Airdrome ids
MUST NOT be treated as global. When `theatre` is provided, unknown names MUST
error with that theatre’s known airfields. When `theatre` is omitted, a name
that maps uniquely MAY resolve; a name present in more than one theatre MUST
fail as ambiguous.

#### Scenario: Manston on TheChannel
- **WHEN** the registry is queried for airfield `Manston` with theatre
  `TheChannel`
- **THEN** it MUST return `airdromeId` 5

#### Scenario: Manston on Normandy fails
- **WHEN** the registry is queried for airfield `Manston` with theatre
  `Normandy`
- **THEN** it MUST raise an error that identifies the unknown name and lists
  known Normandy airfields (or equivalent clear diagnostics)

#### Scenario: NeedsOarPoint on TheChannel fails
- **WHEN** the registry is queried for airfield `NeedsOarPoint` with theatre
  `TheChannel`
- **THEN** it MUST raise an error that identifies the unknown name and lists
  known TheChannel airfields (or equivalent clear diagnostics)

#### Scenario: NeedsOarPoint on Normandy
- **WHEN** the registry is queried for airfield `NeedsOarPoint` with theatre
  `Normandy`
- **THEN** it MUST return `airdromeId` 28

## MODIFIED Requirements

### Requirement: Channel reference registry data
The system SHALL provide committed Channel reference data covering airfields
(display name → `airdromeId` for theatre `TheChannel`), aircraft type ids with
default radio frequency (MHz), supported theatre id `TheChannel`, and named
weather presets used by the Mission Spec. Data MUST use verified DCS
identifiers only. Channel airfields MUST live in the `TheChannel` theatre
package; WWII aircraft, radios, and weather presets MAY be shared era/shared
packages consumed by TheChannel.

#### Scenario: Manston is registered
- **WHEN** the Channel registry is queried for airfield `Manston`
- **THEN** it MUST return `airdromeId` 5

#### Scenario: Spitfire radio default
- **WHEN** the Channel registry is queried for aircraft `SpitfireLFMkIX`
- **THEN** it MUST expose the default group radio frequency 124.0 MHz (Allied
  VHF, matching stock Channel missions)

### Requirement: Registry lookup API
The system SHALL expose a Python lookup API over the packaged registry for
airfield id resolution, aircraft/radio lookup, static planner theatre support,
and weather preset existence so the compiler and later tools share one source
of truth. Static theatre membership MUST remain separate from the user-local
SQLite installation inventory; callers that offer mission options MUST require
both planner support and a currently available local theatre (from the cached
inventory, refreshed on demand).

#### Scenario: Unknown airfield fails clearly
- **WHEN** a caller requests an airfield name not present for the requested
  theatre (or, if unscoped, not present in the packaged registry)
- **THEN** the API MUST raise an error that identifies the unknown name and
  lists known airfields (or equivalent clear diagnostics)

#### Scenario: Supported theatre
- **WHEN** a caller checks theatre `TheChannel`
- **THEN** the registry MUST treat it as supported

#### Scenario: Supported but not locally available
- **WHEN** `TheChannel` is supported by the packaged registry but the (cached
  or freshly refreshed) installation inventory does not report it as available
- **THEN** callers MUST NOT offer `TheChannel` as currently compilable for that
  installation

#### Scenario: Installed but unsupported
- **WHEN** the installation inventory reports a theatre that is absent from the
  packaged registry
- **THEN** callers MUST identify it as locally available but
  planner-unsupported

### Requirement: Needs Oar Point airfield registered
The packaged registry SHALL map curated airfield key `NeedsOarPoint` to DCS
`airdromeId` 28 (PyDCS Normandy airport Needs Oar Point) in the `Normandy`
theatre package.

#### Scenario: NeedsOarPoint resolves
- **WHEN** the registry is queried for airfield `NeedsOarPoint`
- **THEN** it MUST return `airdromeId` 28
