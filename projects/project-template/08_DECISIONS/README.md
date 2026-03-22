# Decisions

Keep project decisions here in a single canonical JSON artifact.

## Purpose

When this folder is populated, it should contain exactly one maintained data artifact: `decisions.json`.

That file captures the key project decisions and the reasoning behind them.

Use this folder for:
- accepted, pending, rejected, or superseded decisions
- rationale, impacts, and trade-offs
- traceability to related requirements, design work, risks, and verification evidence

Do not use this folder for:
- one-markdown-file-per-decision notes
- broad narrative context better suited to `project_definition` or design artifacts
- duplicate copies of requirements, risks, or implementation evidence already stored elsewhere

## Folder Rule

- Keep exactly one JSON data file in this folder: `decisions.json`.
- In the starter project template, do not keep a placeholder JSON file with fake seed content.
- Create `decisions.json` only when the project has real decisions to record.
- If it already exists, update it in place.
- Do not create multiple decision files in this folder.

## Required JSON Shape

`decisions.json` should contain a JSON array.

Each array item must include:
- `date`
- `decision`
- `rationale`
- `impact`

Recommended fields:
- `id`
- `title`
- `status`
- `context`
- `alternatives_considered`
- `decision_maker`
- `related_links`
- `notes`

Keep `impact`, `alternatives_considered`, and `related_links` as arrays. Prefer ISO dates in `YYYY-MM-DD` form. Keep `status` values consistent within the file, such as `proposed`, `accepted`, `rejected`, `superseded`, or `deprecated`.

## Example

```json
[
  {
    "id": "DEC-001",
    "title": "Use a single JSON artifact for decision tracking",
    "date": "2026-03-22",
    "status": "accepted",
    "decision": "Keep project decisions in one canonical `decisions.json` file instead of separate templates or per-decision subfolders.",
    "context": "The project template is being simplified toward single-artifact folder contracts that are easier for humans and agents to maintain consistently.",
    "rationale": "A single JSON file keeps the decision log queryable, avoids scattered markdown stubs, and matches the JSON-first pattern already used in other folders.",
    "impact": [
      "Decision tracking stays in one predictable location.",
      "The README carries the schema example instead of seeding placeholder files.",
      "Related requirements, design notes, and risks can link to stable decision IDs."
    ],
    "alternatives_considered": [
      "One markdown file per decision",
      "Decision subfolders with sidecar notes",
      "No structured decision log"
    ],
    "decision_maker": "project structure maintainers",
    "related_links": [
      "projects/project-template/project_manifest.yaml",
      "projects/project-template/00_GOVERNANCE/change_log/change_log.json"
    ],
    "notes": "Add new decisions as new objects in the array and keep wording concise and evidence-based."
  }
]
```

## Authoring Rules

- Prefer updating `decisions.json` instead of creating new files.
- Keep decisions concise, concrete, and traceable to evidence.
- Record the decision itself, not only discussion notes.
- Make `rationale` specific enough that another reader can understand why the choice was made.
- Update related requirements, design artifacts, risks, and verification links when a decision changes them.
- Move obsolete supporting artifacts to `99_ARCHIVE` only when they are no longer active, while preserving traceability.

