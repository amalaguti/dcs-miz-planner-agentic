## Context

Caucasus and Normandy classify land/sea. A recon AOI on a CAP sea station with
land observe units fails `strike_domain_mismatch` / `motion_domain_mismatch`.
Repair still dumped Channel 125/76 regardless of inferred theatre.

## Goals / Non-Goals

**Goals:** theatre-keyed mismatch repair.

**Non-Goals:** path clamp off Channel; Syria domain.

## Decisions

1. Infer theatre (existing `infer_theatre`). Unspecified → Channel 125/76.
2. Caucasus → `kutaisi_inland_strike` 43/110 (not CAP 270/40, not 125/76).
3. Normandy → `maupertus_inland_strike` 180/133 (not CAP 180/63, not 125/76).
4. Syria/Nevada/Falklands → do not copy french_coast; point at that theatre's
   allowed types (domain still fail-closed).

## Open Questions

- None.
