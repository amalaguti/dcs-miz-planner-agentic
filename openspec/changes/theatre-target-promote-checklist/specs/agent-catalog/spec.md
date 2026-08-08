## ADDED Requirements

### Requirement: Strike unit and theatre promote uses checklist
Expanding known strike/recon units or theatres in the catalog MUST follow the
checked-in theatre/target promote checklist (curated YAML → catalog sync). The
system MUST NOT auto-promote discovery-only install folders or ME scrapes into
known catalog sources.

#### Scenario: Promote path points at checklist
- **WHEN** a developer adds a verified ground/ship id to Channel registry YAML
  and runs catalog sync
- **THEN** the catalog MUST list the new strike unit after sync, and project
  docs MUST point at the promote checklist for the required steps (class shelf,
  motion/AI, examples, invent cues)
