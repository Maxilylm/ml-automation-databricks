"""Shared pytest fixtures for ml-automation-databricks."""

from __future__ import annotations

import pytest


@pytest.fixture
def mock_llm_response():
    """Fixture providing a mock LLM response."""
    return {
        "content": "Test response",
        "model": "claude-opus-4-7",
        "stop_reason": "end_turn",
    }


@pytest.fixture
def sample_dataset():
    """Fixture providing sample dataset for testing."""
    return {
        "rows": [
            {"id": 1, "name": "test_row_1", "value": 100},
            {"id": 2, "name": "test_row_2", "value": 200},
            {"id": 3, "name": "test_row_3", "value": 300},
        ],
        "columns": ["id", "name", "value"],
        "row_count": 3,
    }


@pytest.fixture
def temp_workspace(tmp_path):
    """Fixture providing a temporary workspace directory."""
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()

    # Create standard subdirectories
    (workspace_dir / "data").mkdir()
    (workspace_dir / "models").mkdir()
    (workspace_dir / "logs").mkdir()

    return workspace_dir
