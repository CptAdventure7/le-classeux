---
name: meeting-summary
description: Convert meeting transcripts or notes into structured, traceable summaries inside the selected project's communication section.
---

# Meeting Summary

## Overview

Use this skill to turn meeting transcripts or notes into structured, traceable summaries with attendees, decisions, risks, open questions, action items, detailed topical coverage, and a named-entity inventory for the selected project.

## Trigger Conditions

Use this skill when the user asks to:
- summarize a meeting
- create meeting notes or meeting minutes
- extract action items from a transcript

## Project Mapping

For the selected project root:

- Raw transcript inputs belong in `<project>/09_COMMUNICATION/meetings/raw_notes`
- Meeting summaries belong in `<project>/09_COMMUNICATION/meetings/summaries`
- Meeting-derived decisions belong in `<project>/08_DECISIONS/decisions.json` when explicit decision capture is requested; update the single canonical JSON file in place

## Required Output Sections

The output file must contain these sections in order:

0. Title and date
1. Attendees
2. Highlights and decisions
3. Summary
4. Risks
5. Open Questions
6. Action Items JSON
7. Detailed description of the different topics discussed
8. Named entities and initiatives inventory

Use `Unknown` when information is missing. Do not invent facts.

## Required Workflow

1. Read the transcript text.
2. If the source is not a recognizable transcript, stop and report that the file is not recognized as a transcript.
3. Identify attendees from explicit mentions.
4. Extract decisions, risks, open questions, and action items.
5. Build an exhaustive named-entity inventory.
6. Verify all candidate entities appear in the detailed description or inventory.
7. Write the summary into `<project>/09_COMMUNICATION/meetings/summaries` with a dated filename.
8. If explicit decision capture is requested, create or update `<project>/08_DECISIONS/decisions.json` instead of creating per-meeting decision files or side folders.
9. Normalize or preserve the source transcript under `<project>/09_COMMUNICATION/meetings/raw_notes` as needed.
10. Delete intermediary extraction files, or move them to a local disposal area only if project guidance already allows that.

## Failure Modes To Avoid

- Producing a short summary that loses work-relevant content.
- Omitting names, numbers, technical parameters, or proper nouns.
- Mixing assumptions with explicit decisions without marking uncertainty.
- Dropping uncertain names instead of preserving them with uncertainty tags.
