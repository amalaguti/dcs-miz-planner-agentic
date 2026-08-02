# Plan REPL

## Purpose

Multi-turn interactive CLI chat for planning Mission Specs from scratch, with
host slash commands and an explicit accept gate before Spec YAML is written.

## Requirements

### Requirement: Interactive plan chat CLI
The system SHALL provide a CLI command that starts a multi-turn interactive planning
session on stdin/stdout (plain terminal REPL). The session MUST support squadron voice
resolution (CLI override → prefs → default) consistent with one-shot planning. One-shot
`plan` MUST remain available and unchanged in behaviour for existing callers.

#### Scenario: Start chat session
- **WHEN** a user runs the documented chat/REPL command (with or without `--stub`)
- **THEN** the process MUST enter an interactive loop that accepts user lines until the
  user exits, without requiring a GUI

#### Scenario: One-shot plan still works
- **WHEN** a user runs the existing one-shot `plan` command with a prompt
- **THEN** behaviour MUST remain a single-pass plan to Spec (subject to existing
  nl-agent requirements)

### Requirement: Multi-turn conversation with tools
During a chat session the system SHALL maintain conversation message history across
turns and MUST allow the same agent tools used by one-shot planning (catalog, prefs,
validate, research, etc.) via the tool bridge. Assistant replies MUST be printed for the
user after each completed turn (after any tool round-trips).

#### Scenario: Follow-up turn sees prior context
- **WHEN** the user sends a second natural-language message in the same session after an
  assistant reply
- **THEN** the LLM request MUST include prior session messages (and tool results already
  in history) so the model can refine the plan

#### Scenario: Tool call during chat
- **WHEN** the model requests `find_airfield` (or another registered tool) mid-session
- **THEN** the host MUST dispatch the tool and continue the turn until a final assistant
  text reply is available

### Requirement: Explicit Spec accept before write
A chat session MUST NOT write Mission Spec YAML to disk solely because the model emitted
JSON in a reply. The user MUST explicitly accept (documented slash command and/or an
equally explicit host confirmation flow) before the host validates, writes Spec YAML,
records generation history, and attaches a commander brief.

#### Scenario: Model proposes Spec without accept
- **WHEN** the assistant includes a Mission Spec JSON object in a chat reply and the user
  does not accept
- **THEN** the host MUST NOT write the Spec output file from that reply alone

#### Scenario: Accept writes validated Spec
- **WHEN** the user explicitly accepts a proposed Spec that passes validation
- **THEN** the host MUST write Spec YAML to the session output path, record generation
  history, and surface a commander brief (voice-aware)

#### Scenario: Accept with validation failure
- **WHEN** the user accepts a Spec that fails validation
- **THEN** the host MUST NOT treat the write as success, MUST report validation errors,
  and MUST leave the session open for repair

### Requirement: Host slash commands
The chat REPL SHALL interpret lines beginning with `/` as host commands (not LLM
prompts). At minimum the session MUST support help, quit/exit, showing the current draft
or status, accept, **briefing**, **research**, and **catalog** (and SHOULD support
compile-after-accept, voice override, and prefs display as designed).

#### Scenario: Quit ends session
- **WHEN** the user enters `/quit` or `/exit` (or equivalent documented exit command)
- **THEN** the interactive loop MUST end without requiring further LLM calls

#### Scenario: Help lists commands
- **WHEN** the user enters `/help`
- **THEN** the host MUST print a short list of available slash commands including
  `/briefing`, `/research`, and `/catalog`

### Requirement: Briefing slash command
The chat REPL SHALL support `/briefing`, which prints a commander-voice operational brief
(Situation / Tactics / Procedures / Watch-outs) for the current draft Mission Spec using
the same host brief builder as successful plan accept. If no draft Spec exists, the host
MUST explain that and MUST NOT invent Spec fields.

#### Scenario: Briefing with draft Spec
- **WHEN** the session has a draft Spec and the user enters `/briefing`
- **THEN** the host MUST print a non-empty brief with identifiable section markers in the
  active squadron voice register

#### Scenario: Briefing without draft
- **WHEN** the session has no draft Spec and the user enters `/briefing`
- **THEN** the host MUST report that no mission is drafted yet and MUST NOT write Spec files

### Requirement: Research slash command
The chat REPL SHALL support `/research` with an optional free-text query. The host MUST
invoke the existing research guidance capability (offline fixtures and optional live web)
and print notes. When a query is omitted, the host SHOULD derive a default query from the
draft Spec (mission type / theatre / aircraft) when available. Research notes MUST NOT be
treated as Spec or DCS-id authority. Notes SHOULD be added to session context for later turns.

#### Scenario: Research with explicit query
- **WHEN** the user enters `/research Channel Spitfire dawn patrol weather`
- **THEN** the host MUST return research notes (at least fixture-backed offline) without
  requiring the user to phrase a normal chat turn

#### Scenario: Research does not write Spec
- **WHEN** the user runs `/research`
- **THEN** the host MUST NOT write or accept a Mission Spec solely from that command

### Requirement: Catalog slash command
The chat REPL SHALL support `/catalog`, which prints a human-readable summary of the local
agent catalog relevant to planning (at least offerable/known theatres, known aircraft, and
planning options with support levels) using catalog/list APIs — without calling the LLM.

#### Scenario: Catalog prints without LLM
- **WHEN** the user enters `/catalog` in a stub or live chat session
- **THEN** the host MUST print catalog summary content including at least one known
  aircraft or planning option id, without requiring an LLM completion for that command

### Requirement: Offline stub multi-turn path
The system SHALL provide a stub/scripted LLM (or equivalent) so pytest can exercise a
multi-turn chat session without a live API key, including at least one tool use or
clarifying exchange and an accept that writes a valid Spec.

#### Scenario: Stub chat accept in tests
- **WHEN** a test drives a stub chat session through user turns and `/accept`
- **THEN** a validated Mission Spec YAML MUST be written and the test MUST pass without
  `OPENAI_API_KEY`
