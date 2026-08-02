## Context

M5 wants replayability. Today a Mission Spec is fully concrete: same YAML → same `.miz`.
That is correct for goldens and compile trust, but players cannot “reroll” weather, clock,
geometry, or opposition on a familiar template without hand-editing YAML or asking the
LLM to rewrite the Spec.

Principle stays: **AI plans; software compiles**. Randomization is a **Spec → Spec**
transform that emits another valid Spec. The compiler never rolls dice.

## Goals / Non-Goals

**Goals:**

- Deterministic seeded variation of an existing valid Spec.
- Safe axes only: weather, start_time, geometry (`cap`/`strike`/`escort`), opposition
  (`enemies` when present).
- CLI + library + agent tool; always re-validate before compile.
- Same inputs always produce identical Spec dumps (pytest-stable).

**Non-Goals:**

- Random compile path; seed field required on Mission Spec schema.
- Procedural mission-from-seed-only; changing player/theatre/mission_type.
- Package reshuffle, target unit inventing, or Lua/triggers.
- Breaking or seed-parameterizing golden fixtures.

## Decisions

1. **Spec → Spec, not Spec → .miz random**
   - Rationale: keeps goldens, validation, and briefings on a concrete Spec; seed is an
     input to `randomize_mission_spec`, not a compiler argument.
   - Alternatives: jitter inside PyDCSCompiler (rejected — nondeterministic goldens /
     harder debugging); optional Spec `seed` field compiled away (rejected — conflates
     plan contract with generation metadata).

2. **PRNG: `random.Random(seed)` with explicit draw order**
   - Integer seed (non-negative). Document draw order per axis so tests lock behaviour.
   - Alternatives: `secrets` (nondeterministic); hash-only field tweaks (opaque, hard to
     extend).

3. **Axes as an explicit set (default = all applicable)**
   - Named axes: `weather`, `time`, `geometry`, `opposition`.
   - Skip axes that do not apply (e.g. free_flight has no geometry/opposition).
   - Caller may pass a subset. Unknown axis → clear error.
   - Alternatives: always-all (less flexible for agent “just reroll weather”).

4. **Variation bounds (v1 constants in code, Channel-scoped)**
   - **weather:** uniform among registered WeatherPreset values (may keep current).
   - **time:** start_time ± up to 90 minutes, clamped to 00:00–23:59; minute resolution
     5 minutes after jitter.
   - **geometry:** for present `cap`/`strike`/`escort`: bearing ±30°, distance ±20%
     (floor > 0), altitude ±15% (floor > 0); pattern/engagement unchanged.
   - **opposition:** for each `enemies[]` entry: count in `[max(1,c-1), min(16,c+2)]`;
     aircraft from Channel registry fighters on opposing coalition (known list);
     skill from a small fixed set (`Average`, `Good`, `High`). Empty enemies → no-op.
   - Alternatives: YAML policy file (defer); opposition_density planning ids as sole
     driver (keep advisory; randomize works from concrete enemies).

5. **Identity fields never change**
   - Preserve: `schema_version`, `mission_type`, `theatre`, `date`, `player` (all fields),
     `name`/`description` (optionally append “ (seed N)” in description only when CLI
     flag `--annotate` is set; default off so dumps stay clean).
   - Preserve: objectives, package, targets, payload, engagement/pattern enums.

6. **Surfaces**
   - `randomize_mission_spec(spec, seed, axes=None) -> MissionSpec` in a new module.
   - CLI: `dcs-miz randomize <spec> --seed N [--axes weather,time,…] [-o out.yaml]`.
   - Tool: `randomize_mission` returning structured `{ok, spec, seed, axes}` (Spec as
     dict); agent then validates/compiles as today.
   - Planning options: add advisory family `randomization` id `seeded_reroll` describing
     the tool (no Spec meta mapping required).

7. **Validation**
   - After randomize, caller SHOULD validate; CLI `--validate` default on before write;
     tool returns validation errors without writing. No bypass of shared engine.

## Risks / Trade-offs

- [Over-jitter breaks playability] → Tight % bounds; identity fields fixed; in-game
  spot-check two seeds.
- [Enemy aircraft pick invents ids] → Only registry-listed Channel fighters.
- [Draw-order churn breaks tests] → Document order; pin golden randomize snapshots in
  unit tests (YAML dump equality), separate from `.miz` goldens.
- [Agent double-randomizes] → Tool returns concrete Spec; prompt note: randomize once
  then compile.

## Migration Plan

- Additive only; no schema_version bump; existing Specs/goldens unchanged.
- Catalog schema bump only if planning_options.yaml adds rows (sync on next catalog use).

## Open Questions

- Whether `--annotate` description suffix is worth shipping in v1 (default: yes, optional
  flag only).
- Whether package count jitter belongs in a fast follow (deferred; not v1).
