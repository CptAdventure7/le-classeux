# Project Definition

Store the concise narrative that defines what the project is trying to accomplish and where the effort is bounded.

## Purpose

When this folder is populated, it should contain exactly one maintained artifact: `project_definition.md`.

That file should answer:
- what we are trying to accomplish
- what is in and out of scope for the current effort
- what is in and out of scope for the longer-term direction

Use this folder for:
- the core project narrative
- current-phase scope boundaries
- long-term scope boundaries
- short notes that clarify intent, exclusions, and ambition

Do not use this folder for:
- measurable objectives or KPIs better suited to `objectives_success_metrics`
- stakeholder inventories better suited to `stakeholders`
- assumptions or constraints better suited to `assumptions_constraints`
- duplicate strategy or requirement text copied from elsewhere

## Folder Rule

- Keep exactly one narrative file in this folder: `project_definition.md`.
- In the starter project template, do not keep a placeholder file with fake content.
- Create `project_definition.md` only when the project has real content to capture.
- If it already exists, update it in place.
- Do not split current and long-term scope into separate sibling artifacts unless a later decision explicitly requires it.

## Expected Shape

`project_definition.md` should stay short and reader-first. Recommended sections:
- `Purpose`
- `Current Effort In Scope`
- `Current Effort Out Of Scope`
- `Long-Term In Scope`
- `Long-Term Out Of Scope`

Optional sections:
- `Context`
- `Non-Goals`
- `Notes`
- `Related Links`

## Authoring Rules

- Prefer plain language over framework boilerplate.
- Keep the document focused on boundaries and intent, not implementation detail.
- Update related folders when the project definition changes the meaning of objectives, requirements, decisions, or validation work.
- Link to upstream sources and downstream consequences when they exist.
- Move superseded material to `99_ARCHIVE` rather than deleting traceability.

