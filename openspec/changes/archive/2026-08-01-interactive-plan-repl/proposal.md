## Why

One-shot `dcs-miz plan "…"` cannot refine a mission through dialogue. With tools, prefs,
voice, and mission types in place, planners need a CLI multi-turn chat/REPL to start from
scratch, ask questions, adjust knobs, and only then accept a Spec / compile.

## What Changes

- Add a CLI interactive session (`dcs-miz chat` or equivalent) that keeps conversation
  history, squadron voice, and the existing tool bridge across turns.
- Support building a mission from an empty start: clarify intent, propose options, revise
  draft Spec fields via talk — not only a single prompt → YAML dump.
- Explicit accept / write Spec / optional compile commands (slash or spoken confirm) so
  half-baked chat never silently overwrites a Spec.
- Host slash commands for mission **briefing** (commander voice), **research** (web/tools
  for historical / weather / outcome context), and **catalog** (show known planning catalog).
- Keep one-shot `dcs-miz plan` unchanged for scripts and CI stubs.
- Offline stub/scripted multi-turn path for pytest (no live API required).

## Non-goals

- GUI / web UI / TUI frameworks beyond plain stdin/stdout.
- Multi-user servers, session persistence across process restarts (v1 may be in-memory).
- Changing Mission Spec schema, new mission types, or `.miz` l10n briefings.
- Replacing the one-shot `plan` command.

## Capabilities

### New Capabilities

- `plan-repl`: Multi-turn CLI chat session for interactive Mission Spec planning.

### Modified Capabilities

- `nl-agent`: Clarify that one-shot `plan` remains; interactive sessions use the same
  tools/voice/validation contract via the REPL.

## Impact

- New `agent/` session/REPL module(s), CLI subcommand, prompts for conversational turns,
  tests with scripted stub turns, README + BACKLOG.
- Reuses existing LLM client, tool bridge, prefs, voice, validate/compile.
- Acceptance: interactive session produces a validated Spec YAML (and optionally a `.miz`
  openable in DCS when `--compile` / accept-compile is used).
