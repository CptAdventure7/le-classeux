import unittest
from pathlib import Path


REQUIREMENTS_DIR = Path(__file__).resolve().parent
README_PATHS = [
    REQUIREMENTS_DIR / "user_requirements" / "README.md",
    REQUIREMENTS_DIR / "system_requirements" / "README.md",
    REQUIREMENTS_DIR / "subsystem_requirements" / "README.md",
]


class RequirementSchemaDocsTest(unittest.TestCase):
    def test_requirement_statuses_are_aligned_across_requirement_levels(self) -> None:
        for readme_path in README_PATHS:
            text = readme_path.read_text(encoding="utf-8")
            self.assertIn(
                "Requirement `status` must be one of `Accepted`, `Preliminary`, or `Abandoned`.",
                text,
                msg=f"Expected aligned statuses in {readme_path}",
            )

    def test_examples_use_verification_prefixed_fields_and_tbd_defaults(self) -> None:
        for readme_path in README_PATHS:
            text = readme_path.read_text(encoding="utf-8")
            self.assertIn('"verification_method": "TBD"', text, msg=f"Expected TBD verification method in {readme_path}")
            self.assertIn('"verification_summary": "TBD"', text, msg=f"Expected TBD verification summary in {readme_path}")
            self.assertIn(
                '"verification_compliance_status": "TBD"',
                text,
                msg=f"Expected renamed verification compliance field in {readme_path}",
            )
            self.assertIn(
                '"verification_justification_or_comment": "TBD"',
                text,
                msg=f"Expected renamed verification justification field in {readme_path}",
            )
            self.assertNotIn('"compliance_status":', text, msg=f"Legacy compliance field should be removed from {readme_path}")
            self.assertNotIn(
                '"justification_or_comment":',
                text,
                msg=f"Legacy justification field should be removed from {readme_path}",
            )

    def test_reference_and_follow_up_fields_are_append_only_lists(self) -> None:
        for readme_path in README_PATHS:
            text = readme_path.read_text(encoding="utf-8")
            self.assertIn('"reference": [', text, msg=f"Expected append-only reference list in {readme_path}")
            self.assertIn('"follow_up_comments": [', text, msg=f"Expected append-only follow-up list in {readme_path}")
            self.assertIn(
                '2026-03-23 | source |',
                text,
                msg=f"Expected dated source reference example in {readme_path}",
            )
            self.assertIn(
                '2026-03-23 | open_question |',
                text,
                msg=f"Expected dated follow-up example in {readme_path}",
            )


if __name__ == "__main__":
    unittest.main()
