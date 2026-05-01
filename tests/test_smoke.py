"""Smoke tests for ml-automation-databricks — validate plugin layout invariants."""

from __future__ import annotations

import json
import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def test_plugin_manifest_parses_and_has_required_fields():
    """Test that .cortex-plugin/plugin.json exists, is valid JSON, and has required fields."""
    manifest_path = PLUGIN_ROOT / ".cortex-plugin" / "plugin.json"

    # Check file exists
    assert manifest_path.exists(), f"Manifest not found at {manifest_path}"

    # Check it's valid JSON
    with open(manifest_path) as f:
        manifest = json.load(f)

    # Check required fields
    assert "name" in manifest, "Manifest missing 'name' field"
    assert "version" in manifest, "Manifest missing 'version' field"
    assert "description" in manifest, "Manifest missing 'description' field"

    # Check name starts with "spark-"
    name = manifest["name"]
    assert name.startswith("spark-"), f"Plugin name '{name}' does not start with 'spark-'"


def test_agents_md_lists_all_agents_and_skills():
    """Test that AGENTS.md exists and references all agents and skills."""
    agents_md_path = PLUGIN_ROOT / "AGENTS.md"

    # Check AGENTS.md exists
    assert agents_md_path.exists(), f"AGENTS.md not found at {agents_md_path}"

    # Read AGENTS.md content
    with open(agents_md_path) as f:
        agents_md_text = f.read()

    # Find all agents/*.md files
    agents_dir = PLUGIN_ROOT / "agents"
    agent_stems = set()
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            agent_stems.add(agent_file.stem)

    # Find all skills/*/ directories
    skills_dir = PLUGIN_ROOT / "skills"
    skill_names = set()
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith("."):
                skill_names.add(skill_dir.name)

    # Check all agents are referenced in AGENTS.md
    for agent_name in agent_stems:
        pattern = rf"\b/?{re.escape(agent_name)}\b"
        assert re.search(
            pattern, agents_md_text
        ), f"Agent '{agent_name}' not referenced in AGENTS.md"

    # Check all skills are referenced in AGENTS.md
    for skill_name in skill_names:
        pattern = rf"\b/?{re.escape(skill_name)}\b"
        assert re.search(
            pattern, agents_md_text
        ), f"Skill '{skill_name}' not referenced in AGENTS.md"
