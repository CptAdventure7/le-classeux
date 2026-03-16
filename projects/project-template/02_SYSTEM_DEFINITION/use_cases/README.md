# Use Cases

Store the system use cases here in one markdown artifact.

## Purpose

When this folder is populated, it should contain exactly one maintained artifact:
- `use_cases.md`

That file should capture the current set of user or external-system interactions that define what the system needs to support.

## Folder Rule

- Keep exactly one `.md` file in this folder: `use_cases.md`.
- Create `use_cases.md` only when the project has real content to capture.
- If it already exists, update it in place.
- Do not split use cases across multiple sibling files in this folder.
- Do not keep placeholder artifacts with fake content in the starter template.

## Expected Content

`use_cases.md` should usually include:
- a short scope statement for the use-case set
- the main actors
- the use cases themselves, each with a stable title or identifier
- links to related requirements, architecture views, or decisions when they exist
- at least one Mermaid diagram that summarizes the actors, interactions, or major flows

## Authoring Rules

- Keep the full use-case set together so readers can understand coverage in one pass.
- Prefer concise use-case descriptions over long scenario prose unless detail is necessary.
- Update linked architecture, requirements, validation, or decision artifacts when the use-case set changes materially.
- Move superseded material to `99_ARCHIVE` rather than deleting traceability.

