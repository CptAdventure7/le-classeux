import unittest
from pathlib import Path


REQUIREMENTS_EXAMPLE_PATH = (
    Path(__file__).resolve().parents[1] / "examples" / "requirements.md"
)


class RequirementsExampleGuidanceTest(unittest.TestCase):
    def test_requirement_status_values_include_preliminary_accepted_and_abandoned(self) -> None:
        text = REQUIREMENTS_EXAMPLE_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "Requirement status values must be one of: `Accepted`, `Preliminary`, `Abandoned`.",
            text,
        )

    def test_verification_fields_are_named_and_held_at_tbd_in_early_phase(self) -> None:
        text = REQUIREMENTS_EXAMPLE_PATH.read_text(encoding="utf-8")

        self.assertIn("verification_compliance_status", text)
        self.assertIn("verification_justification_or_comment", text)
        self.assertIn("keep verification fields as `TBD` in early project phases", text)
        self.assertNotIn("Status of conformity values must be one of", text)

    def test_reference_and_follow_up_guidance_are_dated_append_only(self) -> None:
        text = REQUIREMENTS_EXAMPLE_PATH.read_text(encoding="utf-8")

        self.assertIn("`reference` must be an append-only dated source list", text)
        self.assertIn(
            "`follow_up_comments` must be an append-only dated list of comments, open questions, or changes",
            text,
        )


if __name__ == "__main__":
    unittest.main()
