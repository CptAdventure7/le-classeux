import json
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_ROOT = REPO_ROOT / "projects" / "test-project"

EXPECTED_ARTIFACTS = {
    "00_GOVERNANCE/current_overview": "2026-03-22-dashboard-seed-overview.md",
    "01_PROJECT_FOUNDATION/project_definition": "2026-03-22-project-definition-dummy.md",
    "01_PROJECT_FOUNDATION/objectives_success_metrics": "2026-03-22-objectives-success-metrics-dummy.md",
    "01_PROJECT_FOUNDATION/stakeholders": "2026-03-22-stakeholders-dummy.md",
    "01_PROJECT_FOUNDATION/glossary": "2026-03-22-glossary-dummy.md",
    "01_PROJECT_FOUNDATION/assumptions_constraints": "2026-03-22-assumptions-constraints-dummy.md",
    "01_PROJECT_FOUNDATION/business_case": "2026-03-22-business-case-dummy.md",
    "02_SYSTEM_DEFINITION/use_cases": "2026-03-22-use-cases-dummy.md",
    "02_SYSTEM_DEFINITION/system_architecture": "2026-03-22-system-architecture-dummy.md",
    "03_REQUIREMENTS/user_requirements": "2026-03-22-user-requirements-dummy.md",
    "03_REQUIREMENTS/system_requirements": "2026-03-22-system-requirements-dummy.md",
    "03_REQUIREMENTS/subsystem_requirements": "2026-03-22-subsystem-requirements-dummy.md",
    "04_DESIGN_AND_IMPLEMENTATION/design": "2026-03-22-dashboard-design-dummy.md",
    "04_DESIGN_AND_IMPLEMENTATION/system_risk_register": "system_risk_register.json",
    "04_DESIGN_AND_IMPLEMENTATION/design_reviews": "2026-03-22-dashboard-seed-review.md",
    "04_DESIGN_AND_IMPLEMENTATION/prototypes": "2026-03-22-prototype-note-dummy.md",
    "05_EXPERIMENT_AND_VERIFICATION/test_protocols": "2026-03-22-dashboard-seed-protocol.md",
    "05_EXPERIMENT_AND_VERIFICATION/test_results": "2026-03-22-dashboard-seed-results.md",
    "05_EXPERIMENT_AND_VERIFICATION/experiments": "2026-03-22-dashboard-seed-experiment.md",
    "05_EXPERIMENT_AND_VERIFICATION/analysis": "2026-03-22-dashboard-seed-analysis.md",
    "05_EXPERIMENT_AND_VERIFICATION/lessons_learned": "2026-03-22-dashboard-seed-lessons.md",
    "06_RESEARCH_AND_REFERENCES/papers": "2026-03-22-dashboard-seed-paper-note.md",
    "06_RESEARCH_AND_REFERENCES/standards": "2026-03-22-dashboard-seed-standard-note.md",
    "06_RESEARCH_AND_REFERENCES/patents": "2026-03-22-dashboard-seed-patent-note.md",
    "06_RESEARCH_AND_REFERENCES/competitor_landscape": "2026-03-22-dashboard-seed-competitor-note.md",
    "06_RESEARCH_AND_REFERENCES/cots": "2026-03-22-dashboard-seed-cots-note.md",
    "06_RESEARCH_AND_REFERENCES/web_references": "2026-03-22-dashboard-seed-web-note.md",
    "06_RESEARCH_AND_REFERENCES/presentations": "2026-03-22-dashboard-seed-presentation-note.md",
    "07_PROJECT_EXECUTION/roadmap": "roadmap.json",
    "07_PROJECT_EXECUTION/execution_items": "EXEC-ISSUE-001-dashboard-seed-validation.json",
    "07_PROJECT_EXECUTION/budget_resources": "2026-03-22-dashboard-seed-budget-note.md",
    "07_PROJECT_EXECUTION/procurement": "2026-03-22-dashboard-seed-procurement-note.md",
    "07_PROJECT_EXECUTION/project_risk_register": "project_risk_register.json",
    "07_PROJECT_EXECUTION/change_requests": "2026-03-22-dashboard-seed-change-request.md",
    "08_DECISIONS": "decisions.json",
    "09_COMMUNICATION/meetings/raw_notes": "2026-03-22-dashboard-seed-sync-raw-notes.md",
    "09_COMMUNICATION/meetings/summaries": "2026-03-22-dashboard-seed-sync-summary.md",
    "09_COMMUNICATION/internal_updates": "2026-03-22-dashboard-seed-internal-update.md",
    "09_COMMUNICATION/external_updates": "2026-03-22-dashboard-seed-external-update.md",
    "09_COMMUNICATION/reporting": "2026-03-22-dashboard-seed-report.md",
    "10_OPERATIONS_AND_HANDOFF/deployment_installation": "2026-03-22-dashboard-seed-deployment-note.md",
    "10_OPERATIONS_AND_HANDOFF/user_docs": "2026-03-22-dashboard-seed-user-doc.md",
    "10_OPERATIONS_AND_HANDOFF/maintenance": "2026-03-22-dashboard-seed-maintenance-note.md",
    "10_OPERATIONS_AND_HANDOFF/training": "2026-03-22-dashboard-seed-training-note.md",
    "10_OPERATIONS_AND_HANDOFF/support_notes": "2026-03-22-dashboard-seed-support-note.md",
    "99_ARCHIVE/current_overview": "2026-01-15-archived-overview-dummy.md",
    "99_ARCHIVE/deprecated": "2026-02-01-deprecated-artifact-note.md",
    "99_ARCHIVE/obsolete_decisions": "2026-02-10-obsolete-decision-note.md",
}

