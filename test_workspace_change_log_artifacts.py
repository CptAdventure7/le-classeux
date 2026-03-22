import json
import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parent
WORKSPACE_CHANGE_LOG_DIR = WORKSPACE_ROOT / "workspace_change_log"
WORKSPACE_CHANGE_LOG_README_PATH = WORKSPACE_CHANGE_LOG_DIR / "README.md"
WORKSPACE_CHANGE_LOG_JSON_PATH = WORKSPACE_CHANGE_LOG_DIR / "change_log.json"
ROOT_README_PATH = WORKSPACE_ROOT / "README.md"
ROOT_AGENTS_PATH = WORKSPACE_ROOT / "AGENTS.md"


class WorkspaceChangeLogArtifactsTest(unittest.TestCase):
    def test_workspace_change_log_folder_contains_readme_and_json_log(self) -> None:
        self.assertTrue(WORKSPACE_CHANGE_LOG_DIR.is_dir())
        self.assertTrue(WORKSPACE_CHANGE_LOG_README_PATH.is_file())
        self.assertTrue(WORKSPACE_CHANGE_LOG_JSON_PATH.is_file())

    def test_workspace_change_log_readme_documents_json_contract(self) -> None:
        readme_text = WORKSPACE_CHANGE_LOG_README_PATH.read_text(encoding="utf-8")

        self.assertIn("# Workspace Change Log", readme_text)
        self.assertIn("outside any individual project", readme_text)
        self.assertIn("`change_log.json`", readme_text)
        self.assertIn("top-level JSON array", readme_text)
        self.assertIn("`change_summary` and `date`", readme_text)
        self.assertIn("most recent entry appears first", readme_text)

    def test_workspace_change_log_json_uses_expected_entry_shape(self) -> None:
        change_log = json.loads(WORKSPACE_CHANGE_LOG_JSON_PATH.read_text(encoding="utf-8"))

        self.assertIsInstance(change_log, list)
        self.assertGreaterEqual(len(change_log), 1)
        self.assertEqual(set(change_log[0].keys()), {"change_summary", "date"})
        self.assertRegex(change_log[0]["date"], r"^\d{4}-\d{2}-\d{2}-\d{2}h\d{2}$")

    def test_root_guidance_routes_non_project_changes_to_workspace_change_log(self) -> None:
        root_readme_text = ROOT_README_PATH.read_text(encoding="utf-8")
        root_agents_text = ROOT_AGENTS_PATH.read_text(encoding="utf-8")

        self.assertIn("workspace_change_log", root_readme_text)
        self.assertIn("workspace_change_log/change_log.json", root_agents_text)
        self.assertIn("outside any individual project", root_agents_text)


if __name__ == "__main__":
    unittest.main()
