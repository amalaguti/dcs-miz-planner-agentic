## Why

M2 proved free-flight compile trustworthiness, but the concept’s first product story is a
dawn Manston intercept vs Bf-109s. Judgment (2026-07-26) reordered the backlog: prove combat
Spec + compile in-game before building the agent layer. Without this slice, `enemies` /
`objectives` stay forever-reserved stubs and M3 tools only wrap free flight.

## What Changes

- Extend Mission Spec for an `intercept` mission type with typed `enemies` (and a minimal
  `objectives` shape) using verified DCS ids (`SpitfireLFMkIX`, `Bf-109K-4`, `TheChannel`).
- **BREAKING** for anyone relying on “any non-empty enemies always fail”: intercept Specs
  with non-empty enemies MUST validate and compile; free_flight still refuses non-empty
  extensions.
- Compiler places player cold at Manston and an enemy Bf-109K-4 flight for the checked-in
  intercept example (Channel coords documented in design; no invented aircraft/theatre ids).
- Validation + golden fixtures cover the intercept example; Manston free-flight goldens remain.
- Checked-in example Spec + in-game acceptance for the intercept `.miz`.

## Non-goals

- Natural-language agent, tool surface, squadron voice.
- Full trigger / win-lose graph (M6); intercept v1 is placement (+ optional trivial native
  behaviour only if required for a loadable mission).
- New weather preset `dawn_clear` (use early `start_time` + existing `sunny_clear` unless
  design finds a trivial preset addition).
- CAP / ground-attack / escort; Mist/MOOSE; multi-theatre.
- Package versioning / tags.

## Capabilities

### New Capabilities

- *(none — extend existing mission-spec / compiler / validation / golden-fixtures)*

### Modified Capabilities

- `mission-spec`: Intercept mission type; allow non-empty `enemies` / minimal `objectives`
  for intercept; keep free_flight rules.
- `miz-compiler`: Compile intercept Spec to `.miz` with player + enemy flight; free flight
  unchanged.
- `mission-validation`: Validate intercept combinations via registry; still refuse unsupported
  types and non-empty `triggers`.
- `golden-fixtures`: Intercept structural golden (or sibling fixture dir) alongside Manston
  free-flight.

## Impact

- `models.py`, `validation.py`, `compiler/pydcs_compiler.py`, examples, tests/fixtures, docs.
- Registry already has `Bf-109K-4` radio — reuse; may add spawn/coord notes if needed.
- Acceptance: open compiled intercept `.miz` in DCS ME / Instant Action.
