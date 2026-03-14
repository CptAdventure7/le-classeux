# Milestones

This folder belongs to the project-template context bank.

## What Belongs Here

Milestone tracking artifacts for execution planning and delivery follow-through.

Use `milestones.md` as the folder-level board that aggregates the active milestone view.
Store each milestone as a separate JSON file in this folder so milestone details remain individually traceable and easy to cross-link.

## What Does Not Belong Here

- Unscoped notes that should live in a broader parent folder.
- Duplicate copies of documents that already exist elsewhere in the context bank.
- Final decisions without a link to the originating issue, requirement, or review.
- Mixed multi-milestone detail records bundled into one JSON file.

## Cross-Links To Maintain

- Link to the immediate upstream context that justifies the artifact.
- Link to downstream evidence, implementation, or decision records affected by changes here.
- Review adjacent folders when a change affects related material: `07_PROJECT_EXECUTION/roadmap`, `07_PROJECT_EXECUTION/work_packages`, `07_PROJECT_EXECUTION/backlog`, `07_PROJECT_EXECUTION/issues`.

## Detailed Authoring Guidance

The sections below capture the drafting, update, cross-linking, and any folder-specific formatting rules for this folder.

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
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.

