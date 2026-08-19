# Prompt catalog — agent creativity eval

Maintain this file when shipping new `mission_behaviour` / `mission_inspiration` cards,
campaign tools, or creative-memory behaviour. Each scenario is a **vague human ask** plus
what a good assertive agent should roughly do.

Ids are stable; edit `prompt` / `expect` / `notes` as product evolves.

---

## ff-interesting

- **prompt:** interesting free flight from Manston
- **expect:**
  - `mission_type`: free_flight
  - applies **1–2** behaviours (prefer `altitude_speed_gates` and/or `sound_flag_chain`)
  - calls `list_mission_options` (and uses `mission_inspiration` / `mission_behaviour`)
- **fail if:** empty zones/triggers and no narrative/sound/gates
- **notes:** Baseline assertiveness for vague FF.

## ff-honest-hop

- **prompt:** give me a Channel hop that keeps me honest, don't over-specify
- **expect:**
  - free_flight (or clear hop framing)
  - `altitude_speed_gates` (inspiration `low_level_channel_hop`)
  - continuous altitude and/or speed conditions + messages (usually after `time_more`)
- **fail if:** bare free_flight with no gates
- **notes:** Explicit “honest” should map to ingress discipline.

## intercept-difficulty-menu

- **prompt:** dawn scramble from Manston, make it immersive but I choose difficulty
- **expect:**
  - `mission_type`: intercept
  - `radio_late_activation` **complete**: `late_activation` on enemies **and**
    `radio_item_add` + `activate_group` (and usually a flag) in triggers
  - optional `narrative.enabled` **only if** triggers stay empty for narrative expand;
    do **not** combine narrative pack with hand triggers, and do **not** leave
    late-activated enemies with no activate path
- **fail if:** `late_activation: true` with empty triggers
- **notes:** Half-recipe is worse than narrative-only.

## campaign-big-show-vibe

- **prompt:** something like a Big Show style sortie near Manston, surprise me
- **expect:**
  - calls `list_installed_campaigns` (or otherwise uses Doc/campaign themes)
  - maps vibe onto packaged behaviours (often `narrative_pack` and/or intercept immersion)
  - does **not** import `.miz` as Spec
- **fail if:** never consults campaigns/Docs when ask names a campaign; or invents Lua
- **notes:** Inspiration channel — Doc titles over `.cmp` stages.

## strike-marked-ingress

- **prompt:** ground attack across the Channel, help me find the target area
- **expect:**
  - `mission_type`: ground_attack
  - `mark_smoke` (zone + mark and/or smoke); optional `group_life_less`
  - valid strike + payload + targets
- **fail if:** GA with no visual cue and no life-% beat when ask wanted findability
- **notes:** Maps to inspiration `marked_strike_ingress`.

## cap-narrative

- **prompt:** CAP south-east of Manston, immersive but I don't want to write triggers
- **expect:**
  - `mission_type`: cap with nested `cap`
  - `narrative.enabled: true` and empty zones/triggers
  - enemies non-empty (narrative packs need opposition for win beats)
- **fail if:** hand-written triggers together with narrative, or narrative with no enemies
- **notes:** Inspiration `cap_with_narrative_beats`.

## pair-as-lead

- **prompt:** take a pair from Hawkinge, keep it simple
- **expect:**
  - Channel (or Hawkinge) free_flight / hop framing
  - `player.flight.size` 2 and `role: lead` (AI mate in the player group)
  - omit escort `package[]` (this is a section, not a strike package)
- **fail if:** solo (no `player.flight`) when the ask said pair; or a Mosquito `package[]` used as the wingman
- **notes:** Catalog `player_flight_size` pair + inspiration `rhubarb_pair`. Compiler already exists (`#15b`).

## wingman-join-up

- **prompt:** I'm flying as two, put me as wingman and I'll join up after takeoff
- **expect:**
  - `player.flight.size` 2, `role: wingman`, `join_up` true (or omitted default)
  - separate AI lead group + Follow (not Player on slot 2)
- **fail if:** `role: lead` when the ask said wingman; or `join_up: false` with no reason
- **notes:** Schema already documents wingman Follow. Prefer Manston or Hawkinge parking.

## recon-ops-colour

- **prompt:** dawn recce from Manston, give me some ops colour but I don't want to write triggers
- **expect:**
  - `mission_type: recon`
  - `narrative.enabled: true` and empty zones/triggers in the authored Spec
  - weapons hold / no payload
- **fail if:** hand-written recon triggers, or CAP narrative pack used instead of recon
- **notes:** Inspiration `dawn_recce_narrative`; expander prepends push then find beat.

---

## Catalog maintenance checklist

When adding a behaviour card:

1. Add a scenario (or extend an existing one) with a vague prompt a pilot might say
2. List concrete Spec signals in `expect` / `fail if`
3. Run `uv run python .cursor/skills/eval-agent-creativity/scripts/run_eval.py --only <id>`
