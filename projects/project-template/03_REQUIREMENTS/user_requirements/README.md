# User Requirements

User-facing needs, jobs-to-be-done, and externally visible acceptance statements live here.

## Canonical Artifact

- Keep one top-level `user_requirements.json` file in this folder when real content exists.
- Do not keep placeholder JSON files. The example schema belongs in this README until the project has actual requirements to record.
- `user_requirements.json` must be a top-level JSON array where each object is one requirement.

## Authoring Rules

- Use IDs with the `PRJ-UN-` prefix.
- Requirement `status` must be one of `Accepted`, `Preliminary`, or `Abandoned`.
- Obsolete or non-relevant requirements must remain in `user_requirements.json` and be retagged as `Abandoned`; do not delete them from the live record.
- If a requirement is already tagged `Accepted`, do not modify it unless there is explicit user confirmation recorded in `00_GOVERNANCE/change_log/change_log.json`.
- Keep `verification_method`, `verification_summary`, `verification_compliance_status`, `verification_report_reference`, and `verification_justification_or_comment` at `TBD` during early project phases. Only populate them once the requirement enters an active verification phase.
- `verification_compliance_status` must stay `TBD` until verification work is underway. During verification, it must be one of `Undetermined`, `Compliant`, or `Non-compliant`.
- Put early-phase allocation notes, open questions, and change context in `need_number_or_parent_requirement`, `difficulty_of_realization`, and `follow_up_comments` instead of filling verification fields too early.
- `reference` must be an append-only array of dated source entries using `YYYY-MM-DD | source | <path or citation>`.
- `follow_up_comments` must be an append-only array of dated comments, open questions, or change notes using `YYYY-MM-DD | <comment_type> | <note>`.
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
  "verification_method": "TBD",
  "verification_summary": "TBD",
  "verification_compliance_status": "TBD",
  "verification_report_reference": "TBD",
  "verification_justification_or_comment": "TBD",
  "difficulty_of_realization": "TBD",
  "compliance_follow_up": "TBD",
  "reference": [
    "2026-03-23 | source | 01_PROJECT_FOUNDATION/project_definition/project_definition_baseline.md"
  ],
  "date_of_last_update": "2026-03-23",
  "follow_up_comments": [
    "2026-03-23 | open_question | Confirm the user-facing acceptance check before allocating verification work."
  ]
}
```

