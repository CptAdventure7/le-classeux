import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = REPO_ROOT / "agent" / "skills" / "general-update" / "scripts" / "generate_runtime_scan_summary.ps1"


class RuntimeScanSummaryGeneratorTests(unittest.TestCase):
    def test_generator_writes_cache_payload_with_section_summaries(self) -> None:
        self.assertTrue(SCRIPT_PATH.exists(), f"Expected runtime scan generator at {SCRIPT_PATH}")

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "projects" / "alpha-lab"
            self._write_project_fixture(project_root)

            result = self._run_generator(project_root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"Generator failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
            )

            payload = json.loads(result.stdout)
            cache_path = project_root / "00_GOVERNANCE" / "current_overview" / "runtime_scan_summary.json"

            self.assertTrue(cache_path.exists(), "Expected generator to write the runtime scan cache file")
            self.assertEqual(payload["cache_path"], "00_GOVERNANCE/current_overview/runtime_scan_summary.json")
            self.assertEqual(payload["refresh_after_hours"], 24)
            self.assertEqual(payload["max_depth"], 3)
            self.assertEqual(payload["mode"], "normal")
            self.assertEqual(
                [section["folder"] for section in payload["sections"]],
                ["00_GOVERNANCE", "03_REQUIREMENTS", "07_PROJECT_EXECUTION"],
            )

            governance = payload["sections"][0]
            requirements = payload["sections"][1]
            execution = payload["sections"][2]

            self.assertEqual(governance["state"], "has_content")
            self.assertEqual(governance["meaningful_file_count"], 1)
            self.assertIsNotNone(governance["latest_update"])

            self.assertEqual(requirements["state"], "has_content")
            self.assertEqual(requirements["meaningful_file_count"], 1)

            self.assertEqual(execution["state"], "has_content")
            self.assertEqual(execution["meaningful_file_count"], 1)

    def test_generator_reuses_fresh_cache_until_forced_refresh(self) -> None:
        self.assertTrue(SCRIPT_PATH.exists(), f"Expected runtime scan generator at {SCRIPT_PATH}")

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "projects" / "alpha-lab"
            self._write_project_fixture(project_root)
            cache_path = project_root / "00_GOVERNANCE" / "current_overview" / "runtime_scan_summary.json"
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(
                json.dumps(
                    {
                        "generated_at": "2099-01-01T00:00:00Z",
                        "cache_path": "00_GOVERNANCE/current_overview/runtime_scan_summary.json",
                        "refresh_after_hours": 24,
                        "max_depth": 3,
                        "mode": "normal",
                        "sections": [
                            {
                                "folder": "00_GOVERNANCE",
                                "state": "has_content",
                                "meaningful_file_count": 999,
                                "latest_update": "2099-01-01T00:00:00Z",
                            }
                        ],
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            cached_result = self._run_generator(project_root)
            self.assertEqual(cached_result.returncode, 0, msg=cached_result.stderr)
            cached_payload = json.loads(cached_result.stdout)
            self.assertEqual(cached_payload["sections"][0]["meaningful_file_count"], 999)

            refreshed_result = self._run_generator(project_root, force_refresh=True)
            self.assertEqual(refreshed_result.returncode, 0, msg=refreshed_result.stderr)
            refreshed_payload = json.loads(refreshed_result.stdout)
            self.assertNotEqual(refreshed_payload["sections"][0]["meaningful_file_count"], 999)

    def test_generator_skips_archive_and_files_beyond_scan_depth(self) -> None:
        self.assertTrue(SCRIPT_PATH.exists(), f"Expected runtime scan generator at {SCRIPT_PATH}")

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "projects" / "alpha-lab"
            self._write_project_fixture(project_root)

            deep_path = (
                project_root
                / "03_REQUIREMENTS"
                / "user_requirements"
                / "deep"
                / "deeper"
                / "too-deep.md"
            )
            deep_path.parent.mkdir(parents=True, exist_ok=True)
            deep_path.write_text("# Too Deep\n", encoding="utf-8")

            archive_file = project_root / "99_ARCHIVE" / "obsolete_decisions" / "history.md"
            archive_file.parent.mkdir(parents=True, exist_ok=True)
            archive_file.write_text("# History\n", encoding="utf-8")

            result = self._run_generator(project_root)

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(result.stdout)

            self.assertNotIn("99_ARCHIVE", [section["folder"] for section in payload["sections"]])
            requirements = next(section for section in payload["sections"] if section["folder"] == "03_REQUIREMENTS")
            self.assertEqual(requirements["meaningful_file_count"], 1)

    def _run_generator(self, project_root: Path, force_refresh: bool = False) -> subprocess.CompletedProcess[str]:
        command = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(SCRIPT_PATH),
            "-ProjectRoot",
            str(project_root),
        ]
        if force_refresh:
            command.append("-ForceRefresh")

        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

    def _write_project_fixture(self, project_root: Path) -> None:
        (project_root / "00_GOVERNANCE" / "current_overview").mkdir(parents=True, exist_ok=True)
        (project_root / "03_REQUIREMENTS" / "user_requirements").mkdir(parents=True, exist_ok=True)
        (project_root / "07_PROJECT_EXECUTION" / "roadmap").mkdir(parents=True, exist_ok=True)
        (project_root / "99_ARCHIVE" / "obsolete_decisions").mkdir(parents=True, exist_ok=True)

        (project_root / "project_manifest.yaml").write_text(
            textwrap.dedent(
                """
                project_name: Alpha Lab
                project_slug: alpha-lab
                structure_version: 2
                strategy: progressive_disclosure
                runtime_scan:
                  enabled: true
                  cache_relative_path: 00_GOVERNANCE/current_overview/runtime_scan_summary.json
                  refresh_after_hours: 24
                  max_depth: 3
                  include_sections:
                    - 00_GOVERNANCE
                    - 03_REQUIREMENTS
                    - 07_PROJECT_EXECUTION
                    - 99_ARCHIVE
                  meaningful_extensions:
                    - .md
                    - .json
                  ignore_files:
                    - README.md
                    - project_manifest.yaml
                    - local_manifest.yaml
                    - .gitkeep
                  ignore_section_ids:
                    - 99_ARCHIVE
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "00_GOVERNANCE" / "current_overview" / "README.md").write_text(
            "# Current Overview\n",
            encoding="utf-8",
        )
        (project_root / "00_GOVERNANCE" / "current_overview" / "2026-03-24-current.md").write_text(
            "# Current Overview\n\nFresh governance summary.\n",
            encoding="utf-8",
        )

        (project_root / "03_REQUIREMENTS" / "user_requirements" / "README.md").write_text(
            "# User Requirements\n",
            encoding="utf-8",
        )
        (project_root / "03_REQUIREMENTS" / "user_requirements" / "user_requirements.json").write_text(
            json.dumps({"id": "USR-001", "title": "Need one concise scan summary"}, indent=2) + "\n",
            encoding="utf-8",
        )

        (project_root / "07_PROJECT_EXECUTION" / "roadmap" / "local_manifest.yaml").write_text(
            "folder: roadmap\n",
            encoding="utf-8",
        )
        (project_root / "07_PROJECT_EXECUTION" / "roadmap" / "roadmap.json").write_text(
            json.dumps({"roadmap_title": "Alpha roadmap"}, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
