"""Local .env loading for OPENAI_API_KEY and related settings."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from dcs_miz_planner.agent.llm import live_llm_from_env
from dcs_miz_planner.env_load import load_local_dotenv, reset_dotenv_loaded_for_tests


@pytest.fixture(autouse=True)
def _reset_dotenv_flag() -> None:
    reset_dotenv_loaded_for_tests()
    yield
    reset_dotenv_loaded_for_tests()


def test_load_local_dotenv_sets_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=sk-from-dotenv\n", encoding="utf-8")
    assert load_local_dotenv(dotenv_path=env_file) is True
    assert os.environ.get("OPENAI_API_KEY") == "sk-from-dotenv"


def test_load_local_dotenv_does_not_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-from-shell")
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=sk-from-dotenv\n", encoding="utf-8")
    assert load_local_dotenv(dotenv_path=env_file) is True
    assert os.environ.get("OPENAI_API_KEY") == "sk-from-shell"


def test_load_local_dotenv_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "nope.env"
    assert load_local_dotenv(dotenv_path=missing) is False


def test_live_llm_from_env_reads_after_dotenv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=sk-dotenv-live\n", encoding="utf-8")
    load_local_dotenv(dotenv_path=env_file)
    client = live_llm_from_env()
    assert client.api_key == "sk-dotenv-live"
