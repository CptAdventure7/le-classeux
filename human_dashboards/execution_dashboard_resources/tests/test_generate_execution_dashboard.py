import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = REPO_ROOT / "human_dashboards" / "execution_dashboard_resources" / "generate_execution_dashboard.ps1"


class GenerateExecutionDashboardTests(unittest.TestCase):
    def test_generator_builds_html_from_execution_items(self) -> None:
        self.assertTrue(
            SCRIPT_PATH.exists(),
            f"Expected dashboard generator at {SCRIPT_PATH}",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            output_html = workspace_root / "dashboard.html"

            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(SCRIPT_PATH),
                    "-WorkspaceRoot",
                    str(workspace_root),
                    "-OutputHtmlPath",
                    str(output_html),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"Generator failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
            )
            self.assertTrue(output_html.exists(), "Expected generator to create dashboard HTML")

            html = output_html.read_text(encoding="utf-8")
            self.assertIn("Execution Radar", html)
            self.assertIn("Alpha milestone", html)
            self.assertIn("Alpha blocker", html)
            self.assertIn("Planned", html)
            self.assertIn("In Progress", html)
            self.assertIn("Blocked", html)
            self.assertIn("Done", html)
            self.assertIn("Filter by project", html)
            self.assertIn("project-alpha", html)

    def _write_workspace_fixture(self, workspace_root: Path) -> None:
        (workspace_root / "projects").mkdir(parents=True, exist_ok=True)
        (workspace_root / "projects_manifest.yaml").write_text(
            textwrap.dedent(
                """
                workspace_name: sample-workspace
                structure_version: 1
                strategy: project_index
                projects:
                  - id: project-alpha
                    name: project-alpha
                    path: projects/project-alpha
                    manifest: projects/project-alpha/project_manifest.yaml
                    purpose: "Fixture project"
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        project_root = workspace_root / "projects" / "project-alpha"
        execution_items = project_root / "07_PROJECT_EXECUTION" / "execution_items"
        execution_items.mkdir(parents=True, exist_ok=True)

        (project_root / "project_manifest.yaml").write_text(
            "project_name: project-alpha\n",
            encoding="utf-8",
        )

        (execution_items / "local_manifest.yaml").write_text(
            textwrap.dedent(
                """
                folder: execution_items
                summary: "Fixture execution items"
                files:
                  - name: README.md
                    summary: "Guidance"
                    original_links: []
                  - name: local_manifest.yaml
                    summary: "Local index"
                    original_links: []
                  - name: EXEC-MILESTONE-001-alpha-milestone.json
                    summary: "Fixture milestone"
                    original_links: []
                  - name: EXEC-ISSUE-001-alpha-blocker.json
                    summary: "Fixture issue"
                    original_links: []
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (execution_items / "EXEC-MILESTONE-001-alpha-milestone.json").write_text(
            json.dumps(
                {
                    "id": "EXEC-MILESTONE-001",
                    "type": "milestone",
                    "title": "Alpha milestone",
                    "status": "planned",
                    "owner": "Systems",
                    "created": "2026-03-22",
                    "target_date": "2026-04-10",
                    "completion_date": None,
                    "priority": "high",
                    "summary": "Reach the first alpha checkpoint.",
                    "dependencies": [],
                    "linked_artifacts": [],
                    "notes": [],
                    "deliverables": [
                        "Alpha package ready for review"
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        (execution_items / "EXEC-ISSUE-001-alpha-blocker.json").write_text(
            json.dumps(
                {
                    "id": "EXEC-ISSUE-001",
                    "type": "issue",
                    "title": "Alpha blocker",
                    "status": "blocked",
                    "owner": "Verification",
                    "created": "2026-03-22",
                    "target_date": "2026-03-29",
                    "completion_date": None,
                    "priority": "critical",
                    "summary": "Verification fixture is missing.",
                    "dependencies": [
                        "EXEC-MILESTONE-001"
                    ],
                    "linked_artifacts": [],
                    "notes": [
                        "Waiting on procurement"
                    ],
                    "problem_statement": "The fixture is not available for the test sequence.",
                    "definition_of_done": [
                        "Fixture received",
                        "Verification rerun scheduled"
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
