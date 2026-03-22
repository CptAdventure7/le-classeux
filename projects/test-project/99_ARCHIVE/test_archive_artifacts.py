import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
PROJECT_MANIFEST_PATH = PROJECT_DIR / "project_manifest.yaml"
ARCHIVE_README_PATH = PROJECT_DIR / "99_ARCHIVE" / "README.md"
ARCHIVED_OVERVIEW_README_PATH = PROJECT_DIR / "99_ARCHIVE" / "current_overview" / "README.md"
CURRENT_OVERVIEW_README_PATH = PROJECT_DIR / "00_GOVERNANCE" / "current_overview" / "README.md"


class ArchiveArtifactsTest(unittest.TestCase):
    def test_manifest_uses_current_overview_archive_folder(self) -> None:
        manifest_text = PROJECT_MANIFEST_PATH.read_text(encoding="utf-8")

        self.assertIn("- id: current_overview", manifest_text)
        self.assertNotIn("- id: snapshots", manifest_text)
        self.assertNotIn("- id: retired_requirements", manifest_text)
        self.assertNotIn("- id: legacy_tests", manifest_text)

    def test_archive_readmes_document_current_overview_retirement_flow(self) -> None:
        archive_readme_text = ARCHIVE_README_PATH.read_text(encoding="utf-8")
        archived_overview_readme_text = ARCHIVED_OVERVIEW_README_PATH.read_text(encoding="utf-8")

        self.assertIn("`current_overview`, `deprecated`, `obsolete_decisions`", archive_readme_text)
        self.assertNotIn("retired_requirements", archive_readme_text)
        self.assertNotIn("legacy_tests", archive_readme_text)
        self.assertIn("# Current Overview", archived_overview_readme_text)
        self.assertIn("retired weekly overviews", archived_overview_readme_text)

    def test_remaining_archive_readmes_are_simple(self) -> None:
        readmes = [
            ARCHIVE_README_PATH,
            ARCHIVED_OVERVIEW_README_PATH,
            PROJECT_DIR / "99_ARCHIVE" / "deprecated" / "README.md",
            PROJECT_DIR / "99_ARCHIVE" / "obsolete_decisions" / "README.md",
        ]

        for readme_path in readmes:
            text = readme_path.read_text(encoding="utf-8")
            self.assertNotIn("## What Does Not Belong Here", text)
            self.assertNotIn("## Cross-Links To Maintain", text)
            self.assertNotIn("## Detailed Authoring Guidance", text)

    def test_governance_readme_points_old_overviews_to_archive_current_overview(self) -> None:
        current_overview_text = CURRENT_OVERVIEW_README_PATH.read_text(encoding="utf-8")

        self.assertIn("retire older weekly overviews", current_overview_text)
        self.assertIn("../../99_ARCHIVE/current_overview/README.md", current_overview_text)
        self.assertNotIn("99_ARCHIVE/snapshots", current_overview_text)


if __name__ == "__main__":
    unittest.main()
