---
name: general-update
description: Run a repository-wide project context refresh for the selected project, propagate durable changes into canonical artefacts, update the project governance log, and commit with the standardized general-update message.
---

# General Update

## Overview

Use this skill to perform a project-wide context refresh inside the selected project folder. Gather all new repository material since the most recent general-update commit, determine what changed, update the affected canonical artefacts, add the required cross-links, record the run in the project's governance change log, and commit with the standardized general-update message.

## Trigger Conditions

Use this skill when the user asks to:
- run a general update
- refresh the project context
- propagate recent repository changes across the context bank
- update requirements, risks, decisions, issues, or related artefacts from new project material

## Required Inputs

- The active project root, for example `project/`
- Accessible git history for the repository

If git metadata is unavailable, stop and report that the general update workflow cannot run because git history is unavailable in this workspace.

## Required Workflow

1. Resolve the selected project root.
2. Read `<project>/README.md`, `<project>/AGENTS.md`, and `<project>/project_manifest.yaml`.
3. Find the previous general-update anchor commit whose subject is exactly `chore(general-update): run repository-wide general update`.
4. Capture the pre-commit `HEAD` hash for the run.
5. Build the candidate evidence set from:
   - `git diff --name-status <anchor>..HEAD` when an anchor exists
   - the full active project tree when no anchor exists
   - `git status --short` so working-tree changes are included
6. For each changed or impacted path, read the nearest local `README.md` before going deeper.
7. Review all active top-level project sections for downstream impact, even if many conclude with no change.
8. Update the nearest canonical artefacts first.
9. Add explicit upstream, peer, and downstream links where the new context changes interpretation.
10. Record repository-level changes in `<project>/00_GOVERNANCE/change_log/change_log.md`.
11. Verify links, identifiers, and traceability after edits.
12. Commit with the exact standardized message below.

## Commit Message

The commit subject must be exactly:

`chore(general-update): run repository-wide general update`

The commit body must include:

```text
Previous-general-update: <commit-hash|none>
Source-range: <anchor-or-none>..<pre-commit-head>
Run-timestamp: YYYY-MM-DD-HHhMM
```

## Failure Modes To Avoid

- Updating only the file the user mentioned and skipping downstream impact.
- Treating only new files as new context while ignoring modified or deleted files.
- Creating disconnected summaries instead of updating canonical artefacts.
- Skipping the project governance change log update.
- Using a non-standardized commit subject that breaks future anchor detection.
