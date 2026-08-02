## Context

Intercept and CAP compile Channel air combat (player + optional enemy aircraft, CAP Orbit /
ROE). `payloads.yaml` is empty and `payload_family` planning options are `future`. PyDCS
exposes SpitfireLFMkIX bomb CLSIDs (250 lb wing / 500 lb centreline), WWII ground vehicles
(e.g. `Blitz_36-6700A`, `flak18`), and `GroundAttack` / `Bombing` tasks. Payload install
scanning remains disabled (`LESSONS_LEARNED`); loadouts must be applied from registry CLSIDs
only.

## Goals / Non-Goals

**Goals:**

- Represent and compile one checked-in Channel ground-attack: Spitfire cold at Manston with a
  named bomb preset, ingress to an airfield-relative strike point, place a small red ground
  target group, GroundAttack tasking.
- Validation + golden + example; free_flight / intercept / CAP unchanged.
- Promote payload families from `future` to Spec-backed named presets; register a minimal
  ground-unit SoT.
- Light agent/voice/schema awareness of `ground_attack`.

**Non-Goals:**

- Escort, briefings→`l10n`, triggers/Lua, multi-theatre, non-Spitfire strikers.
- Agent-invented coords or CLSIDs; re-enable PyDCS payload dir scanning.
- Air opposition on the strike Spec (v1); win/lose triggers.
- Named airfield/runway attack (`BombingRunway`) (defer); friendly/same-side targets (reject).
- Full historical occupation-map GIS (v1 uses Channel WWII convention: land strikes on
  Axis continent; water = ships).
- Waypoint/Lua-scripted tank jettison (player cockpit + allow-jettison options only).

## Decisions

1. **`mission_type: ground_attack`**
   - Same short enum style as `free_flight` / `intercept` / `cap`.
   - Alternative rejected: overload CAP with ground targets — muddies air patrol semantics.

2. **Nested `strike` block (required for ground_attack; forbidden otherwise)**
   - Fields (v1):
     - `bearing_deg` (0–360) and `distance_km` (>0): target area relative to **player
       airfield** (same CAP station math).
     - `altitude_m` (positive): ingress / attack altitude.
     - `practice` (bool, default false): when true, allow same-coalition practice targets.
   - Alternative rejected: named registry strike points only — less flexible for the agent;
     named sugar can wrap the same fields later.

3. **Top-level `targets` list (required non-empty for ground_attack) — enemy only**
   - Each entry: `unit` (exact DCS land **or** ship type id), `count` (1–16), `skill`
     (default Average), `country` (default `ThirdReich`), `coalition` (default `red`).
   - **No friendly fire (combat):** when `strike.practice` is false/omitted, every target's
     `coalition` MUST oppose `player.coalition`.
   - **Practice exception:** `strike.practice: true` allows same-coalition / home-territory
     targets for bombing-practice narrative (e.g. blue player, UK-side trucks). DCS ME
     accepts friendly units as placeable targets; the player bombs them as a range. Combat
     Specs stay enemy-only.
   - **Enemy geography (combat):** land vehicles on territory held by the enemy at the
     mission date (Channel WWII blue → Axis French/Belgian coast). Mid-Channel water MUST
     use sea-domain ships/boats.
   - Registry: `ground_units.yaml` (`domain: land`) + `ships.yaml` (`domain: sea`); compiler
     resolves via `get_strike_unit` and places `vehicle_group` vs `ship_group`.
   - Do **not** reuse `enemies` (air only). Air `enemies` MUST be empty for ground_attack v1.

