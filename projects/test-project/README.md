# test project

`test project` is an evidence-first project context bank for keeping project knowledge traceable, current, and easy to retrieve.

## Current Overview Summary

- Last updated: `2026-03-22`
- Current phase: `Dashboard seed data`

`test project` now contains one short dummy artifact in every leaf content folder so the human dashboard can exercise section routing, Markdown rendering, and canonical JSON views without relying on real project history.

### Canonical Next Reads

- [Weekly dashboard seed overview](00_GOVERNANCE/current_overview/2026-03-22-dashboard-seed-overview.md)
- [Execution seed issue](07_PROJECT_EXECUTION/execution_items/EXEC-ISSUE-001-dashboard-seed-validation.json)
- [Roadmap seed](07_PROJECT_EXECUTION/roadmap/roadmap.json)
- [Project risk seed](07_PROJECT_EXECUTION/project_risk_register/project_risk_register.json)
- [Decision log seed](08_DECISIONS/decisions.json)

### Active Watchpoints

- keep all seeded artifacts clearly labeled as dummy data
- update local manifests whenever seeded files move or are removed
- avoid relying on archive content unless the dashboard is explicitly testing archived sections

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
