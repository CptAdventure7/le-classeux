from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Iterable

import yaml


TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt"}


def instantiate_project(
    *,
    workspace_root: Path,
    project_slug: str,
    project_name: str,
    purpose: str,
    date_stamp: str | None = None,
    timestamp: str | None = None,
    template_slug: str = "project-template",
) -> Path:
    workspace_root = Path(workspace_root).resolve()
    template_root = workspace_root / "projects" / template_slug
    target_root = workspace_root / "projects" / project_slug
    date_stamp = date_stamp or datetime.now().strftime("%Y-%m-%d")
    timestamp = timestamp or datetime.now().strftime("%Y-%m-%d-%Hh%M")

    validate_inputs(workspace_root, template_root, target_root, project_slug)

    shutil.copytree(template_root, target_root)
    rewrite_text_files(
        target_root=target_root,
        template_slug=template_slug,
        project_slug=project_slug,
        project_name=project_name,
    )
    rewrite_project_manifest(target_root / "project_manifest.yaml", project_slug, project_name)
    rewrite_root_readme(target_root / "README.md", project_name, purpose, date_stamp)
    reset_change_log(target_root, project_slug, template_slug, timestamp)
    clear_seed_execution_items(target_root)
    rewrite_execution_items_manifest(target_root)
    register_project(workspace_root, project_slug, project_name, purpose)
    ensure_no_stale_template_identity(
        target_root=target_root,
        template_slug=template_slug,
        allowed_paths={target_root / "00_GOVERNANCE" / "change_log" / "change_log.json"},
    )

    return target_root


def validate_inputs(
    workspace_root: Path,
    template_root: Path,
    target_root: Path,
    project_slug: str,
) -> None:
    if not (workspace_root / "projects_manifest.yaml").exists():
        raise FileNotFoundError("Workspace projects_manifest.yaml is missing.")
    if not template_root.exists():
        raise FileNotFoundError(f"Template project is missing: {template_root}")
    if target_root.exists():
        raise FileExistsError(f"Target project already exists: {target_root}")
    if not re.fullmatch(r"[a-z0-9-]+", project_slug):
        raise ValueError("project_slug must use lowercase letters, digits, and hyphens only.")


def rewrite_text_files(
    *,
    target_root: Path,
    template_slug: str,
    project_slug: str,
    project_name: str,
) -> None:
    old_path_token = f"projects/{template_slug}"
    new_path_token = f"projects/{project_slug}"

    for path in iter_text_files(target_root):
        content = path.read_text(encoding="utf-8")
        content = content.replace(old_path_token, new_path_token)
        content = content.replace(template_slug, project_name)
        path.write_text(content, encoding="utf-8")


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def rewrite_project_manifest(manifest_path: Path, project_slug: str, project_name: str) -> None:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["project_name"] = project_name
    manifest["project_slug"] = project_slug
    manifest_path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def rewrite_root_readme(readme_path: Path, project_name: str, purpose: str, date_stamp: str) -> None:
    readme = readme_path.read_text(encoding="utf-8")
    summary = (
        "## Current Overview Summary\n\n"
        f"- Last updated: `{date_stamp}`\n"
        "- Current phase: `Instantiation`\n\n"
        f"`{project_name}` is a newly instantiated evidence-first project context bank. {purpose}\n\n"
        "### Active Watchpoints\n\n"
        "- replace template-era examples and placeholder language with project-specific evidence before adding downstream artefacts\n"
        "- keep `00_GOVERNANCE/change_log/change_log.json` as the first durable memory record and update it with every repository change\n"
        "- create execution items only when real delivery work exists; do not carry template sample data into live project tracking\n"
    )
    pattern = re.compile(
        r"## Current Overview Summary\s+.*?(?=\n## How To Work In This Project)",
        re.DOTALL,
    )
    if not pattern.search(readme):
        raise ValueError("Unable to find the Current Overview Summary section in the project README.")
    updated = pattern.sub(summary.rstrip() + "\n", readme, count=1)
    updated = re.sub(r"^# .+$", f"# {project_name}", updated, count=1, flags=re.MULTILINE)
    readme_path.write_text(updated, encoding="utf-8")


def reset_change_log(target_root: Path, project_slug: str, template_slug: str, timestamp: str) -> None:
    change_log_path = target_root / "00_GOVERNANCE" / "change_log" / "change_log.json"
    payload = [
        {
            "change_summary": (
                f"instantiated `projects/{project_slug}` from `projects/{template_slug}` "
                "and registered it in `projects_manifest.yaml`"
            ),
            "date": timestamp,
        }
    ]
    change_log_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def clear_seed_execution_items(target_root: Path) -> None:
    execution_root = target_root / "07_PROJECT_EXECUTION" / "execution_items"
    for path in execution_root.glob("EXEC-*.json"):
        path.unlink()


def rewrite_execution_items_manifest(target_root: Path) -> None:
    manifest_path = target_root / "07_PROJECT_EXECUTION" / "execution_items" / "local_manifest.yaml"
    payload = {
        "folder": "execution_items",
        "summary": (
            "Unified execution tracking lives here. Keep one JSON file per issue or milestone, "
            "use `type` to distinguish them, and maintain this manifest as the quick local index."
        ),
        "files": [
            {
                "name": "README.md",
                "summary": "Defines the single-folder JSON-per-item contract for execution issues and milestones, with no separate board artifact.",
                "original_links": [],
            },
            {
                "name": "local_manifest.yaml",
                "summary": "Folder-local file index for quick triage, with short summaries and any known links to original source files.",
                "original_links": [],
            },
        ],
    }
    manifest_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def register_project(workspace_root: Path, project_slug: str, project_name: str, purpose: str) -> None:
    manifest_path = workspace_root / "projects_manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    projects = manifest.setdefault("projects", [])

    if any(project.get("id") == project_slug for project in projects):
        raise ValueError(f"projects_manifest.yaml already contains project id '{project_slug}'.")

    projects.append(
        {
            "id": project_slug,
            "name": project_name,
            "path": f"projects/{project_slug}",
            "manifest": f"projects/{project_slug}/project_manifest.yaml",
            "purpose": purpose,
        }
    )
    manifest_path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def ensure_no_stale_template_identity(
    *,
    target_root: Path,
    template_slug: str,
    allowed_paths: set[Path],
) -> None:
    for path in iter_text_files(target_root):
        if path in allowed_paths:
            continue
        if template_slug in path.read_text(encoding="utf-8"):
            raise ValueError(f"Stale template identifier '{template_slug}' remains in {path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Instantiate a new project from the workspace project-template scaffold."
    )
    parser.add_argument("--workspace-root", type=Path, default=Path.cwd())
    parser.add_argument("--project-slug", required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--date-stamp")
    parser.add_argument("--timestamp")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    instantiate_project(
        workspace_root=args.workspace_root,
        project_slug=args.project_slug,
        project_name=args.project_name,
        purpose=args.purpose,
        date_stamp=args.date_stamp,
        timestamp=args.timestamp,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
