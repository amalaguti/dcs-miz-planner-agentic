## MODIFIED Requirements

### Requirement: Registry lookup API
The system SHALL expose a Python lookup API over the Channel registry for airfield id resolution,
aircraft/radio lookup, static planner theatre support, and weather preset existence so the compiler
and later tools share one source of truth. Static theatre membership MUST remain separate from the user-local SQLite installation inventory;
callers that offer mission options MUST require both planner support and a currently available
local theatre (from the cached inventory, refreshed on demand).

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
