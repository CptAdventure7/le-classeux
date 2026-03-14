# Cots

This folder belongs to the Maxwell context bank.

## What Belongs Here

Commercial off-the-shelf component evaluations. Add one subfolder per candidate or vendor when needed.

This includes vendor-specific web evidence, supplier comparisons, downselect records, and product-level assessment notes that would otherwise be misfiled as generic web references.

## What Does Not Belong Here

- Unscoped notes that should live in a broader parent folder.
- Duplicate copies of documents that already exist elsewhere in the context bank.
- Final decisions without a link to the originating issue, requirement, or review.

## Cross-Links To Maintain

- Link to the immediate upstream context that justifies the artifact.
- Link to downstream evidence, implementation, or decision records affected by changes here.
- Review adjacent folders when a change affects related material: `06_RESEARCH_AND_REFERENCES/literature_map`, `06_RESEARCH_AND_REFERENCES/papers`, `06_RESEARCH_AND_REFERENCES/standards`.

## Detailed Authoring Guidance

The sections below capture the drafting, update, cross-linking, and any folder-specific formatting rules for this folder.

Read `README.md` in this folder before drafting or editing documents.

## Drafting Rules

- Create new files only when the concept is meaningfully distinct from existing material.
- Prefer incremental updates that preserve history and traceability.
- Use explicit links to related folders and files instead of restating the same content.
- Use this folder for vendor-specific web research and COTS downselect evidence rather than storing that material in `../web_references`.

## Update Rules

- When content changes here, check whether linked requirements, decisions, tests, or plans also need updates.
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.
- Link to source web pages directly when vendor claims, specifications, pricing, or support commitments are part of the COTS assessment.
