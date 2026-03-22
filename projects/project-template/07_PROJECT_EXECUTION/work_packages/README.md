# Work Packages

Keep work-package planning here in a single canonical JSON artifact.

## Purpose

When this folder is populated, it should contain exactly one maintained data artifact: `work_packages.json`.

That file captures all work packages used to plan and track execution.

Use this folder for:
- work-package scope and ownership
- inputs, outputs, dependencies, and deliverables
- package status and completion notes
- links to roadmap items, issues, milestones, and related evidence

Do not use this folder for:
- one-file-per-package markdown notes
- broad narrative planning better suited to `roadmap`
- duplicate copies of issue, milestone, or evidence records already stored elsewhere

## Folder Rule

- Keep exactly one JSON data file in this folder: `work_packages.json`.
- In the starter project template, do not keep a placeholder JSON file with fake seed content.
- Create `work_packages.json` only when the project has real work-package content to record.
- If it already exists, update it in place.
- Do not create multiple work-package files in this folder.

## Required JSON Shape

`work_packages.json` should contain a JSON array.

Each array item must include:
- `id`
- `title`
- `summary`
- `status`
- `owner`
- `inputs`
- `outputs`
- `dependencies`

Recommended fields:
- `deliverables`
- `start_date`
- `target_date`
- `completion_date`
- `linked_artifacts`
- `notes`

Keep `inputs`, `outputs`, `dependencies`, `deliverables`, and `linked_artifacts` as arrays. Use `null` when `completion_date` is not known yet. Prefer repository-relative paths in `linked_artifacts`.

## Example

```json
[
  {
    "id": "WP-001",
    "title": "Prototype integration baseline",
    "summary": "Define and track the initial integration package for the prototype baseline.",
    "status": "in_progress",
    "owner": "systems lead",
    "inputs": [
      "Approved prototype scope",
      "Initial subsystem interface assumptions"
    ],
    "outputs": [
      "Integrated prototype baseline",
      "Initial verification handoff package"
    ],
    "dependencies": [
      "MILESTONE-001",
      "ISSUE-004"
    ],
    "deliverables": [
      "Prototype integration checklist",
      "Baseline completion note"
    ],
    "start_date": "2026-04-01",
    "target_date": "2026-04-15",
    "completion_date": null,
    "linked_artifacts": [
      "projects/project-template/07_PROJECT_EXECUTION/roadmap/roadmap.md",
      "projects/project-template/07_PROJECT_EXECUTION/milestones"
    ],
    "notes": "Update this entry when scope, dependencies, dates, or ownership changes."
  }
]
```

## Authoring Rules

- Prefer updating `work_packages.json` instead of creating new files.
- Keep entries concise and delivery-oriented.
- Use stable IDs so related roadmap, issue, and milestone artifacts can link back cleanly.
- Keep status values consistent within the file, such as `planned`, `in_progress`, `blocked`, `complete`, or `cancelled`.
- When a work package changes linked milestones, issues, or evidence, update those artifacts as well.

