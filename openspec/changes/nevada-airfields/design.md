## Context

Stage A bound Nevada with Nellis=4, USA, Su-25T 251.0 MHz, invent free_flight
only. Live PyDCS `Nevada.airport_list()` has 17 airports (id 12 absent).
Numeric ids collide with other theatres (Groom Lake 2 vs Mount Pleasant 2 vs
Merville Calonne 2; Nellis 4 vs Maupertus 4 vs Dunkirk 4). All Nevada fields
are US hosts — no second country.

## Goals / Non-Goals

**Goals:**

- Curate eight verified Nevada airfields (not all 17).
- Compile a Groom Lake free-flight smoke (USA blue) without lifting combat invent.
- Infer theatre from the new Spec keys; lookup stays theatre-scoped.

**Non-Goals:**

- Places, CAP/GA, domain, intercept spawn, extra countries, dump of 17 fields,
  new aircraft/payloads.

## Decisions

1. **Eight airfields, not 17.** Live `airport_list()` curated keys:
   `Nellis=4`, `GroomLake=2` (PyDCS `Groom Lake` / `Groom_Lake`), `Creech=1`,
   `TonopahTestRange=18` (`Tonopah Test Range`), `NorthLasVegas=15`
   (`North Las Vegas`), `HendersonExecutive=8` (`Henderson Executive`),
   `BoulderCity=6` (`Boulder City`), `Mesquite=13`. Leave out McCarran (thin
   parking), helo/thin fields, Mina (0 slots). Alternative (dump every AF)
   rejected — Caucasus/Syria curated 8.

2. **No countries.yaml edit.** USA already modern. Extra-AF smoke stays USA
   blue. `usaaf` is voice only. Channel+USA still unknown.

3. **Groom Lake example is USA blue.** Invent/schema stay Nellis. Stub LLM
   stays Manston. GroomLake 2 is not MountPleasant 2. Radio 251.0 (not ATC).

4. **infer_theatre maps the new camelCase keys** (and keeps Nellis). Combat
   refuse unchanged. Registry MUST reject `Groom_Lake`.

5. **N1-style Groom Lake contracts**, not a full golden. Assert `airdromeId=2`
   on Nevada theatre (not Falklands Mount Pleasant).

## Risks / Trade-offs

- [GroomLake 2 confused with MountPleasant] → theatre-scoped lookup + compile
  zip theatre Nevada.
- [Invent copies Groom Lake as home] → schema/notes stay Nellis.

## Migration Plan

Implement on `nevada-airfields`. Rollback = revert the branch. Channel goldens
must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
