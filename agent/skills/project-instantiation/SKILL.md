---
name: project-instantiation
description: Use when creating a new project under `projects/` from the shared `projects/project-template` scaffold, including registration in `projects_manifest.yaml`, governance bootstrap, template-data reset, and initial verification of the new context bank.
---

# Project Instantiation

## Overview

Instantiate new projects from `projects/project-template` without inheriting the template's working history. The template is structural source material, not live project state, so identity, governance history, and seeded execution samples must be rewritten or removed during bootstrap.

## Required Inputs

- project slug in lowercase hyphen-case
- project display name
- one-sentence project purpose for `projects_manifest.yaml`

## Required Workflow

1. Read `projects_manifest.yaml`, `README.md`, `projects/project-template/README.md`, and `projects/project-template/project_manifest.yaml`.
2. Treat a missing `projects/project-template/AGENTS.md` as expected. This workspace merged project-side agent guidance into `README.md`; do not invent a new sidecar agent file unless the workspace policy changes.
3. Run:

```bash
python agent/skills/project-instantiation/scripts/instantiate_project.py \
  --workspace-root . \
  --project-slug <project-slug> \
  --project-name "<Project Name>" \
  --purpose "<one-sentence purpose>"
```

4. Inspect the new project and confirm the bootstrap did all of the following:
   - created `projects/<project-slug>/`
   - updated `project_manifest.yaml` with the new name and slug
   - rewrote the root project README summary for a fresh instantiation state
   - reset `00_GOVERNANCE/change_log/change_log.json` to one instantiation entry
   - removed seeded `EXEC-*.json` sample files from `07_PROJECT_EXECUTION/execution_items`
   - rewrote `07_PROJECT_EXECUTION/execution_items/local_manifest.yaml`
   - appended the project to `projects_manifest.yaml`
5. Search the new project for stale `project-template` identifiers. The only acceptable remaining reference is the provenance mention inside the new project's first change-log entry.
6. Add project-specific seed artifacts only after the clean bootstrap is complete, then log those extra edits in the new project's change log.

## Quick Reference

| Need | Action |
| --- | --- |
| New project folder | Copy from `projects/project-template` through the helper script, not by manual file explorer duplication |
| Workspace registration | Verify the appended entry in `projects_manifest.yaml` |
| Governance bootstrap | Keep exactly one initial entry in `00_GOVERNANCE/change_log/change_log.json` |
| Execution cleanup | Remove template `EXEC-*.json` samples and keep only `README.md` plus `local_manifest.yaml` in the local manifest |
| Identity cleanup | Replace template slug, README summary, and manifest values before adding real project content |

## Example

User request: "Instantiate a new project called Alpha Lab from the local template and register it in the workspace manifest."

Response pattern:
- collect the slug, display name, and one-sentence purpose if they were not supplied
- run the helper script
- inspect the new project diff
- report any remaining template-era content before proceeding with further edits

## Common Mistakes

- Copying the template folder manually and forgetting to update `projects_manifest.yaml`.
- Preserving the template's governance history instead of resetting the new project's `change_log.json`.
- Leaving sample execution-item JSON files in the new project.
- Reintroducing a project-level `AGENTS.md` even though this workspace now keeps project guidance in `README.md`.
- Treating template examples as live project artifacts instead of replacing them with real project evidence.
