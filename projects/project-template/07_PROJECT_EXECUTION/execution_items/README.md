# Execution Items

Keep execution tracking here in one unified JSON-per-item folder. Use this folder for both issues and milestones. Do not keep a separate board file.

## Folder Contract

- Keep one JSON file per execution item.
- Keep `local_manifest.yaml` as the folder index for quick triage.
- Use `type` to distinguish `issue` and `milestone`.
- Prefer updating an existing item file in place instead of creating duplicates.
- Use stable IDs so roadmap, procurement, change requests, and evidence can link back cleanly.

## Keep Here

- blockers, follow-ups, and delivery problems tracked as `issue`
- checkpoints, target outcomes, and date-bound delivery markers tracked as `milestone`
- dependencies, owners, linked artifacts, and completion state for either type

## JSON Shape

Each execution item file should use these shared keys:

- `id`
- `type`
- `title`
- `status`
- `owner`
- `created`
- `target_date`
- `completion_date`
- `priority`
- `summary`
- `dependencies`
- `linked_artifacts`
- `notes`

Type-specific keys:

- `issue`: `problem_statement`, `definition_of_done`
- `milestone`: `deliverables`

Keep `dependencies`, `linked_artifacts`, `notes`, `definition_of_done`, and `deliverables` as arrays. Use `null` when `target_date` or `completion_date` is not known yet. Prefer repository-relative paths in `linked_artifacts`.

## Example

```json
{
  "id": "EXEC-ISSUE-001",
  "type": "issue",
  "title": "Vendor evidence gap",
  "status": "blocked",
  "owner": "Program Management",
  "created": "2026-03-22",
  "target_date": null,
  "completion_date": null,
  "priority": "high",
  "summary": "Missing vendor documentation is blocking procurement review closure.",
  "dependencies": [
    "EXEC-MILESTONE-002"
  ],
  "linked_artifacts": [
    "projects/project-template/07_PROJECT_EXECUTION/procurement/vendor-a/decision.md"
  ],
  "notes": [
    "Escalated in weekly sync."
  ],
  "problem_statement": "The project cannot close procurement review without the missing evidence.",
  "definition_of_done": [
    "Required vendor documents received",
    "Procurement review updated"
  ]
}
```

## Local Manifest

- Review `local_manifest.yaml` when entering this folder to quickly see whether any local files are relevant.
- Keep `local_manifest.yaml` up to date whenever files are added, removed, renamed, or materially repurposed.
