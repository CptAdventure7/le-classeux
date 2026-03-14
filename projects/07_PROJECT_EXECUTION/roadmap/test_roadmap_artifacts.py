import json
import unittest
from pathlib import Path


ROADMAP_DIR = Path(__file__).resolve().parent
README_PATH = ROADMAP_DIR / "README.md"
ROADMAP_JSON_PATH = ROADMAP_DIR / "roadmap.json"
ROADMAP_HTML_PATH = ROADMAP_DIR / "roadmap.html"


class RoadmapArtifactsTest(unittest.TestCase):
    def test_readme_documents_canonical_json_format(self) -> None:
        readme_text = README_PATH.read_text(encoding="utf-8")

        self.assertIn("## Roadmap Format", readme_text)
        self.assertIn("Store roadmap content in JSON format.", readme_text)
        self.assertIn("roadmap.json", readme_text)
        self.assertIn("phase", readme_text)
        self.assertIn("items", readme_text)
        self.assertIn("dependencies", readme_text)
        self.assertIn("owner", readme_text)
        self.assertIn("target_date", readme_text)
        self.assertIn("status", readme_text)

    def test_sample_roadmap_json_matches_expected_shape(self) -> None:
        roadmap = json.loads(ROADMAP_JSON_PATH.read_text(encoding="utf-8"))

        self.assertIn("roadmap_title", roadmap)
        self.assertIn("last_updated", roadmap)
        self.assertIn("source_links", roadmap)
        self.assertIsInstance(roadmap["items"], list)
        self.assertGreater(len(roadmap["items"]), 0)

        item = roadmap["items"][0]
        self.assertEqual(
            {
                "id",
                "title",
                "phase",
                "status",
                "owner",
                "target_date",
                "summary",
                "dependencies",
                "source_links",
            },
            set(item),
        )

    def test_html_references_canonical_json_file(self) -> None:
        html_text = ROADMAP_HTML_PATH.read_text(encoding="utf-8")

        self.assertIn("fetch(\"./roadmap.json\")", html_text)
        self.assertIn("application/json", html_text)
        self.assertIn("embedded-roadmap-data", html_text)
        self.assertIn("JSON.parse", html_text)
        self.assertIn("window.location.protocol === \"file:\"", html_text)
        self.assertIn("roadmap.items", html_text)
        self.assertIn("roadmap_title", html_text)

    def test_no_legacy_metadata_directories_are_present(self) -> None:
        legacy_dirs = [
            child for child in ROADMAP_DIR.iterdir() if child.is_dir() and child.name.startswith("~")
        ]
        self.assertFalse(
            legacy_dirs,
            "Roadmap folder should rely on the governance change log and git commits for traceability.",
        )


if __name__ == "__main__":
    unittest.main()
