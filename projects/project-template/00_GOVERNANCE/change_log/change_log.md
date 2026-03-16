# Change Log

- applied the single-canonical-JSON pattern to `01_PROJECT_FOUNDATION/objectives_success_metrics`, created `objectives_success_metrics.json`, restored the missing `assumptions_constraints.json`, and added `stakeholder_provenance` to both folder schemas and example artifacts (2026-03-15-00h50).
- clarified `01_PROJECT_FOUNDATION/assumptions_constraints` to use exactly one canonical JSON file, created `assumptions_constraints.json`, and updated the folder README to require create-or-update behavior for that single artifact (2026-03-15-00h35).
- simplified `01_PROJECT_FOUNDATION/assumptions_constraints/README.md` into a compact JSON-first folder contract with required fields, authoring rules, and an inline example artifact schema (2026-03-15-00h20).
- simplified the `project-template` top-level section `README.md` files to match the concise `00_GOVERNANCE/README.md` pattern and list only each section's direct child folders (2026-03-15-00h00).
- merged `projects/project-template/AGENTS.md` into the project `README.md`, simplified the top-level guidance, and removed the redundant sidecar agent file (2026-03-14-21h45).
- renamed the sole project context bank from `Maxwell` to `project-template`, renamed the workspace manifest to `projects_manifest.yaml`, and updated active navigation plus README references accordingly (2026-03-14-15h38).
- moved the Maxwell context bank under `projects/Maxwell/`, made `projects/README.md` a simple project-listing note, and updated root plus project navigation references for the new named-project folder layout (2026-03-14-16h30).
- added a shallow workspace-level `project_manifest.yaml` that lists the `projects` entrypoint and aligned the root README plus AGENTS guidance to route through it before opening project internals (2026-03-14-16h15).
- renamed the workspace project container from `project` to `projects` and aligned the workspace-level guidance and restructure plan to use the plural path consistently (2026-03-14-16h05).
- renamed the shared agent persona folder from `agent/persona` to `agent/personas` and aligned the workspace-level guidance to use the plural path consistently (2026-03-14-15h55).
- restructured the repository into a workspace root with `project/` and shared `agent/` folders, migrated governance workflows into `agent/skills`, added workspace-level entrypoint guides, and aligned the project manifest and governance references to the new layout (2026-03-14-15h45).
- merged each non-root folder's local `AGENTS.md` guidance into its `README.md`, removed the redundant sidecar agent files, and aligned repository conventions plus roadmap validation to the simplified README-only structure (2026-03-14-15h05).
- removed the repository-wide legacy sidecar memory pattern, deleted the related metadata folders, and aligned guidance to rely on `00_GOVERNANCE/change_log/change_log.md` plus the final git commit for traceability (2026-03-14-14h35).
- clarified that vendor-specific web evidence and COTS assessments belong in `06_RESEARCH_AND_REFERENCES/cots`, and updated both `cots` and `web_references` guidance plus local history notes to reflect that migration boundary (2026-03-12-08h43).
- updated `07_PROJECT_EXECUTION/milestones` to use a folder-level `milestones.md` board plus one JSON file per milestone, and aligned the local guidance and template to that execution pattern (2026-03-12-08h43).
- removed the dedicated research-note subsection from `06_RESEARCH_AND_REFERENCES`, deleted its obsolete artifacts, and aligned the section map and neighboring cross-links to the current structure (2026-03-12-00h20).
- added a standard weekly snapshot template to `00_GOVERNANCE/current_overview/AGENTS.md` so current-overview reports use a consistent health-check structure with evidence links and coherence checks (2026-03-12-00h10).
- clarified `00_GOVERNANCE/current_overview` as a weekly rolling snapshot area for project health, recent notable changes, focus, attention points, and information-coherence checks, with archival to `99_ARCHIVE/snapshots` after about two months (2026-03-12-00h05).
- made the governance workflows more discoverable from the root agent instructions by pointing directly to the workflows folder and the general update workflow (2026-03-11-20h42).
- clarified in the root agent instructions that every repository change must also be recorded in this governance change log (2026-03-11-20h42).
- added the general update workflow to standardize repo-wide context refresh, cross-link propagation, and commit-message anchoring for future runs (2026-03-11-18h00).
- updated change log convention to use a single append-only markdown file and removed local change-log history folders (2026-03-11-14h30).
# 2026-03-14

- Added a root-level `LLM_CURRENT_RECAP.md` file for low-token project routing.
- Updated `00_GOVERNANCE/current_overview/README.md` to require maintaining the compact LLM recap alongside weekly snapshots.
- Updated `README.md` so the recommended read order starts with the root-level LLM recap, then the project manifest, before deeper folder traversal.
- Replaced the standalone recap file with a `Current Overview Summary` section in the project `README.md` and updated governance guidance to treat that section as the low-token entrypoint.
