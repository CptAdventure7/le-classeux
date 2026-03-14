# Change Log

This folder belongs to the Maxwell context bank.

## What Belongs Here

Chronological governance-level changes, not detailed technical implementation notes.

Use the local `change_log.md` as an append-only record. Add each new change at the top so the most recent entry appears first.

## Entry Format

- Write one concise bullet per change.
- End each entry with a timestamp in `YYYY-MM-DD-HHhMM` form.
- Example: `- added requirement REQ-334 about cake (2026-03-10-11h32).`

## What Does Not Belong Here

- Separate memory folders or sidecar history notes.
- Multi-line change records.
- Detailed implementation notes that belong in requirements, design, validation, or decision artefacts.

## Cross-Links To Maintain

- Link to the immediate upstream context that justifies the artifact.
- Link to downstream evidence, implementation, or decision records affected by changes here.
- Review adjacent folders when a change affects related material: `00_GOVERNANCE/current_overview`.

## Detailed Authoring Guidance

The sections below capture the drafting, update, cross-linking, and any folder-specific formatting rules for this folder.

Read `README.md` in this folder before updating the change log.

## Change Log Rules

- Update the local `change_log.md` file instead of creating separate dated markdown files.
- Keep the log append-only, with the most recent entry at the top.
- Add one line per change and end it with a timestamp in `YYYY-MM-DD-HHhMM` form.
- Keep the change log as the only append-only memory artifact inside the repository.
