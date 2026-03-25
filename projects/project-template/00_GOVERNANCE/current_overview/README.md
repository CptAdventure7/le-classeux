# Current Overview

This folder belongs to the project-template context bank.

## What Belongs Here

Weekly rolling snapshots of current project health, current-state summaries, active priorities, and navigation pointers for new readers.

This folder also owns the compact LLM-facing recap published as the `Current Overview Summary` section in [`../../README.md`](../../README.md). That root-level section is the low-token entrypoint for agents and should be updated whenever the active weekly snapshot changes materially.
This folder also stores `runtime_scan_summary.json`, a metadata-only scan cache that summarizes which opted-in top-level sections appear populated without opening their contents. Keep it refreshed on demand or when it is older than 24 hours.

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
- the minimal facts needed to refresh the `Current Overview Summary` section in [`../../README.md`](../../README.md)

Lifecycle expectations:
- keep the active weekly snapshots here while they remain operationally relevant
- after about two months, retire older weekly overviews to [99_ARCHIVE/current_overview](../../99_ARCHIVE/current_overview/README.md)
- preserve traceability by linking each snapshot to the upstream evidence it summarizes
- Do not treat `99_ARCHIVE` as active scan scope in normal routing. It is history-only and should enter the agent path only for explicit historical or traceability queries.

## What Does Not Belong Here

- Unscoped notes that should live in a broader parent folder.
- Duplicate copies of documents that already exist elsewhere in the context bank.
- Final decisions without a link to the originating issue, requirement, or review.
- Long-form meeting notes, raw logs, or detailed plans that should remain in their canonical folders.
- Timeless reference material that belongs in requirements, decisions, risks, or workflows instead of a time-bounded snapshot.
- Detailed evidence dumps inside the root-level summary section; keep that artifact short and route readers to canonical sources instead.
- Manual interpretations of folder fullness inside `runtime_scan_summary.json`; that cache is for cheap metadata-only scan results, not human judgement.

## Cross-Links To Maintain

- Link to the immediate upstream context that justifies the artifact.
- Link to downstream evidence, implementation, or decision records affected by changes here.
- Link to the concrete sources behind the snapshot when available, especially issues, milestones, decisions, meeting summaries, risk registers, and internal updates.
- Review adjacent folders when a change affects related material: `00_GOVERNANCE/change_log`, `07_PROJECT_EXECUTION`, `08_DECISIONS`, `09_COMMUNICATION`, `10_OPERATIONS_AND_HANDOFF`.
- When `runtime_scan_summary.json` is refreshed, keep its configuration aligned with `project_manifest.yaml` and avoid adding `99_ARCHIVE` back into normal-mode scan scope.

## Drafting Rules

- Treat this folder as the project health-check layer, not as a replacement for canonical source artifacts.
- Maintain one rolling snapshot per week. Update that week's snapshot in place; start a new snapshot when a new week begins.
- Write snapshots as concise operational reporting focused on recent developments, current focus, urgent attention points, and information coherence.
- Call out missed deliveries, stale issues, unresolved blockers, and contradictory or stale information explicitly.
- Include a clear judgement on current information stability: what appears reliable, what looks stale, and what needs verification.
- When a snapshot ages past roughly two months, retire older weekly overviews to `99_ARCHIVE/current_overview` instead of leaving this folder crowded with stale current-state reports.
- After updating the active weekly snapshot, refresh the `Current Overview Summary` section in [`../../README.md`](../../README.md) in the same change if the project state, priorities, canonical next reads, or archive-avoidance guidance changed.
- Keep the root-level summary intentionally smaller than the weekly snapshot: prefer a 150-300 word limit, a few bullets, and direct links to the most useful next files instead of repeating narrative detail.
- Treat `runtime_scan_summary.json` as a mechanical routing aid. It should stay metadata-only, cheap to regenerate on Windows, and limited to the manifest-opted top-level sections with a maximum recursive scan depth of 3.

## Update Rules

- If a weekly snapshot is updated repeatedly, keep the file focused on the same reporting window instead of turning it into a multi-month running log.
- Treat the root-level summary section as a continuously updated index, not a dated log. It should always describe the current state only.

## Root-Level Summary Section

Maintain the `Current Overview Summary` section in [`../../README.md`](../../README.md) as the compact machine-facing project recap.

Required content:
- last-updated date
- current phase or operating mode
- 1 short paragraph on the active project state
- 3-7 canonical files or folders to open next
- stale or archival areas to avoid unless explicitly needed
- open risks, blockers, or verification needs only if currently active

Authoring rules:
- keep it terse and navigational
- do not restate full weekly snapshot sections
- prefer links over prose
- remove stale bullets instead of accumulating history
- optimize for first-read routing by an LLM with limited context budget

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
