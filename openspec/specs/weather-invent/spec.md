# weather-invent

## Purpose

Invent-time resolution of concrete Channel weather snapshots from named Spec
patterns, date/time priors, and a seed — always-on within-pattern variation
before compile apply.

## Requirements

### Requirement: Weather invent resolves seeded snapshots
The system SHALL resolve a concrete weather snapshot from Mission Spec
`weather`, `date`, `start_time`, and `weather_opts.seed` before compile apply.
Resolution MUST be deterministic for the same inputs. When `weather_opts.seed`
is omitted and a Spec YAML is written, the system MUST assign a seed and
persist it under `weather_opts.seed`.

#### Scenario: Same seed same snapshot
- **WHEN** invent resolution runs twice with the same Spec fields and seed
- **THEN** the resolved gallery (or legacy density) and numeric fields MUST match

#### Scenario: Different seeds differ within class
- **WHEN** invent resolution runs twice with the same pattern and date/time but
  two different seeds
- **THEN** at least one applied weather numeric or gallery id within the
  pattern’s allowed family MUST differ

### Requirement: Hybrid gallery and numeric priors
For patterns with a gallery family, invent MUST pick a `cloud_preset` only from
that pattern’s allowed within-family list, weighted by Spec date (season) and
start time (e.g. morning fog risk), then soft-nudge numerics (temperature, QNH,
wind, turbulence, fog, cloud base) and apply seeded jitter. Invent MUST NOT
silently select a gallery id outside the pattern’s family. Patterns without
gallery (legacy density trio) MUST NOT gain a rainy or broken gallery via invent.

#### Scenario: Rain pattern stays rainy family
- **WHEN** invent resolves a rain-overcast pattern for any season/seed
- **THEN** the resolved `cloud_preset` MUST be a rainy gallery id allowed for
  that pattern (or the pattern’s declared rainy set)

#### Scenario: Sunny clear stays non-gallery or clear path
- **WHEN** invent resolves `sunny_clear`
- **THEN** the snapshot MUST NOT set a rainy or broken gallery preset
