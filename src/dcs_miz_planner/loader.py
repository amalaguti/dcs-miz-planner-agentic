"""Load and validate a Mission Spec from YAML."""

from __future__ import annotations

from pathlib import Path

import yaml

from .models import MissionSpec


def load_mission_spec(path: str | Path) -> MissionSpec:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return MissionSpec.model_validate(data)