4. **Named payload preset on `player.payload` (required for ground_attack)**
   - String key into `payloads.yaml` (e.g. `spitfire_2x250_slipper`). Meta includes
     `aircraft` and ordered `{pylon, clsid}` pairs using verified SpitfireLFMkIX CLSIDs.
   - Forbidden / omitted on free_flight, intercept, and CAP for v1.
   - Compiler applies pylons after `_disable_payload_scan` (manual CLSID loadout; never scan
     install `UnitPayloads`).
   - **Centreline constraint:** pylon 2 is either a bomb **or** a tank — never both.
     Cross-Channel strike → wing bombs + slipper tank; local/short strike MAY use
     centreline 500 lb without a tank.
   - Seed presets:
     - `spitfire_2x250_slipper` — LH+RH 250 lb + `SPITFIRE_45GAL_SLIPPER_TANK` (**default
       Channel-crossing example**)
     - `spitfire_2x250` — wing 250s only (no tank)
     - `spitfire_1x500` — centreline 500 lb (no tank; shorter radius)
   - **Jettison:** player drops the tank in the cockpit before the attack run. Compiler MUST
     NOT set `OptRestrictJettison`. Optionally set `OptJettisonEmptyTanks` for AI hygiene.
     No Spec field and no waypoint/Lua jettison script in v1 — cover procedure in the
     commander brief / schema notes.

5. **Objective `attack_ground`**
   - Required non-empty `objectives` including `attack_ground`. Validate-only (no win/lose
     triggers). Reject on non–ground_attack types unless a later change allows it.

6. **Compiler path**
   - Player cold start; set `group.task = GroundAttack.name`.
   - Apply registry payload pylons to player unit(s); when the preset includes a slipper
     tank, ensure jettison is allowed (`OptRestrictJettison` unset/false); MAY set
     `OptJettisonEmptyTanks`.
   - Climb + IP / target waypoints at airfield-relative strike point; attach `Bombing` (or
     `AttackGroup` once the ground group exists — prefer Bombing at Point for v1 simplicity;
     document choice in LESSONS if AttackGroup proves better in ME).
   - Place ground vehicle group(s) at/near strike point on the **enemy** coalition/country
     from each target entry (default red/`ThirdReich` for blue player); never place targets
     on the player's coalition.
   - Keep radio + theatre-member workarounds.

7. **Example Spec**
   - `examples/manston_ground_attack.yaml`: Manston morning, `sunny_clear`, strike **inland**
     near Dunkirk (≈125° / 76 km — past the coast toward St Omer; do not stop short over
     water), **`spitfire_2x250_slipper`**, 2–3× `Blitz_36-6700A`.
   - Golden `tests/fixtures/manston_ground_attack/`: GroundAttack task, bomb + slipper CLSIDs,
     ground unit type(s), player/theatre/freq.

8. **Planning options / catalog / agent**
   - Add `mission_type` / `ground_attack` as `supported`.
   - Promote `payload_family` entries to `supported` with `meta.payload` → Spec
     `player.payload` (include slipper and non-slipper bomb presets; label Channel-crossing).
   - `get_mission_spec_schema` / planning rules / commander brief gain a ground-attack branch
     that recommends slipper tank for Channel crossings and reminds the pilot to jettison
     before the attack.

## Risks / Trade-offs

- [Payload KeyError if install scan re-enabled] → Keep `_disable_payload_scan`; apply CLSID
  pylons only from registry.
- [Wrong ground unit id string] → Verify against PyDCS `.id` during apply; refuse unknown via
  registry validation.
- [Bombing vs AttackGroup AI behaviour] → Prefer simple Bombing-at-point for v1; verify in ME;
  record LESSONS if switched.
- [Target offset off-map] → Conservative Manston-relative example; ME smoke during accept.
- [Scope creep into air escort / triggers] → Explicit non-goals; empty `enemies` / `triggers`.

## Migration Plan

1. Registry payloads + ground_units + models/validators.
2. Compiler GA path + example YAML.
3. Validation + planning_options + catalog/agent/voice light updates.
4. Golden + refresh; pytest/Ruff green.
5. In-game accept; BACKLOG → done; LESSONS for loadout/target math.

## Open Questions

- Exact example bearing/distance_km: finalize during apply from Channel airport geometry
  (**verify landfall** — short of a coastal field along a sea approach is still water).
- Bombing vs AttackGroup: decide during compiler apply after a quick ME check (default Bombing).
- For every future ground-attack Spec: run the LESSONS land/sea/enemy/practice checklist
  before in-game accept.
