## Context

Eval showed consult-then-under-emit. `#30c` fixed prompts/infer; still need host pressure
and example copying.

## Goals / Non-Goals

**Goals:** One immersion repair turn; immersion-first schema examples; no invent randomize.

**Non-Goals:** Blocking all bare Specs; changing CLI randomize.

## Decisions

1. **Cue regex on user prompt** → suggested behaviour + example path in nudge (not validate error).
2. **Agent schema map** separate from golden/compile bare examples (`_AGENT_EXAMPLE_FILES`).
3. **Filter `randomize_mission`** from `TOOL_DEFINITIONS` like mutating tools (remain in
   `ALL_TOOL_DEFINITIONS` for tests/host if needed; CLI keeps `randomize` command).

## Risks / Trade-offs

- [Extra LLM turn latency] → once per plan only
- [False positive cues] → nudge soft; user can still emit bare after repair attempt
- [Schema tests expect bare FF] → update asserts to gates example
