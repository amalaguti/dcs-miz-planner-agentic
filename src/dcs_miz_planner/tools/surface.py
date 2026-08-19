"""Agent-facing tool callables (catalog lookups + validate/compile + user memory)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from ..catalog import CatalogService
from ..compiler import PyDCSCompiler
from ..install.campaigns import index_installed_campaigns
from ..install.models import TheatreInventory
from ..loader import SpecLoadError, load_mission_spec
from ..memory import UserMemoryService
from ..models import MissionSpec
from ..randomize import RandomizeError, parse_axes, randomize_mission_spec
from ..validation import validate_mission_spec as _validate_mission_spec
from .research import gather_research_notes, retrieval_mode
from .results import err_result, ok_result


def _strike_theatre_match(row: dict[str, Any], theatre_f: str) -> bool:
    """True when a catalog strike row is offerable for ``theatre_f``.

    WWII rows stay tagged ``TheChannel`` and land units are also offered on
    Normandy; sea_craft stay Channel-only. Modern trucks are tagged
    ``Caucasus`` and match that theatre by stored ``theatre_id``. Theatre
    ``Syria``, ``Nevada``, and ``Falklands`` dual-offer those modern **land** rows at query
    time without retagging stored ``theatre_id``.
    """
    row_theatre = str(row["theatre_id"])
    if row_theatre == theatre_f:
        return True
    if theatre_f in {"Syria", "Nevada", "Falklands"}:
        return (
            row_theatre == "Caucasus"
            and str(row.get("era_id") or "") == "modern"
            and str(row.get("domain") or "").casefold() == "land"
        )
    if theatre_f != "Normandy":
        return False
    if row_theatre != "TheChannel":
        return False
    if str(row.get("era_id") or "") != "wwii":
        return False
    return str(row.get("domain") or "").casefold() == "land"


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


def list_strike_targets(
    *,
    domain: str | None = None,
    class_id: str | None = None,
    q: str | None = None,
    theatre: str | None = None,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """List known Channel strike/recon units from catalog SQLite (after sync).

    Optional filters: ``domain`` (``land``|``sea``), ``class_id`` (strike_target_class
    id), case-insensitive substring ``q`` on unit_id/label, and ``theatre``.
    Does not read registry YAML or PyDCS at call time. Strike rows stay tagged
    TheChannel; WWII land units are also offered when ``theatre`` is Normandy.
    Sea-domain units stay Channel-only. Modern land trucks tagged Caucasus are
    also offered when ``theatre`` is Syria, Nevada, or Falklands.
    """
    domain_f = (domain or "").strip().casefold() or None
    if domain_f is not None and domain_f not in {"land", "sea"}:
        return err_result(
            "domain must be 'land' or 'sea' when set",
            code="invalid_query",
            domain=domain,
        )
    class_f = (class_id or "").strip() or None
    needle = (q or "").strip().casefold() or None
    theatre_f = (theatre or "").strip() or None

    service = _catalog(db_path)
    rows = service.list_rows("strike_units")
    units: list[dict[str, Any]] = []
    for row in rows:
        row_domain = str(row["domain"])
        if domain_f is not None and row_domain.casefold() != domain_f:
            continue
        if theatre_f is not None and not _strike_theatre_match(row, theatre_f):
            continue
        class_ids = row.get("class_ids")
        if not isinstance(class_ids, list):
            class_ids = []
        class_ids_s = [str(c) for c in class_ids]
        if class_f is not None and class_f not in class_ids_s:
            continue
        unit_id = str(row["unit_id"])
        label = str(row["label"])
        if needle is not None and (
            needle not in unit_id.casefold() and needle not in label.casefold()
        ):
            continue
        units.append(
            {
                "unit_id": unit_id,
                "label": label,
                "domain": row_domain,
                "class_ids": class_ids_s,
                "theatre": str(row["theatre_id"]),
                "era_id": str(row.get("era_id") or ""),
            }
        )
    return ok_result(units=units)


def list_mission_options(
    *,
    theatre: str | None = None,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Return known planning enums, enriched options, and offerable theatres.

    When ``theatre`` is set, ``channel_place`` rows whose ``meta.theatre`` does
    not match are omitted. Other families pass through. Omitted ``theatre``
    returns all rows.
    """
    theatre_f = (theatre or "").strip() or None
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
        if (
            theatre_f is not None
            and opt.family == "channel_place"
            and str(meta.get("theatre") or "") != theatre_f
        ):
            continue
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


