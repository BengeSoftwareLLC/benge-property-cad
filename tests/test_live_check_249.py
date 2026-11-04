"""Temporary CI-only rule for the data-plane#249 BYOI live check; removed after the check."""

import os

import pytest

import config


@pytest.mark.skipif(os.environ.get("GITHUB_WORKFLOW") != "File Template CAD CI", reason="CI-only live-check rule")
def test_project_name_stays_file_template() -> None:
    assert config.PROJECT_NAME == "File Template", "PROJECT_NAME must stay 'File Template' (live-check rule)"
