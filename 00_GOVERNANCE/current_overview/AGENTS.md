# Agent Instructions

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
- Add a new note under `~history/` when fresh information affects how this folder's current documents should be read.
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
