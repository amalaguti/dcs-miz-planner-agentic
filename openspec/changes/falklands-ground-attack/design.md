## Context

Falklands Stage C shipped Mount Pleasant CAP/intercept/escort at **150° / 40 km**
(South Atlantic **sea**). A land strike must not reuse that station. Goose Green
24 is an uncurated west-coast landmark: Nevada’s “15 km past” lands in Falkland
Sound. The land analogue is **15 km short**. Modern trucks and
`su25t_2x_fab250` already ship — reuse them; do not invent ids. Domain still
fail-closes on Falklands until this slice.

## Goals / Non-Goals

**Goals:** validate + compile Mount Pleasant GA; invent GA; Syria-style domain
so CAP 150/40 is sea and GA 269/21 is land; dual-offer modern land trucks.

**Non-Goals:** recon, new unit YAML, intercept_spawn edits, Instant Action as
merge gate, promoting Goose Green 24 as a Spec key.

## Decisions

1. **Strike 269° / 21 km / 2000 m.** Live PyDCS: MPA → Goose Green is 268.80° /
   36.01 km. **269/36 REJECT** (0.13 km from GG). **269/51 REJECT** (Sound).
   Station **x=72951.81977681704 y=26171.946448715786**. CAP 150/40
   **x=38677.30416062245 y=67168.748047** MUST NOT equal the GA station.

2. **Domain = Syria-style seaward windows** on `{1,2,3,24,29}`, not Nevada
   desert-default. MPA 120–180°; Stanley 45–135°; San Carlos 240–330°; Goose
   Green 250–290°; Gull Point 180–240°. Near AF 3 km → land. Add Falklands to
   `DOMAIN_THEATRES`. Do not dump 27 AFs.

3. **Place `east_falkland_inland_strike`.** GA only. Extend `mount_pleasant_home`.
   Do not add GA to the CAP place.

4. **Argentina-red trucks** (`Ural-375` / `GAZ-66`), payload `su25t_2x_fab250`,
   player UK blue. Dual-offer Caucasus modern land rows on theatre=Falklands.

5. **Dedicated `_FALKLANDS_GA_NOTES`.** Drop GA from unsupported combat; recon
   stays refused.

## Risks / Trade-offs

- [269/36 near Goose Green] → lock 21 km; document in the example comment.
- [Nevada desert-default] → CAP 150/40 would classify land; use seaward windows.
- [Omitted country → ThirdReich] → example MUST set Argentina.
- [180/40 land-gap via Gull Point] → known gap; not the GA station.

## Open Questions

- None.
