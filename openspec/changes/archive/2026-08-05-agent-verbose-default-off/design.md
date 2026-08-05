## Context

`DEFAULT_VERBOSE = True` and CLI `--verbose` defaults were left on for early agent
debugging. Adversarial C3 / backlog `#10b` ask to flip before release polish.

## Goals / Non-Goals

**Goals:**
- Quiet stderr by default for `dcs-miz plan` and `dcs-miz chat`
- Keep `--verbose` / `--no-verbose` and `/verbose on|off` working
- Single SoT constant (`DEFAULT_VERBOSE`) used by agent + CLI defaults

**Non-Goals:**
- Prefs DB persistence for verbose
- Changing log content format

## Decisions

1. **Flip `DEFAULT_VERBOSE` to `False`** and wire CLI `default=DEFAULT_VERBOSE` (or
   `default=False` matching the constant) so plan/chat stay aligned.
   - Alternative: only change CLI — rejected; `PlanSession` / `plan_mission` would still
     default noisy when called from tests/library without an explicit flag.

2. **No prefs migration** — verbose stays a session/CLI concern for this slice.

## Risks / Trade-offs

- [Developers forget `--verbose`] → README + help text say how to enable; `/verbose on` in chat
- [Tests assumed default on] → Update banner/default assertions; keep explicit `verbose=True` where testing the toggle
