# Agent Instructions

Read `README.md` in this folder before drafting or editing documents.

## Drafting Rules

- Create new files only when the concept is meaningfully distinct from existing material.
- Prefer incremental updates that preserve history and traceability.
- Use explicit links to related folders and files instead of restating the same content.
- Keep the top-level kanban snapshot in `kanban.md` present and current.
- Draft issue records in Markdown using the canonical template in `issue-template.md`.
- Every issue file in this folder should preserve this exact field order in the header list:
  - `ID`
  - `Title`
  - `Type`
  - `Priority`
  - `Owner`
  - `Status`
  - `Created`
  - `Due`
- Every issue file in this folder should include these sections in order:
  - `## Context`
  - `## Problem Statement`
  - `## Acceptance Criteria`
  - `## Dependencies`
  - `## Notes / Links`
- Update `kanban.md` whenever an issue is created, changes status, or is re-prioritized in a way that affects the board snapshot.
- Use the canonical kanban structure in `kanban.md` with these sections in order:
  - `## Backlog`
  - `## In Progress`
  - `## Blocked`
  - `## Review`
  - `## Done`
  - `## Notes`
- Keep acceptance criteria as Markdown checkboxes.
- Use `unknown` when the due date is not yet defined.
- Use this format ex: - KEY-ISSUE-007 Build COTS downselect matrix and vendor evidence request from.

## Update Rules

- When content changes here, check whether linked requirements, decisions, tests, or plans also need updates.
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.

