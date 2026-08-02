"""Agent-facing tool callables (catalog lookups + validate/compile + user memory)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..catalog import CatalogService
from ..compiler import PyDCSCompiler
from ..install.models import TheatreInventory
from ..loader import SpecLoadError, load_mission_spec
from ..memory import UserMemoryService
from ..validation import validate_mission_spec as _validate_mission_spec
from .research import gather_research_notes
from .results import err_result, ok_result


def _catalog(db_path: Path | str | None = None) -> CatalogService:
    return CatalogService(db_path=db_path)


def _memory(db_path: Path | str | None = None) -> UserMemoryService:
    return UserMemoryService(db_path=db_path)


def find_airfield(
    query: str,
    *,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Find known catalog airfields whose name matches ``query`` (case-insensitive substring)."""
    q = (query or "").strip()
    if not q:
        return err_result("query must be a non-empty string", code="invalid_query")

    service = _catalog(db_path)
    rows = service.list_rows("airfields")
    needle = q.casefold()
    matches = [r for r in rows if needle in str(r["name"]).casefold()]
    if not matches:
        return err_result(
            f"No known airfield matching {query!r}",
            code="not_found",
            query=query,
            airfields=[],
        )
    return ok_result(query=query, airfields=matches)


def get_aircraft_details(
    aircraft_id: str,
    *,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Return known catalog details for one aircraft id."""
    aid = (aircraft_id or "").strip()
    if not aid:
        return err_result("aircraft_id must be a non-empty string", code="invalid_query")

    service = _catalog(db_path)
    rows = service.list_rows("aircraft")
    for row in rows:
        if row["aircraft_id"] == aid:
            return ok_result(
                aircraft_id=row["aircraft_id"],
                radio_mhz=row["radio_mhz"],
            )
    known = [str(r["aircraft_id"]) for r in rows]
    return err_result(
        f"Unknown aircraft {aircraft_id!r}",
        code="not_found",
        aircraft_id=aircraft_id,
        known=known,
    )


def list_mission_options(
    *,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Return known planning enums, enriched options, and offerable theatres."""
    service = _catalog(db_path)
    snap = service.ensure_synced()
    theatres = service.list_theatres(include_discovered=True)
    offerable = [
        {
            "theatre_id": v.theatre_id,
            "known": v.known,
            "installed": v.installed,
            "install_state": v.install_state,
            "planner_supported": v.planner_supported,
            "offerable": v.offerable,
        }
        for v in theatres
        if v.offerable
    ]
    options = []
    for opt in snap.planning_options:
        try:
            meta = json.loads(opt.meta_json) if opt.meta_json else {}
        except json.JSONDecodeError:
            meta = {}
        if not isinstance(meta, dict):
            meta = {}
        options.append(
            {
                "family": opt.family,
                "id": opt.id,
                "label": opt.label,
                "description": opt.description,
                "support": opt.support,
                "meta": meta,
            }
        )
    return ok_result(
        mission_types=[r.value for r in snap.mission_types],
        start_types=[r.value for r in snap.start_types],
        weather_presets=[w.name for w in snap.weather_presets],
        coalitions=[r.value for r in snap.coalitions],
        objective_types=[r.value for r in snap.objective_types],
        countries=[r.value for r in snap.countries],
        aircraft=[a.aircraft_id for a in snap.aircraft],
        options=options,
        offerable_theatres=offerable,
    )


def get_mission_spec_schema(mission_type: str) -> dict[str, Any]:
    """Return a compact derived Mission Spec example + notes for ``mission_type``."""
    # Lazy import: avoid tools ↔ agent package init cycles.
    from ..agent.spec_schema import build_spec_schema, supported_mission_types

    key = (mission_type or "").strip()
    if not key:
        return err_result(
            "mission_type must be a non-empty string",
            code="invalid_mission_type",
            supported=list(supported_mission_types()),
        )
    try:
        view = build_spec_schema(key)
    except ValueError as exc:
        return err_result(
            str(exc),
            code="unsupported_mission_type",
            mission_type=key,
            supported=list(supported_mission_types()),
        )
    except FileNotFoundError as exc:
        return err_result(str(exc), code="example_missing", mission_type=key)
    return ok_result(
        mission_type=view.mission_type,
        example=view.example,
        notes=list(view.notes),
        anti_patterns=list(view.anti_patterns),
    )


def validate_mission_spec(
    spec_path: str | Path,
    *,
    db_path: Path | str | None = None,
    inventory: TheatreInventory | None = None,
) -> dict[str, Any]:
    """Validate a Mission Spec YAML path via the shared validation engine."""
    path = Path(spec_path)
    if not path.is_file():
        return err_result(f"Spec not found: {path}", code="not_found", path=str(path))

    try:
        spec = load_mission_spec(path)
    except SpecLoadError as exc:
        return err_result(str(exc), code="spec_load_error", path=str(path))

    if inventory is None and db_path is not None:
        from ..install import InventoryService

        inventory = InventoryService(db_path=db_path).get()

    result = _validate_mission_spec(spec, inventory=inventory)
    errors = [
        {
            "code": e.code,
            "path": e.path,
            "message": e.message,
            "hint": e.hint,
        }
        for e in result.errors
    ]
    if result.ok:
        return ok_result(path=str(path), errors=errors)
    return err_result(
        "Mission Spec validation failed",
        code="validation_failed",
        path=str(path),
        errors=errors,
    )


def compile_mission(
    spec_path: str | Path,
    output_path: str | Path,
    *,
    db_path: Path | str | None = None,
    inventory: TheatreInventory | None = None,
) -> dict[str, Any]:
    """Compile a Mission Spec YAML to a ``.miz`` via PyDCSCompiler."""
    path = Path(spec_path)
    if not path.is_file():
        return err_result(f"Spec not found: {path}", code="not_found", path=str(path))

    try:
        spec = load_mission_spec(path)
    except SpecLoadError as exc:
        return err_result(str(exc), code="spec_load_error", path=str(path))

    if inventory is None and db_path is not None:
        from ..install import InventoryService

        inventory = InventoryService(db_path=db_path).get()

    pre = validate_mission_spec(path, inventory=inventory)
    if not pre.get("ok"):
        return pre

    out = Path(output_path)
    try:
        written = PyDCSCompiler(inventory=inventory).compile(spec, out)
    except ValueError as exc:
        return err_result(str(exc), code="compile_failed", path=str(path))
    return ok_result(path=str(path), output=str(written))


def get_user_prefs(
    keys: list[str] | None = None,
    *,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Return stored user preferences (empty map when none are set)."""
    prefs = _memory(db_path).get_prefs(keys)
    return ok_result(prefs=prefs)


def set_user_prefs(
    prefs: dict[str, Any] | None = None,
    *,
    db_path: Path | str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """Upsert preference keys; returns the full prefs map after write."""
    payload = dict(prefs or {})
    # Allow flat tool-call kwargs (set_user_prefs(preferred_airfield="Manston")).
    for key, value in extra.items():
        if key == "db_path":
            continue
        payload[key] = value
    if not payload:
        return err_result("prefs must include at least one key", code="invalid_query")
    updated = _memory(db_path).set_prefs(payload)
    return ok_result(prefs=updated)


def record_generation(
    *,
    outcome: str,
    prompt: str | None = None,
    mission_type: str | None = None,
    theatre: str | None = None,
    spec_path: str | None = None,
    miz_path: str | None = None,
    detail: dict[str, Any] | None = None,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Append a generation history row."""
    outcome_s = (outcome or "").strip()
    if not outcome_s:
        return err_result("outcome must be a non-empty string", code="invalid_query")
    gid = _memory(db_path).record_generation(
        outcome=outcome_s,
        prompt=prompt,
        mission_type=mission_type,
        theatre=theatre,
        spec_path=spec_path,
        miz_path=miz_path,
        detail=detail,
    )
    return ok_result(generation_id=gid, outcome=outcome_s)


def record_feedback(
    *,
    source: str = "agent",
    generation_id: int | None = None,
    score: int | None = None,
    note: str | None = None,
    tags: list[Any] | None = None,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Append satisfaction feedback, optionally linked to a generation id."""
    source_s = (source or "").strip() or "agent"
    if score is None and not (note or "").strip() and not tags:
        return err_result(
            "feedback requires score, note, and/or tags",
            code="invalid_query",
        )
    fid = _memory(db_path).record_feedback(
        source=source_s,
        generation_id=generation_id,
        score=score,
        note=note,
        tags=tags,
    )
    return ok_result(feedback_id=fid, generation_id=generation_id, source=source_s)


def list_generation_history(
    limit: int = 20,
    *,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """List recent generation history rows (newest first)."""
    rows = _memory(db_path).list_generations(limit=limit)
    generations = [
        {
            "id": r.id,
            "created_at": r.created_at,
            "prompt": r.prompt,
            "mission_type": r.mission_type,
            "theatre": r.theatre,
            "spec_path": r.spec_path,
            "miz_path": r.miz_path,
            "outcome": r.outcome,
            "detail": r.detail,
        }
        for r in rows
    ]
    return ok_result(generations=generations)


def research_guidance(
    query: str,
    *,
    mission_type: str | None = None,
    theatre: str | None = None,
    aircraft: str | None = None,
    live: bool | None = None,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """
    Gather short tactics/procedure/history notes for commander briefs.

    Soft-fails: always returns ok with notes (fixtures on offline or live error/empty).
    Live mode sets ``warning`` when web retrieval fails or returns nothing.
    Research is not Spec or DCS-id authority. ``db_path`` unused (tool signature parity).
    """
    del db_path
    q = (query or "").strip()
    if not q:
        return err_result("query must be a non-empty string", code="invalid_query")
    notes, warning = gather_research_notes(
        q,
        mission_type=mission_type,
        theatre=theatre,
        aircraft=aircraft,
        live=live,
    )
    payload: dict[str, Any] = {"notes": notes, "query": q}
    if mission_type:
        payload["mission_type"] = mission_type
    if theatre:
        payload["theatre"] = theatre
    if aircraft:
        payload["aircraft"] = aircraft
    if warning:
        payload["warning"] = warning
    return ok_result(**payload)
