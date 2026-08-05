"""Creative decision detail convention and history→bias helper."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .models import FeedbackRecord, GenerationRecord

# detail.creative.sources vocabulary
SOURCE_CATALOG = "catalog"
SOURCE_CAMPAIGN_DOC = "campaign_doc"
SOURCE_RESEARCH = "research"
SOURCE_USER_REQUEST = "user_request"
SOURCE_SPEC_INFER = "spec_infer"

CREATIVE_SOURCES = frozenset(
    {
        SOURCE_CATALOG,
        SOURCE_CAMPAIGN_DOC,
        SOURCE_RESEARCH,
        SOURCE_USER_REQUEST,
        SOURCE_SPEC_INFER,
    }
)

# Optional taste prefs (schemaless JSON values)
PREF_PREFERRED_BEHAVIOURS = "preferred_behaviours"
PREF_AVOID_BEHAVIOURS = "avoid_behaviours"
PREF_CREATIVITY_LEVEL = "creativity_level"
CREATIVITY_QUIET = "quiet"
CREATIVITY_ASSERTIVE = "assertive"
CREATIVITY_MAX = "max"

_HIGH_SCORE = 4
_LOW_SCORE = 2


@dataclass(frozen=True)
class CreativeBias:
    prefer: tuple[str, ...] = ()
    avoid: tuple[str, ...] = ()


@dataclass
class _ScoreAcc:
    weight: float = 0.0
    hits: int = 0


def build_creative_detail(
    *,
    behaviours: Sequence[str] | None = None,
    inspirations: Sequence[str] | None = None,
    sources: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Build the ``detail[\"creative\"]`` object (omits empty lists)."""
    creative: dict[str, Any] = {}
    if behaviours:
        creative["behaviours"] = [str(b).strip() for b in behaviours if str(b).strip()]
    if inspirations:
        creative["inspirations"] = [str(i).strip() for i in inspirations if str(i).strip()]
    if sources:
        creative["sources"] = [str(s).strip() for s in sources if str(s).strip()]
    return creative


