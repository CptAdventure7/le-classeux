# Issues

Keep execution issues here. Use one Markdown file per issue. If you maintain a board view, keep it in `kanban.md`.

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
- `## Acceptance Criteria`
- `## Dependencies`
- `## Notes / Links`

Keep acceptance criteria as Markdown checkboxes. Use `unknown` if the due date is not set.

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

## Acceptance Criteria
- [ ] Required vendor documents received
- [ ] Procurement review updated

## Dependencies
- `../procurement/...`
- `../milestones/...`

## Notes / Links
- Escalated in weekly sync.
```

