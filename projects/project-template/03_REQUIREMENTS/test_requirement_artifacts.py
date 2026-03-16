import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from requirements_validator import (
    ALLOWED_STATUSES,
    change_log_confirms_requirement,
    find_modified_accepted_requirement_ids,
    find_removed_requirement_ids,
    validate_current_requirement_files,
    validate_requirement_history,
)


REQUIREMENTS_DIR = Path(__file__).resolve().parent


class RequirementArtifactsTest(unittest.TestCase):
    def _init_git_repo(self, root: Path) -> None:
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.name", "Codex"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "codex@example.com"], cwd=root, check=True, capture_output=True, text=True)

    def test_readmes_document_abandoned_and_confirmation_rules(self) -> None:
        readme_paths = [
            REQUIREMENTS_DIR / "user_requirements" / "README.md",
            REQUIREMENTS_DIR / "system_requirements" / "README.md",
            REQUIREMENTS_DIR / "subsystem_requirements" / "README.md",
        ]

        for readme_path in readme_paths:
            readme_text = readme_path.read_text(encoding="utf-8")
            self.assertIn("Requirement `status` must be one of `Accepted`, `Preliminary`, or `Abandoned`.", readme_text)
            self.assertIn("Obsolete or non-relevant requirements must remain", readme_text)
            self.assertIn("explicit user confirmation", readme_text)

    def test_removed_requirements_are_detected(self) -> None:
        previous_entries = [
            {"id": "PRJ-REQ-1", "status": "Accepted", "statement": "Original"},
            {"id": "PRJ-REQ-2", "status": "Preliminary", "statement": "Keep me"},
        ]
        current_entries = [
            {"id": "PRJ-REQ-2", "status": "Preliminary", "statement": "Keep me"},
        ]

        self.assertEqual(["PRJ-REQ-1"], find_removed_requirement_ids(previous_entries, current_entries))

    def test_modified_accepted_requirements_are_detected(self) -> None:
        previous_entries = [
            {"id": "PRJ-REQ-1", "status": "Accepted", "statement": "Original"},
            {"id": "PRJ-REQ-2", "status": "Preliminary", "statement": "Draft"},
        ]
        current_entries = [
            {"id": "PRJ-REQ-1", "status": "Accepted", "statement": "Changed"},
            {"id": "PRJ-REQ-2", "status": "Accepted", "statement": "Draft"},
        ]

        self.assertEqual(
            ["PRJ-REQ-1"],
            find_modified_accepted_requirement_ids(previous_entries, current_entries),
        )

    def test_change_log_confirmation_requires_requirement_id_and_phrase(self) -> None:
        change_log_text = (
            "- updated accepted requirement PRJ-REQ-12 after explicit user confirmation "
            "(2026-03-16-13h14)."
        )

        self.assertTrue(change_log_confirms_requirement(change_log_text, "PRJ-REQ-12"))
        self.assertFalse(change_log_confirms_requirement(change_log_text, "PRJ-REQ-99"))

    def test_validator_accepts_valid_status_values_in_live_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            live_dir = root / "projects" / "project-template" / "03_REQUIREMENTS" / "user_requirements"
            live_dir.mkdir(parents=True)
            (live_dir / "requirements.json").write_text(
                json.dumps(
                    [
                        {"id": "PRJ-UN-1", "status": "Preliminary"},
                        {"id": "PRJ-UN-2", "status": "Accepted"},
                        {"id": "PRJ-UN-3", "status": "Abandoned"},
                    ]
                ),
                encoding="utf-8",
            )

            violations = validate_current_requirement_files(root)

        self.assertEqual([], violations)

    def test_validator_rejects_unknown_status_values_in_live_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            live_dir = root / "projects" / "project-template" / "03_REQUIREMENTS" / "user_requirements"
            live_dir.mkdir(parents=True)
            (live_dir / "requirements.json").write_text(
                json.dumps([{"id": "PRJ-UN-1", "status": "Obsolete"}]),
                encoding="utf-8",
            )

            violations = validate_current_requirement_files(root)

        self.assertEqual(
            [
                (
                    "projects/project-template/03_REQUIREMENTS/user_requirements/requirements.json",
                    "PRJ-UN-1",
                    f"status must be one of {sorted(ALLOWED_STATUSES)}",
                )
            ],
            violations,
        )

    def test_history_validator_detects_deleted_tracked_requirement_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._init_git_repo(root)

            requirement_path = (
                root / "projects" / "project-template" / "03_REQUIREMENTS" / "user_requirements" / "requirements.json"
            )
            requirement_path.parent.mkdir(parents=True)
            requirement_path.write_text(
                json.dumps([{"id": "PRJ-UN-1", "status": "Accepted", "statement": "Original"}]),
                encoding="utf-8",
            )

            change_log_path = (
                root
                / "projects"
                / "project-template"
                / "00_GOVERNANCE"
                / "change_log"
                / "change_log.md"
            )
            change_log_path.parent.mkdir(parents=True)
            change_log_path.write_text("# Change Log\n", encoding="utf-8")

            subprocess.run(["git", "add", "."], cwd=root, check=True, capture_output=True, text=True)
            subprocess.run(
                ["git", "commit", "-m", "Add requirements"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )

            requirement_path.unlink()

            violations = validate_requirement_history(root)

        self.assertEqual(
            [
                "projects/project-template/03_REQUIREMENTS/user_requirements/requirements.json: tracked requirement file was removed; keep its entries and tag obsolete ones Abandoned instead"
            ],
            violations,
        )


if __name__ == "__main__":
    unittest.main()
