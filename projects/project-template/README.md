# project-template

`project-template` is a reusable project context-bank scaffold for keeping project knowledge traceable, current, and easy to retrieve.

## Purpose

- Keep requirements, decisions, design context, execution artefacts, and verification evidence in one place.
- Use this root README as a lightweight entrypoint only.
- Rely on local folder `README.md` files and shared `agent/skills/` workflows for detailed guidance.

## How To Navigate

- Start with `project_manifest.yaml` for the authoritative top-level structure.
- Use the shared `project-navigation` skill at `../../agent/skills/project-navigation/SKILL.md` when you need low-token routing into the project.
- Move to the narrowest relevant folder before reading deeper artefacts.
- Read that folder's local `README.md` before creating or editing files there.
- Prefer active sections over `99_ARCHIVE` unless you need historical traceability.
- If sources conflict, state the conflict explicitly and rely on linked evidence instead of guessing.

## Broad Maintenance Rules

- Update existing canonical artefacts when possible instead of creating parallel summaries.
- Keep traceability between source material, requirements, decisions, execution items, and verification evidence.
- Record every repository change in `00_GOVERNANCE/change_log/change_log.json`, keeping the newest entry first.
- Refresh this README only when the broad entrypoint guidance changes.
