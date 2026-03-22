# Objectives Success Metrics

Store objectives and success metrics here in a single canonical JSON artifact with minimal boilerplate.

## Purpose

When this folder is populated, it should contain exactly one maintained data artifact: `objectives_success_metrics.json`.

That file captures the project's objectives and the metrics used to judge success.

Use this folder for:
- business or mission objectives
- user-outcome objectives
- operational objectives
- measurable success metrics and targets

Do not use this folder for:
- broad narrative notes better suited to `project_definition`
- detailed stakeholder lists better suited to `stakeholders`
- duplicate copies of evidence already stored elsewhere

## Folder Rule

- Keep exactly one JSON data file in this folder: `objectives_success_metrics.json`.
- In the starter project template, do not keep a placeholder JSON file with fake seed content.
- Create `objectives_success_metrics.json` only when the project has real objectives or metrics to record.
- If it already exists, update it in place.
- Do not create multiple objective or metric files in this folder.

## Required JSON Shape

`objectives_success_metrics.json` should contain a JSON array.

Each array item must include:
- `description`: the objective or success metric statement
- `rationale`: why it matters to the project
- `source`: where it came from
- `importance`: a numeric importance score
- `stakeholder_provenance`: which stakeholder, group, or source context introduced or justified the entry

Recommended fields:
- `id`: stable identifier
- `type`: `objective` or `success_metric`
- `target`: the measurable threshold when relevant
- `status`: such as `active`, `tracked`, `met`, `missed`, or `retired`
- `notes`: short clarification if needed
- `related_links`: links to upstream or downstream artifacts

## Example

```json
[
  {
    "id": "OSM-001",
    "type": "objective",
    "description": "Keep the project template easy for humans and agents to navigate with minimal repeated folder guidance.",
    "rationale": "A concise structure lowers retrieval cost and reduces drift between related project artifacts.",
    "source": "projects/test-project/README.md",
    "importance": 5,
    "stakeholder_provenance": "project context-bank maintainers",
    "status": "active",
    "related_links": [
      "projects/test-project/project_manifest.yaml",
      "projects/test-project/01_PROJECT_FOUNDATION/project_definition/README.md"
    ]
  },
  {
    "id": "OSM-002",
    "type": "success_metric",
    "description": "Core foundation folders use one canonical structured artifact instead of repeated narrative boilerplate.",
    "rationale": "Structured artifacts are easier to maintain, compare, and update over time.",
    "source": "folder authoring convention",
    "importance": 4,
    "stakeholder_provenance": "repository governance maintainers",
    "target": "One canonical JSON file per structured foundation folder where applicable",
    "status": "tracked"
  }
]
```

## Authoring Rules

- Prefer updating `objectives_success_metrics.json` instead of creating new files.
- Keep wording concrete and evidence-based.
- Use one consistent importance scale within a file. Recommended scale: `1` low to `5` critical.
- Make `source` specific enough that another reader can trace it.
- Use `target` for entries that need measurable success thresholds.
- When an entry changes related requirements, design, validation, or decisions, update the linked artifacts as well.
- Move superseded material to `99_ARCHIVE` rather than deleting traceability.

