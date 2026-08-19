"""Extra-home place cards: schema rewrite, invent clamp, M8 knob nudges.

Place-card meta on ``channel_place`` ``*_home`` rows is the geometry SoT.
Invent/chat may clamp cloned default-home stations; CLI validate does not.
"""

from __future__ import annotations

import re
from typing import Any

from ..models import MissionSpec, MissionType, PlayerFlightRole
from ..registry import ChannelRegistry, get_channel_registry

EXTRA_HOME_THEATRE: dict[str, str] = {
    "Hawkinge": "TheChannel",
    "Detling": "TheChannel",
    "BigginHill": "TheChannel",
    "Chailey": "Normandy",
    "Tangmere": "Normandy",
    "FordAF": "Normandy",
}

PACKAGED_EXTRA_HOME_EXAMPLES: dict[tuple[str, str], str] = {
    ("Hawkinge", MissionType.FREE_FLIGHT.value): "hawkinge_cold_freeflight.yaml",
    ("Hawkinge", MissionType.CAP.value): "hawkinge_cap.yaml",
    ("Chailey", MissionType.FREE_FLIGHT.value): "chailey_cold_freeflight.yaml",
}

_CHANNEL_DEFAULT_CAP = (135.0, 25.0)
_CHANNEL_DEFAULT_STRIKE = (125.0, 76.0)
_CHANNEL_DEFAULT_ESCORT = (120.0, 55.0)
_NORMANDY_DEFAULT_CAP = (180.0, 63.0)
_NORMANDY_DEFAULT_STRIKE = (180.0, 133.0)

_NAMED_PLACE_CUE = re.compile(
    r"\b(french\s+coast|dunkirk|calais|harbour|harbor|mid-?channel|u-?boat|"
    r"cherbourg|maupertus|cotentin|inland\s+of)\b",
    re.IGNORECASE,
)
_MUSTANG_CUE = re.compile(r"\b(mustang|p-?51d?)\b", re.IGNORECASE)
_ARTILLERY_CUE = re.compile(
    r"\b(artillery|howitzer|lefh|wespe|105\s*mm|field\s+gun)\b",
    re.IGNORECASE,
)
_SCENERY_CUE = re.compile(
    r"\b(hangar|dispersal|scenery|revetment|airfield\s+props?)\b",
    re.IGNORECASE,
)
_FAILURES_CUE = re.compile(
    r"\b(magneto|failures?|engine\s+fail|cockpit\s+fail)\b",
    re.IGNORECASE,
)
_ORDERS_CUE = re.compile(
    r"\b(section\s+orders?|rejoin|section:\s*engage|f10\s+section)\b",
    re.IGNORECASE,
)
_DISCIPLINE_CUE = re.compile(
    r"\b(fail[- ]to[- ]follow|don'?t\s+wander|wander(\s+off)?|fail\s+me|"
    r"stay\s+with\s+(the\s+)?(lead|section)|section\s+bubble)\b",
    re.IGNORECASE,
)
_PAIR_CUE = re.compile(
    r"\b(a pair|pair from|two-ship|rhubarb|flying as two|as two)\b",
    re.IGNORECASE,
)
_WINGMAN_CUE = re.compile(r"\bwingman\b", re.IGNORECASE)
_AIRFIELD_IN_JSON = re.compile(r'"airfield"\s*:\s*"([A-Za-z0-9_]+)"')

_ARTILLERY_IDS = frozenset({"LeFH_18-40-105", "Wespe124", "M2A1-105"})
_EPS = 0.51


def is_extra_home(airfield: str | None) -> bool:
    return bool(airfield) and airfield in EXTRA_HOME_THEATRE


def extra_home_theatre(airfield: str | None) -> str | None:
    if not airfield:
        return None
    return EXTRA_HOME_THEATRE.get(airfield)


def packaged_extra_home_filename(airfield: str | None, mission_type: str) -> str | None:
    if not airfield:
        return None
    return PACKAGED_EXTRA_HOME_EXAMPLES.get((airfield, mission_type))


def infer_airfield(text: str | None) -> str | None:
    """Best-effort ``player.airfield`` from rejected Spec JSON."""
    if not text:
        return None
    m = _AIRFIELD_IN_JSON.search(text)
    if not m:
        return None
    name = m.group(1)
    if name in EXTRA_HOME_THEATRE or name in {"Manston", "NeedsOarPoint"}:
        return name
    return name if name else None


def extra_home_meta(
    airfield: str,
    *,
    registry: ChannelRegistry | None = None,
) -> dict[str, Any] | None:
    """Return ``*_home`` place-card meta for an extra-home airfield."""
    reg = registry or get_channel_registry()
    for opt in reg.list_planning_options():
        if opt.family != "channel_place":
            continue
        meta = opt.meta or {}
        if meta.get("role") != "extra_home":
            continue
        if meta.get("airfield") == airfield:
            return dict(meta)
    return None


