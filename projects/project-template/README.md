# project-template

`project-template` is an evidence-first project context bank for keeping project knowledge traceable, current, and easy to retrieve.

## Current Overview Summary

- Last updated: `2026-03-25`
- Current phase: `Template / low-token routing refinement`

`project-template` is a context-bank scaffold optimized for traceable project memory. The current focus is keeping routing cheap for simple projects by pairing the manifest with a cached metadata-only `runtime_scan_summary.json` so agents can skip scaffold-only top-level sections without opening empty branches.

### Active Watchpoints

- keep root-level routing concise so agents do not spend tokens on repeated folder boilerplate
- keep the runtime scan cache metadata-only, top-level only, and bounded to the manifest-opted sections with a 24-hour refresh window
- keep `99_ARCHIVE` out of the normal runtime scan baseline unless the query is explicitly historical
- keep `05_EXPERIMENT_AND_VERIFICATION` on a simple one-file-per-analysis, experiment, protocol, or result pattern
- keep `07_PROJECT_EXECUTION` centered on one canonical execution-item pattern with a folder-local manifest and no parallel board concepts
- update this section whenever the active overview, priorities, or best next reads change

## How To Work In This Project

- Start with the `Current Overview Summary` section in this README for the compact current-state summary and recommended next reads.
- For low-token routing, use the local `project-navigation` skill at `agent/skills/project-navigation/SKILL.md` before opening many section folders.
- Then check `project_manifest.yaml` for the authoritative folder map.
- After that, move to the narrowest relevant folder and read that folder's local `README.md` before opening deeper artefacts.
- Prefer active working sections over `99_ARCHIVE`, and use archived material only for historical traceability.
- Treat dated filenames in `YYYY-MM-DD-*` form as freshness signals when comparing similar artefacts.
- If sources conflict, state the conflict explicitly and rely on linked evidence instead of guessing.
- Avoid deep folder-by-folder README traversal before checking this summary and the manifest

## Update Rules

- Update the existing artefact when possible instead of creating duplicate summaries.
- Keep links between upstream context, related requirements or decisions, and downstream evidence.
- Record every repository change in `00_GOVERNANCE/change_log/change_log.json`, keeping the newest entry at the top of the JSON array.
- When current state changes materially, refresh the `Current Overview Summary` section in this README alongside the relevant governance snapshot so the root-level entrypoint stays accurate.
