## ADDED Requirements

### Requirement: Synthetic METAR ICAO is Channel-only
Commander/compile briefing synthetic METAR SHALL use ICAO `EGMH` only for
theatre `TheChannel`. For `Normandy`, the brief MUST NOT emit `EGMH` and MUST
NOT invent a Needs Oar Point ICAO. A SIM remark MAY still appear without a
fake station code.

#### Scenario: Channel brief still uses EGMH
- **WHEN** a TheChannel Spec briefing includes synthetic METAR
- **THEN** the METAR line MUST include `EGMH`

#### Scenario: Normandy brief omits EGMH
- **WHEN** a Normandy NeedsOarPoint Spec briefing includes weather text
- **THEN** it MUST NOT include `EGMH` or an invented ICAO
