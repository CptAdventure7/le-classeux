# Change Log

- moved the `07_PROJECT_EXECUTION/milestones` board example into the local README and removed the seeded `milestones.md` template file so the board is created only when a project actually starts tracking milestones (2026-03-21-23h12).

- moved the `07_PROJECT_EXECUTION/issues` Kanban reference example into the local README and removed the separate `kanban.md` template file so the folder guidance stays self-contained (2026-03-21-23h20).

- clarified `07_PROJECT_EXECUTION/procurement/README.md` so procurement records follow a one-folder-per-item pattern, with each item folder regrouping quotes, evaluations, approvals, and related execution links (2026-03-21-23h15).

- integrated the `07_PROJECT_EXECUTION/milestones/milestones.md` board guidance into `07_PROJECT_EXECUTION/milestones/README.md` and removed the inline milestone JSON example so the README is guidance-only (2026-03-21-23h09).

- added a simple `07_PROJECT_EXECUTION/issues/kanban.md` reference board that lists all active issues in one human-readable table, and renamed the issue template section from `Acceptance Criteria` to `Definition of Done` in the issues README (2026-03-21-23h05).

- merged `09_COLLABORATION` and `10_COMMUNICATION` into `09_COMMUNICATION`, renumbered `11_OPERATIONS_AND_HANDOFF` to `10_OPERATIONS_AND_HANDOFF`, and updated manifest plus roadmap/current-overview references to the new structure (2026-03-21-22h55).

- removed `99_ARCHIVE/retired_requirements` and `99_ARCHIVE/legacy_tests`, simplified the remaining `99_ARCHIVE` README files to short folder-level guidance, and aligned the archive manifest plus verification test with the slimmer archive structure (2026-03-21-22h40).

- renamed `99_ARCHIVE/snapshots` to `99_ARCHIVE/current_overview`, updated the archive manifest and cross-links, and clarified in governance that older weekly overviews should be retired into the new archive folder (2026-03-21-22h35).

- simplified all README files under `07_PROJECT_EXECUTION`, removed repeated boilerplate, kept folder guidance minimal, moved the milestone example into `milestones/README.md`, and removed the separate `milestone-template.json` sidecar template (2026-03-21-22h30).

- simplified all README files under `11_OPERATIONS_AND_HANDOFF` to remove repeated boilerplate and keep only short folder-level guidance for deployment, installation, user docs, maintenance, training, support notes, and release notes (2026-03-21-22h15).

- simplified all README files under `10_COMMUNICATION` to remove repeated boilerplate and keep only concise scope guidance for `internal_updates`, `external_updates`, and `reporting` (2026-03-21-00h15).

- simplified the `09_COLLABORATION` README files to remove repeated boilerplate, keep only simple folder-level guidance, and point `meetings/summaries` to the `meeting-summary` skill for summary structure (2026-03-21-00h10).

- simplified all README files under `06_RESEARCH_AND_REFERENCES` to remove repeated folder boilerplate and keep only concise scope guidance, with the main remaining distinction being `cots` for vendor-specific assessments versus `web_references` for general web research (2026-03-21-00h00).

- renamed `05_EXPERIMENTS_AND_VALIDATION` to `05_EXPERIMENT_AND_VERIFICATION`, removed the `nonconformities` template folder, and simplified the `05` README files to a minimal one-markdown-file-per-analysis, experiment, protocol, or result pattern with meaningful filenames and update-in-place guidance (2026-03-16-16h45).

- removed the `code_repositories`, `models_simulations`, `benchmarks`, `calibration`, `datasets`, `test_strategy`, `validation_plan`, `bibliography`, `literature_map`, `backlog`, `demos`, `customer_feedback`, and `visuals` template folders; deleted all `08_DECISIONS` subfolders; and aligned the manifest plus surviving README/example links to the slimmer structure (2026-03-16-15h10).

- simplified `04_DESIGN_AND_IMPLEMENTATION/design_reviews/README.md` to remove repeated boilerplate, defined a one-markdown-file-per-review pattern named `YYYY-MM-DD-<concise-meaningful-name>.md`, required the core review categories, and aligned `Action Items` with the meeting-summary JSON structure (2026-03-16-14h35).
- removed the separate `04_DESIGN_AND_IMPLEMENTATION/icd_interface_control_docs` section from the project template, updated related structure references, and clarified in `02_SYSTEM_DEFINITION/system_architecture/README.md` that interface control details belong inside architecture artifacts (2026-03-16-14h20).
- simplified `04_DESIGN_AND_IMPLEMENTATION/design/README.md` to remove repeated boilerplate, defined `system_design_info.md` as the main design artifact, and changed subsystem design records to a one-file-per-subsystem markdown pattern named `<subsystem_name>_design_info.md` that also carries implementation detail (2026-03-16-14h05).
- simplified `04_DESIGN_AND_IMPLEMENTATION/system_risk_register/README.md` to remove repeated boilerplate, moved the example into the README, defined `system_risk_register.json` as the single canonical artifact created only for real content, and removed the seeded example JSON file from the starter template (2026-03-16-13h55).
- simplified `01_PROJECT_FOUNDATION/business_case/README.md` to remove generic folder boilerplate, define `business_case.md` as the single canonical artifact, and focus the guidance on capturing a concise decision-ready business case (2026-03-16-13h45).
- clarified requirement lifecycle guidance so obsolete or non-relevant requirements stay in live requirement files as `Abandoned`, and `Accepted` requirements require explicit user confirmation before modification (2026-03-16-13h14).
- simplified `02_SYSTEM_DEFINITION/system_architecture/README.md` and `02_SYSTEM_DEFINITION/use_cases/README.md` to remove repeated boilerplate, defined `system_overview.md` as the primary architecture artifact with optional additional markdown views, required Mermaid diagrams in those artifacts, and constrained use cases to a single canonical `use_cases.md` file (2026-03-15-02h20).
- updated `03_REQUIREMENTS/subsystem_requirements/README.md` so subsystem requirement IDs now use `PRJ-<three-letter subsystem acronym>-<n>` instead of `PRJ-SUBREQ-<n>`, and aligned the example accordingly (2026-03-15-02h00).
- simplified the three `03_REQUIREMENTS/*_requirements/README.md` files to remove repeated boilerplate, clarified that JSON examples live in the READMEs, changed `subsystem_requirements` to a one-file-per-subsystem pattern named `<subsystem>_requirements.json`, and removed the placeholder requirement JSON files (2026-03-15-01h50).
- converted `01_PROJECT_FOUNDATION/glossary` and `01_PROJECT_FOUNDATION/stakeholders` to the same single-canonical-JSON folder contract used by `assumptions_constraints`, defining `glossary.json` and `stakeholders.json` schemas and removing repeated README boilerplate (2026-03-15-01h35).
- merged `01_PROJECT_FOUNDATION/project_brief` and `01_PROJECT_FOUNDATION/scope` into `01_PROJECT_FOUNDATION/project_definition`, simplified the merged README to a single-artifact contract around `project_definition.md`, and updated neighboring references accordingly (2026-03-15-01h20).
- removed placeholder JSON files from the starter template for `assumptions_constraints` and `objectives_success_metrics`, and clarified in both READMEs that the canonical JSON file is created only when real project content exists (2026-03-15-01h05).
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
