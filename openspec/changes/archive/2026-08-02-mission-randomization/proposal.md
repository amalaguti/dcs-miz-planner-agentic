## Why

Fixed Specs always compile the same sortie. Players want replayability—different weather,
clock, geometry, or opposition on a familiar template—without asking the LLM to invent a
new Spec each time. M5 needs **seeded**, deterministic variation so the same seed
reproduces the same concrete Spec (and thus the same `.miz`).

## What Changes

- Add a **seeded Spec → Spec** randomize step: given a valid base Mission Spec + integer
  seed (+ optional axis flags), produce another valid Spec with controlled variation.
- Same `(base Spec, seed, axes)` MUST always yield the same output Spec (no wall-clock
  randomness; compiler stays fully deterministic on a concrete Spec).
- v1 axes (only where the mission type already has the field): weather preset, start_time
  jitter, combat geometry (`cap` / `strike` / `escort` bearing/distance/altitude), and
  opposition (`enemies` count / aircraft / skill when present).
- Expose via library API, `dcs-miz randomize` CLI, and an agent tool so chat can “reroll”
  before compile.
- Tests prove determinism and validation of randomized Specs; optional example of
  randomize-then-compile. In-game accept: open two different-seed `.miz` files from the
  same base and confirm they differ in ME where expected.

## Non-goals

- Nondeterministic compile (no random inside PyDCSCompiler).
- Generating a mission from seed alone with no base Spec.
- Changing mission type, theatre, player aircraft/airfield, or inventing new unit ids
  outside the Channel registry.
- Lua / triggers / radio banks / dynamic campaign.
- Refreshing golden fixtures to be seed-dependent.

## Capabilities

### New Capabilities
- `mission-randomization`: Seeded Spec→Spec variation contract (axes, determinism,
  validation of output).

### Modified Capabilities
- `agent-tools`: Add a tool to randomize a Mission Spec with a seed (and optional axes).
- `mission-options`: Optional planning option / docs for “randomize with seed” as an
  agent-facing knob (advisory or supported once the tool exists).
- `mission-validation`: Randomized Specs MUST still pass the same validation engine
  before compile (no special bypass).

## Impact

- New module (e.g. `randomize.py`) + CLI subcommand + tools surface
- Tests for seed stability and axis behaviour; examples/docs/BACKLOG/README
- Compiler and golden fixtures unchanged for fixed Specs
