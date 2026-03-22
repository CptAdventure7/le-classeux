# test project

`test project` is an evidence-first project context bank for keeping project knowledge traceable, current, and easy to retrieve.

## Current Overview Summary

- Last updated: `2026-03-22`
- Current phase: `Instantiation`

`test project` is a newly instantiated evidence-first project context bank. Project context bank for testing the human dashboard implementation.

### Active Watchpoints

- replace template-era examples and placeholder language with project-specific evidence before adding downstream artefacts
- keep `00_GOVERNANCE/change_log/change_log.json` as the first durable memory record and update it with every repository change
- create execution items only when real delivery work exists; do not carry template sample data into live project tracking

## How To Work In This Project

- Start with the `Current Overview Summary` section in this README for the compact current-state summary and recommended next reads.
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
