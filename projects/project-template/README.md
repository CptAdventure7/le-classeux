# project-template

`project-template` is an evidence-first project context bank for keeping project knowledge traceable, current, and easy to retrieve.

## How To Work In This Project

- Start with [`LLM_CURRENT_RECAP.md`](LLM_CURRENT_RECAP.md) for the compact current-state summary and recommended next reads.
- Then check `project_manifest.yaml` for the authoritative folder map.
- After that, move to the narrowest relevant folder and read that folder's local `README.md` before opening deeper artefacts.
- Prefer active working sections over `99_ARCHIVE`, and use archived material only for historical traceability.
- Treat dated filenames in `YYYY-MM-DD-*` form as freshness signals when comparing similar artefacts.
- If sources conflict, state the conflict explicitly and rely on linked evidence instead of guessing.

## Update Rules

- Update the existing artefact when possible instead of creating duplicate summaries.
- Keep links between upstream context, related requirements or decisions, and downstream evidence.
- Record every repository change in `00_GOVERNANCE/change_log/change_log.md`, keeping the newest entry at the top.
- When current state changes materially, refresh `LLM_CURRENT_RECAP.md` alongside the relevant governance snapshot so the root-level entrypoint stays accurate.

## More Detail

The authoritative folder map and section purposes live in `project_manifest.yaml`.


