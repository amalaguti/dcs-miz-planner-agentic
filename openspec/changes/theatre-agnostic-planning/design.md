## Context

Slice 0 packaged YAML (`era/wwii`, `shared`, `theatres/TheChannel`,
`theatres/Normandy`) and theatre-scoped `airdrome_id`. Planning helpers still
hardcode TheChannel: invent prompts, UK–FR domain chord, Hawkinge/Dover
intercept, `french_coast_strike_belt` clamp, EGMH METAR, `KNOWN_COUNTRIES`,
strike `theatre_id=TheChannel`. Normandy smoke is free_flight at
NeedsOarPoint=28 only.

## Goals / Non-Goals

**Goals:**

- Theatre-keyed hooks; Channel recipes remain the only filled recipes.
- Invent may offer Normandy as **free_flight only**.
- Fail closed on Normandy intercept and land/sea domain geometry.
- Channel intercept golden stays bit-identical.

**Non-Goals:**

- F1 Normandy places / intercept / extra AFs / combat examples.
- `theatre_place` rename; modern countries; invented ICAO; `Normandy2`.

## Decisions

1. **Domain — fail-closed** if Spec needs strike/recon/path domain and
   `theatre != TheChannel` (`domain_unsupported_theatre`). Do not run the
   Channel chord. CAP/escort hand Specs may still compile (airfield-relative).
   **Path clamp / harbour nudges skip** (return `None`) on non-Channel.
   `airfield_relative_map_point` MUST pass `theatre=spec.theatre`.

2. **Intercept — `intercept_unsupported_theatre`.** Compiler `_place_enemies`
   refuses unless TheChannel. Keep literals
   Hawkinge `26989.935547`/`-29402.577148` + Dover `+4000`/`-6000` (golden
   `30989.935547`/`-35402.577148`). Do not recompute from `airport_list()`.

3. **Join-up 120°** stays generic airfield-relative (NeedsOarPoint wingman
   Follow still works).

4. **`data/era/wwii/countries.yaml`:** `UK`, `ThirdReich` only. Germany is a
   hint, not a known country. `allowlists` + catalog sync load from registry.
   `models.py` defaults stay WWII UK/ThirdReich.

5. **Strike catalog:** `era_id=wwii` + `theatre_id=TheChannel`. Persist
   theatre→era from `theatre.yaml`. Do not tag `Normandy`. Schema v5→v6.
   `list_strike_targets(theatre="Normandy")` returns empty.

6. **Invent Normandy combat — refuse.** Schema `theatre=` : Normandy+free_flight
   uses NeedsOarPoint example; combat types do not return a Manston skeleton.
   Keep family `channel_place`; add `meta.theatre: TheChannel`. Stub default
   stays Manston; optional test-only NeedsOarPoint JSON.

7. **METAR:** TheChannel → `EGMH`; Normandy → no fake ICAO, still `NOSIG RMK
   SIM`. Miz-patch reweather fail-closed unless miz theatre is TheChannel.
   Realism WWII years from era map, not `if theatre != TheChannel: skip`.

## Risks / Trade-offs

- [False-green domain] Channel chord on Normandy (x,y) → Mitigation:
  fail-closed before classify.
- [Hawkinge on Normandy intercept] absolute Channel coords → Mitigation:
  validate + compile refuse.
- [Invent clones french_coast] → Mitigation: prompts + clamp skip + schema
  theatre=.
- [Strike empty theatre_id looks agnostic] → Mitigation: keep
  `theatre_id=TheChannel` this slice.
- [Join-up 120° odd at Needs Oar Point] → Mitigation: accept until F1.

## Migration Plan

One PR on `theatre-agnostic-planning`. Catalog schema bump wipes `synced_at`.
Rollback = revert. ME Instant Action do-soon after merge.

## Open Questions

- None blocking. F1 supplies Normandy places and intercept recipes.
