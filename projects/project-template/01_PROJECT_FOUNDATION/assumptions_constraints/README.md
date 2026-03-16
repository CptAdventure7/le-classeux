# Assumptions Constraints

Store assumptions and constraints here in a single canonical JSON artifact with minimal boilerplate.

## Purpose

When this folder is populated, it should contain exactly one maintained data artifact: `assumptions_constraints.json`.

That file captures all assumptions and constraints that shape the project.

Use this folder for:
- planning assumptions
- technical constraints
- organizational or operational constraints
- external dependencies or boundary conditions

Do not use this folder for:
- final decisions without supporting context
- broad narrative notes better suited to `project_brief` or `scope`
- duplicate copies of evidence already stored elsewhere

## Folder Rule

- Keep exactly one JSON data file in this folder: `assumptions_constraints.json`.
- In the starter project template, do not keep a placeholder JSON file with fake seed content.
- Create `assumptions_constraints.json` only when the project has real assumptions or constraints to record.
- If it already exists, update it in place.
- Do not create multiple assumption or constraint files in this folder.

## Required JSON Shape

`assumptions_constraints.json` should contain a JSON array.

Each array item must include:
- `description`: the assumption or constraint itself
- `rationale`: why it exists or why it matters
- `source`: where it came from
- `importance`: a numeric importance score
- `stakeholder_provenance`: which stakeholder, group, or source context introduced or justified the entry

Recommended fields:
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
    "stakeholder_provenance": "workspace governance and project-structure maintainers",
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
    "stakeholder_provenance": "project context-bank maintainers",
    "status": "active"
  }
]
```

## Authoring Rules

- Prefer updating `assumptions_constraints.json` instead of creating new files.
- Keep wording concrete and evidence-based.
- Use one consistent importance scale within a file. Recommended scale: `1` low to `5` critical.
- Make `source` specific enough that another reader can trace it.
- When an entry changes related requirements, design, validation, or decisions, update the linked artifacts as well.
- Move superseded material to `99_ARCHIVE` rather than deleting traceability.

