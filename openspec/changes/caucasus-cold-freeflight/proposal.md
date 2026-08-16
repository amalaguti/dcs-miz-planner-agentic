## Why

Caucasus is installed and PyDCS-bound, but the planner only supports Channel and
Normandy. Stage A needs a Manston-class smoke: one airfield, one modern country
and aircraft, terrain bind, and a compiling free-flight Spec — without copying
WWII ids or Manston skeletons onto the map.

## What Changes

- Bind Spec theatre `Caucasus` to PyDCS `Caucasus`. Package
  `data/theatres/Caucasus/` with `Batumi: 22` only (do not dump all 21 fields).
- Add era `modern`: `Georgia` and `Su-25T` at 251.0 MHz. Loader walks era
  countries/aircraft. Validate era-filters so Channel/Normandy stay UK /
  ThirdReich + WWII aircraft.
- Ship `examples/batumi_cold_freeflight.yaml` (2024-06-06, `sunny_clear`,
  Georgia blue, cold parking).
- Invent: Caucasus is **free_flight only**. Schema `theatre=Caucasus` uses the
  Batumi example; combat types raise with no Manston/NeedsOarPoint skeleton.
  Generalize the every-turn combat refuse (TheChannel all six; Normandy FF+CAP;
  else FF only). Infer theatre from `Batumi`.

## Non-goals

- Extra airfields, places, CAP/GA/intercept examples, domain classifier,
  intercept spawn, strike dual-tag, paid jets, USA/Russia, modern
  payloads/failures, `theatre_place` rename.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: Caucasus package; `modern` era; Batumi 22; Georgia;
  Su-25T 251; era-keyed countries/aircraft.
- `mission-validation`: era-filtered known countries/aircraft.
- `miz-compiler`: Caucasus terrain; Batumi cold FF compile.
- `nl-agent`: invent table; Caucasus FF only; repair must not inject
  Manston/Normandy.
- `agent-tools`: schema theatre=Caucasus FF example; combat raise.
- `agent-catalog`: catalog lists Caucasus + Batumi after sync.

## Impact

`theatre_terrain.py`, `registry.py`, `allowlists.py`, `validation.py`, invent
schema/session/planner, new era/theatre YAML, Batumi example + N1 tests.
Channel goldens stay green. Acceptance: hermetic pytest + compile the Batumi
example. ME Instant Action is do-soon after merge.
