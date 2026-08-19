"""Derived Mission Spec examples for agent prompts and tools.

Source of truth remains ``MissionSpec`` + checked-in ``examples/*.yaml``.
This module projects compact, LLM-friendly examples — not a second schema SoT.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..loader import load_mission_spec
from ..models import MissionSpec, MissionType

_EXAMPLE_FILES: dict[str, str] = {
    MissionType.FREE_FLIGHT.value: "manston_cold_freeflight.yaml",
    MissionType.INTERCEPT.value: "manston_dawn_intercept.yaml",
    MissionType.CAP.value: "manston_cap.yaml",
    MissionType.GROUND_ATTACK.value: "manston_ground_attack.yaml",
    MissionType.ESCORT.value: "manston_escort.yaml",
    MissionType.RECON.value: "manston_recon.yaml",
}

# Preferred examples for get_mission_spec_schema / invent (immersion-first).
_AGENT_EXAMPLE_FILES: dict[str, str] = {
    MissionType.FREE_FLIGHT.value: "manston_freeflight_altitude_speed_gates.yaml",
    MissionType.INTERCEPT.value: "manston_dawn_intercept_radio.yaml",
    MissionType.CAP.value: "manston_cap_narrative.yaml",
    MissionType.GROUND_ATTACK.value: "manston_ground_attack_markers.yaml",
    MissionType.ESCORT.value: "manston_escort_narrative.yaml",
    MissionType.RECON.value: "manston_recon.yaml",
}

_NORMANDY_FREE_FLIGHT_EXAMPLE = "needs_oar_point_cold_freeflight.yaml"
_NORMANDY_CAP_EXAMPLE = "needs_oar_point_cap.yaml"
_NORMANDY_GROUND_ATTACK_EXAMPLE = "needs_oar_point_ground_attack.yaml"
_NORMANDY_INTERCEPT_EXAMPLE = "needs_oar_point_dawn_intercept.yaml"
_NORMANDY_ESCORT_EXAMPLE = "needs_oar_point_escort.yaml"
_NORMANDY_RECON_EXAMPLE = "needs_oar_point_recon.yaml"
_NORMANDY_UNSUPPORTED_COMBAT: frozenset[str] = frozenset()
_CAUCASUS_FREE_FLIGHT_EXAMPLE = "batumi_cold_freeflight.yaml"
_CAUCASUS_CAP_EXAMPLE = "batumi_black_sea_cap.yaml"
_CAUCASUS_GROUND_ATTACK_EXAMPLE = "batumi_kutaisi_ground_attack.yaml"
_CAUCASUS_INTERCEPT_EXAMPLE = "batumi_dawn_intercept.yaml"
_CAUCASUS_ESCORT_EXAMPLE = "batumi_black_sea_escort.yaml"
_CAUCASUS_RECON_EXAMPLE = "batumi_kutaisi_recon.yaml"
_CAUCASUS_UNSUPPORTED_COMBAT: frozenset[str] = frozenset()
_SYRIA_FREE_FLIGHT_EXAMPLE = "incirlik_cold_freeflight.yaml"
_SYRIA_CAP_EXAMPLE = "incirlik_iskenderun_cap.yaml"
_SYRIA_INTERCEPT_EXAMPLE = "incirlik_dawn_intercept.yaml"
_SYRIA_ESCORT_EXAMPLE = "incirlik_iskenderun_escort.yaml"
_SYRIA_GROUND_ATTACK_EXAMPLE = "incirlik_aleppo_ground_attack.yaml"
_SYRIA_RECON_EXAMPLE = "incirlik_aleppo_recon.yaml"
_SYRIA_UNSUPPORTED_COMBAT: frozenset[str] = frozenset()
_NEVADA_FREE_FLIGHT_EXAMPLE = "nellis_cold_freeflight.yaml"
_NEVADA_CAP_EXAMPLE = "nellis_north_range_cap.yaml"
_NEVADA_INTERCEPT_EXAMPLE = "nellis_dawn_intercept.yaml"
_NEVADA_ESCORT_EXAMPLE = "nellis_north_range_escort.yaml"
_NEVADA_GROUND_ATTACK_EXAMPLE = "nellis_creech_ground_attack.yaml"
_NEVADA_RECON_EXAMPLE = "nellis_creech_recon.yaml"
_NEVADA_UNSUPPORTED_COMBAT: frozenset[str] = frozenset()
_FALKLANDS_FREE_FLIGHT_EXAMPLE = "mount_pleasant_cold_freeflight.yaml"
_FALKLANDS_CAP_EXAMPLE = "mount_pleasant_south_atlantic_cap.yaml"
_FALKLANDS_INTERCEPT_EXAMPLE = "mount_pleasant_dawn_intercept.yaml"
_FALKLANDS_ESCORT_EXAMPLE = "mount_pleasant_south_atlantic_escort.yaml"
_FALKLANDS_GROUND_ATTACK_EXAMPLE = "mount_pleasant_east_falkland_ground_attack.yaml"
_FALKLANDS_RECON_EXAMPLE = "mount_pleasant_east_falkland_recon.yaml"
_FALKLANDS_UNSUPPORTED_COMBAT: frozenset[str] = frozenset()
_KOLA_FREE_FLIGHT_EXAMPLE = "bodo_cold_freeflight.yaml"
_KOLA_UNSUPPORTED_COMBAT: frozenset[str] = frozenset(
    {
        MissionType.INTERCEPT.value,
        MissionType.CAP.value,
        MissionType.GROUND_ATTACK.value,
        MissionType.ESCORT.value,
        MissionType.RECON.value,
    }
)

ANTI_PATTERNS: tuple[str, ...] = (
    'top-level "airfield" / "aircraft" (use nested player.aircraft / player.airfield)',
    '"date" as an ISO string like "1944-06-06" (use {"year","month","day"})',
    'enemies like {"type":"intercept_enemy","id":"..."} (use aircraft + count)',
    "objectives nested under cap or strike (objectives is top-level only)",
    "Lua / script / Mist fields inside triggers (typed when/then only; no free-form script)",
    "friendly / same-coalition targets without strike.practice true",
    "inventing bomb CLSIDs (use named player.payload presets from the catalog)",
    (
        "ASW / submerged U-boat hunt (depth charges, sonobuoys, asw mission_type) — "
        "Channel Spitfire only attacks surfaced sea_craft (e.g. Uboat_VIIC)"
    ),
)

_TYPE_NOTES: dict[str, tuple[str, ...]] = {
    MissionType.FREE_FLIGHT.value: (
        (
            "enemies, objectives, and targets must be empty lists; omit cap and strike; "
            "omit player.payload."
        ),
        (
            "optional player.flight: size 2–4, role lead|wingman (default lead), "
            "ai_skill for mates (default Average), join_up (default true — wingman "
            "Follows AI lead + shared route). Omit for solo. Wingman emits a "
            "separate AI lead group plus your Player ship (SP cannot Player-on-slot-2). "
            "See manston_freeflight_flight_lead.yaml / manston_freeflight_flight_wingman.yaml "
            "/ manston_cap_flight_wingman.yaml."
        ),
        (
            "Immersion OK: non-empty triggers/zones for altitude_speed_gates or "
            "sound_flag_chain (see manston_freeflight_altitude_speed_gates.yaml / "
            "manston_freeflight_sound_flags.yaml)."
        ),
    ),
    MissionType.INTERCEPT.value: (
        'enemies must be non-empty; objectives must include {"type":"intercept_enemy"}.',
        "omit the cap and strike blocks; omit player.payload.",
        (
            "optional narrative.enabled true: expands to typed triggers (scramble / "
            "bandits-down win). Requires empty zones/triggers and enemies; conflicts with "
            "hand-authored triggers."
        ),
        (
            "optional late_activation on enemies; trigger actions radio_item_add / "
            "activate_group for F10 difficulty menus (see manston_dawn_intercept_radio)."
        ),
    ),
    MissionType.CAP.value: (
        "nested cap is required (bearing_deg, distance_km, altitude_m, pattern, engagement).",
        'top-level objectives must include {"type":"patrol"}; enemies are optional.',
        "station is airfield-relative bearing/distance — never invent raw map x/y.",
        "omit strike, targets, and player.payload.",
        (
            "optional narrative.enabled true: expands to typed zones/triggers "
            "(push / on-station / bandits-down win). Requires empty zones/triggers and "
            "at least one enemy; conflicts with hand-authored triggers."
        ),
        "optional late_activation on enemies; radio_item_add / activate_group as for intercept.",
    ),
    MissionType.GROUND_ATTACK.value: (
        "nested strike is required (bearing_deg, distance_km, altitude_m).",
        (
            "player.payload is required (named preset; prefer spitfire_2x250_slipper for "
            "Channel crossings)."
        ),
        (
            "targets must be non-empty. Call list_mission_options (strike_target_class / "
            "ground_ai_preset / channel_place) then list_strike_targets before inventing "
            "targets[]; prefer returned exact DCS unit_ids and allowlisted ai_preset only. "
            "Cue table: inland truck/convoy → soft + path + convoy_transit; flak/AAA → "
            "aaa + static + aaa_alert; mid-Channel under way → sea + patrol + "
            "ship_under_way; harbour/dock → list_strike_targets(domain=sea) + "
            "static + harbour_static (never soft land trucks). Copy "
            "channel_place strike_bearing_deg/strike_distance_km (french coast ~125/76 "
            "inland; mid-Channel ~140/40 water; coastal_harbour ~120/68). Land paths: "
            "prefer 2–3 points from french_coast path_point_deltas near strike "
            "(e.g. 125/76, 128/77, 122/78) — not mid-Channel. Combat: opposing "
            "coalition; land on Axis continent for Channel WWII; water = ships. Practice "
            "(strike.practice true): same-coalition / UK-side targets allowed for "
            "bombing practice narrative."
        ),
        (
            "Surfaced U-boat / sea hunt: use sea_craft ids from list_strike_targets "
            "(e.g. Uboat_VIIC) on mid-Channel water (manston_uboat_hunt.yaml; ~140°/40 km). "
            "Prefer motion: patrol + ai_preset ship_under_way when under way; harbour/dock → "
            "list_strike_targets(domain=sea) + coastal_harbour (~120°/68 km) + static + "
            "harbour_static. Attack while surfaced — not ASW."
        ),
        (
            "Optional targets[].motion: static|patrol|path. Soft vehicles often path/patrol; "
            "AAA stay static. Invent path = prefer 2–3 airfield-relative points from "
            "path_point_deltas (manston_ground_attack_convoy). "
            "Optional speed_kmh within curated unit band; omit for seeded cruise + waypoint jitter. "
            "Moving land groups default Disperse Under Fire 180s (disperse_under_fire_s; 0=off)."
        ),
        (
            "Optional targets[].ai_preset (convoy_transit|aaa_alert|ship_under_way|harbour_static) "
            "and/or ai {roe,alarm_state,engage_air_weapons,restrict_targets,interception_range} "
            "plus land move_formation (off_road|on_road|rank|cone|vee|…). Soft: no interception_range; "
            "sea: no move_formation/restrict_targets. ME lists ≠ capability. "
            "Examples: manston_ground_attack_flak_alert, convoy with convoy_transit."
        ),
        'objectives must include {"type":"attack_ground"}; enemies must be empty.',
        "omit the cap block. Pilot jettisons the slipper tank in the cockpit before attack.",
        (
            "optional narrative.enabled true: expands to typed zones/triggers (push / "
            "ingress / targets-down win via target_dead). Requires empty zones/triggers, "
            "strike, and targets; conflicts with hand-authored triggers."
        ),
    ),
    MissionType.ESCORT.value: (
        "nested escort is required (bearing_deg, distance_km, altitude_m, engagement).",
        (
            "package must be non-empty and same coalition as the player (friendly only); "
            "e.g. MosquitoFBMkVI."
        ),
        'objectives must include {"type":"escort_package"}; enemies optional (bounce).',
        "destination is airfield-relative bearing/distance — never invent raw map x/y.",
        "omit strike, targets, cap, recon, and player.payload.",
        (
            "optional narrative.enabled true: expands to typed zones/triggers (push / "
            "with-package / bounce-down win). Requires empty zones/triggers, escort, "
            "package, and enemies; conflicts with hand-authored triggers."
        ),
    ),
    MissionType.RECON.value: (
        ("nested recon is required (bearing_deg, distance_km, altitude_m, radius_m?, mark?)."),
        'objectives must include {"type":"recon_area"}; omit player.payload.',
        (
            "optional targets = observe-only enemy contacts (opposing coalition). "
            "Call list_mission_options then list_strike_targets before inventing "
            "contacts; prefer returned exact unit_ids. Same cue table as GA "
            "(convoy/flak/U-boat/harbour → class + motion + ai_preset). Copy "
            "channel_place aoi_*/strike_* geometry (mid-Channel ~140/40). Harbour → "
            "list_strike_targets(domain=sea) + coastal_harbour. Empty "
            "targets = area recon."
        ),
        (
            "Surfaced U-boat locate: mid-Channel water + Uboat_VIIC contact "
            "(manston_uboat_recon.yaml; ~140°/40 km); prefer motion: patrol + ai_preset "
            "ship_under_way when under way; harbour → list_strike_targets(domain=sea) + "
            "coastal_harbour + static + harbour_static; weapons hold — not depth-charge ASW."
        ),
        (
            "Optional targets[].motion (static|patrol|path) same as ground_attack — "
            "observe-only contacts may still move. Optional ai_preset/ai/move_formation "
            "same class rules as GA (e.g. ship_under_way on U-boat)."
        ),
        "AOI is airfield-relative — never invent raw map x/y. enemies must be empty.",
        "omit strike, cap, escort, package. zones/triggers must stay empty (find beat injected).",
        "Not a bomb run — weapons hold; report AOI then RTB.",
    ),
}

_COMMON_NOTES: tuple[str, ...] = (
    (
        'schema_version must be "1"; theatre is an offerable id '
        "(TheChannel for combat; Normandy all six types at NeedsOarPoint; "
        "Caucasus all six types at Batumi; Syria all six types at Incirlik; "
        "Nevada all six types at Nellis; "
        "Falklands all six types at Mount Pleasant)."
    ),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    (
        "Optional player.flight on any mission type: {size: 2-4, role: lead|wingman, "
        "ai_skill, join_up, orders?, discipline?}; omit for solo. Human skill must stay Player; mates use "
        "ai_skill. Wingman join_up (default true) → Follow AI lead + shared route. "
        "Optional orders: curated list [rejoin|engage|orbit|rtb|break] → F10 Section:… "
        "menus (list_mission_options family player_flight_order). "
        "Optional discipline (wingman+join_up only): {radius_m?, soft_after_s?, "
        "hard_after_s?, hard: message_end|mission_end|section_rtb} — omit = off; "
        "{} = defaults (family player_flight_discipline)."
    ),
    (
        "Optional top-level failures list (omit/[] = none): each entry "
        "{id, start_after_s, probability?, random_pause_s?} with curated Channel "
        "SpitfireLFMkIX failure ids only (ENG0_MAGNETO0, radiator leaks, control rod "
        "damage, fuel/hydraulic pumps — see list_mission_options family "
        "aircraft_failure and aircraft_failures.yaml). Compiler writes the ME "
        "Failures panel table (After/Within minutes; Within 0 never fires). "
        "Never invent ids or Lua. Example: manston_freeflight_magneto_failure.yaml."
    ),
    (
        "Optional typed zones/triggers (no Lua): conditions time_more|flag_is|"
        "flag_equals|flag_more|flag_less|time_since_flag|unit_dead|target_dead|"
        "group_life_less|coalition_in_zone|unit_altitude_higher|unit_altitude_lower|"
        "unit_speed_higher|unit_speed_lower; actions message|set_flag|set_flag_value|"
        "inc_flag|set_flag_random|sound|mission_end|radio_item_add|radio_item_remove|"
        "activate_group|deactivate_group|mark|smoke. set_flag_random sets a numeric "
        "flag to a uniform integer in [min, max] (ME Set Flag Random). group_life_less "
        "uses enemy_index or target_index "
        "plus percent 1–100 (remaining group life). mark uses zone name + text (F10 "
        "map mark); smoke uses zone name + curated color "
        "(green|red|white|orange|blue). unit_altitude_* use altitude_m and optional "
        "agl (default true, player unit only); unit_speed_* use speed_kmh (player "
        "only). sound uses curated asset_id only "
        "(no paths). enemies/targets may set late_activation true (dormant until "
        "activate_group). Compiler emits native ME trigger tables for validated "
        "graphs. Optional narrative.enabled (cap|intercept|escort|ground_attack) "
        "expands a curated pack into that vocabulary when zones/triggers are empty. "
        "Optional dynamics (fixed|live|choose|hybrid + pools) expands play-time "
        "dice/F10/activate graphs the same way; XOR with narrative.enabled."
    ),
    "Fill DCS ids and airfield names from tools/prefs — examples are Channel templates.",
    (
        "For creative immersion/challenge: list_mission_options families "
        "mission_inspiration (advisory patterns) and mission_behaviour (supported "
        "recipes with meta.recipe / Spec types / example paths). For co-design of "
        "play-time variation, strike targets, or Channel places: also consult "
        "dynamics_mode, strike_target_class, and channel_place (dynamics_mode maps "
        "to Spec dynamics.mode + pools). For concrete unit ids call list_strike_targets; "
        "do not invent unit/ship ids. For training "
        "system failures: aircraft_failure (curated Spitfire Set Failure ids → Spec "
        "failures). Optionally "
        "research_guidance(focus=mission_design) and list_installed_campaigns "
        "(Doc filenames by default; include_doc_text for cached PDF excerpts). "
        "Map ideas onto packaged "
        "behaviours only — never Lua or .miz→Spec import. Immersion examples: "
        "manston_freeflight_altitude_speed_gates.yaml, "
        "manston_dawn_intercept_radio.yaml, "
        "manston_dawn_intercept_dynamics_live.yaml / "
        "manston_dawn_intercept_dynamics_hybrid.yaml, "
        "manston_cap_narrative.yaml / manston_dawn_intercept_narrative.yaml / "
        "manston_ground_attack_narrative.yaml / manston_escort_narrative.yaml, "
        "manston_freeflight_sound_flags.yaml, "
        "manston_ground_attack_markers.yaml / manston_ground_attack_life_less.yaml."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Caucasus Stage A: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_CAUCASUS_FF_NOTES: tuple[str, ...] = (
    (
        "Caucasus invent is all six types: airfield Batumi, "
        "Su-25T, sunny_clear, Georgia blue. CAP, intercept, and escort station 270° / 40 km / 4000 m west "
        "over the Black Sea (not Manston 135/25, not Cherbourg 180/63, not Hawkinge, not escort 120/55). "
        "Ground attack and recon AOI 43° / 110 km inland past Kutaisi (not CAP 270/40). "
        "Do not copy Channel or "
        "Normandy geometry onto Caucasus."
    ),
    ('schema_version must be "1"; theatre is Caucasus (all six types at Batumi).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    (
        "enemies, objectives, and targets must be empty lists; omit cap and strike; "
        "omit player.payload. Omit failures — modern Caucasus has no curated "
        "aircraft_failure shelf."
    ),
    (
        "optional player.flight: size 2–4, role lead|wingman (default lead), "
        "ai_skill for mates (default Average), join_up (default true — wingman "
        "Follows AI lead + shared route). Omit for solo. Wingman emits a "
        "separate AI lead group plus your Player ship. Do not copy other-theatre "
        "flight YAML onto Caucasus."
    ),
    (
        "Fill DCS ids from tools/prefs using examples/batumi_cold_freeflight.yaml. "
        "Channel and Normandy example YAML paths do not apply."
    ),
    (
        "Optional typed zones/triggers (no Lua) use the same condition/action "
        "vocabulary; do not copy other-theatre immersion YAML."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_CAUCASUS_CAP_NOTES: tuple[str, ...] = (
    (
        "Caucasus invent is all six types: airfield Batumi, "
        "Su-25T, sunny_clear, Georgia blue. CAP, intercept, and escort station 270° / 40 km / 4000 m west "
        "over the Black Sea (not Manston 135/25, not Cherbourg 180/63, not escort 120/55). "
        "Enemies: Su-25T, country Russia, coalition red (do not default "
        "ThirdReich)."
    ),
    ('schema_version must be "1"; theatre is Caucasus (CAP at Batumi).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player, cap; enemies/objectives default to lists."
    ),
    (
        "Fill DCS ids from tools/prefs using examples/batumi_black_sea_cap.yaml. "
        "Channel and Normandy example YAML paths do not apply."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_CAUCASUS_GA_NOTES: tuple[str, ...] = (
    (
        "Caucasus invent is all six types: airfield Batumi, "
        "Su-25T, sunny_clear, Georgia blue. Strike 43° / 110 km / 2000 m inland "
        "past Kutaisi (not CAP/escort 270/40 which is sea, not Manston 125/76, not "
        "Cherbourg 180/63). Escort station 270° / 40 km (not Channel escort 120/55). "
        "Call list_strike_targets(theatre=Caucasus) for "
        "modern trucks (Ural-375 / GAZ-66 / ZIL-135). Country Russia red. Do "
        "not copy Channel or Normandy geometry onto Caucasus."
    ),
    ('schema_version must be "1"; theatre is Caucasus (ground_attack at Batumi).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested strike is required (bearing_deg, distance_km, altitude_m).",
    (
        "player.payload is required (named preset; prefer su25t_2x_fab250 — "
        "inner pylons 5 and 7 FAB-250). Omit failures — modern Caucasus has no "
        "curated aircraft_failure shelf."
    ),
    (
        "targets must be non-empty land units from list_strike_targets"
        "(theatre=Caucasus). Combat: opposing coalition (Russia red). "
        "Copy kutaisi_inland_strike 43/110. Stopping short (~100 km) is near "
        "Kutaisi field. Fill ids from examples/batumi_kutaisi_ground_attack.yaml."
    ),
    'objectives must include {"type":"attack_ground"}; enemies must be empty.',
    "omit the cap block. Do not copy Channel or Normandy example YAML paths.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_CAUCASUS_INTERCEPT_NOTES: tuple[str, ...] = (
    (
        "Caucasus invent is all six types: airfield Batumi, "
        "Su-25T, sunny_clear, Georgia blue. "
        "Enemies spawn on the Black Sea corridor (270° / 40 km from "
        "Batumi — same station as batumi_black_sea_cap; not Hawkinge / "
        "Dover / Cherbourg). Escort uses the same 270/40 station (not Channel escort 120/55). "
        "Enemies: Su-25T, country Russia, coalition red "
        "(do not default ThirdReich). Do not copy Channel or "
        "Normandy geometry onto Caucasus."
    ),
    ('schema_version must be "1"; theatre is Caucasus (intercept at Batumi).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    'enemies must be non-empty; objectives must include {"type":"intercept_enemy"}.',
    "omit the cap and strike blocks; omit player.payload.",
    "Fill DCS ids from examples/batumi_dawn_intercept.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_CAUCASUS_ESCORT_NOTES: tuple[str, ...] = (
    (
        "Caucasus invent is all six types: airfield Batumi, "
        "Su-25T, sunny_clear, Georgia blue. Package destination is the Black Sea "
        "corridor (270° / 40 km / 4000 m — same station as batumi_black_sea_cap; "
        "not Channel escort 120/55, not Cherbourg 180/63). Friendly package e.g. Su-25T, "
        "country Georgia (PackageFlight defaults to UK). Bounce: Su-25T, country "
        "Russia, coalition red (do not omit country). Do not "
        "copy Channel or Normandy geometry onto Caucasus."
    ),
    ('schema_version must be "1"; theatre is Caucasus (escort at Batumi).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested escort is required (bearing_deg, distance_km, altitude_m, engagement).",
    (
        "package must be non-empty and same coalition as the player (friendly only); "
        "e.g. Su-25T, country Georgia."
    ),
    'objectives must include {"type":"escort_package"}; enemies optional (bounce).',
    "destination is airfield-relative bearing/distance — never invent raw map x/y.",
    "omit strike, targets, cap, recon, and player.payload.",
    "Fill DCS ids from examples/batumi_black_sea_escort.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_CAUCASUS_RECON_NOTES: tuple[str, ...] = (
    (
        "Caucasus invent is all six types: airfield Batumi, "
        "Su-25T, sunny_clear, Georgia blue. Recon AOI is inland past Kutaisi "
        "(43° / 110 km / 2000 m — same land station as kutaisi_inland_strike; "
        "not Manston 125/76, not CAP 270/40 sea). Observe land units from "
        "list_strike_targets(theatre=Caucasus). Weapons hold. Do not copy "
        "Channel or Normandy geometry onto Caucasus."
    ),
    ('schema_version must be "1"; theatre is Caucasus (recon at Batumi).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    ("nested recon is required (bearing_deg, distance_km, altitude_m, radius_m?, mark?)."),
    'objectives must include {"type":"recon_area"}; omit player.payload.',
    (
        "optional targets = observe-only enemy contacts (opposing coalition). "
        "Call list_strike_targets(theatre=Caucasus) for modern trucks "
        "(Ural-375 / GAZ-66 / ZIL-135). Copy kutaisi_inland_strike 43/110. "
        "Country Russia red. Sea craft stay Channel-only."
    ),
    "AOI is airfield-relative — never invent raw map x/y. enemies must be empty.",
    "omit strike, cap, escort, package. zones/triggers must stay empty (find beat injected).",
    "Not a bomb run — weapons hold; report AOI then RTB.",
    "Fill DCS ids from examples/batumi_kutaisi_recon.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Syria: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_SYRIA_FF_NOTES: tuple[str, ...] = (
    (
        "Syria invent is all six types: airfield Incirlik, Su-25T, "
        "sunny_clear, Turkey blue. CAP, intercept, and escort station 180° / 40 km / 4000 m south "
        "over the Gulf of Iskenderun (not Cherbourg 180/63, not Caucasus 270/40, not escort 120/55). "
        "GA/recon AOI 121° / 200 km inland past Aleppo (not CAP 180/40). Do not copy Channel, "
        "Normandy, or Caucasus geometry onto Syria."
    ),
    ('schema_version must be "1"; theatre is Syria (free_flight at Incirlik).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    (
        "enemies, objectives, and targets must be empty lists; omit cap and strike; "
        "omit player.payload. Omit failures — modern Syria has no curated "
        "aircraft_failure shelf."
    ),
    (
        "optional player.flight: size 2–4, role lead|wingman (default lead), "
        "ai_skill for mates (default Average), join_up (default true — wingman "
        "Follows AI lead + shared route). Omit for solo. Wingman emits a "
        "separate AI lead group plus your Player ship. Do not copy other-theatre "
        "flight YAML onto Syria."
    ),
    (
        "Fill DCS ids from tools/prefs using examples/incirlik_cold_freeflight.yaml. "
        "Channel, Normandy, and Caucasus example YAML paths do not apply."
    ),
    (
        "Optional typed zones/triggers (no Lua) use the same condition/action "
        "vocabulary; do not copy other-theatre immersion YAML."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_SYRIA_CAP_NOTES: tuple[str, ...] = (
    (
        "Syria invent is all six types: airfield Incirlik, Su-25T, "
        "sunny_clear, Turkey blue. CAP, intercept, and escort station 180° / 40 km / 4000 m south "
        "over the Gulf of Iskenderun (not Cherbourg 180/63, not Caucasus 270/40, "
        "not Manston 135/25, not escort 120/55). Enemies: Su-25T, country Syria, coalition red "
        "(do not default ThirdReich). GA/recon AOI 121° / 200 km inland past Aleppo (not this CAP 180/40)."
    ),
    ('schema_version must be "1"; theatre is Syria (CAP at Incirlik).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player, cap; enemies/objectives default to lists."
    ),
    (
        "Fill DCS ids from tools/prefs using examples/incirlik_iskenderun_cap.yaml. "
        "Channel, Normandy, and Caucasus example YAML paths do not apply."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_SYRIA_INTERCEPT_NOTES: tuple[str, ...] = (
    (
        "Syria invent is all six types: airfield Incirlik, "
        "Su-25T, sunny_clear, Turkey blue. Enemies spawn on the Gulf of "
        "Iskenderun corridor (180° / 40 km from Incirlik — same station as "
        "incirlik_iskenderun_cap; not Hawkinge / Dover / Cherbourg 180/63 / "
        "Caucasus 270/40 / escort 120/55). "
        "Enemies: Su-25T, country Syria, coalition red (do not default "
        "ThirdReich). GA/recon AOI 121° / 200 km inland past Aleppo (not this CAP 180/40)."
    ),
    ('schema_version must be "1"; theatre is Syria (intercept at Incirlik).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    'enemies must be non-empty; objectives must include {"type":"intercept_enemy"}.',
    "omit the cap and strike blocks; omit player.payload.",
    "Fill DCS ids from examples/incirlik_dawn_intercept.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_SYRIA_ESCORT_NOTES: tuple[str, ...] = (
    (
        "Syria invent is all six types: airfield Incirlik, "
        "Su-25T, sunny_clear, Turkey blue. Package destination is the Gulf of "
        "Iskenderun corridor (180° / 40 km / 4000 m — same station as "
        "incirlik_iskenderun_cap; not Channel escort 120/55, not Cherbourg 180/63, "
        "not Batumi 270/40). Friendly package e.g. Su-25T, "
        "country Turkey (PackageFlight defaults to UK). Bounce: Su-25T, country "
        "Syria, coalition red (do not omit country; theatre id Syria ≠ country Syria). "
        "GA/recon AOI 121° / 200 km inland past Aleppo (not this escort 180/40). "
        "Do not copy Channel, Normandy, or Caucasus "
        "geometry onto Syria."
    ),
    ('schema_version must be "1"; theatre is Syria (escort at Incirlik).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested escort is required (bearing_deg, distance_km, altitude_m, engagement).",
    (
        "package must be non-empty and same coalition as the player (friendly only); "
        "e.g. Su-25T, country Turkey."
    ),
    'objectives must include {"type":"escort_package"}; enemies optional (bounce).',
    "destination is airfield-relative bearing/distance — never invent raw map x/y.",
    "omit strike, targets, cap, recon, and player.payload.",
    "Fill DCS ids from examples/incirlik_iskenderun_escort.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_SYRIA_GA_NOTES: tuple[str, ...] = (
    (
        "Syria invent is all six types: airfield Incirlik, "
        "Su-25T, sunny_clear, Turkey blue. Strike 121° / 200 km / 2000 m inland "
        "past Aleppo (not CAP/escort 180/40 which is sea, not Kutaisi 43/110, not "
        "Maupertus 180/133, not Manston 125/76). Call list_strike_targets(theatre=Syria) for "
        "modern trucks (Ural-375 / GAZ-66 / ZIL-135). Country Syria red. Do "
        "not copy Channel, Normandy, or Caucasus geometry onto Syria."
    ),
    ('schema_version must be "1"; theatre is Syria (ground_attack at Incirlik).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested strike is required (bearing_deg, distance_km, altitude_m).",
    (
        "player.payload is required (named preset; prefer su25t_2x_fab250 — "
        "inner pylons 5 and 7 FAB-250). Omit failures — modern Syria has no "
        "curated aircraft_failure shelf."
    ),
    (
        "targets must be non-empty land units from list_strike_targets"
        "(theatre=Syria). Combat: opposing coalition (Syria red). "
        "Copy aleppo_inland_strike 121/200. Stopping short (~185 km) is near "
        "Aleppo field. Fill ids from examples/incirlik_aleppo_ground_attack.yaml."
    ),
    'objectives must include {"type":"attack_ground"}; enemies must be empty.',
    "omit the cap block. Do not copy Channel, Normandy, or Caucasus example YAML paths.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_SYRIA_RECON_NOTES: tuple[str, ...] = (
    (
        "Syria invent is all six types: airfield Incirlik, "
        "Su-25T, sunny_clear, Turkey blue. Recon AOI is inland past Aleppo "
        "(121° / 200 km / 2000 m — same land station as aleppo_inland_strike; "
        "not Manston 125/76, not Kutaisi 43/110, not CAP 180/40 sea). Observe "
        "land units from list_strike_targets(theatre=Syria). Weapons hold. Do "
        "not copy Channel, Normandy, or Caucasus geometry onto Syria."
    ),
    ('schema_version must be "1"; theatre is Syria (recon at Incirlik).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    ("nested recon is required (bearing_deg, distance_km, altitude_m, radius_m?, mark?)."),
    'objectives must include {"type":"recon_area"}; omit player.payload.',
    (
        "optional targets = observe-only enemy contacts (opposing coalition). "
        "Call list_strike_targets(theatre=Syria) for modern trucks "
        "(Ural-375 / GAZ-66 / ZIL-135). Copy aleppo_inland_strike 121/200. "
        "Country Syria red. Sea craft stay Channel-only."
    ),
    "AOI is airfield-relative — never invent raw map x/y. enemies must be empty.",
    "omit strike, cap, escort, package. zones/triggers must stay empty (find beat injected).",
    "Not a bomb run — weapons hold; report AOI then RTB.",
    "Fill DCS ids from examples/incirlik_aleppo_recon.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Nevada Stage A: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_NEVADA_FF_NOTES: tuple[str, ...] = (
    (
        "Nevada invent is all six types: airfield Nellis, Su-25T, "
        "sunny_clear, USA blue. CAP/intercept/escort station 350° / 40 km / 4000 m north over "
        "desert north-range land (not 180/40, not 270/40, not 180/63, not "
        "Creech 303/40). GA/recon AOI 303° / 85 km inland past Creech (not CAP 350/40). "
        "Do not copy Channel, Normandy, Caucasus, or Syria geometry onto Nevada."
    ),
    ('schema_version must be "1"; theatre is Nevada (free_flight at Nellis).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    (
        "enemies, objectives, and targets must be empty lists; omit cap and strike; "
        "omit player.payload. Omit failures — modern Nevada has no curated "
        "aircraft_failure shelf."
    ),
    (
        "optional player.flight: size 2–4, role lead|wingman (default lead), "
        "ai_skill for mates (default Average), join_up (default true — wingman "
        "Follows AI lead + shared route). Omit for solo. Wingman emits a "
        "separate AI lead group plus your Player ship. Do not copy other-theatre "
        "flight YAML onto Nevada."
    ),
    (
        "Fill DCS ids from tools/prefs using examples/nellis_cold_freeflight.yaml. "
        "Channel, Normandy, Caucasus, and Syria example YAML paths do not apply."
    ),
    (
        "Optional typed zones/triggers (no Lua) use the same condition/action "
        "vocabulary; do not copy other-theatre immersion YAML."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_NEVADA_CAP_NOTES: tuple[str, ...] = (
    (
        "Nevada invent is all six types: airfield Nellis, Su-25T, "
        "sunny_clear, USA blue. CAP station 350° / 40 km / 4000 m north over "
        "desert north-range land (not Incirlik 180/40, not Batumi 270/40, not "
        "Cherbourg 180/63, not Manston 135/25, not Creech 303/40). Enemies: "
        "Su-25T, country Russia, coalition red (do not default ThirdReich; "
        "do not put USA on red). GA/recon AOI 303° / 85 km inland past Creech "
        "(not CAP 350/40)."
    ),
    ('schema_version must be "1"; theatre is Nevada (CAP at Nellis).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player, cap; enemies/objectives default to lists."
    ),
    (
        "Fill DCS ids from tools/prefs using examples/nellis_north_range_cap.yaml. "
        "Channel, Normandy, Caucasus, and Syria example YAML paths do not apply."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Nevada intercept: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_NEVADA_INTERCEPT_NOTES: tuple[str, ...] = (
    (
        "Nevada invent is all six types: airfield Nellis, "
        "Su-25T, sunny_clear, USA blue. Enemies spawn on the desert north-range "
        "corridor (350° / 40 km from Nellis — same station as "
        "nellis_north_range_cap; not Hawkinge / Dover / Syria 180/40 / "
        "Caucasus 270/40 / Cherbourg 180/63). "
        "Enemies: Su-25T, country Russia, coalition red (do not default "
        "ThirdReich; do not put USA on red). GA/recon AOI 303° / 85 km inland "
        "past Creech (not CAP 350/40)."
    ),
    ('schema_version must be "1"; theatre is Nevada (intercept at Nellis).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    'enemies must be non-empty; objectives must include {"type":"intercept_enemy"}.',
    "omit the cap and strike blocks; omit player.payload.",
    "Fill DCS ids from examples/nellis_dawn_intercept.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Nevada escort: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_NEVADA_ESCORT_NOTES: tuple[str, ...] = (
    (
        "Nevada invent is all six types: airfield Nellis, "
        "Su-25T, sunny_clear, USA blue. Package destination is the desert "
        "north-range corridor (350° / 40 km / 4000 m — same station as "
        "nellis_north_range_cap; not Channel escort 120/55, not Incirlik 180/40, "
        "not Batumi 270/40, not Cherbourg 180/63). Friendly package e.g. Su-25T, "
        "country USA (PackageFlight defaults to UK). Bounce: Su-25T, country "
        "Russia, coalition red (do not default ThirdReich; do not put USA on red). "
        "GA/recon AOI 303° / 85 km inland past Creech (not CAP 350/40). "
        "Do not copy Channel, Normandy, Caucasus, or "
        "Syria geometry onto Nevada."
    ),
    ('schema_version must be "1"; theatre is Nevada (escort at Nellis).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested escort is required (bearing_deg, distance_km, altitude_m, engagement).",
    (
        "package must be non-empty and same coalition as the player (friendly only); "
        "e.g. Su-25T, country USA."
    ),
    'objectives must include {"type":"escort_package"}; enemies optional (bounce).',
    "destination is airfield-relative bearing/distance — never invent raw map x/y.",
    "omit strike, targets, cap, recon, and player.payload.",
    "Fill DCS ids from examples/nellis_north_range_escort.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Nevada GA: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_NEVADA_GA_NOTES: tuple[str, ...] = (
    (
        "Nevada invent is all six types: "
        "airfield Nellis, Su-25T, sunny_clear, USA blue. Strike 303° / 85 km / "
        "2000 m inland past Creech (not CAP/escort 350/40, not Aleppo 121/200, "
        "not Kutaisi 43/110, not Manston 125/76). Call list_strike_targets"
        "(theatre=Nevada) for modern trucks (Ural-375 / GAZ-66 / ZIL-135). "
        "Country Russia red. Do not copy Channel, Normandy, Caucasus, or Syria "
        "geometry onto Nevada."
    ),
    ('schema_version must be "1"; theatre is Nevada (ground_attack at Nellis).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested strike is required (bearing_deg, distance_km, altitude_m).",
    (
        "player.payload is required (named preset; prefer su25t_2x_fab250 — "
        "inner pylons 5 and 7 FAB-250). Omit failures — modern Nevada has no "
        "curated aircraft_failure shelf."
    ),
    (
        "targets must be non-empty land units from list_strike_targets"
        "(theatre=Nevada). Combat: opposing coalition (Russia red). "
        "Copy creech_range_strike 303/85. Stopping short (~70 km) is near "
        "Creech field. Fill ids from examples/nellis_creech_ground_attack.yaml."
    ),
    'objectives must include {"type":"attack_ground"}; enemies must be empty.',
    "omit the cap block. Do not copy Channel, Normandy, Caucasus, or Syria example YAML paths.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Nevada recon: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_NEVADA_RECON_NOTES: tuple[str, ...] = (
    (
        "Nevada invent is all six types: airfield Nellis, "
        "Su-25T, sunny_clear, USA blue. Recon AOI is inland past Creech "
        "(303° / 85 km / 2000 m — same land station as creech_range_strike; "
        "not Manston 125/76, not Aleppo 121/200, not Kutaisi 43/110, not CAP "
        "350/40 north-range). Observe land units from "
        "list_strike_targets(theatre=Nevada). Weapons hold. Do not copy "
        "Channel, Normandy, Caucasus, or Syria geometry onto Nevada."
    ),
    ('schema_version must be "1"; theatre is Nevada (recon at Nellis).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    ("nested recon is required (bearing_deg, distance_km, altitude_m, radius_m?, mark?)."),
    'objectives must include {"type":"recon_area"}; omit player.payload.',
    (
        "optional targets = observe-only enemy contacts (opposing coalition). "
        "Call list_strike_targets(theatre=Nevada) for modern trucks "
        "(Ural-375 / GAZ-66 / ZIL-135). Copy creech_range_strike 303/85. "
        "Country Russia red. Sea craft stay Channel-only."
    ),
    "AOI is airfield-relative — never invent raw map x/y. enemies must be empty.",
    "omit strike, cap, escort, package. zones/triggers must stay empty (find beat injected).",
    "Not a bomb run — weapons hold; report AOI then RTB.",
    "Fill DCS ids from examples/nellis_creech_recon.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Kola Stage A: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_KOLA_FF_NOTES: tuple[str, ...] = (
    (
        "Kola invent is free_flight only: airfield Bodo, Su-25T, sunny_clear, "
        "Norway blue. Refuse intercept/cap/ground_attack/escort/recon. Do not copy "
        "Channel, Normandy, Caucasus, Syria, Nevada, or Falklands geometry onto Kola."
    ),
    ('schema_version must be "1"; theatre is Kola (free_flight at Bodo).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    (
        "enemies, objectives, and targets must be empty lists; omit cap and strike; "
        "omit player.payload. Omit failures — modern Kola has no curated "
        "aircraft_failure shelf."
    ),
    (
        "optional player.flight: size 2–4, role lead|wingman (default lead), "
        "ai_skill for mates (default Average), join_up (default true — wingman "
        "Follows AI lead + shared route). Omit for solo. Wingman emits a "
        "separate AI lead group plus your Player ship. Do not copy other-theatre "
        "flight YAML onto Kola."
    ),
    (
        "Fill DCS ids from tools/prefs using examples/bodo_cold_freeflight.yaml. "
        "Channel, Normandy, Caucasus, Syria, Nevada, and Falklands example YAML "
        "paths do not apply."
    ),
    (
        "Optional typed zones/triggers (no Lua) use the same condition/action "
        "vocabulary; do not copy other-theatre immersion YAML."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Falklands Stage C: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_FALKLANDS_FF_NOTES: tuple[str, ...] = (
    (
        "Falklands invent is all six types: airfield "
        "MountPleasant, Su-25T, sunny_clear, UK blue. CAP/intercept/escort station "
        "150° / 40 km / 4000 m SSE over the South Atlantic. GA/recon AOI 269° / 21 km "
        "inland short of Goose Green (not CAP 150/40). Do not copy Channel, Normandy, "
        "Caucasus, Syria, or Nevada geometry onto Falklands."
    ),
    ('schema_version must be "1"; theatre is Falklands (all six types at Mount Pleasant).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    (
        "enemies, objectives, and targets must be empty lists; omit cap and strike; "
        "omit player.payload. Omit failures — modern Falklands has no curated "
        "aircraft_failure shelf."
    ),
    (
        "optional player.flight: size 2–4, role lead|wingman (default lead), "
        "ai_skill for mates (default Average), join_up (default true — wingman "
        "Follows AI lead + shared route). Omit for solo. Wingman emits a "
        "separate AI lead group plus your Player ship. Do not copy other-theatre "
        "flight YAML onto Falklands."
    ),
    (
        "Fill DCS ids from tools/prefs using examples/mount_pleasant_cold_freeflight.yaml. "
        "Channel, Normandy, Caucasus, Syria, and Nevada example YAML paths do not apply."
    ),
    (
        "Optional typed zones/triggers (no Lua) use the same condition/action "
        "vocabulary; do not copy other-theatre immersion YAML."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_FALKLANDS_CAP_NOTES: tuple[str, ...] = (
    (
        "Falklands invent is all six types: airfield "
        "MountPleasant, Su-25T, sunny_clear, UK blue. CAP station 150° / 40 km "
        "/ 4000 m SSE over the South Atlantic (not Nellis 350/40, not Incirlik "
        "180/40, not Batumi 270/40, not Cherbourg 180/63, not Manston 135/25). "
        "Enemies: Su-25T, country Argentina, coalition red (do not default "
        "ThirdReich; do not put UK on red). GA/recon AOI 269° / 21 km inland short of "
        "Goose Green (not CAP 150/40). "
        "Chile is deferred. Port Stanley is not a CAP home."
    ),
    ('schema_version must be "1"; theatre is Falklands (CAP at Mount Pleasant).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player, cap; enemies/objectives default to lists."
    ),
    (
        "Fill DCS ids from tools/prefs using examples/mount_pleasant_south_atlantic_cap.yaml. "
        "Channel, Normandy, Caucasus, Syria, and Nevada example YAML paths do not apply."
    ),
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Falklands intercept: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_FALKLANDS_INTERCEPT_NOTES: tuple[str, ...] = (
    (
        "Falklands invent is all six types: airfield "
        "MountPleasant, Su-25T, sunny_clear, UK blue. Enemies spawn on the "
        "South Atlantic corridor (150° / 40 km from Mount Pleasant — same "
        "station as mount_pleasant_south_atlantic_cap; not Hawkinge / Dover / "
        "Nellis 350/40 / Incirlik 180/40 / Caucasus 270/40 / Cherbourg 180/63). "
        "Enemies: Su-25T, country Argentina, coalition red (do not default "
        "ThirdReich; do not put UK on red). GA/recon AOI 269° / 21 km inland short of "
        "Goose Green (not CAP 150/40). "
        "Chile is deferred. Port Stanley is not a CAP home."
    ),
    ('schema_version must be "1"; theatre is Falklands (intercept at Mount Pleasant).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    'enemies must be non-empty; objectives must include {"type":"intercept_enemy"}.',
    "omit the cap and strike blocks; omit player.payload.",
    "Fill DCS ids from examples/mount_pleasant_dawn_intercept.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Falklands escort: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_FALKLANDS_ESCORT_NOTES: tuple[str, ...] = (
    (
        "Falklands invent is all six types: airfield "
        "MountPleasant, Su-25T, sunny_clear, UK blue. Package destination is the "
        "South Atlantic corridor (150° / 40 km / 4000 m — same station as "
        "mount_pleasant_south_atlantic_cap; not Channel escort 120/55, not Nellis "
        "350/40, not Incirlik 180/40, not Batumi 270/40, not Cherbourg 180/63). "
        "Friendly package e.g. Su-25T, country UK (PackageFlight defaults to UK — "
        "still set explicitly). Bounce: Su-25T, country Argentina, coalition red "
        "(do not default ThirdReich; do not put UK on red). GA/recon AOI 269° / 21 km "
        "inland short of Goose Green (not CAP 150/40). Chile is deferred. Port "
        "Stanley is not a CAP home."
    ),
    ('schema_version must be "1"; theatre is Falklands (escort at Mount Pleasant).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested escort is required (bearing_deg, distance_km, altitude_m, engagement).",
    (
        "package must be non-empty and same coalition as the player (friendly only); "
        "e.g. Su-25T, country UK."
    ),
    'objectives must include {"type":"escort_package"}; enemies optional (bounce).',
    "destination is airfield-relative bearing/distance — never invent raw map x/y.",
    "omit strike, targets, cap, recon, and player.payload.",
    "Fill DCS ids from examples/mount_pleasant_south_atlantic_escort.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Falklands GA: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_FALKLANDS_GA_NOTES: tuple[str, ...] = (
    (
        "Falklands invent is all six types: "
        "airfield MountPleasant, Su-25T, sunny_clear, UK blue. Strike 269° / 21 km / "
        "2000 m inland short of Goose Green (not CAP/escort 150/40, not 269/36 near "
        "Goose Green, not 269/51 Sound sea, not Nevada 303/85, not Aleppo 121/200, "
        "not Kutaisi 43/110, not Manston 125/76). Call list_strike_targets"
        "(theatre=Falklands) for modern trucks (Ural-375 / GAZ-66 / ZIL-135). "
        "Country Argentina red. Do not copy Channel, Normandy, Caucasus, Syria, or "
        "Nevada geometry onto Falklands. Recon AOI uses the same 269/21 station."
    ),
    ('schema_version must be "1"; theatre is Falklands (ground_attack at Mount Pleasant).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested strike is required (bearing_deg, distance_km, altitude_m).",
    (
        "player.payload is required (named preset; prefer su25t_2x_fab250 — "
        "inner pylons 5 and 7 FAB-250). Omit failures — modern Falklands has no "
        "curated aircraft_failure shelf."
    ),
    (
        "targets must be non-empty land units from list_strike_targets"
        "(theatre=Falklands). Combat: opposing coalition (Argentina red). "
        "Copy east_falkland_inland_strike 269/21. Stopping at ~36 km is near "
        "Goose Green field; 51 km is Sound water. Fill ids from "
        "examples/mount_pleasant_east_falkland_ground_attack.yaml."
    ),
    'objectives must include {"type":"attack_ground"}; enemies must be empty.',
    "omit the cap block. Do not copy Channel, Normandy, Caucasus, Syria, or Nevada example YAML paths.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

# Falklands recon: do not concatenate _COMMON_NOTES / _TYPE_NOTES (those cite
# Manston YAML, Spitfire failures, and channel_place as templates to copy).
_FALKLANDS_RECON_NOTES: tuple[str, ...] = (
    (
        "Falklands invent is all six types: airfield MountPleasant, "
        "Su-25T, sunny_clear, UK blue. Recon AOI is inland short of Goose Green "
        "(269° / 21 km / 2000 m — same land station as east_falkland_inland_strike; "
        "not Manston 125/76, not Aleppo 121/200, not Kutaisi 43/110, not Nevada "
        "303/85, not CAP 150/40 South Atlantic). Observe land units from "
        "list_strike_targets(theatre=Falklands). Weapons hold. Do not copy "
        "Channel, Normandy, Caucasus, Syria, or Nevada geometry onto Falklands."
    ),
    ('schema_version must be "1"; theatre is Falklands (recon at Mount Pleasant).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    ("nested recon is required (bearing_deg, distance_km, altitude_m, radius_m?, mark?)."),
    'objectives must include {"type":"recon_area"}; omit player.payload.',
    (
        "optional targets = observe-only enemy contacts (opposing coalition). "
        "Call list_strike_targets(theatre=Falklands) for modern trucks "
        "(Ural-375 / GAZ-66 / ZIL-135). Copy east_falkland_inland_strike 269/21. "
        "Country Argentina red. Sea craft stay Channel-only."
    ),
    "AOI is airfield-relative — never invent raw map x/y. enemies must be empty.",
    "omit strike, cap, escort, package. zones/triggers must stay empty (find beat injected).",
    "Not a bomb run — weapons hold; report AOI then RTB.",
    "Fill DCS ids from examples/mount_pleasant_east_falkland_recon.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_MT_IN_JSON = re.compile(r'"mission_type"\s*:\s*"([a-z_]+)"')
_THEATRE_IN_JSON = re.compile(r'"theatre"\s*:\s*"([A-Za-z0-9_]+)"')
_AIRFIELD_IN_JSON = re.compile(r'"airfield"\s*:\s*"([A-Za-z0-9_]+)"')
_SCHEMA_THEATRES = frozenset(
    {"TheChannel", "Normandy", "Caucasus", "Syria", "Nevada", "Falklands", "Kola"}
)


@dataclass(frozen=True)
class SpecSchemaView:
    mission_type: str
    example: dict[str, Any]
    notes: tuple[str, ...]
    anti_patterns: tuple[str, ...] = ANTI_PATTERNS


def examples_dir() -> Path:
    """Repo ``examples/`` directory (…/src/dcs_miz_planner/agent → parents[3])."""
    return Path(__file__).resolve().parents[3] / "examples"


def supported_mission_types() -> tuple[str, ...]:
    return tuple(_EXAMPLE_FILES.keys())


def build_spec_schema(mission_type: str, theatre: str | None = None) -> SpecSchemaView:
    """Load and validate the packaged example for ``mission_type`` (immersion-first).

    Default / TheChannel stubs stay Manston. ``theatre=Normandy`` uses
    NeedsOarPoint for all six mission types. ``theatre=Caucasus`` uses Batumi
    for all six mission types. ``theatre=Syria`` uses Incirlik for
    all six mission types. ``theatre=Nevada`` uses Nellis for all six
    mission types (CAP/intercept/escort 350° / 40 km desert north-range;
    GA/recon 303° / 85 km inland past Creech). ``theatre=Falklands`` uses
    Mount Pleasant for all six mission types
    (CAP/intercept/escort 150° / 40 km South Atlantic; GA/recon 269° / 21 km inland
    short of Goose Green). Falklands recon uses the East Falkland inland example
    (no Manston / NeedsOarPoint / Batumi / Incirlik / Nellis combat skeleton).
    ``theatre=Kola`` uses Bodo for free_flight only (combat types raise).
    """
    key = (mission_type or "").strip()
    if key not in _EXAMPLE_FILES:
        allowed = ", ".join(supported_mission_types())
        raise ValueError(f"Unsupported mission_type {mission_type!r}; expected one of: {allowed}")
    theatre_id = (theatre or "").strip() or None
    if theatre_id == "Kola":
        if key in _KOLA_UNSUPPORTED_COMBAT:
            raise ValueError(
                f"Combat mission_type {key!r} is not supported for theatre Kola; "
                "use free_flight at Bodo or theatre TheChannel"
            )
        filename = _KOLA_FREE_FLIGHT_EXAMPLE
        path = examples_dir() / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing Spec example for {key}: {path}")
        spec = load_mission_spec(path)
        if spec.mission_type.value != key:
            raise ValueError(
                f"Example {path.name} has mission_type {spec.mission_type.value!r}, "
                f"expected {key!r}"
            )
        example = json.loads(spec.model_dump_json())
        MissionSpec.model_validate(example)
        notes = _notes_for(key, theatre_id)
        return SpecSchemaView(mission_type=key, example=example, notes=notes)

    if theatre_id == "Falklands":
        if key in _FALKLANDS_UNSUPPORTED_COMBAT:
            raise ValueError(
                f"Combat mission_type {key!r} is not supported for theatre Falklands; "
                "use a Falklands-supported type at Mount Pleasant or theatre TheChannel"
            )
        if key == MissionType.CAP.value:
            filename = _FALKLANDS_CAP_EXAMPLE
        elif key == MissionType.INTERCEPT.value:
            filename = _FALKLANDS_INTERCEPT_EXAMPLE
        elif key == MissionType.ESCORT.value:
            filename = _FALKLANDS_ESCORT_EXAMPLE
        elif key == MissionType.GROUND_ATTACK.value:
            filename = _FALKLANDS_GROUND_ATTACK_EXAMPLE
        elif key == MissionType.RECON.value:
            filename = _FALKLANDS_RECON_EXAMPLE
        else:
            filename = _FALKLANDS_FREE_FLIGHT_EXAMPLE
        path = examples_dir() / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing Spec example for {key}: {path}")
        spec = load_mission_spec(path)
        if spec.mission_type.value != key:
            raise ValueError(
                f"Example {path.name} has mission_type {spec.mission_type.value!r}, "
                f"expected {key!r}"
            )
        example = json.loads(spec.model_dump_json())
        MissionSpec.model_validate(example)
        notes = _notes_for(key, theatre_id)
        return SpecSchemaView(mission_type=key, example=example, notes=notes)

    if theatre_id == "Nevada":
        if key in _NEVADA_UNSUPPORTED_COMBAT:
            raise ValueError(
                f"Combat mission_type {key!r} is not supported for theatre Nevada; "
                "use a Nevada-supported type at Nellis or theatre TheChannel"
            )
        if key == MissionType.CAP.value:
            filename = _NEVADA_CAP_EXAMPLE
        elif key == MissionType.INTERCEPT.value:
            filename = _NEVADA_INTERCEPT_EXAMPLE
        elif key == MissionType.ESCORT.value:
            filename = _NEVADA_ESCORT_EXAMPLE
        elif key == MissionType.GROUND_ATTACK.value:
            filename = _NEVADA_GROUND_ATTACK_EXAMPLE
        elif key == MissionType.RECON.value:
            filename = _NEVADA_RECON_EXAMPLE
        else:
            filename = _NEVADA_FREE_FLIGHT_EXAMPLE
        path = examples_dir() / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing Spec example for {key}: {path}")
        spec = load_mission_spec(path)
        if spec.mission_type.value != key:
            raise ValueError(
                f"Example {path.name} has mission_type {spec.mission_type.value!r}, "
                f"expected {key!r}"
            )
        example = json.loads(spec.model_dump_json())
        MissionSpec.model_validate(example)
        notes = _notes_for(key, theatre_id)
        return SpecSchemaView(mission_type=key, example=example, notes=notes)

    if theatre_id == "Syria":
        if key in _SYRIA_UNSUPPORTED_COMBAT:
            raise ValueError(
                f"Combat mission_type {key!r} is not supported for theatre Syria; "
                "use a Syria-supported type at Incirlik or theatre TheChannel"
            )
        if key == MissionType.CAP.value:
            filename = _SYRIA_CAP_EXAMPLE
        elif key == MissionType.INTERCEPT.value:
            filename = _SYRIA_INTERCEPT_EXAMPLE
        elif key == MissionType.ESCORT.value:
            filename = _SYRIA_ESCORT_EXAMPLE
        elif key == MissionType.GROUND_ATTACK.value:
            filename = _SYRIA_GROUND_ATTACK_EXAMPLE
        elif key == MissionType.RECON.value:
            filename = _SYRIA_RECON_EXAMPLE
        else:
            filename = _SYRIA_FREE_FLIGHT_EXAMPLE
        path = examples_dir() / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing Spec example for {key}: {path}")
        spec = load_mission_spec(path)
        if spec.mission_type.value != key:
            raise ValueError(
                f"Example {path.name} has mission_type {spec.mission_type.value!r}, "
                f"expected {key!r}"
            )
        example = json.loads(spec.model_dump_json())
        MissionSpec.model_validate(example)
        notes = _notes_for(key, theatre_id)
        return SpecSchemaView(mission_type=key, example=example, notes=notes)

    if theatre_id == "Caucasus":
        if key in _CAUCASUS_UNSUPPORTED_COMBAT:
            raise ValueError(
                f"Combat mission_type {key!r} is not supported for theatre Caucasus; "
                "use a Caucasus-supported type at Batumi or theatre TheChannel"
            )
        if key == MissionType.CAP.value:
            filename = _CAUCASUS_CAP_EXAMPLE
        elif key == MissionType.GROUND_ATTACK.value:
            filename = _CAUCASUS_GROUND_ATTACK_EXAMPLE
        elif key == MissionType.INTERCEPT.value:
            filename = _CAUCASUS_INTERCEPT_EXAMPLE
        elif key == MissionType.ESCORT.value:
            filename = _CAUCASUS_ESCORT_EXAMPLE
        elif key == MissionType.RECON.value:
            filename = _CAUCASUS_RECON_EXAMPLE
        else:
            filename = _CAUCASUS_FREE_FLIGHT_EXAMPLE
        path = examples_dir() / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing Spec example for {key}: {path}")
        spec = load_mission_spec(path)
        if spec.mission_type.value != key:
            raise ValueError(
                f"Example {path.name} has mission_type {spec.mission_type.value!r}, "
                f"expected {key!r}"
            )
        example = json.loads(spec.model_dump_json())
        MissionSpec.model_validate(example)
        notes = _notes_for(key, theatre_id)
        return SpecSchemaView(mission_type=key, example=example, notes=notes)

    if theatre_id == "Normandy":
        if key in _NORMANDY_UNSUPPORTED_COMBAT:
            raise ValueError(
                f"Combat mission_type {key!r} is not supported for theatre Normandy; "
                "use a Normandy-supported type at NeedsOarPoint or theatre TheChannel"
            )
        if key == MissionType.CAP.value:
            filename = _NORMANDY_CAP_EXAMPLE
        elif key == MissionType.GROUND_ATTACK.value:
            filename = _NORMANDY_GROUND_ATTACK_EXAMPLE
        elif key == MissionType.INTERCEPT.value:
            filename = _NORMANDY_INTERCEPT_EXAMPLE
        elif key == MissionType.ESCORT.value:
            filename = _NORMANDY_ESCORT_EXAMPLE
        elif key == MissionType.RECON.value:
            filename = _NORMANDY_RECON_EXAMPLE
        else:
            filename = _NORMANDY_FREE_FLIGHT_EXAMPLE
        path = examples_dir() / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing Spec example for {key}: {path}")
        spec = load_mission_spec(path)
        if spec.mission_type.value != key:
            raise ValueError(
                f"Example {path.name} has mission_type {spec.mission_type.value!r}, "
                f"expected {key!r}"
            )
        example = json.loads(spec.model_dump_json())
        MissionSpec.model_validate(example)
        notes = _notes_for(key, theatre_id)
        return SpecSchemaView(mission_type=key, example=example, notes=notes)

    filename = _AGENT_EXAMPLE_FILES.get(key) or _EXAMPLE_FILES[key]

    path = examples_dir() / filename
    if not path.is_file():
        # Fall back to bare compile example if immersion file missing.
        filename = _EXAMPLE_FILES[key]
        path = examples_dir() / filename
    if not path.is_file():
        raise FileNotFoundError(f"Missing Spec example for {key}: {path}")

    spec = load_mission_spec(path)
    if spec.mission_type.value != key:
        raise ValueError(
            f"Example {path.name} has mission_type {spec.mission_type.value!r}, expected {key!r}"
        )
    example = json.loads(spec.model_dump_json())
    # Re-validate the projected dict so drift fails loudly.
    MissionSpec.model_validate(example)
    notes = _notes_for(key, theatre_id)
    return SpecSchemaView(mission_type=key, example=example, notes=notes)


# Normandy GA: do not concatenate _TYPE_NOTES (those cite french_coast / Manston).
_NORMANDY_GA_NOTES: tuple[str, ...] = (
    (
        "Normandy invent is all six types: airfield NeedsOarPoint, "
        "SpitfireLFMkIX, sunny_clear, UK blue. Strike 180° / "
        "133 km / 2000 m inland of Maupertus (not Manston 125/76, not CAP "
        "180/63 which is sea). Call list_strike_targets(theatre=Normandy) for "
        "land units (Blitz / flak18). Sea craft stay Channel-only. Do not copy "
        "channel_place geometry (french "
        "coast belts, Hawkinge) onto Normandy."
    ),
    ('schema_version must be "1"; theatre is Normandy (ground_attack at NeedsOarPoint).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested strike is required (bearing_deg, distance_km, altitude_m).",
    (
        "player.payload is required (named preset; prefer spitfire_2x250_slipper "
        "for the Channel crossing to Cotentin)."
    ),
    (
        "targets must be non-empty land units from list_strike_targets"
        "(theatre=Normandy). Combat: opposing coalition (ThirdReich red). "
        "Copy maupertus_inland_strike 180/133. Stopping short (~120 km) is water. "
        "Flak/AAA → static + aaa_alert. Fill ids from "
        "examples/needs_oar_point_ground_attack.yaml."
    ),
    'objectives must include {"type":"attack_ground"}; enemies must be empty.',
    "omit the cap block. Pilot jettisons the slipper tank in the cockpit before attack.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_NORMANDY_INTERCEPT_NOTES: tuple[str, ...] = (
    (
        "Normandy invent is all six types: airfield NeedsOarPoint, "
        "SpitfireLFMkIX, sunny_clear, UK blue. "
        "Enemies spawn on the Cherbourg corridor (180° / 63 km from "
        "NeedsOarPoint — same station as cherbourg_channel_cap; not Hawkinge / "
        "Dover / Manston). Do not copy channel_place "
        "geometry (french coast belts, Hawkinge) onto Normandy."
    ),
    ('schema_version must be "1"; theatre is Normandy (intercept at NeedsOarPoint).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    'enemies must be non-empty; objectives must include {"type":"intercept_enemy"}.',
    "omit the cap and strike blocks; omit player.payload.",
    "Fill DCS ids from examples/needs_oar_point_dawn_intercept.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_NORMANDY_ESCORT_NOTES: tuple[str, ...] = (
    (
        "Normandy invent is all six types: airfield NeedsOarPoint, "
        "SpitfireLFMkIX, sunny_clear, UK blue. Package "
        "destination is the Cherbourg corridor (180° / 63 km / 4000 m — same "
        "station as cherbourg_channel_cap; not Manston 120/55). Friendly package "
        "e.g. MosquitoFBMkVI. Do not copy channel_place geometry "
        "(french coast belts, Hawkinge) onto Normandy."
    ),
    ('schema_version must be "1"; theatre is Normandy (escort at NeedsOarPoint).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    "nested escort is required (bearing_deg, distance_km, altitude_m, engagement).",
    (
        "package must be non-empty and same coalition as the player (friendly only); "
        "e.g. MosquitoFBMkVI."
    ),
    'objectives must include {"type":"escort_package"}; enemies optional (bounce).',
    "destination is airfield-relative bearing/distance — never invent raw map x/y.",
    "omit strike, targets, cap, recon, and player.payload.",
    "Fill DCS ids from examples/needs_oar_point_escort.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_NORMANDY_RECON_NOTES: tuple[str, ...] = (
    (
        "Normandy invent is all six types: airfield NeedsOarPoint, "
        "SpitfireLFMkIX, sunny_clear, UK blue. Recon AOI is inland of Maupertus "
        "(180° / 133 km / 2000 m — same land station as maupertus_inland_strike; "
        "not Manston 125/76, not CAP 180/63 sea). Observe land units from "
        "list_strike_targets(theatre=Normandy). Weapons hold. Do not copy "
        "channel_place geometry (french coast belts, Hawkinge) onto Normandy."
    ),
    ('schema_version must be "1"; theatre is Normandy (recon at NeedsOarPoint).'),
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    ("nested recon is required (bearing_deg, distance_km, altitude_m, radius_m?, mark?)."),
    'objectives must include {"type":"recon_area"}; omit player.payload.',
    (
        "optional targets = observe-only enemy contacts (opposing coalition). "
        "Call list_strike_targets(theatre=Normandy) for land units. Copy "
        "maupertus_inland_strike 180/133. Sea craft stay Channel-only."
    ),
    "AOI is airfield-relative — never invent raw map x/y. enemies must be empty.",
    "omit strike, cap, escort, package. zones/triggers must stay empty (find beat injected).",
    "Not a bomb run — weapons hold; report AOI then RTB.",
    "Fill DCS ids from examples/needs_oar_point_recon.yaml.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)


def _notes_for(mission_type: str, theatre: str | None) -> tuple[str, ...]:
    if theatre == "Kola":
        return _KOLA_FF_NOTES
    if theatre == "Falklands":
        if mission_type == MissionType.CAP.value:
            return _FALKLANDS_CAP_NOTES
        if mission_type == MissionType.INTERCEPT.value:
            return _FALKLANDS_INTERCEPT_NOTES
        if mission_type == MissionType.ESCORT.value:
            return _FALKLANDS_ESCORT_NOTES
        if mission_type == MissionType.GROUND_ATTACK.value:
            return _FALKLANDS_GA_NOTES
        if mission_type == MissionType.RECON.value:
            return _FALKLANDS_RECON_NOTES
        return _FALKLANDS_FF_NOTES
    if theatre == "Nevada":
        if mission_type == MissionType.CAP.value:
            return _NEVADA_CAP_NOTES
        if mission_type == MissionType.INTERCEPT.value:
            return _NEVADA_INTERCEPT_NOTES
        if mission_type == MissionType.ESCORT.value:
            return _NEVADA_ESCORT_NOTES
        if mission_type == MissionType.GROUND_ATTACK.value:
            return _NEVADA_GA_NOTES
        if mission_type == MissionType.RECON.value:
            return _NEVADA_RECON_NOTES
        return _NEVADA_FF_NOTES
    if theatre == "Syria":
        if mission_type == MissionType.CAP.value:
            return _SYRIA_CAP_NOTES
        if mission_type == MissionType.INTERCEPT.value:
            return _SYRIA_INTERCEPT_NOTES
        if mission_type == MissionType.ESCORT.value:
            return _SYRIA_ESCORT_NOTES
        if mission_type == MissionType.GROUND_ATTACK.value:
            return _SYRIA_GA_NOTES
        if mission_type == MissionType.RECON.value:
            return _SYRIA_RECON_NOTES
        return _SYRIA_FF_NOTES
    if theatre == "Caucasus":
        if mission_type == MissionType.CAP.value:
            return _CAUCASUS_CAP_NOTES
        if mission_type == MissionType.GROUND_ATTACK.value:
            return _CAUCASUS_GA_NOTES
        if mission_type == MissionType.INTERCEPT.value:
            return _CAUCASUS_INTERCEPT_NOTES
        if mission_type == MissionType.ESCORT.value:
            return _CAUCASUS_ESCORT_NOTES
        if mission_type == MissionType.RECON.value:
            return _CAUCASUS_RECON_NOTES
        return _CAUCASUS_FF_NOTES
    if theatre == "Normandy":
        if mission_type == MissionType.GROUND_ATTACK.value:
            return _NORMANDY_GA_NOTES
        if mission_type == MissionType.INTERCEPT.value:
            return _NORMANDY_INTERCEPT_NOTES
        if mission_type == MissionType.ESCORT.value:
            return _NORMANDY_ESCORT_NOTES
        if mission_type == MissionType.RECON.value:
            return _NORMANDY_RECON_NOTES
        extra = (
            (
                "Normandy invent is all six types: airfield NeedsOarPoint, "
                "SpitfireLFMkIX, sunny_clear, UK blue. CAP, intercept, and escort "
                "station 180° / 63 km / 4000 m (not Manston 135/25 or escort 120/55, "
                "not Hawkinge). Ground attack and recon AOI 180° / 133 km inland of "
                "Maupertus (not Manston 125/76). Do not copy channel_place "
                "geometry (french coast belts, Hawkinge) onto Normandy."
            ),
        )
        return extra + _COMMON_NOTES + _TYPE_NOTES.get(mission_type, ())
    return _COMMON_NOTES + _TYPE_NOTES.get(mission_type, ())


def infer_mission_type(text: str | None, *, default: str = MissionType.FREE_FLIGHT.value) -> str:
    """Best-effort ``mission_type`` from rejected Spec text; else ``default``."""
    if not text:
        return default
    m = _MT_IN_JSON.search(text)
    if m and m.group(1) in _EXAMPLE_FILES:
        return m.group(1)
    return default


def infer_theatre(text: str | None) -> str | None:
    """Best-effort Spec theatre from rejected JSON; else None (Manston default)."""
    if not text:
        return None
    m = _THEATRE_IN_JSON.search(text)
    if m and m.group(1) in _SCHEMA_THEATRES:
        return m.group(1)
    af = _AIRFIELD_IN_JSON.search(text)
    if af and af.group(1) in {"NeedsOarPoint", "Maupertus"}:
        return "Normandy"
    if af and af.group(1) in {
        "Batumi",
        "Kobuleti",
        "SenakiKolkhi",
        "Kutaisi",
        "TbilisiLochini",
        "Vaziani",
        "SochiAdler",
        "Mozdok",
    }:
        return "Caucasus"
    if af and af.group(1) in {
        "Incirlik",
        "RamatDavid",
        "Damascus",
        "BeirutRaficHariri",
        "Aleppo",
        "BasselAlAssad",
        "Palmyra",
        "KingHusseinAirCollege",
    }:
        return "Syria"
    if af and af.group(1) in {
        "Nellis",
        "GroomLake",
        "Creech",
        "TonopahTestRange",
        "NorthLasVegas",
        "HendersonExecutive",
        "BoulderCity",
        "Mesquite",
    }:
        return "Nevada"
    if af and af.group(1) in {
        "MountPleasant",
        "Mount_Pleasant",
        "PortStanley",
        "SanCarlosFOB",
        "RioGallegos",
        "RioGrande",
        "Ushuaia",
        "PuntaArenas",
        "SanJulian",
    }:
        return "Falklands"
    if af and af.group(1) == "Bodo":
        return "Kola"
    return None


def format_spec_schema_fragment(view: SpecSchemaView) -> str:
    """Human/LLM-readable example + notes for prompts and repair nudges."""
    example_json = json.dumps(view.example, indent=2, ensure_ascii=False)
    notes = "\n".join(f"- {n}" for n in view.notes)
    antis = "\n".join(f"- {a}" for a in view.anti_patterns)
    return (
        f"Mission Spec example for mission_type={view.mission_type!r} "
        f"(derived from packaged examples; validate before accept):\n"
        f"{example_json}\n\n"
        f"Notes:\n{notes}\n\n"
        f"DO NOT emit:\n{antis}"
    )


# Thin always-on reminder for the system prompt (no full skeletons).
SPEC_SHAPE_REMINDER = """\
Mission Spec JSON (schema_version "1") — extra fields are rejected.
Before emitting Spec JSON, call get_mission_spec_schema with the mission_type
(free_flight | intercept | cap | ground_attack | escort | recon) and optional theatre.
Copy that example's structure. Default stub is Manston / TheChannel; Normandy
all six types use NeedsOarPoint; Caucasus all six types
use Batumi; Syria all six types use Incirlik; Nevada all six types use Nellis
(CAP/intercept/escort 350° / 40 km desert north-range; GA/recon 303° / 85 km
inland past Creech); Falklands all six types use
Mount Pleasant (CAP/intercept/escort 150° / 40 km South Atlantic; GA/recon 269° / 21 km
inland short of Goose Green). Falklands
recon uses the East Falkland inland envelope. Kola free_flight only uses Bodo
(combat types raise).
Immersion: after matching the envelope, apply 1–2 mission_behaviour recipes (zones/
triggers, narrative.enabled, late_activation+activate_group, gates, etc.) when the user
left challenge unspecified — see schema notes for example YAML paths.

Always required envelope:
  schema_version, mission_type, theatre, date, start_time, weather, player,
  enemies (list), objectives (list), triggers (list; use [] when unused —
  non-empty OK for supported immersion behaviours), zones (list; [] when unused)

Anti-patterns (fatal):
- top-level airfield/aircraft → use nested player{}
- date as "YYYY-MM-DD" → use {"year","month","day"}
- enemies as {type,id} → use {aircraft,count,...}
- objectives under cap/strike → objectives stay top-level
- friendly ground targets without strike.practice → combat strikes need opposing coalition
- inventing DCS ids / CLSIDs — use tools/prefs and named player.payload only
- late_activation without activate_group (dormant groups — validation rejects)
"""
