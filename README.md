# Workspace Memory

This repository is the workspace root for one or more project context banks plus shared agent resources.

## Layout

- `project/`: the current project context bank, with its own `README.md`, `AGENTS.md`, and `project_manifest.yaml`.
- `agent/skills/`: reusable workflow skills that are not owned by a single project.
- `agent/personas/`: persona definitions for future agent specializations.
- `docs/plans/`: implementation and restructuring plans that explain larger repository changes.

## Working Instructions

- Start here, then choose the relevant project folder.
- For project work, read that project's `README.md`, `AGENTS.md`, and `project_manifest.yaml` before descending further.
- Use local `README.md` files inside the selected project for folder-level scope and authoring rules.
- Use `agent/skills/` for reusable workflows that apply across projects.
