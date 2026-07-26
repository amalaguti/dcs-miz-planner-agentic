"""Load and validate a Mission Spec from YAML."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from .models import MissionSpec


class SpecLoadError(ValueError):
    """Raised when a Mission Spec YAML is malformed or fails validation.

    Carries a user-facing message so the CLI can report expected validation
    failures without dumping a stack trace.
    """


def load_mission_spec(path: str | Path) -> MissionSpec:
    path = Path(path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SpecLoadError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise SpecLoadError(
            f"{path}: expected a Mission Spec mapping at the top level, got {type(data).__name__}"
        )
    try:
        return MissionSpec.model_validate(data)
    except ValidationError as exc:
        raise SpecLoadError(_format_validation_error(path, exc)) from exc


def _format_validation_error(path: Path, exc: ValidationError) -> str:
    lines = [f"{path}: invalid Mission Spec ({exc.error_count()} error(s)):"]
    for err in exc.errors():
        loc = ".".join(str(p) for p in err["loc"]) or "(root)"
        lines.append(f"  - {loc}: {err['msg']}")
    return "\n".join(lines)
