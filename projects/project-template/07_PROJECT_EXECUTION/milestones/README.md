# Milestones

Keep milestone tracking here. Use `milestones.md` for the board view and one JSON file per milestone for details.

## `milestones.md`

When a project is instantiated and milestone tracking starts, create `milestones.md` as the board view. Do not keep a seeded template `milestones.md` file in the project template.

Keep the board concise and update it whenever a milestone is created, changes status, moves date, or completes.

Use these sections:

- `## Active Milestones`
- `## Watchlist`
- `## Recently Completed`
- `## Notes`

Each active or completed entry should stay to a one-line summary with the milestone ID, short title, and the most important date or state. Use `Watchlist` for milestones at risk, blocked, or otherwise needing attention. Use `Notes` only for short folder-level reminders about how the board should be maintained.

Example board shape:

```md
# Milestones

## Active Milestones

- KEY-MILESTONE-001 Prototype integration baseline due 2026-05-15

## Watchlist

- None.

## Recently Completed

- None.

## Notes

- Keep this file synchronized with milestone creation, status changes, due-date movement, and completion.
```

## Per-milestone JSON Files

Create one JSON file per milestone when the board needs supporting detail. Keep the filename aligned to the milestone ID and title so it is easy to scan.

Each file should capture milestone summaries and status changes, target and completion dates, deliverables and dependencies, and links to roadmap, issues, work packages, and evidence.

Each milestone file should use these keys:

- `id`
- `title`
- `summary`
- `status`
- `owner`
- `created`
- `target_date`
- `completion_date`
- `deliverables`
- `dependencies`
- `linked_artifacts`
- `notes`

Keep `deliverables`, `dependencies`, and `linked_artifacts` as arrays. Use `null` when `completion_date` is not known yet. Link dependencies and related evidence with repository-relative paths when possible.

