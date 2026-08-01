## Context

Mission date should match the historical backdrop the user has in mind. Current Channel
content is WWII-oriented; later we may support other eras. Modern dates stay valid.

## Goals / Non-Goals

**Goals:** Advisory warning when Channel date looks mismatched to its usual WWII backdrop;
open wording (WWII / other eras / modern OK); prompt guidance; success path unchanged.

**Non-Goals:** Blocking dates; Cold War compile support; aircraft production-year tables.

## Decisions

1. **v1 heuristic:** Channel theatre → usual backdrop years 1939–1945; warn outside that.
2. **Severity:** warning only.
3. **Copy:** emphasize user choice of era, not “you must use WWII.”

## Risks / Trade-offs

- [Modern Channel free flight warns] → Intended advisory; text says modern is allowed.
