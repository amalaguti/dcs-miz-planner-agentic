## Why

Adversarial C1: LLM-exposed tools can compile to disk, set prefs, and poison generation
memory without host confirmation. For local single-user, still fail-left so confused/injected
tool calls cannot mutate state or write `.miz` outside `out/`.

## What Changes

- **BREAKING (agent tools):** LLM tool surface is read-only by default (no `compile_mission`,
  `set_user_prefs`, `record_generation`, `record_feedback` in default tool list).
- `dispatch_tool` rejects those names unless `allow_mutating=True` (host/tests only).
- `compile_mission` output path MUST resolve under an allowed `out/` directory.
- Hosts keep recording generations via Python memory APIs (not LLM tools).
- Prompt: note prefs/compile/feedback are host slash/CLI, not agent tools.

## Non-goals

- Multi-user auth; interactive confirm UI; removing Python APIs for CLI.
- Sandboxing validate/randomize/research.

## Capabilities

### Modified
- `agent-tools`: default tool surface read-only; mutating dispatch gated; compile path allowlist.
- `nl-agent`: prompt notes host-owned mutate/compile.

## Impact

`tool_bridge.py`, `llm.default_tools`, `tools/surface.py` compile path check, tests, prompts.
