"""Squadron-commander voice packs, resolution, and host-side briefs."""

from __future__ import annotations

from typing import Any

from ..models import MissionSpec

VOICE_RAF = "raf"
VOICE_USAAF = "usaaf"
VOICE_NEUTRAL = "neutral"
DEFAULT_VOICE = VOICE_RAF
KNOWN_VOICES = frozenset({VOICE_RAF, VOICE_USAAF, VOICE_NEUTRAL})

_ALIASES: dict[str, str] = {
    "raf": VOICE_RAF,
    "royal air force": VOICE_RAF,
    "uk": VOICE_RAF,
    "british": VOICE_RAF,
    "usaaf": VOICE_USAAF,
    "usaa": VOICE_USAAF,
    "us": VOICE_USAAF,
    "usa": VOICE_USAAF,
    "american": VOICE_USAAF,
    "us army air forces": VOICE_USAAF,
    "neutral": VOICE_NEUTRAL,
    "off": VOICE_NEUTRAL,
    "none": VOICE_NEUTRAL,
    "plain": VOICE_NEUTRAL,
}

_RAF_PACK = """\
Persona (RAF squadron commander):
You address the pilot as their squadron commander — calm, direct, period-appropriate.
Use restrained RAF Fighter Command register and jargon when speaking (not in Spec JSON):
scramble, bandits, kite, angels, bogey only if fitting, RTB, ops, gen, prang (sparingly).
No modern chatbot filler ("Happy to help!", emoji). Sound like a wartime briefing officer.
"""

_USAAF_PACK = """\
Persona (USAAF squadron commander):
You address the pilot as their skipper / squadron CO — calm, direct, period-appropriate.
Use restrained USAAF Eighth Air Force flavour and jargon when speaking (not in Spec JSON):
bogeys, bandits, fighters, scramble, angels, skipper, RTB, flak, bounce (sparingly).
No modern chatbot filler. Sound like a wartime briefing officer talking to his pilots.
"""

_OPS_BRIEF_RULES = """\
Operational brief (after Spec is accepted by the host):
When advising pilots, cover tactics for the mission type and plan, procedures
(start-up / taxi / climb / engagement / recovery as relevant), and watch-outs
(weather, fuel, bogeys/bandits, navigation, deconfliction). Prefer researched notes
from research_guidance or well-known WWII fighter practice; label uncertainty.
Do NOT put slang or briefing prose into Mission Spec field values — Spec JSON stays plain.
High-level guidance only; not a substitute for real flight training.
"""

_PERSONA_PACKS: dict[str, str] = {
    VOICE_RAF: _RAF_PACK,
    VOICE_USAAF: _USAAF_PACK,
    VOICE_NEUTRAL: "",
}


def normalize_voice(raw: str | None) -> str | None:
    """Return a known voice id, or None if blank/unknown."""
    if raw is None:
        return None
    key = " ".join(str(raw).strip().lower().split())
    if not key:
        return None
    if key in KNOWN_VOICES:
        return key
    return _ALIASES.get(key)


def resolve_voice(
    *,
    cli_voice: str | None = None,
    prefs: dict[str, Any] | None = None,
    default: str = DEFAULT_VOICE,
) -> str:
    """CLI override → squadron_voice pref → default. Unknown inputs fall back to default."""
    for candidate in (cli_voice, (prefs or {}).get("squadron_voice")):
        normalized = normalize_voice(
            candidate if isinstance(candidate, str) else (str(candidate) if candidate else None)
        )
        if normalized is not None:
            return normalized
    return normalize_voice(default) or DEFAULT_VOICE


def persona_pack(voice: str) -> str:
    """Return curated persona text for a resolved voice id."""
    return _PERSONA_PACKS.get(voice, "")


def ops_brief_rules() -> str:
    return _OPS_BRIEF_RULES


def _weather_phrase(spec: MissionSpec) -> str:
    """Pilot-facing meteorological wording for briefs (not Spec enum ids)."""
    from ..registry import RegistryError, get_channel_registry

    try:
        return get_channel_registry().weather_preset(spec.weather.value).description
    except RegistryError:
        return spec.weather.value


