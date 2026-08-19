## Why

R8 pinned pydcs to git `e20f328`, so `dcs.terrain.Kola` exists in the venv, but
the planner still has no factory, registry package, or smoke Spec. Stage A
needs a Manston-class bind: one airfield, one modern host country, reused
Su-25T, and a compiling free-flight example — without dumping 37 Kola
airports or starting combat.

## What Changes

- Bind Spec theatre `Kola` to PyDCS `Kola`. Package `data/theatres/Kola/`
  with `Bodo: 7` only (live `Kola().airport_list()`; 94 parking slots). Spec
  key is `Bodo` (PyDCS name `Bodo`). Do not dump all 37 fields.
- Add `Norway` to era `modern` countries (PyDCS `countries.Norway` id 12).
  Reuse `Su-25T` at 251.0 MHz. Do not add Norway to `era/wwii`.
- Ship `examples/bodo_cold_freeflight.yaml` (2024-06-06, `sunny_clear`,
  Norway blue, cold parking).
- Invent: Kola is **free_flight only**. Schema `theatre=Kola` uses the Bodo
  example; combat types raise with no prior-map skeleton. Dedicated
  `_KOLA_FF_NOTES`. Infer theatre from `Kola` or airfield `Bodo`.
- Retarget unbound stand-in tests off Kola onto **Iraq** (compile / domain /
  intercept copies). Replace “Kola exists in pydcs but unbound” with
  **GermanyCW** (`dcs.terrain.Germany`, name `GermanyCW`).

## Non-goals

- Extra airfields, places, CAP/GA/intercept/escort/recon, Finland/Sweden/
  Russia hosts, paid jets, modern payloads/failures, `theatre_place`.
- Binding Iraq, `MarianaIslandsWWII`, or GermanyCW.
- Dual-offering Caucasus trucks on Kola strike lists.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: Kola package; Bodo 7; Norway in modern era.
- `mission-validation`: Kola smoke validates; Channel+Norway unknown.
- `miz-compiler`: Kola terrain; Bodo cold FF compile.
- `nl-agent`: invent table; Kola FF only; repair must not inject prior maps.
- `agent-tools`: schema theatre=Kola FF example; combat raise; dedicated notes.
- `agent-catalog`: catalog lists Kola + Bodo after sync.

## Impact

`theatre_terrain.py`, invent schema, modern countries YAML, Kola theatre
YAML, example + N1 tests. Channel goldens stay green. Acceptance: hermetic
pytest + compile the Bodo example. ME Instant Action is do-soon after merge.
