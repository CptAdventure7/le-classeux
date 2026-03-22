# Change Log

This folder belongs to the project-template context bank.

## What Belongs Here

Chronological governance-level changes, not detailed technical implementation notes.

Use the local `change_log.json` as an append-only record. Add each new change at the top of the array so the most recent entry appears first.

## Entry Format

- Keep `change_log.json` as a top-level JSON array.
- Each entry must be a JSON object with exactly these fields: `change_summary` and `date`.
- Keep the log append-only, with the most recent entry at index `0`.
- Store `date` in `YYYY-MM-DD-HHhMM` form.
- Example:

```json
{
  "change_summary": "added requirement REQ-334 about cake",
  "date": "2026-03-10-11h32"
}
```
- Example:

```json
{
  "change_summary": "changed requirement PRJ-REQ-12 status to Abandoned instead of removing it",
  "date": "2026-03-10-11h40"
}
```
- Example:

```json
{
  "change_summary": "updated accepted requirement PRJ-REQ-12 after explicit user confirmation",
  "date": "2026-03-10-11h45"
}
```
- Keep the change log as the only append-only memory artifact inside the project.

## What Does Not Belong Here

- Separate memory folders or sidecar history notes.
- Multi-line change records.
- Detailed implementation notes that belong in requirements, design, validation, or decision artefacts.

## Cross-Links To Maintain

- Link to the immediate upstream context that justifies the artifact.
- Link to downstream evidence, implementation, or decision records affected by changes here.
