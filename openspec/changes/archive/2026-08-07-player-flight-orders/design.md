## Context

`#15b` places multi-ship player sections; `#15c` adds wingman Follow + shared route.
Stock DCS gives limited lead→wingman radio when Player is group unit #1 with AI
mates in the **same** group. Wingman `#15b` uses a **separate** AI lead group, so
stock same-group radio does not command that lead. Existing Spec already has
`radio_item_add` / flags / activate patterns (`#25`).

PyDCS can push AI tasks (`Follow`, `Orbit`, `Land`, ROE/option tasks, etc.) onto
controllable groups. Prefer those + F10 flags over Mist/Lua.

## Goals / Non-Goals

**Goals:** Curated Spec-selected section orders; F10 (and/or documented stock radio
for lead); compiler emit for lead mates and wingman AI lead; validate; example;
ME smoke.

**Non-Goals:** Free-form NL→Lua orders; full AI wingman chat; `#15e` discipline
bubbles (only share rejoin order id); Client/MP; expanding escort `package` orders.

## Decisions

1. **Spec shape** — on `player.flight`, optional:
   ```yaml
   orders:
     - rejoin
     - engage
     - orbit
     - rtb
     - break
   ```
   - Omit / empty → no section-order F10 pack from this feature.
   - Ids from a Channel curated set (YAML or frozen enum). v1 minimum:
     `rejoin`, `engage`, `orbit`, `rtb`, `break` (aliases: `form_up`→`rejoin`,
     `cover` may map to engage/hold — pick one cover behaviour or defer).
   - Requires `player.flight` present; solo Specs reject `orders`.

2. **Who is commanded**
   - `role: lead` → AI units in the **player group** (mates).
   - `role: wingman` (+ join_up or not) → the **AI lead group** created by `#15b`.
   - Never command the Player unit’s skill away from Player.

3. **Emit pattern (v1)** — for each selected order id:
   - Mission-start (or after short `time_more`) `radio_item_add` with stable label
     (e.g. `Section: Rejoin`) and dedicated flag.
   - ONCE/continuous trigger: flag set → clear flag → apply curated PyDCS task
     pack to the AI section group; optional short `message`.
   - Pack behaviours (human-authored mapping, not LLM):
     - `rejoin` → Follow player (lead) or re-Follow AI lead / form on lead (wingman
       case: tell AI lead to wait/orbit briefly OR player Follow again — prefer
       “AI lead resume outbound/CAP; player Follow” vs “lead Follow player” —
       **Decision:** wingman `rejoin` = reinforce Follow on player→lead; lead
       `rejoin` = mates Follow player unit.
     - `engage` → set ROE weapons free / search-engage on AI section.
     - `orbit` → Orbit at current/station reference (CAP station if present, else
       short orbit near airfield bearing).
     - `rtb` → Land at home airfield for AI section.
     - `break` → clear Follow / independent (stop formation task); optional message.

4. **Stock radio** — do not block stock DCS wingman menu for lead same-group; F10
   pack is additive and Spec-selected. Document in brief which F10 items exist.

5. **Agent** — planning_options family `player_flight_order`; schema notes; never
   invent order ids.

6. **`#15e` hook** — discipline may later fire the same `rejoin` pack via flags;
   keep order emitters callable from one helper module.

## Risks / Trade-offs

- [Risk] AI task API quirks per mission type → Mitigation: free-flight + CAP
  examples first; GA/escort smoke later.
- [Risk] F10 label collisions → Mitigation: `Section: …` prefix; unique flags.
- [Risk] Rejoin semantics differ lead vs wingman → Mitigation: document both;
  ME smoke each role.
- [Risk] Overlap with hand `triggers` radio → Mitigation: feature emit independent;
  validate duplicate labels advisory if cheap.

## Migration Plan

- Additive optional field; existing Specs unchanged.

## Open Questions

- Exact Orbit reference for non-CAP (airfield-relative vs player position) — resolve
  in apply with simplest PyDCS-supported option.
- Whether `cover` is v1 or deferred — default **defer**; five ids above are enough.
