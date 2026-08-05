"""Load optional local ``.env`` into process environment (never overrides existing)."""

from __future__ import annotations

from pathlib import Path

_LOADED = False


def load_local_dotenv(*, dotenv_path: Path | str | None = None) -> bool:
    """
    Load a ``.env`` file into ``os.environ`` if present.

    Existing environment variables win (``override=False``). Safe to call repeatedly.
    Returns True when a file was found and loaded (or already loaded this process).
    """
    global _LOADED
    if _LOADED and dotenv_path is None:
        return True

    try:
        from dotenv import load_dotenv
    except ImportError:  # pragma: no cover — dependency declared in pyproject
        return False

    path = Path(dotenv_path) if dotenv_path is not None else Path.cwd() / ".env"
    if not path.is_file():
        return False
    load_dotenv(dotenv_path=path, override=False)
    if dotenv_path is None:
        _LOADED = True
    return True


def reset_dotenv_loaded_for_tests() -> None:
    """Test helper: allow load_local_dotenv to run again."""
    global _LOADED
    _LOADED = False
