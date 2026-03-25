import json
import re
import subprocess
import tempfile
import textwrap
import unittest
from datetime import date, timedelta
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
            self.assertNotIn('<section class="masthead">', html)
            self.assertNotIn("A read-only workspace atlas", html)
            self.assertIn("Alpha milestone", html)
            self.assertIn("Alpha blocker", html)
            self.assertIn("Planned", html)
            self.assertIn("In Progress", html)
            self.assertIn("Blocked", html)
            self.assertIn("Done", html)
            self.assertIn("Filter by project", html)
            self.assertIn("project-alpha", html)
            self.assertIn("const DASHBOARD_WARNINGS_RAW = [];", html)
            self.assertIn("function ensureArray", html)
            self.assertIn("const DASHBOARD_DATA = normalizeItems", html)

    def test_generator_emits_workspace_tabs_with_markdown_and_json_sources(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertIn("Current Overview", html)
            self.assertIn("Execution Items", html)
            self.assertIn("Project Risk Register", html)
            self.assertIn("Foundation", html)
            self.assertIn("Requirements", html)
            self.assertIn("Roadmap", html)
            self.assertIn("Change Log", html)
            self.assertIn("dashboard_seed_overview", html)
            self.assertIn("project_definition_baseline", html)
            self.assertIn("user_needs", html)
            self.assertIn("Template structure simplification", html)
            self.assertIn("Deliverable map locked for review.", html)
            self.assertIn("Critical supplier lead time could delay prototype integration.", html)
            self.assertIn("Initial baseline captured", html)
            self.assertIn("const WORKSPACE_SECTIONS_RAW =", html)
            self.assertIn("function renderMarkdown", html)

    def test_generator_places_sections_full_width_with_generator_note_top_right_and_project_filter_below(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertRegex(
                html,
                re.compile(
                    r'<section class="top-controls">.*?<div class="top-controls-header">.*?<div class="tab-cluster">.*?id="section-tabs".*?</div>.*?<div class="top-controls-note">.*?Generated on <strong>[^<]+</strong>\.?\s*</div>.*?</div>.*?<div class="top-controls-filter-row">.*?for="project-filter">Filter by project</label>.*?id="project-filter".*?for="search-filter">Search</label>.*?id="search-filter".*?</div>.*?</section>',
                    re.DOTALL,
                ),
            )
            self.assertNotIn(
                "The project filter applies across execution items and narrative sections.",
                html,
            )
            self.assertRegex(
                html,
                re.compile(
                    r"\.tabs\s*\{[^}]*display:\s*grid;[^}]*grid-template-columns:\s*repeat\(auto-fit,\s*minmax\(160px,\s*1fr\)\);",
                    re.DOTALL,
                ),
            )
            execution_panel_match = re.search(
                r'<section class="tab-panel is-active" id="execution-panel">(.*?)</section>\s*<section class="tab-panel" id="document-panel">',
                html,
                re.DOTALL,
            )
            self.assertIsNotNone(execution_panel_match, "Expected execution panel markup in generated HTML")
            self.assertNotIn("for=\"project-filter\">Filter by project</label>", execution_panel_match.group(1))
            self.assertNotIn("for=\"search-filter\">Search</label>", execution_panel_match.group(1))
            self.assertIn("Execution Snapshot", execution_panel_match.group(1))

    def test_generator_emits_compact_snapshot_with_due_within_7_days_and_overdue_metrics(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertIn('class="snapshot snapshot-compact"', html)
            self.assertIn('class="snapshot-strip"', html)
            self.assertIn(".snapshot-compact", html)
            self.assertIn(".snapshot-strip", html)
            self.assertIn("Due Within 7 Days", html)
            self.assertIn("Overdue", html)
            self.assertIn('id="overdue-count"', html)
            self.assertIn('overdueCount: document.getElementById("overdue-count")', html)
            self.assertIn("function isOverdue(item)", html)
            self.assertIn("els.overdueCount.textContent = String(filteredItems.filter(isOverdue).length);", html)

    def test_generator_omits_readme_documents_from_workspace_sections(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertNotIn("Stakeholder Notes", html)
            self.assertNotIn("These README-only notes should stay out of the dashboard.", html)
            self.assertNotIn("Legacy Requirements Ingestion Summary", html)
            self.assertNotIn("This ingestion summary should stay out of the dashboard.", html)
            self.assertNotIn("Runtime Scan Summary", html)
            self.assertNotIn("Runtime scan cache content should stay out of the dashboard.", html)

    def test_generator_emits_detail_summary_wrap_styling(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertIn(".details-summary", html)
            self.assertIn("text-wrap: pretty;", html)
            self.assertIn('<p class="details-summary">', html)

    def test_generator_emits_source_path_wrap_styling(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertIn(".details-path", html)
            self.assertIn("overflow-wrap: anywhere;", html)
            self.assertIn("word-break: break-word;", html)
            self.assertIn('<p class="details-path">${item.relative_path}</p>', html)

    def test_generator_emits_compact_json_scan_view_markup(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertIn(".json-collection-table", html)
            self.assertIn(".json-row-summary", html)
            self.assertIn(".json-row-details", html)
            self.assertIn("function renderJsonCompactCollection", html)
            self.assertIn("function getJsonScanColumns", html)

    def test_json_documents_do_not_expand_the_first_row_by_default(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard JSON viewer test")

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

            probe_html = workspace_root / "dashboard-json-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const riskTab = [...document.querySelectorAll(".tab-button")]
                            .find((element) => element.textContent.includes("Project Risk Register"));

                          if (riskTab) {
                            riskTab.click();
                          }

                          const openRowCount = document.querySelectorAll(".json-row-details[open]").length;
                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify({ openRowCount });
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
                probe["openRowCount"],
                0,
                msg=f"Expected JSON rows to start collapsed.\nProbe: {probe}",
            )

    def test_shared_search_filters_execution_items_from_the_top_controls(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard shared-search test")

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

            probe_html = workspace_root / "dashboard-shared-search-execution-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const search = document.getElementById("search-filter");
                          search.value = "blocker";
                          search.dispatchEvent(new Event("input", { bubbles: true }));

                          const visibleCards = [...document.querySelectorAll(".column .card")]
                            .map((element) => element.textContent.replace(/\\s+/g, " ").trim());
                          const itemCount = document.getElementById("item-count")?.textContent?.trim() || "";

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify({ itemCount, visibleCards });
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
            self.assertEqual(probe["itemCount"], "1", msg=f"Expected shared search to keep execution filtering behavior.\nProbe: {probe}")
            self.assertEqual(len(probe["visibleCards"]), 1, msg=f"Expected a single visible execution card after search.\nProbe: {probe}")
            self.assertIn("Alpha blocker", probe["visibleCards"][0], msg=f"Expected blocker card to remain visible.\nProbe: {probe}")

    def test_shared_search_filters_json_documents_by_any_nested_field(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard shared-search test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            (
                workspace_root
                / "projects"
                / "project-alpha"
                / "07_PROJECT_EXECUTION"
                / "roadmap"
                / "roadmap.json"
            ).write_text(
                json.dumps(
                    {
                        "roadmap_title": "project-alpha Delivery Roadmap",
                        "last_updated": "2026-03-22",
                        "items": [
                            {
                                "id": "RDM-001",
                                "title": "Shared dashboard ready for stakeholder review",
                                "status": "in_progress",
                                "owner": "Program Management",
                                "target_date": "2026-04-10",
                            }
                        ],
                    },
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

            probe_html = workspace_root / "dashboard-shared-search-json-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const roadmapTab = [...document.querySelectorAll(".tab-button")]
                            .find((element) => element.textContent.includes("Roadmap"));
                          if (roadmapTab) {
                            roadmapTab.click();
                          }

                          const search = document.getElementById("search-filter");
                          search.value = "stakeholder review";
                          search.dispatchEvent(new Event("input", { bubbles: true }));

                          const docTitles = [...document.querySelectorAll("#doc-links .doc-link .doc-link-title")]
                            .map((element) => element.textContent.replace(/\\s+/g, " ").trim());
                          const viewerText = document.getElementById("doc-viewer-content")?.textContent?.replace(/\\s+/g, " ").trim() || "";

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify({ docTitles, viewerText });
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
            self.assertEqual(probe["docTitles"], ["Roadmap"], msg=f"Expected shared search to find roadmap JSON via a nested field value.\nProbe: {probe}")
            self.assertIn(
                "stakeholder review",
                probe["viewerText"].lower(),
                msg=f"Expected matching JSON content to stay loaded in the viewer.\nProbe: {probe}",
            )

    def test_shared_search_filters_visible_top_level_json_entries_in_selected_document(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard shared-search test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            (
                workspace_root
                / "projects"
                / "project-alpha"
                / "07_PROJECT_EXECUTION"
                / "roadmap"
                / "roadmap.json"
            ).write_text(
                json.dumps(
                    {
                        "roadmap_title": "project-alpha Delivery Roadmap",
                        "last_updated": "2026-03-22",
                        "owner": "Program Management",
                        "items": [
                            {
                                "id": "RDM-001",
                                "title": "Shared dashboard ready for stakeholder review",
                                "status": "in_progress",
                            }
                        ],
                    },
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

            probe_html = workspace_root / "dashboard-shared-search-json-top-level-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const roadmapTab = [...document.querySelectorAll(".tab-button")]
                            .find((element) => element.textContent.includes("Roadmap"));
                          if (roadmapTab) {
                            roadmapTab.click();
                          }

                          const search = document.getElementById("search-filter");
                          search.value = "stakeholder review";
                          search.dispatchEvent(new Event("input", { bubbles: true }));

                          const visibleKeys = [...document.querySelectorAll("#doc-viewer-content > .json-object > .json-entry > .json-key")]
                            .map((element) => element.textContent.replace(/\\s+/g, " ").trim());

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify({ visibleKeys });
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
                probe["visibleKeys"],
                ["items"],
                msg=f"Expected only matching top-level JSON entries to remain visible in the selected document.\nProbe: {probe}",
            )

    def test_shared_search_highlights_matching_json_text(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard shared-search test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            (
                workspace_root
                / "projects"
                / "project-alpha"
                / "07_PROJECT_EXECUTION"
                / "roadmap"
                / "roadmap.json"
            ).write_text(
                json.dumps(
                    {
                        "roadmap_title": "project-alpha Delivery Roadmap",
                        "last_updated": "2026-03-22",
                        "items": [
                            {
                                "id": "RDM-001",
                                "title": "Shared dashboard ready for stakeholder review",
                                "status": "in_progress",
                            }
                        ],
                    },
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

            probe_html = workspace_root / "dashboard-shared-search-json-highlight-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const roadmapTab = [...document.querySelectorAll(".tab-button")]
                            .find((element) => element.textContent.includes("Roadmap"));
                          if (roadmapTab) {
                            roadmapTab.click();
                          }

                          const search = document.getElementById("search-filter");
                          search.value = "stakeholder review";
                          search.dispatchEvent(new Event("input", { bubbles: true }));

                          const highlighted = [...document.querySelectorAll("#doc-viewer-content mark")]
                            .map((element) => element.textContent.replace(/\\s+/g, " ").trim());

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify({ highlighted });
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
            self.assertIn(
                "stakeholder review",
                [value.lower() for value in probe["highlighted"]],
                msg=f"Expected matching JSON text to be highlighted in the viewer.\nProbe: {probe}",
            )

    def test_shared_search_highlights_matching_markdown_text(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard shared-search test")

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

            probe_html = workspace_root / "dashboard-shared-search-markdown-probe.html"
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

                          const search = document.getElementById("search-filter");
                          search.value = "workspace explainable";
                          search.dispatchEvent(new Event("input", { bubbles: true }));

                          const docTitles = [...document.querySelectorAll("#doc-links .doc-link .doc-link-title")]
                            .map((element) => element.textContent.replace(/\\s+/g, " ").trim());
                          const highlighted = [...document.querySelectorAll("#doc-viewer-content mark")]
                            .map((element) => element.textContent.replace(/\\s+/g, " ").trim());

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify({ docTitles, highlighted });
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
                probe["docTitles"],
                ["Project Definition Baseline"],
                msg=f"Expected shared search to keep the matching Markdown document visible.\nProbe: {probe}",
            )
            self.assertIn(
                "workspace explainable",
                [value.lower() for value in probe["highlighted"]],
                msg=f"Expected matching Markdown text to be highlighted in the viewer.\nProbe: {probe}",
            )

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

    def test_stakeholder_general_view_uses_id_name_affiliation_role_and_inspect(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard stakeholder-view test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            stakeholders_dir = workspace_root / "projects" / "project-alpha" / "01_PROJECT_FOUNDATION" / "stakeholders"
            stakeholders_dir.mkdir(parents=True, exist_ok=True)
            (stakeholders_dir / "stakeholders.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "SH-001",
                            "name": "Alex Example",
                            "type": "person",
                            "affiliation": "INO",
                            "role": "Project owner for the alpha fixture.",
                            "influence": "high",
                            "source": "fixtures/stakeholder-source.md",
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

            probe_html = workspace_root / "dashboard-stakeholders-probe.html"
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

                          const stakeholderLink = [...document.querySelectorAll("#doc-links .doc-link")]
                            .find((element) => element.textContent.includes("Stakeholders"));
                          if (stakeholderLink) {
                            stakeholderLink.click();
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
                ["Id", "Name", "Affiliation", "Role", "Inspect"],
                msg=f"Expected stakeholder general-view headers to focus on stakeholder fields.\nProbe: {probe}",
            )
            self.assertEqual(
                probe["firstSummaryCells"],
                [
                    "SH-001",
                    "Alex Example",
                    "INO",
                    "Project owner for the alpha fixture.",
                    "Inspect",
                ],
                msg=f"Expected stakeholder row summary to show id, name, affiliation, role, and inspect only.\nProbe: {probe}",
            )

    def test_requirement_general_view_uses_id_statement_status_date_of_last_update_and_inspect_for_all_requirement_types(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard requirement-view test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)

            (workspace_root / "projects" / "project-alpha" / "03_REQUIREMENTS" / "user_requirements" / "user_requirements.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "USR-001",
                            "statement": "Provide a compact read-only dashboard requirement scan.",
                            "status": "Preliminary",
                            "date_of_last_update": "2026-03-24",
                            "priority": "High",
                        }
                    ],
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (workspace_root / "projects" / "project-alpha" / "03_REQUIREMENTS" / "system_requirements" / "system_requirement.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "SYS-001",
                            "statement": "Render requirements in a compact table.",
                            "status": "Approved",
                            "date_of_last_update": "2026-03-23",
                            "verification_method": "Inspection",
                        }
                    ],
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            subsystem_dir = workspace_root / "projects" / "project-alpha" / "03_REQUIREMENTS" / "subsystem_requirements"
            subsystem_dir.mkdir(parents=True, exist_ok=True)
            (subsystem_dir / "camera_requirements.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "SUB-001",
                            "statement": "Keep the row summary focused on the operator-facing fields.",
                            "status": "Draft",
                            "date_of_last_update": "2026-03-22",
                            "owner": "Optics",
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

            probe_html = workspace_root / "dashboard-requirements-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const requirementsTab = [...document.querySelectorAll(".tab-button")]
                            .find((element) => element.textContent.includes("Requirements"));
                          if (requirementsTab) {
                            requirementsTab.click();
                          }

                          const targetDocuments = ["User Requirements", "System Requirement", "Camera Requirements"];
                          const results = {};

                          targetDocuments.forEach((targetDocument) => {
                            const documentLink = [...document.querySelectorAll("#doc-links .doc-link")]
                              .find((element) => element.textContent.includes(targetDocument));
                            if (documentLink) {
                              documentLink.click();
                              results[targetDocument] = {
                                headerLabels: [...document.querySelectorAll(".json-collection-head .json-column-label")]
                                  .map((element) => element.textContent.trim()),
                                firstSummaryCells: [...document.querySelectorAll(".json-row-summary > *")]
                                  .map((element) => element.textContent.trim()),
                              };
                            }
                          });

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify(results);
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
            expected_headers = ["ID", "Statement", "Status", "Date of last update", "Inspect"]
            expected_rows = {
                "User Requirements": [
                    "USR-001",
                    "Provide a compact read-only dashboard requirement scan.",
                    "Preliminary",
                    "2026-03-24",
                    "Inspect",
                ],
                "System Requirement": [
                    "SYS-001",
                    "Render requirements in a compact table.",
                    "Approved",
                    "2026-03-23",
                    "Inspect",
                ],
                "Camera Requirements": [
                    "SUB-001",
                    "Keep the row summary focused on the operator-facing fields.",
                    "Draft",
                    "2026-03-22",
                    "Inspect",
                ],
            }

            for document_name, expected_row in expected_rows.items():
                self.assertIn(
                    document_name,
                    probe,
                    msg=f"Expected probe results for {document_name}.\nProbe: {probe}",
                )
                self.assertEqual(
                    probe[document_name]["headerLabels"],
                    expected_headers,
                    msg=f"Expected requirement headers to stay focused for {document_name}.\nProbe: {probe}",
                )
                self.assertEqual(
                    probe[document_name]["firstSummaryCells"],
                    expected_row,
                    msg=f"Expected requirement row summary to stay focused for {document_name}.\nProbe: {probe}",
                )

    def test_generator_wraps_long_path_tokens_inside_json_inline_lists(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertRegex(
                html,
                re.compile(
                    r"\.json-inline-list li\s*\{[^}]*min-width:\s*0;[^}]*overflow-wrap:\s*anywhere;[^}]*word-break:\s*break-word;[^}]*\}",
                    re.DOTALL,
                ),
            )

    def test_generator_enforces_wrap_safe_rules_across_json_field_types(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertRegex(
                html,
                re.compile(
                    r"\.json-entry,\s*\.json-card,\s*\.json-row-summary,\s*\.json-row-panel,\s*\.json-key,\s*\.json-primitive,\s*\.json-column-label,\s*\.json-row-index,\s*\.json-cell\s*\{[^}]*min-width:\s*0;[^}]*white-space:\s*normal;[^}]*overflow-wrap:\s*anywhere;[^}]*word-break:\s*break-word;[^}]*\}",
                    re.DOTALL,
                ),
            )

    def test_generator_emits_status_group_filter_and_removes_old_execution_chrome(self) -> None:
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

            html = output_html.read_text(encoding="utf-8")
            self.assertIn('for="status-filter">Filter by status</label>', html)
            self.assertIn('id="status-filter"', html)
            self.assertNotIn("Show cancelled", html)
            self.assertNotIn('id="cancelled-toggle"', html)
            self.assertNotIn("Workspace Dashboard /", html)
            self.assertNotIn("Reading Mode", html)
            self.assertIn(".card-summary", html)
            self.assertIn("text-align: left;", html)
            self.assertIn('<p class="card-summary">', html)

    def test_generator_maps_at_risk_execution_status_to_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            milestone_path = (
                workspace_root
                / "projects"
                / "project-alpha"
                / "07_PROJECT_EXECUTION"
                / "execution_items"
                / "EXEC-MILESTONE-001-alpha-milestone.json"
            )
            milestone = json.loads(milestone_path.read_text(encoding="utf-8"))
            milestone["status"] = "at_risk"
            milestone_path.write_text(json.dumps(milestone, indent=2) + "\n", encoding="utf-8")
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

            html = output_html.read_text(encoding="utf-8")
            self.assertIn("Alpha milestone", html)
            self.assertIn('"status":"blocked"', html)
            self.assertNotIn('"status":"at_risk"', html)
            self.assertNotIn("Skipped EXEC-MILESTONE-001 because status 'at_risk' is not normalized.", html)

    def test_document_tab_click_populates_links_and_viewer(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard interaction test")

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

            probe_html = workspace_root / "dashboard-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const buttons = document.querySelectorAll(".tab-button");
                          if (buttons[0]) {
                            buttons[0].click();
                          }

                          setTimeout(() => {
                            const result = {
                              activeSection: document.getElementById("doc-section-title")?.textContent || "",
                              documentPanelActive: document.getElementById("document-panel")?.classList.contains("is-active") || false,
                              executionPanelActive: document.getElementById("execution-panel")?.classList.contains("is-active") || false,
                              docLinkCount: document.querySelectorAll("#doc-links .doc-link").length,
                              docViewerTextLength: (document.getElementById("doc-viewer-content")?.textContent || "").trim().length
                            };

                            const pre = document.createElement("pre");
                            pre.id = "probe-results";
                            pre.textContent = JSON.stringify(result);
                            document.body.appendChild(pre);
                          }, 0);
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
            self.assertEqual(probe["activeSection"], "Current Overview")
            self.assertTrue(probe["documentPanelActive"])
            self.assertFalse(probe["executionPanelActive"])
            self.assertGreater(
                probe["docLinkCount"],
                0,
                msg=f"Expected document links to render after clicking Current Overview.\nProbe: {probe}",
            )
            self.assertGreater(
                probe["docViewerTextLength"],
                0,
                msg=f"Expected document viewer content to render after clicking Current Overview.\nProbe: {probe}",
            )

    def test_document_viewer_and_cards_keep_project_context_while_staying_compact(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard interaction test")

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

            probe_html = workspace_root / "dashboard-document-simplicity-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const buttons = document.querySelectorAll(".tab-button");
                          if (buttons[0]) {
                            buttons[0].click();
                          }

                          setTimeout(() => {
                            const activeCard = document.querySelector("#doc-links .doc-link");
                            const viewerEyebrow = document.querySelector("#doc-viewer-content .eyebrow");
                            const result = {
                              viewerEyebrowCount: document.querySelectorAll("#doc-viewer-content .eyebrow").length,
                              viewerEyebrowText: viewerEyebrow?.textContent?.trim() || "",
                              viewerMetaGridCount: document.querySelectorAll("#doc-viewer-content .doc-meta-grid").length,
                              viewerPathCount: document.querySelectorAll("#doc-viewer-content .doc-path").length,
                              viewerSectionHeadings: [...document.querySelectorAll("#doc-viewer-content .doc-section h3")]
                                .map((element) => element.textContent.trim()),
                              cardHeaderCount: document.querySelectorAll("#doc-links .doc-link .doc-link-header").length,
                              activeCardMetaTexts: [...(activeCard?.querySelectorAll(".doc-meta") || [])]
                                .map((element) => element.textContent.trim()),
                              cardTitle: activeCard?.querySelector(".doc-link-title")?.textContent?.trim() || "",
                              cardPreviewLength: activeCard?.querySelector(".doc-link-preview")?.textContent?.trim().length || 0,
                              viewerTitle: document.querySelector("#doc-viewer-content h2")?.textContent?.trim() || ""
                            };

                            const pre = document.createElement("pre");
                            pre.id = "probe-results";
                            pre.textContent = JSON.stringify(result);
                            document.body.appendChild(pre);
                          }, 0);
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
            self.assertEqual(probe["viewerEyebrowCount"], 1, msg=f"Expected the opened document header to keep the project label.\nProbe: {probe}")
            self.assertIn("project-alpha", probe["viewerEyebrowText"], msg=f"Expected the opened document header to include the project name.\nProbe: {probe}")
            self.assertEqual(probe["viewerMetaGridCount"], 0, msg=f"Expected no document metadata grid.\nProbe: {probe}")
            self.assertEqual(probe["viewerPathCount"], 0, msg=f"Expected no source path block in the document viewer.\nProbe: {probe}")
            self.assertEqual(
                probe["viewerSectionHeadings"],
                [],
                msg=f"Expected document viewer to render without extra section headings.\nProbe: {probe}",
            )
            self.assertLessEqual(probe["cardHeaderCount"], 1, msg=f"Expected compact document cards.\nProbe: {probe}")
            self.assertEqual(
                probe["activeCardMetaTexts"],
                ["project-alpha"],
                msg=f"Expected the document card to show only the project name beside the title.\nProbe: {probe}",
            )
            self.assertGreater(len(probe["cardTitle"]), 0, msg=f"Expected document card title to remain visible.\nProbe: {probe}")
            self.assertEqual(probe["cardPreviewLength"], 0, msg=f"Expected compact document cards without preview text.\nProbe: {probe}")
            self.assertGreater(len(probe["viewerTitle"]), 0, msg=f"Expected document viewer title to remain visible.\nProbe: {probe}")

    def test_execution_status_filter_groups_active_and_inactive_items(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard interaction test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            execution_items = workspace_root / "projects" / "project-alpha" / "07_PROJECT_EXECUTION" / "execution_items"
            today = date.today()
            recent_done_date = today - timedelta(days=3)
            old_done_date = today - timedelta(days=30)
            local_manifest = execution_items / "local_manifest.yaml"
            local_manifest.write_text(
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
                      - name: EXEC-ISSUE-002-active-progress.json
                        summary: "Active in progress item"
                        original_links: []
                      - name: EXEC-ISSUE-003-recent-done.json
                        summary: "Recently completed item"
                        original_links: []
                      - name: EXEC-ISSUE-004-old-done.json
                        summary: "Older completed item"
                        original_links: []
                      - name: EXEC-ISSUE-005-backlog.json
                        summary: "Backlog item"
                        original_links: []
                      - name: EXEC-ISSUE-006-abandonned.json
                        summary: "Abandonned item"
                        original_links: []
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            items = {
                "EXEC-ISSUE-002-active-progress.json": {
                    "id": "EXEC-ISSUE-002",
                    "type": "issue",
                    "title": "Active progress item",
                    "status": "in_progress",
                    "owner": "Systems",
                    "created": "2026-03-22",
                    "target_date": "2026-03-30",
                    "completion_date": None,
                    "priority": "medium",
                    "summary": "Actively moving.",
                    "dependencies": [],
                    "linked_artifacts": [],
                    "notes": [],
                    "problem_statement": "Needs current attention.",
                    "definition_of_done": ["Completed"],
                },
                "EXEC-ISSUE-003-recent-done.json": {
                    "id": "EXEC-ISSUE-003",
                    "type": "issue",
                    "title": "Recent done item",
                    "status": "done",
                    "owner": "Systems",
                    "created": str(recent_done_date - timedelta(days=10)),
                    "target_date": str(recent_done_date),
                    "completion_date": str(recent_done_date),
                    "priority": "medium",
                    "summary": "Done recently.",
                    "dependencies": [],
                    "linked_artifacts": [],
                    "notes": [],
                    "problem_statement": "Recently closed.",
                    "definition_of_done": ["Completed"],
                },
                "EXEC-ISSUE-004-old-done.json": {
                    "id": "EXEC-ISSUE-004",
                    "type": "issue",
                    "title": "Old done item",
                    "status": "done",
                    "owner": "Systems",
                    "created": str(old_done_date - timedelta(days=10)),
                    "target_date": str(old_done_date),
                    "completion_date": str(old_done_date),
                    "priority": "low",
                    "summary": "Done long ago.",
                    "dependencies": [],
                    "linked_artifacts": [],
                    "notes": [],
                    "problem_statement": "Already historical.",
                    "definition_of_done": ["Completed"],
                },
                "EXEC-ISSUE-005-backlog.json": {
                    "id": "EXEC-ISSUE-005",
                    "type": "issue",
                    "title": "Backlog item",
                    "status": "backlog",
                    "owner": "Systems",
                    "created": "2026-03-01",
                    "target_date": None,
                    "completion_date": None,
                    "priority": "low",
                    "summary": "Queued for later.",
                    "dependencies": [],
                    "linked_artifacts": [],
                    "notes": [],
                    "problem_statement": "Not active yet.",
                    "definition_of_done": ["Completed"],
                },
                "EXEC-ISSUE-006-abandonned.json": {
                    "id": "EXEC-ISSUE-006",
                    "type": "issue",
                    "title": "Abandonned item",
                    "status": "abandonned",
                    "owner": "Systems",
                    "created": "2026-03-01",
                    "target_date": None,
                    "completion_date": "2026-03-05",
                    "priority": "low",
                    "summary": "Explicitly abandoned.",
                    "dependencies": [],
                    "linked_artifacts": [],
                    "notes": [],
                    "problem_statement": "No longer pursued.",
                    "definition_of_done": ["Archived"],
                },
            }

            for name, payload in items.items():
                (execution_items / name).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

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

            probe_html = workspace_root / "dashboard-status-filter-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const getSnapshot = () => ({
                            titles: [...document.querySelectorAll(".card")]
                              .map((element) => element.textContent.replace(/\\s+/g, " ").trim()),
                            columns: [...document.querySelectorAll(".column-title span:last-child")]
                              .map((element) => element.textContent.trim()),
                            statusFilter: document.getElementById("status-filter")?.value || ""
                          });

                          const statusFilter = document.getElementById("status-filter");
                          const active = getSnapshot();

                          if (statusFilter) {
                            statusFilter.value = "inactive";
                            statusFilter.dispatchEvent(new Event("change", { bubbles: true }));
                          }

                          const inactive = getSnapshot();
                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify({ active, inactive });
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
            self.assertEqual(probe["active"]["statusFilter"], "active")
            self.assertIn("Planned", probe["active"]["columns"])
            self.assertIn("In Progress", probe["active"]["columns"])
            self.assertIn("Blocked", probe["active"]["columns"])
            self.assertIn("Done", probe["active"]["columns"])
            self.assertTrue(any("Alpha milestone" in title for title in probe["active"]["titles"]))
            self.assertTrue(any("Alpha blocker" in title for title in probe["active"]["titles"]))
            self.assertTrue(any("Active progress item" in title for title in probe["active"]["titles"]))
            self.assertTrue(any("Recent done item" in title for title in probe["active"]["titles"]))
            self.assertFalse(any("Backlog item" in title for title in probe["active"]["titles"]))
            self.assertFalse(any("Abandonned item" in title for title in probe["active"]["titles"]))
            self.assertFalse(any("Old done item" in title for title in probe["active"]["titles"]))

            self.assertEqual(probe["inactive"]["statusFilter"], "inactive")
            self.assertEqual(probe["inactive"]["columns"], ["Backlog", "Abandonned", "Done"])
            self.assertTrue(any("Backlog item" in title for title in probe["inactive"]["titles"]))
            self.assertTrue(any("Abandonned item" in title for title in probe["inactive"]["titles"]))
            self.assertTrue(any("Old done item" in title for title in probe["inactive"]["titles"]))
            self.assertFalse(any("Recent done item" in title for title in probe["inactive"]["titles"]))
            self.assertFalse(any("Alpha blocker" in title for title in probe["inactive"]["titles"]))

    def test_execution_details_panel_sits_below_filters_and_scrolls_internally(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard layout test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            issue_path = (
                workspace_root
                / "projects"
                / "project-alpha"
                / "07_PROJECT_EXECUTION"
                / "execution_items"
                / "EXEC-ISSUE-001-alpha-blocker.json"
            )
            issue = json.loads(issue_path.read_text(encoding="utf-8"))
            issue["dependencies"] = [f"DEP-{index:03d}" for index in range(1, 19)]
            issue["notes"] = [f"Extended note line {index:02d}" for index in range(1, 33)]
            issue["definition_of_done"] = [f"Definition checkpoint {index:02d}" for index in range(1, 25)]
            issue_path.write_text(json.dumps(issue, indent=2) + "\n", encoding="utf-8")
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

            probe_html = workspace_root / "dashboard-execution-layout-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const blockerCard = [...document.querySelectorAll(".card")]
                            .find((element) => element.textContent.includes("Alpha blocker"));
                          if (blockerCard) {
                            blockerCard.click();
                          }

                          const filters = document.querySelector(".filters");
                          const details = document.getElementById("details");
                          const board = document.querySelector(".board");
                          const filtersRect = filters?.getBoundingClientRect();
                          const detailsRect = details?.getBoundingClientRect();
                          const boardRect = board?.getBoundingClientRect();
                          const detailsStyle = details ? window.getComputedStyle(details) : null;

                          const result = {
                            selectedTitle: details?.querySelector("h2")?.textContent || "",
                            filtersBottom: filtersRect?.bottom || 0,
                            detailsTop: detailsRect?.top || 0,
                            detailsBottom: detailsRect?.bottom || 0,
                            boardTop: boardRect?.top || 0,
                            boardLeft: boardRect?.left || 0,
                            detailsLeft: detailsRect?.left || 0,
                            overflowY: detailsStyle?.overflowY || "",
                            position: detailsStyle?.position || "",
                            clientHeight: details?.clientHeight || 0,
                            scrollHeight: details?.scrollHeight || 0
                          };

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify(result);
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
            self.assertEqual(probe["selectedTitle"], "Alpha blocker")
            self.assertGreaterEqual(
                probe["detailsTop"],
                probe["filtersBottom"],
                msg=f"Expected details panel below filters.\nProbe: {probe}",
            )
            self.assertGreater(
                probe["boardTop"],
                probe["detailsBottom"],
                msg=f"Expected kanban board below details panel.\nProbe: {probe}",
            )
            self.assertLessEqual(
                abs(probe["detailsLeft"] - probe["boardLeft"]),
                2,
                msg=f"Expected details panel aligned with the board, not in a right rail.\nProbe: {probe}",
            )
            self.assertIn(
                probe["overflowY"],
                ("auto", "scroll"),
                msg=f"Expected internal vertical scrolling on the fixed-size details panel.\nProbe: {probe}",
            )
            self.assertGreater(
                probe["scrollHeight"],
                probe["clientHeight"],
                msg=f"Expected overflowing detail content to stay inside the panel.\nProbe: {probe}",
            )

    def test_execution_details_metadata_uses_compact_inline_layout(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard layout test")

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

            probe_html = workspace_root / "dashboard-execution-meta-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const blockerCard = [...document.querySelectorAll(".card")]
                            .find((element) => element.textContent.includes("Alpha blocker"));
                          if (blockerCard) {
                            blockerCard.click();
                          }

                          const metaList = document.querySelector(".details-meta-list");
                          const metaRect = metaList?.getBoundingClientRect();
                          const metaStyle = metaList ? window.getComputedStyle(metaList) : null;

                          const result = {
                            selectedTitle: document.querySelector("#details h2")?.textContent || "",
                            hasCompactMeta: Boolean(metaList),
                            itemCount: metaList?.querySelectorAll(".detail-meta-item").length || 0,
                            display: metaStyle?.display || "",
                            rowGap: metaStyle?.rowGap || "",
                            columnGap: metaStyle?.columnGap || "",
                            height: metaRect?.height || 0
                          };

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify(result);
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
            self.assertEqual(probe["selectedTitle"], "Alpha blocker")
            self.assertTrue(
                probe["hasCompactMeta"],
                msg=f"Expected compact detail metadata container.\nProbe: {probe}",
            )
            self.assertEqual(
                probe["itemCount"],
                4,
                msg=f"Expected four compact metadata items.\nProbe: {probe}",
            )
            self.assertIn(
                probe["display"],
                ("flex", "grid"),
                msg=f"Expected compact metadata to render as a horizontal layout.\nProbe: {probe}",
            )
            self.assertLess(
                probe["height"],
                90,
                msg=f"Expected metadata strip to stay compact instead of forming tall stat cards.\nProbe: {probe}",
            )

    def test_execution_filters_stay_on_one_desktop_row(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard layout test")

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

            probe_html = workspace_root / "dashboard-filters-one-row-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const filtersGrid = document.querySelector(".filters-grid");
                          const filterBlocks = [...document.querySelectorAll(".filters-grid .filter-block")];
                          const tops = filterBlocks.map((element) => Math.round(element.getBoundingClientRect().top));
                          const uniqueTops = [...new Set(tops)];
                          const style = filtersGrid ? window.getComputedStyle(filtersGrid) : null;

                          const result = {
                            filterCount: filterBlocks.length,
                            tops,
                            uniqueTopCount: uniqueTops.length,
                            gridTemplateColumns: style?.gridTemplateColumns || "",
                            columnGap: style?.columnGap || ""
                          };

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify(result);
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
                probe["filterCount"],
                4,
                msg=f"Expected four execution-only filter controls after moving search to the shared top bar.\nProbe: {probe}",
            )
            self.assertEqual(
                probe["uniqueTopCount"],
                1,
                msg=f"Expected all execution filters to stay on one desktop row.\nProbe: {probe}",
            )

    def test_generator_note_sits_above_sections_without_forcing_tab_wrap(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard layout test")

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

            probe_html = workspace_root / "dashboard-top-controls-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const note = document.querySelector(".top-controls-note");
                          const tabs = document.getElementById("section-tabs");
                          const tabButtons = [...document.querySelectorAll("#section-tabs .tab-button")];
                          const noteRect = note?.getBoundingClientRect();
                          const tabsRect = tabs?.getBoundingClientRect();
                          const rowTops = [...new Set(tabButtons.map((element) => Math.round(element.getBoundingClientRect().top)))];

                          const result = {
                            noteBottom: noteRect?.bottom || 0,
                            tabsTop: tabsRect?.top || 0,
                            tabRowCount: rowTops.length,
                            tabCount: tabButtons.length
                          };

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify(result);
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
            self.assertEqual(probe["tabCount"], 7)
            self.assertLessEqual(
                probe["noteBottom"],
                probe["tabsTop"],
                msg=f"Expected generator note to sit above the tabs instead of beside them.\nProbe: {probe}",
            )
            self.assertEqual(
                probe["tabRowCount"],
                1,
                msg=f"Expected section tabs to stay on one row at desktop width.\nProbe: {probe}",
            )

    def test_document_cards_do_not_overlap_viewer_for_long_requirement_and_roadmap_previews(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard layout test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            long_token = "X" * 220
            (
                workspace_root
                / "projects"
                / "project-alpha"
                / "03_REQUIREMENTS"
                / "system_requirements"
                / "system_requirements_baseline.md"
            ).write_text(
                "# System Requirements\n\n" + long_token + "\n",
                encoding="utf-8",
            )
            (
                workspace_root
                / "projects"
                / "project-alpha"
                / "07_PROJECT_EXECUTION"
                / "roadmap"
                / "roadmap.json"
            ).write_text(
                json.dumps(
                    {
                        "roadmap_title": long_token,
                        "items": [
                            {
                                "id": "RDM-001",
                                "title": long_token,
                                "status": "in_progress",
                            }
                        ],
                    },
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

            probe_html = workspace_root / "dashboard-layout-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const labels = ["Requirements", "Roadmap"];
                          const result = {};

                          labels.forEach((label) => {
                            const tab = [...document.querySelectorAll(".tab-button")]
                              .find((element) => element.textContent.includes(label));
                            if (!tab) {
                              return;
                            }

                            tab.click();
                            const activeCard = document.querySelector("#doc-links .doc-link");
                            const viewer = document.querySelector(".doc-viewer");
                            const activeRect = activeCard?.getBoundingClientRect();
                            const viewerRect = viewer?.getBoundingClientRect();

                            result[label] = {
                              section: document.getElementById("doc-section-title")?.textContent || "",
                              activeRight: activeRect?.right || 0,
                              viewerLeft: viewerRect?.left || 0,
                              overlap: Boolean(activeRect && viewerRect && activeRect.right > viewerRect.left)
                            };
                          });

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify(result);
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
            for section_name in ("Requirements", "Roadmap"):
                self.assertEqual(probe[section_name]["section"], section_name)
                self.assertFalse(
                    probe[section_name]["overlap"],
                    msg=(
                        f"Expected {section_name} document card to stay inside the left nav pane.\n"
                        f"Probe: {probe[section_name]}"
                    ),
                )

    def test_roadmap_complex_entries_expand_beyond_single_metadata_cards(self) -> None:
        browser_path = self._find_chromium_path()
        if browser_path is None:
            self.skipTest("Chromium browser not available for dashboard roadmap layout test")

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            self._write_workspace_fixture(workspace_root)
            (
                workspace_root
                / "projects"
                / "project-alpha"
                / "07_PROJECT_EXECUTION"
                / "roadmap"
                / "roadmap.json"
            ).write_text(
                json.dumps(
                    {
                        "roadmap_title": "project-alpha Delivery Roadmap",
                        "last_updated": "2026-03-22",
                        "source_links": [
                            "../01_PROJECT_FOUNDATION/project_definition/project_definition.md",
                            "../01_PROJECT_FOUNDATION/business_case/business_case.md",
                            "../09_COMMUNICATION/internal_updates/2026-03-23-roadmap-vision-reframe.md",
                        ],
                        "items": [
                            {
                                "id": "RDM-001",
                                "title": "Shared dashboard ready for stakeholder review and execution handoff",
                                "status": "in_progress",
                                "owner": "Program Management",
                                "target_date": "2026-04-10",
                            }
                        ],
                    },
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

            probe_html = workspace_root / "dashboard-roadmap-layout-probe.html"
            probe_html.write_text(
                output_html.read_text(encoding="utf-8").replace(
                    "</body>",
                    textwrap.dedent(
                        """
                        <script>
                        window.addEventListener("load", () => {
                          const roadmapTab = [...document.querySelectorAll(".tab-button")]
                            .find((element) => element.textContent.includes("Roadmap"));
                          if (roadmapTab) {
                            roadmapTab.click();
                          }

                          const titleEntry = [...document.querySelectorAll(".json-entry")]
                            .find((element) => element.querySelector(".json-key")?.textContent.trim() === "roadmap_title");
                          const sourceLinksEntry = [...document.querySelectorAll(".json-entry")]
                            .find((element) => element.querySelector(".json-key")?.textContent.trim() === "source_links");
                          const itemsEntry = [...document.querySelectorAll(".json-entry")]
                            .find((element) => element.querySelector(".json-key")?.textContent.trim() === "items");

                          const titleRect = titleEntry?.getBoundingClientRect();
                          const sourceLinksRect = sourceLinksEntry?.getBoundingClientRect();
                          const itemsRect = itemsEntry?.getBoundingClientRect();

                          const pre = document.createElement("pre");
                          pre.id = "probe-results";
                          pre.textContent = JSON.stringify({
                            titleWidth: titleRect?.width || 0,
                            sourceLinksWidth: sourceLinksRect?.width || 0,
                            itemsWidth: itemsRect?.width || 0
                          });
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
            self.assertGreater(
                probe["sourceLinksWidth"],
                probe["titleWidth"] * 1.5,
                msg=f"Expected roadmap source links to render wider than a single metadata card.\nProbe: {probe}",
            )
            self.assertGreater(
                probe["itemsWidth"],
                probe["titleWidth"] * 1.5,
                msg=f"Expected roadmap items to render wider than a single metadata card.\nProbe: {probe}",
            )

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
        (project_root / "00_GOVERNANCE" / "current_overview").mkdir(parents=True, exist_ok=True)
        (project_root / "00_GOVERNANCE" / "change_log").mkdir(parents=True, exist_ok=True)
        (project_root / "01_PROJECT_FOUNDATION" / "project_definition").mkdir(parents=True, exist_ok=True)
        (project_root / "01_PROJECT_FOUNDATION" / "objectives_success_metrics").mkdir(parents=True, exist_ok=True)
        (project_root / "03_REQUIREMENTS" / "user_requirements").mkdir(parents=True, exist_ok=True)
        (project_root / "03_REQUIREMENTS" / "system_requirements").mkdir(parents=True, exist_ok=True)
        (project_root / "07_PROJECT_EXECUTION" / "project_risk_register").mkdir(parents=True, exist_ok=True)
        (project_root / "07_PROJECT_EXECUTION" / "roadmap").mkdir(parents=True, exist_ok=True)

        (project_root / "project_manifest.yaml").write_text(
            "project_name: project-alpha\n",
            encoding="utf-8",
        )

        (project_root / "00_GOVERNANCE" / "current_overview" / "README.md").write_text(
            textwrap.dedent(
                """
                # Current Overview README

                This README explains the folder and should not appear in the dashboard.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "00_GOVERNANCE" / "current_overview" / "2026-03-22-dashboard_seed_overview.md").write_text(
            textwrap.dedent(
                """
                # Current Overview

                ## Current phase

                Template structure simplification

                ## Active priorities

                - Lock the shared dashboard information architecture.
                - Keep the execution view read-only.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "00_GOVERNANCE" / "change_log" / "change_log.json").write_text(
            json.dumps(
                [
                    {
                        "change_summary": "Initial baseline captured",
                        "date": "2026-03-22-16h05",
                    }
                ],
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        (project_root / "01_PROJECT_FOUNDATION" / "project_definition" / "README.md").write_text(
            textwrap.dedent(
                """
                # Project Definition README

                This README should stay hidden from the dashboard.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "01_PROJECT_FOUNDATION" / "project_definition" / "project_definition_baseline.md").write_text(
            textwrap.dedent(
                """
                # Project Definition

                The context bank keeps the workspace explainable for both humans and agents.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "01_PROJECT_FOUNDATION" / "objectives_success_metrics" / "README.md").write_text(
            textwrap.dedent(
                """
                # Objectives And Success Metrics README

                This README should stay hidden from the dashboard.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "01_PROJECT_FOUNDATION" / "objectives_success_metrics" / "objectives_success_metrics.md").write_text(
            textwrap.dedent(
                """
                # Objectives And Success Metrics

                - Deliverable map locked for review.
                - Dashboard sections generated without manual edits.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "03_REQUIREMENTS" / "user_requirements" / "README.md").write_text(
            textwrap.dedent(
                """
                # User Requirements README

                This README should stay hidden from the dashboard.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "03_REQUIREMENTS" / "user_requirements" / "user_needs.md").write_text(
            textwrap.dedent(
                """
                # User Requirements

                Humans can switch between execution tracking and narrative project documents from one dashboard.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "03_REQUIREMENTS" / "system_requirements" / "README.md").write_text(
            textwrap.dedent(
                """
                # System Requirements README

                This README should stay hidden from the dashboard.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "03_REQUIREMENTS" / "system_requirements" / "system_requirements_baseline.md").write_text(
            textwrap.dedent(
                """
                # System Requirements

                - Generate one static HTML file.
                - Display Markdown and JSON sources without editing the project artefacts.
            """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "00_GOVERNANCE" / "current_overview" / "runtime_scan_summary.json").write_text(
            json.dumps(
                {
                    "generated_at": "2026-03-22T16:10:00Z",
                    "summary": "Runtime scan cache content should stay out of the dashboard.",
                    "sections": [
                        {
                            "key": "foundation",
                            "file_count": 2,
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        (project_root / "03_REQUIREMENTS" / "system_requirements" / "2026-03-22-legacy-requirements-ingestion-summary.md").write_text(
            textwrap.dedent(
                """
                # Legacy Requirements Ingestion Summary

                This ingestion summary should stay out of the dashboard.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "01_PROJECT_FOUNDATION" / "stakeholders").mkdir(parents=True, exist_ok=True)
        (project_root / "01_PROJECT_FOUNDATION" / "stakeholders" / "README.md").write_text(
            textwrap.dedent(
                """
                # Stakeholder Notes

                These README-only notes should stay out of the dashboard.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        (project_root / "07_PROJECT_EXECUTION" / "project_risk_register" / "project_risk_register.json").write_text(
            json.dumps(
                [
                    {
                        "id": "RSK-0001",
                        "description": "Critical supplier lead time could delay prototype integration.",
                        "status": "open",
                        "owner": "Program Management",
                    }
                ],
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        (project_root / "07_PROJECT_EXECUTION" / "roadmap" / "roadmap.json").write_text(
            json.dumps(
                {
                    "roadmap_title": "project-alpha Delivery Roadmap",
                    "last_updated": "2026-03-22",
                    "items": [
                        {
                            "id": "RDM-001",
                            "title": "Shared dashboard ready",
                            "status": "in_progress",
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
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

    def _find_chromium_path(self) -> Path | None:
        candidates = [
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        return None


if __name__ == "__main__":
    unittest.main()
