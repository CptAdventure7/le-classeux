# Current Overview

This folder belongs to the Maxwell context bank.

## What Belongs Here

Weekly rolling snapshots of current project health, current-state summaries, active priorities, and navigation pointers for new readers.

Each snapshot is the quick report for "where things stand now" and should help a reader answer:
- what happened recently that matters
- what is currently important
- what the present focus is
- what needs attention now
- whether the project information looks stable, stale, or internally inconsistent

Within a given week, update the same snapshot file in place. When a new week starts, create a new snapshot file for that week rather than extending the prior one indefinitely.

Recommended snapshot content:
- recent notable changes, events, or decisions
- current focus and next near-term priorities
- delivery health, including missed deliveries or slipping commitments
- stale issues, blocked work, or items lacking ownership
- information incoherences, conflicting statements, or outdated references
- a concise health-check assessment of information stability and project coherence

Lifecycle expectations:
- keep the active weekly snapshots here while they remain operationally relevant
- after about two months, move older snapshots to [99_ARCHIVE/snapshots](../../99_ARCHIVE/snapshots/README.md)
- preserve traceability by linking each snapshot to the upstream evidence it summarizes

## What Does Not Belong Here

- Unscoped notes that should live in a broader parent folder.
- Duplicate copies of documents that already exist elsewhere in the context bank.
- Final decisions without a link to the originating issue, requirement, or review.
- Long-form meeting notes, raw logs, or detailed plans that should remain in their canonical folders.
- Timeless reference material that belongs in requirements, decisions, risks, or workflows instead of a time-bounded snapshot.

## Cross-Links To Maintain

- Link to the immediate upstream context that justifies the artifact.
- Link to downstream evidence, implementation, or decision records affected by changes here.
- Link to the concrete sources behind the snapshot when available, especially issues, milestones, decisions, meeting summaries, risk registers, and internal updates.
- Review adjacent folders when a change affects related material: `00_GOVERNANCE/change_log`, `07_PROJECT_EXECUTION`, `08_DECISIONS`, `09_COLLABORATION`, `10_COMMUNICATION`.

## Detailed Authoring Guidance

The sections below capture the drafting, update, cross-linking, and any folder-specific formatting rules for this folder.

Read `README.md` in this folder before drafting or editing documents.

## Drafting Rules

- Create new files only when the concept is meaningfully distinct from existing material.
- Prefer incremental updates that preserve history and traceability.
- Use explicit links to related folders and files instead of restating the same content.
- Treat this folder as the project health-check layer, not as a replacement for canonical source artifacts.
- Maintain one rolling snapshot per week. Update that week's snapshot in place; start a new snapshot when a new week begins.
- Write snapshots as concise operational reporting focused on recent developments, current focus, urgent attention points, and information coherence.
- Call out missed deliveries, stale issues, unresolved blockers, and contradictory or stale information explicitly.
- Include a clear judgement on current information stability: what appears reliable, what looks stale, and what needs verification.
- When a snapshot ages past roughly two months, move it to `99_ARCHIVE/snapshots` instead of leaving this folder crowded with stale current-state reports.

## Update Rules

- When content changes here, check whether linked requirements, decisions, tests, or plans also need updates.
- Rely on linked artifacts, the governance change log, and the final git commit for traceability.
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.
- Prefer one dated weekly filename per snapshot, using the repository date convention when chronology matters.
- If a weekly snapshot is updated repeatedly, keep the file focused on the same reporting window instead of turning it into a multi-month running log.

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.
- When reporting health concerns, link directly to the artifact that shows the problem: stale issue list, slipped milestone, conflicting requirement, outdated communication, or missing decision record.

## Weekly Snapshot Template

Use the structure below for each weekly snapshot and keep it concise.

```md
# Current Overview - YYYY-MM-DD

## Reporting Window

- Week of `YYYY-MM-DD` to `YYYY-MM-DD`
- Last updated: `YYYY-MM-DD-HHhMM`

## Overall Health

- Overall status: `On track | Watch | At risk`
- Information stability: `Stable | Mixed | Unstable`
- Summary: 2-4 sentences on the current state, what changed recently, and how trustworthy/coherent the present picture is.

## What Happened Recently

- Notable event, change, or decision with link to source.
- Notable event, change, or decision with link to source.

## Current Focus

- Active priority and why it matters now.
- Active priority and who or what it depends on.

## Needs Attention

- Missed delivery, slipping commitment, or blocked item.
- Stale issue, ownership gap, or unresolved dependency.
- Contradiction, outdated information, or missing decision that now creates risk.

## Information Coherence Check

- Coherent areas: what appears aligned across requirements, design, execution, and communication.
- Incoherences: what conflicts, looks stale, or is unsupported.
- Verification needs: what should be checked or refreshed next.

## Recommended Immediate Actions

- Action, owner if known, and target timing.
- Action, owner if known, and target timing.

## Source Links

- [Artifact name](relative/path.md)
- [Artifact name](relative/path.md)
```

Template expectations:
- Keep the document as a quick health-check report, not a detailed status deck.
- Prefer evidence-backed bullets over opinion.
- If a section has no material change, say so explicitly instead of leaving it vague.
- If a risk or inconsistency is listed, include the source artifact that demonstrates it.