def _pair(kind: str, meta: dict[str, Any]) -> tuple[float, float, float] | None:
    if kind == "cap":
        b, d, a = (
            meta.get("cap_bearing_deg"),
            meta.get("cap_distance_km"),
            meta.get("cap_altitude_m"),
        )
    elif kind == "strike":
        b, d, a = (
            meta.get("strike_bearing_deg"),
            meta.get("strike_distance_km"),
            meta.get("strike_altitude_m"),
        )
    else:
        b = meta.get("escort_bearing_deg", meta.get("cap_bearing_deg"))
        d = meta.get("escort_distance_km", meta.get("cap_distance_km"))
        a = meta.get("escort_altitude_m", meta.get("cap_altitude_m"))
    if b is None or d is None:
        return None
    return float(b), float(d), float(a if a is not None else 4000)


def _near(bearing: float, distance: float, expected: tuple[float, float]) -> bool:
    return abs(bearing - expected[0]) <= _EPS and abs(distance - expected[1]) <= _EPS


def _set_station(block: dict[str, Any], geom: tuple[float, float, float]) -> None:
    block["bearing_deg"] = geom[0]
    block["distance_km"] = geom[1]
    block["altitude_m"] = geom[2]


def apply_extra_home_example(
    example: dict[str, Any],
    *,
    mission_type: str,
    airfield: str | None,
    theatre: str | None = None,
    registry: ChannelRegistry | None = None,
) -> dict[str, Any]:
    """Rewrite a theatre-default schema example onto an extra home.

    Packaged Hawkinge/Chailey files are already correct — caller should load those
    instead of calling this. Unknown airfields are ignored.
    """
    if not airfield or not is_extra_home(airfield):
        return example
    home_theatre = extra_home_theatre(airfield)
    if theatre and home_theatre and theatre != home_theatre:
        return example
    if packaged_extra_home_filename(airfield, mission_type):
        return example
    meta = extra_home_meta(airfield, registry=registry)
    if not meta:
        return example
    out = dict(example)
    player = dict(out.get("player") or {})
    player["airfield"] = airfield
    out["player"] = player
    key = (mission_type or "").strip()
    if key in {MissionType.CAP.value, MissionType.INTERCEPT.value} and out.get("cap"):
        geom = _pair("cap", meta)
        if geom:
            cap = dict(out["cap"])
            _set_station(cap, geom)
            out["cap"] = cap
    if key == MissionType.ESCORT.value and out.get("escort"):
        geom = _pair("escort", meta)
        if geom:
            escort = dict(out["escort"])
            _set_station(escort, geom)
            out["escort"] = escort
    if key == MissionType.GROUND_ATTACK.value and out.get("strike"):
        geom = _pair("strike", meta)
        if geom:
            strike = dict(out["strike"])
            _set_station(strike, geom)
            out["strike"] = strike
    if key == MissionType.RECON.value and out.get("recon"):
        geom = _pair("strike", meta)
        if geom:
            recon = dict(out["recon"])
            _set_station(recon, geom)
            out["recon"] = recon
    return out


def _default_stations(theatre: str) -> dict[str, tuple[float, float]]:
    if theatre == "Normandy":
        return {
            "cap": _NORMANDY_DEFAULT_CAP,
            "strike": _NORMANDY_DEFAULT_STRIKE,
            "escort": _NORMANDY_DEFAULT_CAP,
        }
    return {
        "cap": _CHANNEL_DEFAULT_CAP,
        "strike": _CHANNEL_DEFAULT_STRIKE,
        "escort": _CHANNEL_DEFAULT_ESCORT,
    }


def try_clamp_extra_home_stations(
    spec: MissionSpec,
    *,
    prompt: str | None = None,
    registry: ChannelRegistry | None = None,
) -> MissionSpec | None:
    """Rewrite extra-home Specs that cloned Manston/NOP default stations.

    Returns a new spec when changed, else None. Does not run on CLI validate.
    """
    airfield = spec.player.airfield
    if not is_extra_home(airfield):
        return None
    home_theatre = extra_home_theatre(airfield)
    if spec.theatre not in {"TheChannel", "Normandy"} or spec.theatre != home_theatre:
        return None
    if prompt and _NAMED_PLACE_CUE.search(prompt):
        return None
    meta = extra_home_meta(airfield, registry=registry)
    if not meta:
        return None
    defaults = _default_stations(spec.theatre)
    updates: dict[str, Any] = {}
    if spec.cap is not None:
        geom = _pair("cap", meta)
        if geom and _near(spec.cap.bearing_deg, spec.cap.distance_km, defaults["cap"]):
            updates["cap"] = spec.cap.model_copy(
                update={
                    "bearing_deg": geom[0],
                    "distance_km": geom[1],
                    "altitude_m": geom[2],
                }
            )
    if spec.escort is not None:
        geom = _pair("escort", meta)
        if geom and _near(spec.escort.bearing_deg, spec.escort.distance_km, defaults["escort"]):
            updates["escort"] = spec.escort.model_copy(
                update={
                    "bearing_deg": geom[0],
                    "distance_km": geom[1],
                    "altitude_m": geom[2],
                }
            )
    if spec.strike is not None:
        geom = _pair("strike", meta)
        if geom and _near(spec.strike.bearing_deg, spec.strike.distance_km, defaults["strike"]):
            updates["strike"] = spec.strike.model_copy(
                update={
                    "bearing_deg": geom[0],
                    "distance_km": geom[1],
                    "altitude_m": geom[2],
                }
            )
    if spec.recon is not None:
        geom = _pair("strike", meta)
        if geom and _near(spec.recon.bearing_deg, spec.recon.distance_km, defaults["strike"]):
            updates["recon"] = spec.recon.model_copy(
                update={
                    "bearing_deg": geom[0],
                    "distance_km": geom[1],
                    "altitude_m": geom[2],
                }
            )
    if not updates:
        return None
    return spec.model_copy(update=updates)


