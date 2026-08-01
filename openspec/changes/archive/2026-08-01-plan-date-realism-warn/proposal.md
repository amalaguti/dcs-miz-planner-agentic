## Why

Live planning may pick a calendar year that does not match the historical backdrop of
the mission content (e.g. modern year for Channel Spitfire/Axis). Dates must remain free
(WWII, later eras such as Cold War when supported, or modern if the user wants); the
system should warn on mismatch, not block.

## What Changes

- After a successful plan, if Channel content’s date falls outside the usual WWII
  backdrop (~1939–1945), emit an advisory warning that explains era alignment and that
  other eras / modern dates are allowed.
- System prompt: choose a date that fits the history the user wants.
- Do not fail the plan for date/era mismatch.

**Non-goals:** Hard-rejecting dates; full historical validation engine; Cold War theatre support yet.

## Capabilities

### New Capabilities
- (none)

### Modified Capabilities
- `nl-agent`: Advisory date/era alignment warning after successful plan.

## Impact

- `agent/realism.py`, planner, CLI `plan`, prompts, tests, brief docs
