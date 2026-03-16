# Design

Detailed design and implementation information lives here as markdown artifacts.

## Canonical Artifacts

- Create one system-level file when real content exists: `system_design_info.md`.
- Create at most one additional markdown file per stable subsystem.
- Name each subsystem file `<subsystem_name>_design_info.md`.
- Keep the design and implementation detail for a given scope in that single file instead of splitting it across multiple sibling documents.
- Do not keep placeholder files in the starter template.

## Authoring Rules

- Start with `system_design_info.md` for the full-system view, then add subsystem files only when the subsystem boundary is clear and the detail would make the system file harder to use.
- Update the existing scope file instead of creating another document for the same subsystem.
- Each design info file should capture the architecture or design choices for that scope, the implementation approach or status that matters for traceability, and links to the related requirements, interfaces, code, validation, risks, and decisions.
- Use concise headings and remove filler; these files should be working design records, not generic templates.
- Move superseded material to `99_ARCHIVE` rather than deleting traceability.

## Example Filenames

- `system_design_info.md`
- `sensor_stack_design_info.md`
- `control_loop_design_info.md`
