# Design Reviews

Store each design review as one markdown artifact.

## Canonical Artifact Pattern

- Create exactly one `.md` file per review.
- Name each file `YYYY-MM-DD-<concise-meaningful-name>.md`.
- Use a short scope name that helps a reader recognize the review topic immediately.
- Update the existing review artifact if the same review record is refined later.
- Do not create placeholder files in the starter template.

## Required Categories

Each review artifact must contain these categories in this order:
- `Project Number`
- `Project Name`
- `Review Date`
- `Review Type`
- `Quality Assessment`
- `Attendee List`
- `Absentee List`
- `Objective`
- `Meeting Notes`
- `Conclusion`
- `Action Items`

`Quality Assessment` must be explicitly `Yes` or `No`.

## Action Items

Write `Action Items` as a JSON array using the same structure as the meeting-summary workflow:

```json
[
  {
    "assignee": "Name or Unknown",
    "description": "Action to complete, with relevant context from the review.",
    "definition_of_done": "Concrete completion condition.",
    "time_horizon": "Exact date or Unknown",
    "status": "backlog"
  }
]
```

Allowed `status` values:
- `backlog`
- `selected for developpement`
- `in progress`

If there are no action items, use an empty array: `[]`.

## Authoring Rules

- Keep one artifact per review; do not split the same review across sibling files.
- Keep the artifact focused on the review record, not on broader design history that belongs in `04_DESIGN_AND_IMPLEMENTATION/design`.
- Link to the reviewed design artifact, related requirements, risks, code, and decisions instead of copying large sections into the review.
- Remove filler and repeated boilerplate; the file should read like a usable review record.
- Move superseded or cancelled review records to `99_ARCHIVE` rather than deleting traceability.

## Example Filename

- `2026-03-16-control-loop-preliminary-review.md`

## Local Manifest

- Review `local_manifest.yaml` when entering this folder to quickly see whether any local files are relevant.
- Keep `local_manifest.yaml` up to date whenever files are added, removed, renamed, or materially repurposed.
