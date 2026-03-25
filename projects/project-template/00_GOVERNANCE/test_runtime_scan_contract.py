import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
PROJECT_MANIFEST_PATH = PROJECT_DIR / "project_manifest.yaml"
GOVERNANCE_README_PATH = PROJECT_DIR / "00_GOVERNANCE" / "README.md"
CURRENT_OVERVIEW_README_PATH = PROJECT_DIR / "00_GOVERNANCE" / "current_overview" / "README.md"


class RuntimeScanContractTest(unittest.TestCase):
    def test_manifest_declares_runtime_scan_contract(self) -> None:
        manifest_text = PROJECT_MANIFEST_PATH.read_text(encoding="utf-8")

        self.assertIn("runtime_scan:", manifest_text)
        self.assertIn("cache_relative_path: 00_GOVERNANCE/current_overview/runtime_scan_summary.json", manifest_text)
        self.assertIn("refresh_after_hours: 24", manifest_text)
        self.assertIn("max_depth: 3", manifest_text)
        self.assertIn("- 00_GOVERNANCE", manifest_text)
        self.assertIn("- 01_PROJECT_FOUNDATION", manifest_text)
        self.assertIn("- 03_REQUIREMENTS", manifest_text)
        self.assertIn("- 07_PROJECT_EXECUTION", manifest_text)
        self.assertIn("- 99_ARCHIVE", manifest_text)

    def test_governance_docs_explain_cached_runtime_scan_summary(self) -> None:
        governance_text = GOVERNANCE_README_PATH.read_text(encoding="utf-8")
        current_overview_text = CURRENT_OVERVIEW_README_PATH.read_text(encoding="utf-8")

        self.assertIn("runtime_scan_summary.json", governance_text)
        self.assertIn("runtime_scan_summary.json", current_overview_text)
        self.assertIn("refreshed on demand or when it is older than 24 hours", current_overview_text)
        self.assertIn("metadata-only scan", current_overview_text)

    def test_governance_docs_keep_archive_out_of_normal_runtime_scan_mode(self) -> None:
        governance_text = GOVERNANCE_README_PATH.read_text(encoding="utf-8")
        current_overview_text = CURRENT_OVERVIEW_README_PATH.read_text(encoding="utf-8")

        self.assertIn("history-only", governance_text)
        self.assertIn("Do not treat `99_ARCHIVE` as active scan scope", current_overview_text)


if __name__ == "__main__":
    unittest.main()
