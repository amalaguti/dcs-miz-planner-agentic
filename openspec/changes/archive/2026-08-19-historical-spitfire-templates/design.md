## Context

`#30g` shipped Rhubarb / dawn recce / Mustang colour. Local scan 2026-08-19
(60 Channel campaign `.miz` + Spitfire IA): MosquitoFBMkVI in Beware and The Big
Show; Schnellboot_type_S130 in Fight or Die; `v1_launcher` in The Big Show 08.
R1/R2 already noted those campaigns are trigger-empty.

## Goals / Non-Goals

**Goals:** sourced notes (web + local); four advisory cards; agent/eval wiring.

**Non-Goals:** new Spec types; `.miz` import; Mustang player cards; weather YAML.

## Decisions

1. **Two sources.** Web = pattern names. Local `.miz` = DCS layout. If they
   disagree, the card follows the flyable DCS pattern.
2. **Spitfire default.** Owner cannot fly P-51; leave `#30g` Mustang card as-is.
3. **Existing vocabulary only.** Escort+Mosquito; CAP; GA sea_craft; GA
   `v1_launcher`. No new compile fields.
4. **Research stays gitignored.** Only curated YAML ids enter the package.

## Risks

- [Noball ski rare in corpus (1 miz)] → still a real ED Channel unit and shelf id.
- [Circus vs Ramrod] → one escort card; do not split bomber-primary vs fighter-primary.
