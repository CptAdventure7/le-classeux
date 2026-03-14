# Change Log

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