def merge_creative_into_detail(
    detail: Mapping[str, Any] | None,
    creative: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Shallow-merge ``creative`` into detail without dropping other keys."""
    out = dict(detail or {})
    if not creative:
        return out
    existing = out.get("creative")
    if isinstance(existing, dict):
        merged = dict(existing)
        for key in ("behaviours", "inspirations", "sources"):
            if creative.get(key):
                merged[key] = list(creative[key])
        out["creative"] = merged
    else:
        out["creative"] = dict(creative)
    return out


def extract_creative(detail: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not detail:
        return None
    raw = detail.get("creative")
    return raw if isinstance(raw, dict) else None


def infer_creative_from_spec(spec: Any) -> dict[str, Any] | None:
    """
    Light heuristic: map Spec fields to ``mission_behaviour`` ids.

    Not authoritative packaging — fills memory when the host did not pass explicit
    creative detail. Returns None when nothing recognizable is present.
    """
    behaviours: list[str] = []

    narrative = getattr(spec, "narrative", None)
    if narrative is not None and bool(getattr(narrative, "enabled", False)):
        behaviours.append("narrative_pack")

    enemies = getattr(spec, "enemies", None) or []
    targets = getattr(spec, "targets", None) or []
    triggers = getattr(spec, "triggers", None) or []
    cond_types: set[str] = set()
    action_types: set[str] = set()
    for trig in triggers:
        for cond in getattr(trig, "when", None) or []:
            t = getattr(cond, "type", None)
            if t:
                cond_types.add(str(t))
        for act in getattr(trig, "then", None) or []:
            t = getattr(act, "type", None)
            if t:
                action_types.add(str(t))

    has_late = any(getattr(e, "late_activation", False) for e in enemies) or any(
        getattr(t, "late_activation", False) for t in targets
    )
    # Complete late-act recipe only — half-recipes must not bias memory.
    if has_late and "activate_group" in action_types:
        behaviours.append("radio_late_activation")

    if cond_types & {
        "unit_altitude_higher",
        "unit_altitude_lower",
        "unit_speed_higher",
        "unit_speed_lower",
    }:
        behaviours.append("altitude_speed_gates")
    if action_types & {"mark", "smoke"}:
        behaviours.append("mark_smoke")
    if "sound" in action_types or cond_types & {
        "flag_equals",
        "flag_more",
        "flag_less",
        "time_since_flag",
    }:
        behaviours.append("sound_flag_chain")
    if "group_life_less" in cond_types:
        behaviours.append("group_life_less")

    # Dedupe preserving order
    seen: set[str] = set()
    ordered: list[str] = []
    for b in behaviours:
        if b not in seen:
            seen.add(b)
            ordered.append(b)
    if not ordered:
        return None
    return build_creative_detail(behaviours=ordered, sources=[SOURCE_SPEC_INFER])


def _behaviours_from_creative(creative: Mapping[str, Any] | None) -> list[str]:
    if not creative:
        return []
    raw = creative.get("behaviours") or []
    if not isinstance(raw, list):
        return []
    return [str(b).strip() for b in raw if str(b).strip()]


def _parse_tag_behaviour(tag: Any) -> tuple[str, str] | None:
    """Return (liked|avoid, behaviour_id) from tags like liked:foo / avoid:bar."""
    if not isinstance(tag, str):
        return None
    t = tag.strip().lower()
    for prefix, kind in (("liked:", "liked"), ("like:", "liked"), ("avoid:", "avoid")):
        if t.startswith(prefix):
            bid = tag.strip()[len(prefix) :].strip()
            if bid:
                return kind, bid
    return None


def _as_id_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    return []


def creative_bias_from_history(
    generations: Sequence[GenerationRecord],
    feedback: Sequence[FeedbackRecord] | None = None,
    *,
    mission_type: str | None = None,
    prefs: Mapping[str, Any] | None = None,
) -> CreativeBias:
    """
    Soft prefer/avoid lists from scored generations + tags + optional prefs.

    Empty history (and no prefs) → empty bias.
    """
    feedback = feedback or ()
    scores_by_gen: dict[int, list[FeedbackRecord]] = {}
    for fb in feedback:
        if fb.generation_id is None:
            continue
        scores_by_gen.setdefault(fb.generation_id, []).append(fb)

    prefer_acc: dict[str, _ScoreAcc] = {}
    avoid_acc: dict[str, _ScoreAcc] = {}
    mt_filter = (mission_type or "").strip().lower() or None

    for gen in generations:
        if mt_filter and (gen.mission_type or "").strip().lower() != mt_filter:
            continue
        behaviours = _behaviours_from_creative(extract_creative(gen.detail))
        if not behaviours:
            continue
        linked = scores_by_gen.get(gen.id, [])
        # Tag-driven signals
        for fb in linked:
            for tag in fb.tags or []:
                parsed = _parse_tag_behaviour(tag)
                if not parsed:
                    continue
                kind, bid = parsed
                if kind == "liked":
                    acc = prefer_acc.setdefault(bid, _ScoreAcc())
                    acc.weight += 2.0
                    acc.hits += 1
                else:
                    acc = avoid_acc.setdefault(bid, _ScoreAcc())
                    acc.weight += 2.0
                    acc.hits += 1
            if fb.score is None:
                continue
            delta = float(fb.score) - 3.0  # 1..5 centered at 3
            if abs(delta) < 0.5:
                continue
            target = prefer_acc if delta > 0 else avoid_acc
            for bid in behaviours:
                acc = target.setdefault(bid, _ScoreAcc())
                acc.weight += abs(delta)
                acc.hits += 1
        # Untagged success still mild prefer if no feedback at all for this gen
        if not linked and (gen.outcome or "").strip().lower() == "success":
            for bid in behaviours:
                acc = prefer_acc.setdefault(bid, _ScoreAcc())
                acc.weight += 0.25
                acc.hits += 1

    prefer = _rank_ids(prefer_acc)
    avoid = _rank_ids(avoid_acc)
    # Prefs strengthen / override
    prefs = prefs or {}
    pref_behaviours = _as_id_list(prefs.get(PREF_PREFERRED_BEHAVIOURS))
    avoid_behaviours = _as_id_list(prefs.get(PREF_AVOID_BEHAVIOURS))
    if pref_behaviours:
        prefer = tuple(dict.fromkeys([*pref_behaviours, *prefer]))
    if avoid_behaviours:
        avoid = tuple(dict.fromkeys([*avoid_behaviours, *avoid]))
    # Drop conflicts: explicit avoid wins over prefer
    if avoid:
        avoid_set = set(avoid)
        prefer = tuple(p for p in prefer if p not in avoid_set)

    level = str(prefs.get(PREF_CREATIVITY_LEVEL) or CREATIVITY_ASSERTIVE).strip().lower()
    if level == CREATIVITY_QUIET:
        prefer = prefer[:1]
    elif level == CREATIVITY_MAX:
        pass  # keep full lists
    else:
        prefer = prefer[:3]
        avoid = avoid[:3]

    return CreativeBias(prefer=prefer, avoid=avoid)


def _rank_ids(acc: Mapping[str, _ScoreAcc]) -> tuple[str, ...]:
    ranked = sorted(acc.items(), key=lambda kv: (-kv[1].weight, -kv[1].hits, kv[0]))
    return tuple(bid for bid, a in ranked if a.weight > 0)


def format_creative_bias_fragment(bias: CreativeBias) -> str:
    """Short prompt addendum; empty string when no bias."""
    if not bias.prefer and not bias.avoid:
        return ""
    lines = ["Creative taste from past generations (soft bias — still pick fitting recipes):"]
    if bias.prefer:
        lines.append(f"- Prefer mission_behaviour ids when inventing: {', '.join(bias.prefer)}")
    if bias.avoid:
        lines.append(f"- Soft-avoid unless the user asks: {', '.join(bias.avoid)}")
    return "\n".join(lines)


def load_creative_bias(
    *,
    db_path: Any = None,
    mission_type: str | None = None,
    history_limit: int = 20,
) -> CreativeBias:
    """Convenience: read memory DB and compute bias (soft-fails to empty)."""
    from .service import UserMemoryService

    try:
        mem = UserMemoryService(db_path=db_path)
        gens = mem.list_generations(limit=history_limit)
        fbs = mem.list_feedback(limit=history_limit * 2)
        prefs = mem.get_prefs()
    except OSError:
        return CreativeBias()
    return creative_bias_from_history(gens, fbs, mission_type=mission_type, prefs=prefs)


def detail_with_inferred_creative(
    detail: Mapping[str, Any] | None,
    spec: Any,
) -> dict[str, Any]:
    """Merge inferred creative into detail only when ``creative`` is absent."""
    out = dict(detail or {})
    if extract_creative(out):
        return out
    inferred = infer_creative_from_spec(spec)
    if not inferred:
        return out
    return merge_creative_into_detail(out, inferred)
