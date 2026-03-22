from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import yaml


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "instantiate_project.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("instantiate_project", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    write_text(
        tmp_path / "projects_manifest.yaml",
        """workspace_name: le-classeux
structure_version: 1
strategy: project_index
projects:
  - id: project-template
    name: project-template
    path: projects/project-template
    manifest: projects/project-template/project_manifest.yaml
    purpose: "Template project."
""",
    )

    project_root = tmp_path / "projects" / "project-template"
    write_text(
        project_root / "README.md",
        """# project-template

## Current Overview Summary

- Last updated: `2026-03-22`
- Current phase: `Template / structure simplification`

`project-template` is the reusable scaffold.

## How To Work In This Project

- Follow the project guidance.
""",
    )
    write_text(
        project_root / "project_manifest.yaml",
        """project_name: project-template
project_slug: project-template
structure_version: 2
strategy: progressive_disclosure
top_level_sections: []
""",
    )
    write_text(
        project_root / "00_GOVERNANCE" / "change_log" / "change_log.json",
        json.dumps(
            [
                {
                    "change_summary": "template history that must not survive instantiation",
                    "date": "2026-03-20-10h00",
                }
            ],
            indent=2,
        ),
    )
    write_text(
        project_root
        / "07_PROJECT_EXECUTION"
        / "execution_items"
        / "README.md",
        "# Execution Items\n",
    )
    write_text(
        project_root
        / "07_PROJECT_EXECUTION"
        / "execution_items"
        / "local_manifest.yaml",
        """folder: execution_items
summary: "Execution items live here."
files:
  - name: README.md
    summary: "Folder guidance."
    original_links: []
  - name: local_manifest.yaml
    summary: "Folder index."
    original_links: []
  - name: EXEC-ISSUE-001-sample.json
    summary: "Sample item."
    original_links: []
""",
    )
    write_text(
        project_root
        / "07_PROJECT_EXECUTION"
        / "execution_items"
        / "EXEC-ISSUE-001-sample.json",
        json.dumps({"id": "EXEC-ISSUE-001", "summary": "sample"}, indent=2),
    )
    write_text(
        project_root / "00_GOVERNANCE" / "README.md",
        "This folder belongs to the project-template context bank.\n",
    )

    return tmp_path


def test_instantiation_bootstraps_new_project_from_template(workspace: Path) -> None:
    module = load_module()

    module.instantiate_project(
        workspace_root=workspace,
        project_slug="alpha-lab",
        project_name="Alpha Lab",
        purpose="Primary Alpha Lab context bank.",
        date_stamp="2026-03-22",
        timestamp="2026-03-22-16h00",
    )

    target_root = workspace / "projects" / "alpha-lab"
    assert target_root.exists()
    assert not (target_root / "07_PROJECT_EXECUTION" / "execution_items" / "EXEC-ISSUE-001-sample.json").exists()

    project_manifest = yaml.safe_load((target_root / "project_manifest.yaml").read_text(encoding="utf-8"))
    assert project_manifest["project_name"] == "Alpha Lab"
    assert project_manifest["project_slug"] == "alpha-lab"

    readme = (target_root / "README.md").read_text(encoding="utf-8")
    assert "# Alpha Lab" in readme
    assert "projects/alpha-lab" not in readme or "project-template" not in readme
    assert "Current phase: `Instantiation`" in readme
    assert "Primary Alpha Lab context bank." in readme

    change_log = json.loads(
        (target_root / "00_GOVERNANCE" / "change_log" / "change_log.json").read_text(encoding="utf-8")
    )
    assert change_log == [
        {
            "change_summary": "instantiated `projects/alpha-lab` from `projects/project-template` and registered it in `projects_manifest.yaml`",
            "date": "2026-03-22-16h00",
        }
    ]

    local_manifest = yaml.safe_load(
        (
            target_root
            / "07_PROJECT_EXECUTION"
            / "execution_items"
            / "local_manifest.yaml"
        ).read_text(encoding="utf-8")
    )
    assert [entry["name"] for entry in local_manifest["files"]] == [
        "README.md",
        "local_manifest.yaml",
    ]

    workspace_manifest = yaml.safe_load((workspace / "projects_manifest.yaml").read_text(encoding="utf-8"))
    assert workspace_manifest["projects"][-1] == {
        "id": "alpha-lab",
        "name": "Alpha Lab",
        "path": "projects/alpha-lab",
        "manifest": "projects/alpha-lab/project_manifest.yaml",
        "purpose": "Primary Alpha Lab context bank.",
    }

    assert "project-template" not in (target_root / "00_GOVERNANCE" / "README.md").read_text(encoding="utf-8")
