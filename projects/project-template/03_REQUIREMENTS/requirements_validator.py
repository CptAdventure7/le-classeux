import json
import subprocess
from pathlib import Path


ALLOWED_STATUSES = {"Accepted", "Preliminary", "Abandoned"}
REQUIREMENTS_ROOT = Path("projects/project-template/03_REQUIREMENTS")
CHANGE_LOG_PATH = Path("projects/project-template/00_GOVERNANCE/change_log/change_log.md")


def _entries_by_id(entries: list[dict]) -> dict[str, dict]:
    return {entry["id"]: entry for entry in entries}


def find_removed_requirement_ids(previous_entries: list[dict], current_entries: list[dict]) -> list[str]:
    previous_ids = set(_entries_by_id(previous_entries))
    current_ids = set(_entries_by_id(current_entries))
    return sorted(previous_ids - current_ids)


def find_modified_accepted_requirement_ids(previous_entries: list[dict], current_entries: list[dict]) -> list[str]:
    previous_by_id = _entries_by_id(previous_entries)
    current_by_id = _entries_by_id(current_entries)
    modified_ids = []

    for requirement_id, previous_entry in previous_by_id.items():
        if previous_entry.get("status") != "Accepted":
            continue

        current_entry = current_by_id.get(requirement_id)
        if current_entry is None:
            continue

        if current_entry != previous_entry:
            modified_ids.append(requirement_id)

    return sorted(modified_ids)


def change_log_confirms_requirement(change_log_text: str, requirement_id: str) -> bool:
    normalized_lines = [line.lower() for line in change_log_text.splitlines()]
    requirement_id_lower = requirement_id.lower()
    return any(
        requirement_id_lower in line and "explicit user confirmation" in line
        for line in normalized_lines
    )


def _iter_live_requirement_files(repo_root: Path) -> list[Path]:
    live_files = [
        repo_root / REQUIREMENTS_ROOT / "user_requirements" / "requirements.json",
        repo_root / REQUIREMENTS_ROOT / "system_requirements" / "requirements.json",
    ]
    subsystem_dir = repo_root / REQUIREMENTS_ROOT / "subsystem_requirements"
    if subsystem_dir.exists():
        live_files.extend(sorted(subsystem_dir.glob("*_requirements.json")))
    return [path for path in live_files if path.exists()]


def _load_requirement_entries(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_current_requirement_files(repo_root: Path) -> list[tuple[str, str, str]]:
    violations: list[tuple[str, str, str]] = []

    for path in _iter_live_requirement_files(repo_root):
        entries = _load_requirement_entries(path)
        relative_path = path.relative_to(repo_root).as_posix()

        for entry in entries:
            status = entry.get("status")
            if status not in ALLOWED_STATUSES:
                violations.append(
                    (
                        relative_path,
                        entry.get("id", "<missing id>"),
                        f"status must be one of {sorted(ALLOWED_STATUSES)}",
                    )
                )

    return violations


def _git_show(repo_root: Path, ref: str, relative_path: Path) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{relative_path.as_posix()}"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def _tracked_requirement_paths(repo_root: Path, ref: str) -> set[Path]:
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, REQUIREMENTS_ROOT.as_posix()],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return set()

    tracked_paths = set()
    for line in result.stdout.splitlines():
        path = Path(line.strip())
        if path.name == "requirements.json" or path.name.endswith("_requirements.json"):
            tracked_paths.add(path)

    return tracked_paths


def validate_requirement_history(repo_root: Path, ref: str = "HEAD") -> list[str]:
    violations: list[str] = []
    change_log_file = repo_root / CHANGE_LOG_PATH
    change_log_text = change_log_file.read_text(encoding="utf-8") if change_log_file.exists() else ""

    current_files = _iter_live_requirement_files(repo_root)
    tracked_relative_paths = {path.relative_to(repo_root) for path in current_files}
    tracked_relative_paths.update(_tracked_requirement_paths(repo_root, ref))

    for relative_path in sorted(tracked_relative_paths):
        previous_text = _git_show(repo_root, ref, relative_path)
        if previous_text is None:
            continue

        current_path = repo_root / relative_path
        if not current_path.exists():
            violations.append(
                f"{relative_path.as_posix()}: tracked requirement file was removed; keep its entries and tag obsolete ones Abandoned instead"
            )
            continue

        current_entries = _load_requirement_entries(current_path)
        previous_entries = json.loads(previous_text)

        removed_ids = find_removed_requirement_ids(previous_entries, current_entries)
        for requirement_id in removed_ids:
            violations.append(
                f"{relative_path.as_posix()}: requirement {requirement_id} was removed; keep it and tag it Abandoned instead"
            )

        modified_accepted_ids = find_modified_accepted_requirement_ids(previous_entries, current_entries)
        for requirement_id in modified_accepted_ids:
            if not change_log_confirms_requirement(change_log_text, requirement_id):
                violations.append(
                    f"{relative_path.as_posix()}: accepted requirement {requirement_id} changed without a matching explicit user confirmation entry in the change log"
                )

    return violations
