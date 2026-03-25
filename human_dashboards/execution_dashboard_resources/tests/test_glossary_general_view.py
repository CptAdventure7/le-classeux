import json
import re
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from test_generate_execution_dashboard import GenerateExecutionDashboardTests, SCRIPT_PATH


class GlossaryGeneralViewTests(unittest.TestCase):
    def _write_workspace_fixture(self, workspace_root: Path) -> None:
        helper = GenerateExecutionDashboardTests()
        helper._write_workspace_fixture(workspace_root)

    def _find_chromium_path(self) -> Path | None:
        helper = GenerateExecutionDashboardTests()
        return helper._find_chromium_path()

    def test_glossary_general_view_uses_id_term_definition_and_inspect(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard glossary-view test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            glossary_dir = workspace_root / "projects" / "project-alpha" / "01_PROJECT_FOUNDATION" / "glossary"
            glossary_dir.mkdir(parents=True, exist_ok=True)
            (glossary_dir / "glossary.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "TERM-001",
                            "term": "DUA",
                            "definition": "Business Unit Director role used in the alpha fixture.",
                            "source": "fixtures/glossary-source.md",
                            "related_links": ["projects/project-alpha/01_PROJECT_FOUNDATION/stakeholders/stakeholders.json"],
                        }
                    ],
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
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

            probe_html = workspace_root / "dashboard-glossary-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const foundationTab = [...document.querySelectorAll(".tab-button")]
                            .find((element) => element.textContent.includes("Foundation"));
                          if (foundationTab) {
                            foundationTab.click();
                          }

                          const glossaryLink = [...document.querySelectorAll("#doc-links .doc-link")]
                            .find((element) => element.textContent.includes("Glossary"));
                          if (glossaryLink) {
                            glossaryLink.click();
                          }

                          const headerLabels = [...document.querySelectorAll(".json-collection-head .json-column-label")]
                            .map((element) => element.textContent.trim());
                          const firstSummaryCells = [...document.querySelectorAll(".json-row-summary > *")]
                            .map((element) => element.textContent.trim());

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify({ headerLabels, firstSummaryCells });
                          document.body.appendChild(pre);
                        });
                        </script>
                        </body>
                        """
                    ),
                ),
                encoding="utf-8",
            )

            dom_dump = subprocess.run(
                [
                    str(browser_path),
                    "--headless",
                    "--disable-gpu",
                    "--window-size=1600,1200",
                    "--virtual-time-budget=1000",
                    "--dump-dom",
                    probe_html.resolve().as_uri(),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(
                dom_dump.returncode,
                0,
                msg=f"Browser dump failed.\nSTDOUT:\n{dom_dump.stdout}\nSTDERR:\n{dom_dump.stderr}",
            )

            match = re.search(r'<pre id="probe-results">(.+?)</pre>', dom_dump.stdout)
            self.assertIsNotNone(
                match,
                msg=f"Expected probe results in dumped DOM.\nSTDOUT:\n{dom_dump.stdout}\nSTDERR:\n{dom_dump.stderr}",
            )

            probe = json.loads(match.group(1))
            self.assertEqual(
                probe["headerLabels"],
                ["Id", "Term", "Definition", "Inspect"],
                msg=f"Expected glossary general-view headers to focus on glossary fields.\nProbe: {probe}",
            )
            self.assertEqual(
                probe["firstSummaryCells"],
                [
                    "TERM-001",
                    "DUA",
                    "Business Unit Director role used in the alpha fixture.",
                    "Inspect",
                ],
                msg=f"Expected glossary row summary to show id, term, definition, and inspect only.\nProbe: {probe}",
            )


if __name__ == "__main__":
    unittest.main()
