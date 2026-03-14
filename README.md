# Workspace Memory

This repository is the workspace root for one or more project context banks plus shared agent resources.

## Layout

- `projects/`: the current project context bank container, with each project keeping its own `README.md`, `AGENTS.md`, and `project_manifest.yaml`.
- `agent/skills/`: reusable workflow skills that are not owned by a single project.
- `agent/personas/`: persona definitions for future agent specializations.
- `docs/plans/`: implementation and restructuring plans that explain larger repository changes.
- `project_manifest.yaml`: shallow workspace manifest that lists the available project entrypoints.

## Working Instructions

- Start here, then choose the relevant project folder.
- Read the root `project_manifest.yaml` to identify the available project entrypoint.
- For project work, read that project's `README.md`, `AGENTS.md`, and `project_manifest.yaml` before descending further.
- Use local `README.md` files inside the selected project for folder-level scope and authoring rules.
- Use `agent/skills/` for reusable workflows that apply across projects.