def _synthetic_metar_line(spec: MissionSpec) -> str:
    """Offline METAR from invent snapshot (shared by CLI brief and compile l10n)."""
    from ..weather_invent import ensure_weather_seed, resolve_weather_snapshot
    from ..weather_metar import format_synthetic_metar

    seeded = ensure_weather_seed(spec)
    snap = resolve_weather_snapshot(seeded)
    return format_synthetic_metar(snap, seeded)


def build_commander_brief(spec: MissionSpec, voice: str) -> str:
    """Deterministic host brief with Situation / Tactics / Procedures / Watch-outs."""
    mt = spec.mission_type.value
    airfield = spec.player.airfield
    aircraft = spec.player.aircraft
    weather = _weather_phrase(spec)
    metar = _synthetic_metar_line(spec)
    start = spec.start_time
    start_type = spec.player.start.value
    flight = spec.player.flight
    if flight is not None:
        role_phrase = "as flight lead" if flight.role.value == "lead" else "as wingman"
        section_phrase = f" in a section of {flight.size}, {role_phrase}"
    else:
        section_phrase = ""

    if voice == VOICE_USAAF:
        opener = (
            f"Listen up. Sortie from {airfield} in the {aircraft}{section_phrase}, "
            f"{start} local, weather {weather}, start {start_type}.\n"
            f"METAR (synthetic): {metar}"
        )
        closing = "Fly smart, keep your head on a swivel, and bring it home."
    elif voice == VOICE_RAF:
        opener = (
            f"Right. You're away from {airfield} in the {aircraft}{section_phrase}, "
            f"{start} hours, weather {weather}, start {start_type}.\n"
            f"METAR (synthetic): {metar}"
        )
        closing = "Keep a sharp lookout, mind your fuel state, and RTB with the kite intact."
    else:
        opener = (
            f"Mission: {mt} from {airfield} ({aircraft}){section_phrase}, "
            f"start {start}, weather {weather}, start type {start_type}.\n"
            f"METAR (synthetic): {metar}"
        )
        closing = "Review the plan, fly the procedures, and abort early if unsafe."

    if mt == "intercept":
        enemy_bits = []
        for e in spec.enemies:
            enemy_bits.append(f"{e.count}× {e.aircraft}")
        opposition = ", ".join(enemy_bits) or "hostile fighters"
        tactics = (
            f"For this intercept against {opposition}: climb with purpose, "
            "gain altitude advantage before committing, bounce from up-sun when you can, "
            "and break contact if the fight turns against you. Pair up; do not chase alone."
        )
        procedures = (
            "Cold or hot start as briefed; taxi clear; climb on the assigned heading toward "
            "the threat axis. Confirm guns/sight; call tally before merge. "
            "Disengage with speed and altitude, then recover to base."
        )
        watch = (
            "Watch for escort fighters above the bombers or bounce from cloud; "
            "guard your six in the merge; mind Channel over-water navigation and fuel; "
            "do not press into flak or numbers you cannot handle."
        )
    elif mt == "cap":
        cap = spec.cap
        station = (
            f"bearing {cap.bearing_deg:g}°, {cap.distance_km:g} km, "
            f"{cap.altitude_m:g} m, pattern {cap.pattern.value}, "
            f"ROE {cap.engagement.value}"
            if cap is not None
            else "assigned CAP station"
        )
        enemy_bits = [f"{e.count}× {e.aircraft}" for e in spec.enemies]
        opposition = ", ".join(enemy_bits) if enemy_bits else "no planned bandits"
        tactics = (
            f"CAP on station ({station}). Hold the orbit, scan systematically, "
            f"and commit only with advantage. Opposition briefed: {opposition}. "
            "Do not chase so far that you abandon the station or bingo fuel."
        )
        procedures = (
            "Start and depart as briefed; climb toward the CAP bearing; "
            "establish the orbit at altitude; manage fuel and lookout cycles; "
            "recover to base when relieved or bingo."
        )
        watch = (
            "Watch bogeys diving from above or out of cloud, fuel state on a long CAP, "
            "navigation over the Channel, and mid-air conflict near the station; "
            "honour your ROE and do not press hopeless odds."
        )
    elif mt == "ground_attack":
        strike = spec.strike
        strike_bits = (
            f"bearing {strike.bearing_deg:g}°, {strike.distance_km:g} km, "
            f"ingress {strike.altitude_m:g} m"
            if strike is not None
            else "assigned strike area"
        )
        tgt_bits = [f"{t.count}× {t.unit}" for t in spec.targets]
        targets = ", ".join(tgt_bits) or "briefed ground targets"
        payload = spec.player.payload or "briefed loadout"
        has_slipper = "slipper" in payload.lower() or "tank" in payload.lower()
        tactics = (
            f"Ground attack on {strike_bits}. Targets: {targets} (enemy only). "
            f"Loadout: {payload}. Run in with a clear abort, release on the briefed "
            "aiming point, and do not linger in flak."
        )
        if has_slipper:
            procedures = (
                "Cold start as briefed; taxi and takeoff with the slipper tank fitted; "
                "climb toward the Channel strike bearing; jettison the external fuel tank "
                "in the cockpit before the attack run; then press the dive/level attack and "
                "recover to base."
            )
            watch = (
                "Watch Channel weather and fuel with the slipper, flak around the target, "
                "navigation over water, and mid-air conflict near the coast; "
                "jettison the tank before combat and do not press a blind attack into cloud."
            )
        else:
            procedures = (
                "Cold start as briefed; taxi and takeoff; climb toward the strike bearing; "
                "confirm bombs/sight; attack the briefed aim point; recover to base."
            )
            watch = (
                "Watch fuel state on a short-radius loadout, flak around the target, "
                "navigation, and mid-air conflict; abort early if you lose the target or "
                "the weather closes in."
            )
    elif mt == "escort":
        escort = spec.escort
        dest = (
            f"bearing {escort.bearing_deg:g}°, {escort.distance_km:g} km, "
            f"{escort.altitude_m:g} m, ROE {escort.engagement.value}"
            if escort is not None
            else "assigned package route"
        )
        pkg_bits = [f"{p.count}× {p.aircraft}" for p in spec.package]
        package = ", ".join(pkg_bits) or "friendly package"
        enemy_bits = [f"{e.count}× {e.aircraft}" for e in spec.enemies]
        opposition = ", ".join(enemy_bits) if enemy_bits else "no planned bounce"
        tactics = (
            f"Escort {package} to {dest}. Stay with the package — do not chase so far "
            f"that you abandon them. Bounce briefed: {opposition}. Commit only with "
            "advantage and return to cover."
        )
        procedures = (
            "Cold start as briefed; climb toward the package route; join and hold "
            "escort position; scan above and out-sun; cover to the destination; "
            "recover with the package or as briefed."
        )
        watch = (
            "Watch fighters diving on the package, fuel on a Channel transit, "
            "mid-air near the formation, and navigation over water; honour ROE and "
            "do not leave the package alone to chase."
        )
    else:
        tactics = (
            "Free flight: treat this as a familiarisation / local area hop. "
            "Build situational awareness, practise gentle handling, and keep clear of "
            "known flak belts and crowded corridors unless tasked."
        )
        procedures = (
            "Complete start checks, taxi and takeoff as briefed, climb to a safe working "
            "altitude, fly a disciplined local pattern or area tour, then recover for a "
            "stable approach and landing."
        )
        watch = (
            "Watch weather deterioration and cloud base, mid-air conflict near the field, "
            "fuel state on the way home, and Channel ditching risk if you wander offshore."
        )

    from ..models import player_flight_join_up_enabled

    if player_flight_join_up_enabled(flight):
        procedures = (
            f"{procedures} After takeoff, climb and join up — Follow the AI section "
            "lead on the briefed route; do not leave the section unless ordered."
        )

    if flight is not None and flight.orders:
        labels = ", ".join(o.value for o in flight.orders)
        procedures = f"{procedures} F10 Other → Section orders available: {labels}."

    if flight is not None and flight.discipline is not None:
        procedures = (
            f"{procedures} Stay with the section after airborne — leaving the "
            "bubble triggers a rejoin warning, then harder consequences."
        )

    if spec.failures:
        watch = (
            f"{watch} Expect possible aircraft system failures on this sortie — "
            "keep a cool head, diagnose early, and abort or RTB if the kite will "
            "not stay airborne."
        )

    return (
        f"## Situation / sortie\n{opener}\n\n"
        f"## Tactics\n{tactics}\n\n"
        f"## Procedures\n{procedures}\n\n"
        f"## Watch-outs\n{watch}\n\n"
        f"{closing}"
    )
