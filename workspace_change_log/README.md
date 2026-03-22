# Workspace Change Log

This folder belongs to the workspace root, not to any single project context bank.

## What Belongs Here

Chronological workspace-level changes that happen outside any individual project, such as updates to shared agent resources, workspace entrypoint guidance, shared dashboards, or other root-owned artifacts.

Use the local `change_log.json` as an append-only record. Add each new change at the top of the array so the most recent entry appears first.

## Entry Format

- Keep `change_log.json` as a top-level JSON array.
- Each entry must be a JSON object with exactly these fields: `change_summary` and `date`.
- Keep the log append-only, with the most recent entry at index `0`.
- Store `date` in `YYYY-MM-DD-HHhMM` form.
- Example:

```json
{
  "change_summary": "added workspace-wide guidance for non-project repository changes",
  "date": "2026-03-22-18h11"
}
```

## What Does Not Belong Here

- Changes that belong inside a specific project context bank.
- Separate sidecar memory folders or history notes.
- Multi-line change records.
- Detailed implementation notes that belong in project artifacts, validation records, or decision records.
