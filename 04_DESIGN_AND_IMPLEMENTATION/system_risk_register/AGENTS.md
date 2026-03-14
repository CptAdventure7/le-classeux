# Agent Instructions

Read `README.md` in this folder before drafting or editing documents.

## Current Canonical Artifact

- The single source of truth for the system risk register is `system_risk_register.json` in this folder.
- Keep system-risk data in that JSON file instead of creating parallel prose summaries unless a separate artifact is explicitly needed.
- When updating risk content, preserve append-only traceability for comments.

## Drafting Rules

- Create new files only when the concept is meaningfully distinct from existing material.
- Prefer incremental updates that preserve history and traceability.
- Use explicit links to related folders and files instead of restating the same content.
- Use the following system-risk structure in `system_risk_register.json`:
  - `id`: format `SRSK-0001`
  - `hazard_category`: hazard class or domain
  - `function_or_subsystem_affected`: string or array; use `multiple` when one risk spans several subsystems
  - `failure_mode`: concise statement of how the system can fail
  - `potential_causes`: array; use `["multiple"]` only when specific causes are not yet decomposed
  - `potential_harm_effects`: array of patient, user, operator, property, or mission harms
  - `severity`: integer `1` to `5`
  - `occurrence`: integer `1` to `5`
  - `possible_control_measures`: array of candidate controls not yet committed
  - `applied_control_measures`: array of controls implemented or formally accepted for implementation
  - `traceability_to_requirement`: array of `REQ-*` identifiers; use an empty array when no requirement link exists yet
  - `control_measure_type`: one of `by_design`, `protective_measure`, or `labelling`
  - `new_risk_introduced_by_control_measure`: `no` or an `SRSK-*` identifier
  - `residual_risk_severity`: integer `1` to `5`
  - `residual_risk_occurrence`: integer `1` to `5`
  - `date_of_last_review`: ISO date `YYYY-MM-DD`
  - `status`: `open`, `mitigated`, `accepted`, or `closed`
  - `owner`: person or team responsible for review and updates
  - `comments`: append-only dated entries
  - `links`: array with zero or more related artifact links
- Treat larger numeric values in `severity`, `occurrence`, `residual_risk_severity`, and `residual_risk_occurrence` as higher risk.
- Prefer arrays for multi-value fields even when there is currently only one value.
- When a control introduces a new risk, create or link the downstream `SRSK-*` entry explicitly instead of embedding that new risk inside the parent record.

## Update Rules

- When content changes here, check whether linked requirements, decisions, tests, or plans also need updates.
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.