def _artillery_units(spec: MissionSpec) -> bool:
    for tgt in spec.targets or []:
        if tgt.unit in _ARTILLERY_IDS:
            return True
    return False


def host_m8_knob_nudge(prompt: str, spec: MissionSpec) -> str | None:
    """One-shot host nudge when the ask implies an M8 card the draft omitted."""
    text = prompt or ""
    if spec.theatre not in {"TheChannel", "Normandy"}:
        return None
    if _MUSTANG_CUE.search(text) and spec.player.aircraft != "P-51D":
        return (
            "[Host] M8 knob: this ask is a Mustang / P-51 sortie. Emit player.aircraft "
            "P-51D with country USA (radio 124.0). For ground_attack use payload "
            "p51d_2x_anm64. Reply with a corrected Mission Spec JSON object ONLY "
            "(no markdown fences)."
        )
    flight = spec.player.flight
    if (
        _ARTILLERY_CUE.search(text)
        and spec.mission_type == MissionType.GROUND_ATTACK
        and not _artillery_units(spec)
    ):
        return (
            "[Host] M8 knob: this ask is an artillery / howitzer hunt. Call "
            "list_strike_targets(class_id=artillery) and emit those unit ids "
            "(LeFH_18-40-105, Wespe124, or M2A1-105), static motion, convoy_transit. "
            "Do not use Blitz. Reply with a corrected Mission Spec JSON object ONLY "
            "(no markdown fences)."
        )
    if _SCENERY_CUE.search(text) and not spec.scenery:
        return (
            "[Host] M8 knob: this ask wants airfield scenery. Apply mission_behaviour "
            "airfield_scenery — emit scenery[] from WWII statics (Hangar A, "
            "Revetment_x4, Tent01, Belgian gate, Shelter; see "
            "manston_freeflight_scenery.yaml). Reply with a corrected Mission Spec "
            "JSON object ONLY (no markdown fences)."
        )
    if _FAILURES_CUE.search(text) and not spec.failures:
        return (
            "[Host] M8 knob: this ask wants aircraft failures. Apply mission_behaviour "
            "aircraft_failures — emit failures[] with curated Spitfire ids (see "
            "manston_freeflight_magneto_failure.yaml). Reply with a corrected Mission "
            "Spec JSON object ONLY (no markdown fences)."
        )
    if _ORDERS_CUE.search(text) and (flight is None or not flight.orders):
        return (
            "[Host] M8 knob: this ask wants F10 section orders. Emit player.flight "
            "with curated orders (rejoin, engage, … — list_mission_options family "
            "player_flight_order). Do not invent free-form order strings. Reply with "
            "a corrected Mission Spec JSON object ONLY (no markdown fences)."
        )
    if _DISCIPLINE_CUE.search(text) and (flight is None or flight.discipline is None):
        return (
            "[Host] M8 knob: this ask is fail-to-follow / stay with the lead. Emit "
            "player.flight role wingman, join_up true, and discipline {} (or "
            "explicit radius/soft/hard). Discipline is wingman+join_up only. Reply "
            "with a corrected Mission Spec JSON object ONLY (no markdown fences)."
        )
    if _WINGMAN_CUE.search(text) and (flight is None or flight.role != PlayerFlightRole.WINGMAN):
        return (
            "[Host] M8 knob: this ask puts the player as wingman. Emit player.flight "
            "size 2 role wingman join_up true (separate AI lead + Follow). Do not use "
            "escort package[] as the wingman. Reply with a corrected Mission Spec JSON "
            "object ONLY (no markdown fences)."
        )
    if _PAIR_CUE.search(text) and flight is None:
        return (
            "[Host] M8 knob: this ask is a pair/section. Emit player.flight size 2 "
            "role lead (AI mate in the player group). Omit escort package[]. Reply with "
            "a corrected Mission Spec JSON object ONLY (no markdown fences)."
        )
    return None
