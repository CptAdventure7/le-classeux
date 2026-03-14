# Agent Instructions

Read `README.md` in this folder before drafting or editing documents.

## Current Canonical Artifact

- The single source of truth for the project risk register is `project_risk_register.json` in this folder.
- Keep project-risk data in that JSON file instead of creating parallel prose summaries unless a separate artifact is explicitly needed.
- When updating risk content, preserve append-only traceability for comments.

## Drafting Rules

- Create new files only when the concept is meaningfully distinct from existing material.
- Prefer incremental updates that preserve history and traceability.
- Use explicit links to related folders and files instead of restating the same content.
- Use the following project-risk structure in `project_risk_register.json`:
  - `id`: format `RSK-XXXX`
  - `description`: risk and technical impact description
  - `type`: one of the approved risk types listed below
  - `status`: `open` or `closed`
  - `development_step`: one of `1`, `2`, `3`, `4.1`, `4.2`, `4.3`
  - `contingency_plan`: actions to put in place if the risk occurs
  - `owner`: person responsible
  - `comment`: append-only entries with date
  - `links`: array with zero or more links
  - `requirement_reference`: `REQ-*` or `UN-*` references
  - `strategy`: `M`, `A`, or `T`
  - `risk_reduction_actions`: array of mitigation actions
  - `occurrence`: `low`, `medium low`, `medium high`, or `high`
  - `severity`: `low`, `medium low`, `medium high`, or `high`
  - `budget_impact`: `low`, `medium low`, `medium high`, or `high`
  - `delay_impact`: `low`, `medium low`, `medium high`, or `high`

## Approved Risk Types

- `TECH: Requis/Requirements`
- `TECH: Qualite/Quality`
- `TECH: Technologie/Technology`
- `TECH: Performance`
- `TECH: Complexite/Complexity`
- `TECH: Interface`
- `TECH: PI/IP`
- `TECH: Sante-Securite/Health-Safety`
- `EXT: Client`
- `EXT: Fournisseur/Supplier`
- `EXT: Contrat/Contract`
- `EXT: Reglementation/Regulatory`
- `EXT: Marche/Market`
- `EXT: Climat/Climate`
- `ORG: Dependances prj/Prj dependencies`
- `ORG: Ressources`
- `ORG: Budget`
- `ORG: Priorisation/Prioritization`
- `PRJ: Planification/Planning`
- `PRJ: Echeancier/Schedule`
- `PRJ: Estime couts/Cost Estimate`
- `PRJ: Controle/Control`
- `PRJ: Communication`

## Update Rules

- When content changes here, check whether linked requirements, decisions, tests, or plans also need updates.
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.


