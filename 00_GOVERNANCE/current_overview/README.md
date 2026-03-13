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
- Review adjacent folders when a change affects related material: `00_GOVERNANCE/change_log`, `00_GOVERNANCE/workflows`, `07_PROJECT_EXECUTION`, `08_DECISIONS`, `09_COLLABORATION`, `10_COMMUNICATION`.
