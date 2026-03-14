# General Update Workflow

## Purpose

Use this workflow to perform a repository-wide context refresh. The agent must gather all new repository material since the most recent commit that explicitly recorded a prior general-update run, determine what that new material changes, update the canonical artifacts that are affected, add the required cross-links, record the run in the governance change log, and then commit the result with the standardized general-update commit message.

Upstream context:
- [AGENTS.md](../../AGENTS.md)
- [README.md](../../README.md)
- [README.md](./README.md)
- [project_manifest.yaml](../../project_manifest.yaml)

Repository evidence:
- [README.md](../../03_REQUIREMENTS/README.md)
- [README.md](../../04_DESIGN_AND_IMPLEMENTATION/system_risk_register/README.md)
- [README.md](../../07_PROJECT_EXECUTION/issues/README.md)
- [README.md](../../07_PROJECT_EXECUTION/project_risk_register/README.md)
- [README.md](../../08_DECISIONS/README.md)
- [README.md](../../10_COMMUNICATION/internal_updates/README.md)

Downstream implications:
- General updates may modify [00_GOVERNANCE/current_overview](../current_overview), [03_REQUIREMENTS](../../03_REQUIREMENTS), [04_DESIGN_AND_IMPLEMENTATION](../../04_DESIGN_AND_IMPLEMENTATION), [05_EXPERIMENTS_AND_VALIDATION](../../05_EXPERIMENTS_AND_VALIDATION), [07_PROJECT_EXECUTION](../../07_PROJECT_EXECUTION), [08_DECISIONS](../../08_DECISIONS), [10_COMMUNICATION](../../10_COMMUNICATION), and [11_OPERATIONS_AND_HANDOFF](../../11_OPERATIONS_AND_HANDOFF).

## Trigger Conditions

Use this workflow when the user asks to:
- run a general update
- refresh the repo context
- propagate recent repo changes across the context bank
- update requirements, risks, decisions, issues, and related artifacts based on new repository material

## Preconditions

- The working directory must be inside a git repository with accessible history.
- The agent must be able to read commit history and changed paths.
- The agent must treat `00_GOVERNANCE` through `11_OPERATIONS_AND_HANDOFF` as the active context bank and use `99_ARCHIVE` only for traceability.

If git metadata is unavailable, stop and report: `General update workflow cannot run because git history is unavailable in this workspace.`

## General-Update Anchor

The prior run anchor is the most recent commit whose subject line is exactly:

`chore(general-update): run repository-wide general update`

Find it with a subject-exact search, for example:

```powershell
git log --grep="^chore\\(general-update\\): run repository-wide general update$" --format="%H %s" -n 1
```

### First-Run Rule

If no prior general-update commit exists, treat the run as the first repository-wide baseline sweep. In that case:
- inspect the full current repository state under `00_GOVERNANCE` through `11_OPERATIONS_AND_HANDOFF`
- do not assume unchanged folders are irrelevant
- record `Previous-general-update: none` in the commit body

## What Counts As New Context

`All new context` means every repository change since the anchor that can alter how the active context bank should be read:

- added files
- modified files
- renamed or moved files
- deleted files that invalidate existing links or summaries
- uncommitted tracked or untracked working-tree changes present when the workflow is run

This includes governance notes, requirements, design content, validation evidence, execution artifacts, decisions, meeting outputs, communication material, and operational handoff content. It does not mean only files in a single folder or only files the user mentions.

## Required Evidence Collection

1. Resolve the git repository root.
2. Save the pre-commit HEAD hash for the run.
3. Find the previous general-update commit hash, if any.
4. Build the candidate path set from:
   - `git diff --name-status <anchor>..HEAD` when an anchor exists
   - the full active repository tree when no anchor exists
   - `git status --short` so working-tree changes are not skipped
5. Exclude `.git` internals and use `99_ARCHIVE` only when a changed active artifact points there or when traceability for retired material is required.
6. For each changed or newly relevant path, read the nearest local `README.md` before descending further.
7. For each folder that will be edited, also read its local `AGENTS.md`.
8. Prefer the newest dated artifact when two same-type artifacts conflict, unless source-priority rules resolve the conflict first.

## Required Review Scope

The workflow must review all active top-level sections for impact, even if many end in `no change required`:

- `00_GOVERNANCE`
- `01_PROJECT_FOUNDATION`
- `02_SYSTEM_DEFINITION`
- `03_REQUIREMENTS`
- `04_DESIGN_AND_IMPLEMENTATION`
- `05_EXPERIMENTS_AND_VALIDATION`
- `06_RESEARCH_AND_REFERENCES`
- `07_PROJECT_EXECUTION`
- `08_DECISIONS`
- `09_COLLABORATION`
- `10_COMMUNICATION`
- `11_OPERATIONS_AND_HANDOFF`

The agent must not silently skip a section because no obvious file changed there. The review can conclude that no update is needed, but that conclusion must come after checking for downstream impact from the changed evidence set.

