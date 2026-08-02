## MODIFIED Requirements

### Requirement: Research slash command
The chat REPL SHALL support `/research` with an optional free-text query. The host MUST
invoke the existing research guidance capability with live retrieval preferred and print
notes. When a query is omitted, the host SHOULD derive a default query from the draft Spec
(mission type / theatre / aircraft) when available. When live research succeeds, printed
notes MUST include at least one non-fixture source. When live research is unavailable
(empty or error), the host MUST clearly label the output as offline fixture fallback (and
surface the warning) so pilots are not misled into treating fixtures as live web results.
Research notes MUST NOT be treated as Spec or DCS-id authority. Notes SHOULD be added to
session context for later turns.

#### Scenario: Research with explicit query
- **WHEN** the user enters `/research Channel Spitfire dawn patrol weather`
- **THEN** the host MUST return research notes (at least fixture-backed when live is
  unavailable) without requiring the user to phrase a normal chat turn

#### Scenario: Live-unavailable research is labelled
- **WHEN** `/research` runs with live preferred and research returns a live-unavailable
  warning with fixture notes
- **THEN** the host output MUST include that warning (or an equivalent offline-fallback
  label) and MUST NOT present the fixtures as unmarked live web success

#### Scenario: Research does not write Spec
- **WHEN** the user runs `/research`
- **THEN** the host MUST NOT write or accept a Mission Spec solely from that command
