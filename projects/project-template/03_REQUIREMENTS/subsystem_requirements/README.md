# Subsystem Requirements

Subsystem-level requirements grouped by technical ownership boundary live here.

## Canonical Artifacts

- Create one JSON file per subsystem when real content exists.
- Name each file `<subsystem>_requirements.json`.
- Do not keep a shared placeholder `requirements.json` in this folder.
- Each subsystem file must be a top-level JSON array where each object is one requirement.

## Authoring Rules

- Use IDs with the `PRJ-<three-letter subsystem acronym>-` prefix, where the acronym is unique within the project.
- Requirement `status` must be one of `Accepted`, `Preliminary`, or `Abandoned`.
- Obsolete or non-relevant requirements must remain in the live subsystem JSON file and be retagged as `Abandoned`; do not delete them from the active record.
- If a requirement is already tagged `Accepted`, do not modify it unless there is explicit user confirmation recorded in `00_GOVERNANCE/change_log/change_log.md`.
- `compliance_status` must be one of `Undetermined`, `Compliant`, or `Non-compliant`.
- Link each subsystem requirement to its parent system requirement and to downstream design, interface, validation, and decision evidence.
- Create a new subsystem file only when the ownership boundary is clear and stable.

## Example Entry

Example filename: `sensor_stack_requirements.json`

```json
{
  "id": "PRJ-SEN-12",
  "requirement_class": "Interface",
  "groupings": [
    "Subsystem Boundary"
  ],
  "statement": "The subsystem shall ...",
  "need_number_or_parent_requirement": "PRJ-REQ-12",
  "priority": "Shall have",
  "status": "Preliminary",
  "verification_method": "Test",
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