MANIFEST_EXPECTATIONS = {
    "04_DESIGN_AND_IMPLEMENTATION/design_reviews/local_manifest.yaml": "2026-03-22-dashboard-seed-review.md",
    "05_EXPERIMENT_AND_VERIFICATION/test_protocols/local_manifest.yaml": "2026-03-22-dashboard-seed-protocol.md",
    "05_EXPERIMENT_AND_VERIFICATION/test_results/local_manifest.yaml": "2026-03-22-dashboard-seed-results.md",
    "05_EXPERIMENT_AND_VERIFICATION/experiments/local_manifest.yaml": "2026-03-22-dashboard-seed-experiment.md",
    "05_EXPERIMENT_AND_VERIFICATION/analysis/local_manifest.yaml": "2026-03-22-dashboard-seed-analysis.md",
    "05_EXPERIMENT_AND_VERIFICATION/lessons_learned/local_manifest.yaml": "2026-03-22-dashboard-seed-lessons.md",
    "06_RESEARCH_AND_REFERENCES/papers/local_manifest.yaml": "2026-03-22-dashboard-seed-paper-note.md",
    "06_RESEARCH_AND_REFERENCES/standards/local_manifest.yaml": "2026-03-22-dashboard-seed-standard-note.md",
    "06_RESEARCH_AND_REFERENCES/patents/local_manifest.yaml": "2026-03-22-dashboard-seed-patent-note.md",
    "06_RESEARCH_AND_REFERENCES/competitor_landscape/local_manifest.yaml": "2026-03-22-dashboard-seed-competitor-note.md",
    "06_RESEARCH_AND_REFERENCES/cots/local_manifest.yaml": "2026-03-22-dashboard-seed-cots-note.md",
    "06_RESEARCH_AND_REFERENCES/web_references/local_manifest.yaml": "2026-03-22-dashboard-seed-web-note.md",
    "06_RESEARCH_AND_REFERENCES/presentations/local_manifest.yaml": "2026-03-22-dashboard-seed-presentation-note.md",
    "07_PROJECT_EXECUTION/execution_items/local_manifest.yaml": "EXEC-ISSUE-001-dashboard-seed-validation.json",
    "07_PROJECT_EXECUTION/budget_resources/local_manifest.yaml": "2026-03-22-dashboard-seed-budget-note.md",
    "07_PROJECT_EXECUTION/procurement/local_manifest.yaml": "2026-03-22-dashboard-seed-procurement-note.md",
    "07_PROJECT_EXECUTION/change_requests/local_manifest.yaml": "2026-03-22-dashboard-seed-change-request.md",
    "09_COMMUNICATION/meetings/raw_notes/local_manifest.yaml": "2026-03-22-dashboard-seed-sync-raw-notes.md",
    "09_COMMUNICATION/meetings/summaries/local_manifest.yaml": "2026-03-22-dashboard-seed-sync-summary.md",
    "09_COMMUNICATION/internal_updates/local_manifest.yaml": "2026-03-22-dashboard-seed-internal-update.md",
    "09_COMMUNICATION/external_updates/local_manifest.yaml": "2026-03-22-dashboard-seed-external-update.md",
    "09_COMMUNICATION/reporting/local_manifest.yaml": "2026-03-22-dashboard-seed-report.md",
    "10_OPERATIONS_AND_HANDOFF/deployment_installation/local_manifest.yaml": "2026-03-22-dashboard-seed-deployment-note.md",
    "10_OPERATIONS_AND_HANDOFF/user_docs/local_manifest.yaml": "2026-03-22-dashboard-seed-user-doc.md",
    "10_OPERATIONS_AND_HANDOFF/maintenance/local_manifest.yaml": "2026-03-22-dashboard-seed-maintenance-note.md",
    "10_OPERATIONS_AND_HANDOFF/training/local_manifest.yaml": "2026-03-22-dashboard-seed-training-note.md",
    "10_OPERATIONS_AND_HANDOFF/support_notes/local_manifest.yaml": "2026-03-22-dashboard-seed-support-note.md",
}

