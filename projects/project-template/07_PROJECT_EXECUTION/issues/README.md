# Issues

Keep execution issues here. Use one Markdown file per issue. If you maintain a board view, keep it simple and make sure it lists every active issue exactly once.

## Keep Here

- blockers
- delivery risks that need active tracking as issues
- actions assigned to an owner
- issue records linked to work packages, milestones, or change requests

## Issue Shape

Each issue file should keep this header order:

- `ID`
- `Title`
- `Type`
- `Priority`
- `Owner`
- `Status`
- `Created`
- `Due`

Then use these sections:

- `## Context`
- `## Problem Statement`
- `## Definition of Done`
- `## Dependencies`
- `## Notes / Links`

Keep the definition of done as Markdown checkboxes. Use `unknown` if the due date is not set.

## Kanban View

If you maintain a board view, keep it human-readable. Keep one row per active issue and move the row when the status changes. Archive or remove rows once the issue is closed so the board stays limited to active work.

## Example

```md
# KEY-ISSUE-007 Vendor evidence gap

- ID: `KEY-ISSUE-007`
- Title: `Vendor evidence gap`
- Type: `External dependency`
- Priority: `High`
- Owner: `Program Management`
- Status: `Blocked`
- Created: `2026-03-21`
- Due: `unknown`

## Context
Waiting on vendor documentation needed for downselect.

## Problem Statement
The project cannot close the procurement review without the missing evidence.

## Definition of Done
- [ ] Required vendor documents received
- [ ] Procurement review updated

## Dependencies
- `../procurement/...`
- `../milestones/...`

## Notes / Links
- Escalated in weekly sync.
```

## Kanban Reference Example

```md
# Issue Board

| ID | Title | Owner | Priority | Status | Due |
| --- | --- | --- | --- | --- | --- |
| `KEY-ISSUE-001` | Vendor evidence gap | `Program Management` | `High` | `Blocked` | `unknown` |
| `KEY-ISSUE-002` | Prototype test fixture ready | `Verification Lead` | `Medium` | `In Progress` | `2026-03-28` |
| `KEY-ISSUE-003` | Supplier quote comparison complete | `Procurement` | `Medium` | `Ready` | `2026-03-30` |
| `KEY-ISSUE-004` | Review open change request scope impact | `Systems Team` | `High` | `To Do` | `2026-03-25` |
| `KEY-ISSUE-005` | Close resolved training material gap | `Operations` | `Low` | `Done` | `2026-03-20` |
```

