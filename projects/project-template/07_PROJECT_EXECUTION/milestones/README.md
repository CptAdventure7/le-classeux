# Milestones

Keep milestone tracking here. Use `milestones.md` for the board view and one JSON file per milestone for details.

## Keep Here

- milestone summaries and status changes
- target and completion dates
- deliverables and dependencies
- links to roadmap, issues, work packages, and evidence

## Milestone JSON Shape

Each milestone file should use these keys:

- `id`
- `title`
- `summary`
- `status`
- `owner`
- `created`
- `target_date`
- `completion_date`
- `deliverables`
- `dependencies`
- `linked_artifacts`
- `notes`

Keep `deliverables`, `dependencies`, and `linked_artifacts` as arrays. Use `null` when `completion_date` is not known yet.

## Example

```json
{
  "id": "KEY-MILESTONE-001",
  "title": "Prototype integration baseline",
  "summary": "Complete the first integrated prototype baseline and supporting evidence for internal review.",
  "status": "Planned",
  "owner": "Systems Team",
  "created": "2026-03-12",
  "target_date": "2026-05-15",
  "completion_date": null,
  "deliverables": [
    "Integrated prototype build",
    "Verification summary",
    "Review package"
  ],
  "dependencies": [
    "../work_packages/WP-001-prototype-integration.md",
    "../issues/KEY-ISSUE-014-prototype-blockers.md"
  ],
  "linked_artifacts": [
    "../roadmap/roadmap.json"
  ],
  "notes": "Link the milestone to the artifacts that determine readiness."
}
```

