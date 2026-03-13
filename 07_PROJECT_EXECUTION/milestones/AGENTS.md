# Agent Instructions

Read `README.md` in this folder before drafting or editing documents.

## Drafting Rules

- Create new files only when the concept is meaningfully distinct from existing material.
- Prefer incremental updates that preserve history and traceability.
- Use explicit links to related folders and files instead of restating the same content.
- Keep the top-level milestone board in `milestones.md` present and current.
- Draft each milestone as a separate JSON file using `milestone-template.json` as the canonical shape reference.
- Every milestone JSON file in this folder should preserve this exact key set:
  - `ID`
  - `Title`
  - `Summary`
  - `Status`
  - `Owner`
  - `Created`
  - `Target Date`
  - `Completion Date`
  - `Deliverables`
  - `Dependencies`
  - `Linked Artifacts`
  - `Notes`
- Update `milestones.md` whenever a milestone is created, changes status, slips, or completes in a way that affects the folder-level execution view.
- Use the canonical milestone board structure in `milestones.md` with these sections in order:
  - `## Active Milestones`
  - `## Watchlist`
  - `## Recently Completed`
  - `## Notes`
- Keep `deliverables`, `dependencies`, and `linked_artifacts` as JSON arrays.
- Use `null` when the completion date is not yet defined.
- Use this format ex: - KEY-MILESTONE-003 Internal validation baseline due 2026-07-15

## Update Rules

- When content changes here, check whether linked requirements, decisions, tests, or plans also need updates.
- Add a new note under `~history/` when fresh information affects how this folder's current documents should be read.
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.
