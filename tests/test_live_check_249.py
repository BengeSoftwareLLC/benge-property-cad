"""Temporary CI-only rule for the data-plane#249 BYOI live check; removed after the check."""

import os
from pathlib import Path

import pytest


@pytest.mark.skipif(os.environ.get("GITHUB_WORKFLOW") != "File Template CAD CI", reason="CI-only live-check rule")
def test_project_name_stays_file_template() -> None:
    source = (Path(__file__).resolve().parents[1] / "config.py").read_text()
    assert 'PROJECT_NAME = "File Template"\n' in source, "PROJECT_NAME must stay 'File Template' (live-check rule)"