def get_mission_spec_schema(
    mission_type: str,
    theatre: str | None = None,
    airfield: str | None = None,
) -> dict[str, Any]:
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
    theatre_id = (theatre or "").strip() or None
    airfield_id = (airfield or "").strip() or None
    try:
        view = build_spec_schema(key, theatre=theatre_id, airfield=airfield_id)
    except ValueError as exc:
        msg = str(exc)
        code = (
            "combat_unsupported_theatre"
            if "not supported for theatre" in msg
            else "unsupported_mission_type"
        )
        return err_result(
            msg,
            code=code,
            mission_type=key,
            theatre=theatre_id,
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
    warnings = [
        {
            "code": w.code,
            "path": w.path,
            "message": w.message,
            "hint": w.hint,
        }
        for w in result.warnings
    ]
    if result.ok:
        return ok_result(path=str(path), errors=errors, warnings=warnings)
    return err_result(
        "Mission Spec validation failed",
        code="validation_failed",
        path=str(path),
        errors=errors,
        warnings=warnings,
    )


def compile_mission(
    spec_path: str | Path,
    output_path: str | Path,
    *,
    db_path: Path | str | None = None,
    inventory: TheatreInventory | None = None,
    voice: str | None = None,
    out_root: Path | str | None = None,
) -> dict[str, Any]:
    """Compile a Mission Spec YAML to a ``.miz`` via PyDCSCompiler.

    ``output_path`` MUST resolve under ``out_root`` (default: ``<repo>/out``).
    """
    path = Path(spec_path)
    if not path.is_file():
        return err_result(f"Spec not found: {path}", code="not_found", path=str(path))

    root = Path(out_root) if out_root is not None else Path(__file__).resolve().parents[3] / "out"
    root = root.resolve()
    out = Path(output_path)
    try:
        resolved_out = out.resolve()
        resolved_out.relative_to(root)
    except (OSError, ValueError):
        return err_result(
            f"Compile output must be under {root} (got {out})",
            code="path_not_allowed",
            path=str(out),
        )

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

    resolved_voice = voice
    if voice is not None:
        from ..agent.voice import resolve_voice

        resolved_voice = resolve_voice(cli_voice=voice)

    try:
        written = PyDCSCompiler(inventory=inventory).compile(
            spec, resolved_out, voice=resolved_voice
        )
    except ValueError as exc:
        return err_result(str(exc), code="compile_failed", path=str(path))
    return ok_result(path=str(path), output=str(written))


def reweather_mission_file(
    miz_path: str | Path,
    weather: str,
    *,
    seed: int | None = None,
    spec_path: str | Path | None = None,
    voice: str | None = None,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Overwrite weather on an existing ``.miz`` (Spec recompile or miz patch)."""
    inventory = None
    if db_path is not None:
        from ..install import InventoryService

        inventory = InventoryService(db_path=db_path).get()
    try:
        from ..reweather import ReweatherError, reweather_mission

        result = reweather_mission(
            miz_path,
            weather,
            seed=seed,
            spec_path=spec_path,
            voice=voice,
            inventory=inventory,
        )
    except ReweatherError as exc:
        return err_result(str(exc), code="reweather_failed", path=str(miz_path))
    return ok_result(**{k: v for k, v in result.items() if k != "ok"})


def randomize_mission(
    *,
    seed: int,
    spec_path: str | Path | None = None,
    spec: dict[str, Any] | None = None,
    axes: list[str] | str | None = None,
    annotate: bool = False,
    validate: bool = True,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Seeded Spec→Spec variation; returns Spec dict (does not compile)."""
    del db_path
    base: MissionSpec
    source_path: str | None = None
    if spec_path is not None:
        path = Path(spec_path)
        if not path.is_file():
            return err_result(f"Spec not found: {path}", code="not_found", path=str(path))
        try:
            base = load_mission_spec(path)
        except SpecLoadError as exc:
            return err_result(str(exc), code="spec_load_error", path=str(path))
        source_path = str(path)
    elif spec is not None:
        try:
            base = MissionSpec.model_validate(spec)
        except ValidationError as exc:
            return err_result(str(exc), code="spec_load_error")
    else:
        return err_result(
            "Provide spec_path or spec",
            code="invalid_query",
        )

    try:
        seed_i = int(seed)
    except (TypeError, ValueError):
        return err_result("seed must be a non-negative integer", code="invalid_query")

    try:
        applied = parse_axes(axes)
        out = randomize_mission_spec(base, seed_i, axes=applied, annotate=annotate)
    except RandomizeError as exc:
        return err_result(str(exc), code="randomize_error")

    if validate:
        result = _validate_mission_spec(out)
        if not result.ok:
            errors = [
                {
                    "code": e.code,
                    "path": e.path,
                    "message": e.message,
                    "hint": e.hint,
                }
                for e in result.errors
            ]
            return err_result(
                "Randomized Spec failed validation",
                code="validation_failed",
                errors=errors,
                seed=seed_i,
                axes=list(applied),
            )

    payload: dict[str, Any] = {
        "spec": out.model_dump(mode="json"),
        "seed": seed_i,
        "axes": list(applied),
    }
    if source_path is not None:
        payload["path"] = source_path
    return ok_result(**payload)


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
    focus: str | None = None,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """
    Gather short tactics/procedure/history notes for commander briefs.

    Soft-fails: always returns ok with notes (fixtures on offline or live error/empty).
    Live mode sets ``warning`` when web retrieval fails or returns nothing.
    ``focus="mission_design"`` biases live search toward User Files / mission repos /
    ME patterns and matches local gitignored research/ QAG HTML offline when present
    (still not Spec-field authority).
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
        focus=focus,
    )
    payload: dict[str, Any] = {
        "notes": notes,
        "query": q,
        "retrieval": retrieval_mode(notes),
    }
    if mission_type:
        payload["mission_type"] = mission_type
    if theatre:
        payload["theatre"] = theatre
    if aircraft:
        payload["aircraft"] = aircraft
    if focus:
        payload["focus"] = focus
    if warning:
        payload["warning"] = warning
    return ok_result(**payload)


def list_installed_campaigns(
    *,
    dcs_root: Path | str | None = None,
    campaigns_dir: Path | str | None = None,
    db_path: Path | str | None = None,
    include_doc_text: bool = False,
) -> dict[str, Any]:
    """
    List local DCS campaigns under ``Mods/campaigns`` for mission inspiration.

    Returns campaign name, mission ``.miz`` filenames, ``Doc/`` PDF filenames, and a
    short ``.cmp`` description when present. When ``include_doc_text`` is true, Doc
    entries include short PDF excerpts (mtime/size cached under ``db_path``). Read-only;
    does not import ``.miz`` into Spec.
    """
    from ..install.doc_extract import DocTextCache, enrich_campaign_docs
    from ..install.store import default_db_path

    index = index_installed_campaigns(explicit_root=dcs_root, campaigns_dir=campaigns_dir)
    cache: DocTextCache | None = None
    if include_doc_text:
        cache = DocTextCache(db_path if db_path is not None else default_db_path())

    campaigns: list[dict[str, Any]] = []
    for c in index.campaigns:
        if include_doc_text:
            docs_out = [
                {"filename": d.filename, "excerpt": d.excerpt}
                for d in enrich_campaign_docs(c.path, [d.filename for d in c.docs], cache=cache)
            ]
        else:
            docs_out = [{"filename": d.filename, "excerpt": None} for d in c.docs]
        campaigns.append(
            {
                "name": c.name,
                "path": c.path,
                "description": c.description,
                "cmp_file": c.cmp_file,
                "missions": [m.filename for m in c.missions],
                "docs": docs_out,
            }
        )
    diags = [{"message": d.message, "source": d.source} for d in index.diagnostics]
    payload: dict[str, Any] = {
        "campaigns": campaigns,
        "dcs_roots": list(index.dcs_roots),
        "diagnostics": diags,
        "include_doc_text": include_doc_text,
    }
    if not campaigns and not index.dcs_roots and campaigns_dir is None and dcs_root is None:
        # No install discovered — structured empty, non-fatal for the agent.
        payload["warning"] = "no DCS World root or campaigns found"
    elif not campaigns:
        payload["warning"] = "no campaigns listed under Mods/campaigns"
    return ok_result(**payload)
