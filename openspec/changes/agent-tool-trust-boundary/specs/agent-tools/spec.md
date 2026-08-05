## ADDED Requirements

### Requirement: Default agent tools are read-only
The default LLM tool list for planning and chat MUST omit mutating tools
(`compile_mission`, `set_user_prefs`, `record_generation`, `record_feedback`). Those
operations MUST remain available to host code via Python APIs or an explicit
`allow_mutating` dispatch flag for tests/admin, not via the default agent tool surface.

#### Scenario: Default tools exclude compile and prefs write
- **WHEN** the default planning tool definitions are listed
- **THEN** they MUST NOT include `compile_mission`, `set_user_prefs`, `record_generation`,
  or `record_feedback`

#### Scenario: Mutating dispatch blocked by default
- **WHEN** `dispatch_tool` is called for `compile_mission` without mutating allowed
- **THEN** it MUST return a structured error and MUST NOT write a `.miz`

### Requirement: Compile output path allowlist
When `compile_mission` runs (host or allowed dispatch), the output path MUST resolve to a
location under an allowed `out/` directory. Paths outside that tree MUST be rejected.

#### Scenario: Compile outside out rejected
- **WHEN** compile is requested with an output path outside the allowed `out/` tree
- **THEN** the call MUST fail with a clear path error and MUST NOT write the file
