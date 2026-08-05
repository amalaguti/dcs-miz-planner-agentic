## Why

Agent `verbose` defaults **on**, so normal `plan` / `chat` dumps LLM rounds and tool
payloads to stderr. Adversarial review **C3** flagged screenshot/log leakage and noisy
CLI for everyday use. Flip the default off now that the product is past early debug-first
polish (`#10b`).

## What Changes

- **BREAKING (CLI UX):** Default for `--verbose` / session verbose becomes **off**. Users who
  relied on always-on traces must pass `--verbose` or `/verbose on`.
- `DEFAULT_VERBOSE` in `agent/verbose.py` → `False`.
- CLI `plan` / `chat` BooleanOptionalAction defaults and help text updated.
- Chat banner / `/verbose` help text updated (default: off).
- README and BACKLOG `#10b` status updated.

## Non-goals

- Changing what verbose logs contain when enabled
- Persisting verbose preference in SQLite prefs (still session/CLI flag only)
- Quieting non-agent CLI commands (`validate`, `compile`, etc.)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `plan-repl`: Document quiet default and opt-in verbose / `/verbose on`
- `nl-agent`: One-shot plan shares the same quiet default for tool-trace stderr

## Impact

- `src/dcs_miz_planner/agent/verbose.py`, `session.py`, `cli.py`
- Tests that assume default-on banners or stderr traces
- README agent section; `docs/BACKLOG.md` `#10b`
