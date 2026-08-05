#!/usr/bin/env python3
"""Live vague-ask harness for eval-agent-creativity skill.

Outputs under out/creative_eval/ (gitignored). Does not touch the default user DB
unless --db is passed explicitly to a real path.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]
CATALOG_PATH = SKILL_DIR / "prompt-catalog.md"
DEFAULT_OUT = REPO_ROOT / "out" / "creative_eval"


def _ensure_src_path() -> None:
    src = REPO_ROOT / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


def parse_catalog(path: Path) -> list[dict[str, str]]:
    """Parse ## id blocks with **prompt:** lines from prompt-catalog.md."""
    text = path.read_text(encoding="utf-8")
    scenarios: list[dict[str, str]] = []
    blocks = re.split(r"^## ", text, flags=re.MULTILINE)
    for block in blocks[1:]:
        lines = block.strip().splitlines()
        if not lines:
            continue
        sid = lines[0].strip()
        if sid.lower().startswith("catalog maintenance"):
            continue
        prompt = ""
        for line in lines[1:]:
            m = re.match(r"-\s+\*\*prompt:\*\*\s+(.*)$", line.strip())
            if m:
                prompt = m.group(1).strip()
                break
        if sid and prompt:
            scenarios.append({"id": sid, "prompt": prompt})
    return scenarios


def summarize_spec(path: Path) -> dict:
    from dcs_miz_planner.loader import load_mission_spec

    spec = load_mission_spec(path)
    conds: list[str] = []
    acts: list[str] = []
    for t in spec.triggers or []:
        for c in t.when or []:
            conds.append(str(getattr(c, "type", "?")))
        for a in t.then or []:
            acts.append(str(getattr(a, "type", "?")))
    late = any(getattr(e, "late_activation", False) for e in (spec.enemies or []))
    late |= any(getattr(t, "late_activation", False) for t in (spec.targets or []))
    narr = bool(getattr(getattr(spec, "narrative", None), "enabled", False))
    return {
        "mission_type": spec.mission_type.value,
        "name": spec.name,
        "narrative_enabled": narr,
        "late_activation": late,
        "zones": [z.name for z in (spec.zones or [])],
        "condition_types": sorted(set(conds)),
        "action_types": sorted(set(acts)),
        "trigger_count": len(spec.triggers or []),
        "enemy_count": len(spec.enemies or []),
        "has_altitude_or_speed": bool(
            set(conds)
            & {
                "unit_altitude_higher",
                "unit_altitude_lower",
                "unit_speed_higher",
                "unit_speed_lower",
            }
        ),
        "has_mark_or_smoke": bool(set(acts) & {"mark", "smoke"}),
        "has_radio_activate": bool(set(acts) & {"radio_item_add", "activate_group"}),
        "incomplete_late_act": late and not (set(acts) & {"activate_group"}),
        "has_sound_or_flags": bool(
            ("sound" in acts)
            or set(conds) & {"flag_equals", "flag_more", "flag_less", "time_since_flag"}
        ),
        "has_group_life_less": "group_life_less" in conds,
    }


def preflight(*, dcs_root: str | None, db: Path) -> dict:
    from dcs_miz_planner.catalog import CatalogService
    from dcs_miz_planner.tools import list_installed_campaigns, list_mission_options

    CatalogService(db_path=db).sync()
    opts = list_mission_options(db_path=db)
    behaviours = [
        o["id"] for o in opts.get("options", []) if o.get("family") == "mission_behaviour"
    ]
    inspirations = [
        o["id"] for o in opts.get("options", []) if o.get("family") == "mission_inspiration"
    ]
    camp_kwargs: dict = {}
    if dcs_root:
        camp_kwargs["dcs_root"] = dcs_root
    camps = list_installed_campaigns(**camp_kwargs)
    return {
        "behaviours": behaviours,
        "inspirations": inspirations,
        "campaigns_ok": bool(camps.get("ok")),
        "campaign_count": len(camps.get("campaigns") or []),
        "campaigns": [
            {
                "name": c["name"],
                "docs": len(c.get("docs") or []),
                "missions": len(c.get("missions") or []),
            }
            for c in (camps.get("campaigns") or [])
        ],
    }


def run_scenarios(
    scenarios: list[dict[str, str]],
    *,
    out_dir: Path,
    db: Path,
    stub: bool,
    voice: str,
) -> list[dict]:
    from dcs_miz_planner.agent import StubLLM, live_llm_from_env, plan_mission
    from dcs_miz_planner.memory import UserMemoryService

    llm = StubLLM() if stub else live_llm_from_env()
    results: list[dict] = []
    for i, sc in enumerate(scenarios, 1):
        out = out_dir / f"{sc['id']}.yaml"
        print(f"\n=== {sc['id']}: {sc['prompt']!r} ===", flush=True)
        result = plan_mission(
            sc["prompt"],
            out,
            llm=llm,
            compile_output=False,
            db_path=db,
            voice=voice,
            verbose=True,
            max_turns=10,
        )
        row: dict = {
            "id": sc["id"],
            "prompt": sc["prompt"],
            "ok": result.ok,
            "error": result.error,
            "generation_id": result.generation_id,
            "spec_path": str(result.spec_path) if result.spec_path else None,
        }
        if result.ok and result.spec_path:
            row["spec"] = summarize_spec(Path(result.spec_path))
            print(json.dumps(row["spec"], indent=2), flush=True)
        else:
            print(f"FAILED: {result.error}", flush=True)
        results.append(row)

    mem = UserMemoryService(db_path=db)
    hist = []
    for g in mem.list_generations(limit=50):
        hist.append(
            {
                "id": g.id,
                "mission_type": g.mission_type,
                "outcome": g.outcome,
                "creative": (g.detail or {}).get("creative"),
                "prompt": (g.prompt or "")[:100],
            }
        )
    report = {"results": results, "history": hist, "stub": stub}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out_dir / 'report.json'}", flush=True)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List scenario ids")
    parser.add_argument("--preflight", action="store_true", help="Catalog/campaigns only")
    parser.add_argument("--only", action="append", default=[], help="Scenario id (repeatable)")
    parser.add_argument("--stub", action="store_true", help="Stub LLM (harness smoke only)")
    parser.add_argument("--voice", default="raf")
    parser.add_argument("--dcs-root", default=None, help="DCS World root for campaigns")
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output dir (default {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="Eval SQLite (default: <out>/eval.sqlite)",
    )
    args = parser.parse_args(argv)

    scenarios = parse_catalog(CATALOG_PATH)
    if args.list:
        for sc in scenarios:
            print(f"{sc['id']}\t{sc['prompt']}")
        return 0

    _ensure_src_path()
    from dcs_miz_planner.env_load import load_local_dotenv

    load_local_dotenv()

    out_dir = args.out if args.out.is_absolute() else REPO_ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    db = args.db if args.db is not None else out_dir / "eval.sqlite"

    pf = preflight(dcs_root=args.dcs_root, db=db)
    print("=== PREFLIGHT ===", flush=True)
    print(json.dumps(pf, indent=2), flush=True)
    if args.preflight:
        return 0 if pf["behaviours"] and pf["inspirations"] else 1

    selected = scenarios
    if args.only:
        want = set(args.only)
        selected = [s for s in scenarios if s["id"] in want]
        missing = want - {s["id"] for s in selected}
        if missing:
            print(f"Unknown scenario ids: {sorted(missing)}", file=sys.stderr)
            return 2
    if not selected:
        print("No scenarios selected", file=sys.stderr)
        return 2

    results = run_scenarios(selected, out_dir=out_dir, db=db, stub=args.stub, voice=args.voice)
    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