JSON_EXPECTATIONS = {
    "04_DESIGN_AND_IMPLEMENTATION/system_risk_register/system_risk_register.json": "risks",
    "07_PROJECT_EXECUTION/roadmap/roadmap.json": "items",
    "07_PROJECT_EXECUTION/project_risk_register/project_risk_register.json": "__list__",
    "08_DECISIONS/decisions.json": "__list__",
    "07_PROJECT_EXECUTION/execution_items/EXEC-ISSUE-001-dashboard-seed-validation.json": "problem_statement",
}


class TestProjectSeedArtifactsTests(unittest.TestCase):
    def test_expected_seed_artifacts_exist(self) -> None:
        for relative_folder, expected_name in EXPECTED_ARTIFACTS.items():
            artifact_path = PROJECT_ROOT / relative_folder / expected_name
            self.assertTrue(
                artifact_path.exists(),
                f"Expected seeded artifact at {artifact_path}",
            )

    def test_local_manifests_index_seeded_artifacts(self) -> None:
        for manifest_relative_path, expected_name in MANIFEST_EXPECTATIONS.items():
            manifest_path = PROJECT_ROOT / manifest_relative_path
            payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            file_names = [item["name"] for item in payload["files"]]
            self.assertIn(
                expected_name,
                file_names,
                f"Expected {expected_name} in {manifest_path}",
            )

    def test_canonical_json_artifacts_are_well_formed(self) -> None:
        for relative_path, expected_key in JSON_EXPECTATIONS.items():
            artifact_path = PROJECT_ROOT / relative_path
            payload = json.loads(artifact_path.read_text(encoding="utf-8"))
            if expected_key == "__list__":
                self.assertIsInstance(payload, list, f"Expected list payload in {artifact_path}")
            else:
                self.assertIn(expected_key, payload, f"Missing key {expected_key} in {artifact_path}")

    def test_change_log_and_root_summary_reflect_dashboard_seeding(self) -> None:
        change_log_path = PROJECT_ROOT / "00_GOVERNANCE" / "change_log" / "change_log.json"
        change_log = json.loads(change_log_path.read_text(encoding="utf-8"))
        self.assertIn("dashboard dummy artifacts", change_log[0]["change_summary"])

        root_readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Dashboard seed data", root_readme)
        self.assertIn("2026-03-22-dashboard-seed-overview.md", root_readme)


if __name__ == "__main__":
    unittest.main()
