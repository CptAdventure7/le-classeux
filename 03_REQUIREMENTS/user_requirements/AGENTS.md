# Agent Instructions

Read `README.md` in this folder before drafting or editing documents.

## Drafting Rules

- Create new files only when the concept is meaningfully distinct from existing material.
- Prefer incremental updates that preserve history and traceability.
- Use explicit links to related folders and files instead of restating the same content.

## Update Rules

- When content changes here, check whether linked requirements, decisions, tests, or plans also need updates.
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.

## Requirement Drafting

- Store requirements in the single `requirements.json` file for this folder. Do not split the canonical requirement set across multiple markdown files.
- Keep `requirements.json` as a top-level JSON array where each item is one requirement object.
- Use IDs with the `PRJ-UN-` prefix in this folder.
- Requirement status values must be one of: `Accepted`, `Preliminary`, `Abandoned`.
- Compliance status values must be one of: `Undetermined`, `Compliant`, `Non-compliant`.
- Update parent allocation if a subsystem requirement changes system behavior or ownership.
- Cross-link to source needs, design allocation, decision records, and validation evidence.
- Use this object shape for each requirement entry:

```json
{
  "id": "PRJ-UN-12",
  "requirement_class": "Functional",
  "groupings": [
    "User Need"
  ],
  "statement": "The user shall be able to ...",
  "need_number_or_parent_requirement": null,
  "priority": "Shall have",
  "status": "Preliminary",
  "verification_method": "Inspection",
  "verification_summary": "Summarize how the requirement will be verified.",
  "compliance_status": "Undetermined",
  "verification_report_reference": "TBD",
  "justification_or_comment": null,
  "difficulty_of_realization": "TBD",
  "compliance_follow_up": "TBD",
  "reference": "TBD",
  "date_of_last_update": "2026-02-18",
  "follow_up_comments": "2026-02-18: Source and traceability note."
}
```

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.