## Propagation Rules

Apply these rules after collecting the new context:

1. Update the nearest canonical artifact first.
   - Use the folder-local canonical file when defined, such as `requirements.json`, `project_risk_register.json`, `kanban.md`, or a local append-only `change_log.md`.
2. Create a new artifact only when:
   - the local folder guidance clearly expects a separate artifact type, and
   - the new context introduces a meaningfully distinct concept that should not be merged into an existing file.
3. Add explicit links to:
   - upstream source material that introduced the new information
   - peer artifacts affected by the same change
   - downstream evidence, plans, decisions, or communication artifacts that now need to align
4. Record repository-level changes in `00_GOVERNANCE/change_log/change_log.md` when the refresh updates canonical artifacts or repository guidance.
5. Surface conflicts explicitly instead of silently choosing one interpretation when sources disagree.

## Cross-Section Update Expectations

Use the changed evidence to check these common propagation paths:

- Foundation or system-definition changes:
  - update scope, stakeholders, assumptions, use cases, architecture framing, and any affected requirements
- Requirement changes:
  - update design allocation, validation plans or results, issue tracking, and decision records
- Design or interface changes:
  - update design artifacts, system risks, validation plans, and issues
- Validation or experiment changes:
  - update compliance or verification references in requirements, open issues, risks, and communications
- Execution changes:
  - update roadmap, backlog, issues, milestones, change requests, and project risks
- Decision-worthy changes:
  - update or create decision records in `08_DECISIONS`
- Meeting-derived changes:
  - propagate decisions, risks, issues, and follow-up work out of collaboration artifacts
- Communication or handoff changes:
  - align internal updates, reporting, release notes, user documentation, and support or training notes

## Minimum Update Targets To Check Every Run

Every run must explicitly consider whether the evidence set requires changes in:

- [00_GOVERNANCE/current_overview](../current_overview)
- [03_REQUIREMENTS/user_requirements](../../03_REQUIREMENTS/user_requirements)
- [03_REQUIREMENTS/system_requirements](../../03_REQUIREMENTS/system_requirements)
- [03_REQUIREMENTS/subsystem_requirements](../../03_REQUIREMENTS/subsystem_requirements)
- [04_DESIGN_AND_IMPLEMENTATION/system_risk_register](../../04_DESIGN_AND_IMPLEMENTATION/system_risk_register)
- [07_PROJECT_EXECUTION/project_risk_register](../../07_PROJECT_EXECUTION/project_risk_register)
- [07_PROJECT_EXECUTION/issues](../../07_PROJECT_EXECUTION/issues)
- [08_DECISIONS](../../08_DECISIONS)
- [10_COMMUNICATION/internal_updates](../../10_COMMUNICATION/internal_updates)

If a target is unchanged, leave it unchanged. If it is affected, update it in the local canonical form rather than writing a disconnected summary somewhere else.

## Workflow

1. Confirm git history is available. Stop if it is not.
2. Read the root [README.md](../../README.md), [AGENTS.md](../../AGENTS.md), and [project_manifest.yaml](../../project_manifest.yaml).
3. Determine the previous general-update anchor commit using the exact standardized commit subject.
4. Capture the pre-commit HEAD hash for the current run.
5. Build the complete candidate evidence set from git diff, git status, and first-run full sweep rules.
6. Read the nearest local `README.md` for each changed or impacted folder before opening deeper files.
7. Read local `AGENTS.md` for each folder that will be edited.
8. Extract concrete new facts, changed facts, deleted context, and cross-link impacts from the evidence set.
9. Update the canonical artifacts required by those facts across the active sections.
10. Update append-only change logs where governance or decision logs need a new top entry.
11. Verify links, identifiers, and traceability after edits.
12. Commit the result with the exact standardized commit subject and explicit body fields below.

## Standardized Commit Message

The commit subject line must be exactly:

`chore(general-update): run repository-wide general update`

The commit body must include these explicit lines:

```text
Previous-general-update: <commit-hash|none>
Source-range: <anchor-or-none>..<pre-commit-head>
Run-timestamp: YYYY-MM-DD-HHhMM
```

Example:

```text
chore(general-update): run repository-wide general update

Previous-general-update: a1b2c3d4
Source-range: a1b2c3d4..9e8f7a6b
Run-timestamp: 2026-03-11-18h00
```

Future runs must use the exact subject line above when searching for the last general-update run.

## Failure Modes To Avoid

- Updating only the file the user mentioned and skipping downstream impacts.
- Treating `all new context` as only newly created files while ignoring modified or deleted files.
- Creating duplicate summaries instead of updating canonical artifacts.
- Changing requirements, risks, or decisions without updating linked design, validation, issues, or communication records.
- Skipping the governance change log update when the refresh changed repository state.
- Using a non-standardized commit subject that breaks future anchor detection.
- Running in a workspace copy without git history and pretending the anchor was checked.



