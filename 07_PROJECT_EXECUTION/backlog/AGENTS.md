# Agent Instructions

Read `README.md` in this folder before drafting or editing documents.

## Drafting Rules

- Create new files only when the concept is meaningfully distinct from existing material.
- Prefer incremental updates that preserve history and traceability.
- Use explicit links to related folders and files instead of restating the same content.
- Treat every backlog item in this folder as an issue record.
- Use the same Markdown formatting and structure used for issue records in `../issues/`.
- Every backlog item file in this folder should preserve this exact field order in the header list:
  - `ID`
  - `Title`
  - `Type`
  - `Priority`
  - `Owner`
  - `Status`
  - `Created`
  - `Due`
- Every backlog item file in this folder should include these sections in order:
  - `## Context`
  - `## Problem Statement`
  - `## Acceptance Criteria`
  - `## Dependencies`
  - `## Notes / Links`
- Keep acceptance criteria as Markdown checkboxes.
- Use `unknown` when the due date is not yet defined.
- Use this format for backlog item identifiers: `KEY-ISSUE-007 Build COTS downselect matrix and vendor evidence request`.

## Update Rules

- When content changes here, check whether linked requirements, decisions, tests, or plans also need updates.
- Add a new note under `~history/` when fresh information affects how this folder's current documents should be read.
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.
