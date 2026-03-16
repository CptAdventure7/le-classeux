# User Requirements

User-facing needs, jobs-to-be-done, and externally visible acceptance statements live here.

## Canonical Artifact

- Keep one top-level `requirements.json` file in this folder when real content exists.
- Do not keep placeholder JSON files. The example schema belongs in this README until the project has actual requirements to record.
- `requirements.json` must be a top-level JSON array where each object is one requirement.

## Authoring Rules

- Use IDs with the `PRJ-UN-` prefix.
- Requirement `status` must be one of `Accepted`, `Preliminary`, or `Abandoned`.
- Obsolete or non-relevant requirements must remain in `requirements.json` and be retagged as `Abandoned`; do not delete them from the live record.
- If a requirement is already tagged `Accepted`, do not modify it unless there is explicit user confirmation recorded in `00_GOVERNANCE/change_log/change_log.md`.
- `compliance_status` must be one of `Undetermined`, `Compliant`, or `Non-compliant`.
- Link each requirement to its source need and to downstream design, validation, and decision evidence.
- When requirements change, update affected material in `system_requirements` and `subsystem_requirements`.

## Example Entry

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

