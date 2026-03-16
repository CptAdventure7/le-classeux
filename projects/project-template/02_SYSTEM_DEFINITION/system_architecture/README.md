# System Architecture

Store the system architecture views here as markdown artifacts with Mermaid diagrams.

## Purpose

Start with one general-view artifact for the full system:
- `system_overview.md`

That file should explain the main system boundary, the major parts, and how the pieces relate at a high level.

Add more `.md` artifacts only when they provide a clearly different view that the overview should not absorb, such as:
- a subsystem-specific architecture view
- a deployment or integration view
- a data-flow or interface-focused view

## Folder Rule

- Keep architecture artifacts in `.md` files only.
- Create `system_overview.md` first when real project content exists.
- Update the overview in place instead of splitting it too early.
- Treat interface definitions and interface control details as architecture artifacts in this folder.
- Add additional markdown artifacts only for stable subsystem or specific-view needs.
- Name additional files for the view they represent, for example `sensor_subsystem_architecture.md` or `external_interfaces_view.md`.
- Do not keep placeholder artifacts with fake content in the starter template.

## Required Content

Every architecture artifact in this folder must include:
- concise narrative text for the view it captures
- at least one Mermaid diagram as part of the artifact
- links to the related upstream use cases, requirements, or decisions when they exist

`system_overview.md` should usually cover:
- system purpose or scope boundary
- major subsystems or components
- principal external actors or systems
- the most important interfaces or flows

## Authoring Rules

- Prefer the general system view unless a narrower view materially improves clarity.
- Keep each artifact focused on one architecture viewpoint.
- Use Mermaid as the default visual representation rather than external images.
- When a view changes the architecture meaningfully, update linked use cases, requirements, design artifacts, or decisions as needed.
- Move superseded material to `99_ARCHIVE` rather than deleting traceability.

