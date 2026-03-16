# Stakeholders

Store stakeholders here in a single canonical JSON artifact with minimal boilerplate.

## Purpose

When this folder is populated, it should contain exactly one maintained data artifact: `stakeholders.json`.

That file captures the people, groups, or organizations that shape the project and their roles in it.

Use this folder for:
- project sponsors, owners, users, reviewers, approvers, and contributors
- internal and external actors who influence scope, constraints, or decisions
- role summaries that clarify what each stakeholder does in this project

Do not use this folder for:
- glossary or terminology content better suited to `glossary`
- detailed resourcing plans better suited to `07_PROJECT_EXECUTION`
- duplicate biographical notes without project relevance

## Folder Rule

- Keep exactly one JSON data file in this folder: `stakeholders.json`.
- In the starter project template, do not keep a placeholder JSON file with fake seed content.
- Create `stakeholders.json` only when the project has real stakeholders to record.
- If it already exists, update it in place.
- Do not create multiple stakeholder files in this folder.

## Required JSON Shape

`stakeholders.json` should contain a JSON array.

Each array item must include:
- `name`: the stakeholder's name
- `type`: the stakeholder category such as `person`, `team`, `customer`, `partner`, or `organization`
- `affiliation`: the organization, team, or group they belong to
- `role`: a short few-sentence description of what this stakeholder does in the project

Recommended fields:
- `id`: stable identifier
- `influence`: qualitative or numeric indication of decision influence
- `source`: where the stakeholder information came from
- `notes`: short clarification if needed
- `related_links`: links to artifacts affected by or owned by the stakeholder

## Example

```json
[
  {
    "id": "SH-001",
    "name": "Project structure maintainer",
    "type": "person",
    "affiliation": "project-template workspace",
    "role": "Maintains the project-template folder model and its authoring conventions. Reviews structural changes to keep the context bank queryable, consistent, and traceable across updates.",
    "source": "workspace governance and repository conventions",
    "related_links": [
      "projects/project-template/README.md",
      "projects/project-template/project_manifest.yaml"
    ]
  }
]
```

## Authoring Rules

- Prefer updating `stakeholders.json` instead of creating new files.
- Keep each `role` concrete and specific to the project rather than generic job-title text.
- Make `affiliation` and `type` consistent across entries so the file stays queryable.
- If stakeholder changes affect requirements, decisions, ownership, or validation plans, update the linked artifacts as well.
- Move superseded material to `99_ARCHIVE` rather than deleting traceability.

