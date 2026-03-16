# Assumptions Constraints

Store assumptions and constraints here as JSON artifacts with minimal boilerplate.

## Purpose

Each artifact in this folder should capture one or more assumptions or constraints that shape the project.

Use this folder for:
- planning assumptions
- technical constraints
- organizational or operational constraints
- external dependencies or boundary conditions

Do not use this folder for:
- final decisions without supporting context
- broad narrative notes better suited to `project_brief` or `scope`
- duplicate copies of evidence already stored elsewhere

## Required JSON Shape

Each record must include:
- `description`: the assumption or constraint itself
- `rationale`: why it exists or why it matters
- `source`: where it came from
- `importance`: a numeric importance score

Recommended supporting fields:
- `id`: stable identifier
- `type`: `assumption` or `constraint`
- `status`: such as `active`, `validated`, `invalidated`, or `retired`
- `notes`: short clarification if needed
- `related_links`: links to upstream or downstream artifacts

## Example

```json
[
  {
    "id": "AC-001",
    "type": "constraint",
    "description": "The first release must fit the existing project-template folder model.",
    "rationale": "The repository is structured for evidence-first project memory, so introducing a competing structure would reduce traceability and retrieval quality.",
    "source": "projects/project-template/project_manifest.yaml",
    "importance": 5,
    "status": "active",
    "related_links": [
      "projects/project-template/README.md",
      "projects/project-template/01_PROJECT_FOUNDATION/scope/README.md"
    ]
  },
  {
    "id": "AC-002",
    "type": "assumption",
    "description": "Assumptions and constraints can be reviewed independently instead of being embedded in long narrative documents.",
    "rationale": "A structured JSON format reduces repeated prose and makes the content easier to query, compare, and update over time.",
    "source": "folder authoring convention",
    "importance": 4,
    "status": "active"
  }
]
```

## Authoring Rules

- Prefer updating an existing JSON artifact instead of creating overlapping files.
- Keep wording concrete and evidence-based.
- Use one consistent importance scale within a file. Recommended scale: `1` low to `5` critical.
- Make `source` specific enough that another reader can trace it.
- When an entry changes related requirements, design, validation, or decisions, update the linked artifacts as well.
- Move superseded material to `99_ARCHIVE` rather than deleting traceability.

