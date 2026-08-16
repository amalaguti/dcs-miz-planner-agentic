## Context

Era packages key countries and aircraft. UK is already dual-era. Aircraft
loader allows the same id in two eras only when the `AircraftRef` is identical
(same radio). Caucasus/Syria/Nevada/Falklands currently fail Spitfire.

## Goals / Non-Goals

**Goals:**

- Spitfire LF Mk IX (and CW) known in `modern` as well as `wwii`.
- Validate + compile a Batumi Spitfire free-flight.
- Keep Channel+Su-25T unknown.

**Non-Goals:**

- Su-25T on WWII maps. Other WWII types on modern. Caucasus combat invent.

## Decisions

1. **Dual-era copy, same radio 124.0.** Matches UK country pattern. Collision
   guard in `_load_era_identity` requires identical refs. Alternative (drop
   era filter for all aircraft) rejected — would allow Frogfoot on Channel.

2. **Both LFMkIX and LFMkIXCW.** Same DCS module. Not Mosquito/109/190 this
   slice.

3. **Example is Batumi + UK + Spitfire.** Invent/schema stay Su-25T Georgia.
   Stub LLM stays Manston.

4. **N1-style compile contracts** (`airdromeId` 22, type SpitfireLFMkIX,
   frequency 124.0). No full golden.

## Risks / Trade-offs

- [Invent still emits Su-25T] → intentional default; user Specs may choose
  Spitfire.
- [Georgia+Spitfire also validates] → both are modern; allowed.

## Migration Plan

Implement on `spitfire-dual-era`. Rollback = revert. ME Instant Action
do-soon (`out/batumi_spitfire_freeflight.miz`).

## Open Questions

- None.
