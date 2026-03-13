import json
import unittest
from pathlib import Path


ROADMAP_DIR = Path(__file__).resolve().parent
AGENTS_PATH = ROADMAP_DIR / "AGENTS.md"
ROADMAP_JSON_PATH = ROADMAP_DIR / "roadmap.json"
ROADMAP_HTML_PATH = ROADMAP_DIR / "roadmap.html"
HISTORY_DIR = ROADMAP_DIR / "~history"


class RoadmapArtifactsTest(unittest.TestCase):
    def test_agents_documents_canonical_json_format(self) -> None:
        agents_text = AGENTS_PATH.read_text(encoding="utf-8")

        self.assertIn("## Roadmap Format", agents_text)
        self.assertIn("Store roadmap content in JSON format.", agents_text)
        self.assertIn("roadmap.json", agents_text)
        self.assertIn("phase", agents_text)
        self.assertIn("items", agents_text)
        self.assertIn("dependencies", agents_text)
        self.assertIn("owner", agents_text)
        self.assertIn("target_date", agents_text)
        self.assertIn("status", agents_text)

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

    def test_history_note_exists_for_guidance_change(self) -> None:
        history_files = list(HISTORY_DIR.glob("*.json"))
        self.assertTrue(history_files, "Expected a history note for the roadmap guidance change.")


if __name__ == "__main__":
    unittest.main()
