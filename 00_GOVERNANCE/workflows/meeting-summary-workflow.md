# Meeting Summary Workflow

## Purpose

Use this workflow to turn meeting transcripts or notes into structured, traceable summaries with attendees, decisions, risks, open questions, action items, detailed topical coverage, and a named-entity inventory.

Upstream context:
- [AGENTS.md](../../AGENTS.md)
- [README.md](./README.md)
- [README.md](../../09_COLLABORATION/meetings/README.md)
- [README.md](../../09_COLLABORATION/meetings/summaries/README.md)

Repository evidence:
- [README.md](../../09_COLLABORATION/meetings/raw_notes/README.md)
- [README.md](../../09_COLLABORATION/meetings/summaries/README.md)
- [project_manifest.yaml](../../project_manifest.yaml)

Downstream implications:
- Meeting summaries may feed [08_DECISIONS/decisions_from_meetings](../../08_DECISIONS/decisions_from_meetings) when explicit decision capture is requested.

## Trigger Conditions

Use this workflow when the user asks to:
- summarize a meeting
- create meeting notes or meeting minutes
- extract action items from a transcript

## Accepted Inputs

- Meeting transcript in `.txt`, `.md`, `.docx`, `.pdf`, or other plain-text-compatible format.
- If a direct path is given, process that file.
- If no direct path is given, sequentially process transcripts in [09_COLLABORATION/meetings/raw_notes](../../09_COLLABORATION/meetings/raw_notes) that are not already normalized to the `meeting-transcript-YYYY-MM-DD-HHhMM.txt` naming convention.
- If the transcript is `.docx`, extract text first.
- If the transcript is `.pdf`, extract text first.
- If the format is unclear or unsupported, stop and ask the user for a text export.

## Repository Mapping For Maxwell

The provided guidance referenced `04_COLLABORATION`, but this repository uses `09_COLLABORATION`. Apply the workflow to the active repository structure:

- Raw transcript inputs belong in [09_COLLABORATION/meetings/raw_notes](../../09_COLLABORATION/meetings/raw_notes).
- Meeting summaries belong in [09_COLLABORATION/meetings/summaries](../../09_COLLABORATION/meetings/summaries).
- Meeting-derived decision logs belong in [08_DECISIONS/decisions_from_meetings](../../08_DECISIONS/decisions_from_meetings) when requested.

## Required Output Format

Conversation output must return only the summary content, with no preamble or label.

The output file must contain the sections below in this exact order. Use `Unknown` when information is missing. Use the language of the meeting for the summary content itself, typically French or English. Preserve accentuated characters correctly.

0. Title and date
1. Attendees
2. Highlights and decisions
3. Summary
4. Risks
5. Open Questions
6. Action Items JSON
7. Detailed description of the different topics discussed
8. Named entities and initiatives inventory

### Section Rules

**0) Title and date**
- First line: meeting title.
- Second line: meeting date in `YYYY-MM-DD-HHhMM` when known, otherwise `Unknown`.

**1) Attendees**
- Bullet list.
- Use `Unknown` if attendees cannot be determined.

**2) Highlights and decisions**
- Bullet list.
- Include both confirmed decisions and important discussion outcomes.
- Mark uncertainty when a point is implied rather than explicit.

**3) Summary**
- One plain-text paragraph.

**4) Risks**
- Bullet list, or `None`.

**5) Open Questions**
- Bullet list, or `None`.

**6) Action Items JSON**
- JSON array of objects.
- One task per object.
- Required keys:
  - `assignee`
  - `description`
  - `definition_of_done`
  - `time_horizon`
  - `status`
- Allowed `status` values:
  - `backlog`
  - `selected for developpement`
  - `in progress`
- If multiple actors share an action, split into separate objects.

**7) Detailed description of the different topics discussed**
- Organize by logical topic, not strict chronology.
- Preserve conceptual detail with enough fidelity that the original transcript is not needed for work understanding.
- Do not collapse distinct named initiatives into generic phrasing when names are available.

**8) Named entities and initiatives inventory**
- Exhaustive bullet list of all project, program, product, codename, person, organization, location, feature, and system names mentioned.
- Preserve uncertain spellings and add `(uncertain transcription)` when needed.
- Include aliases or variants when present.
- Include one short evidence anchor per item with speaker and timestamp when available.
- Include one short type and confidence note, for example `(type: project, confidence 70%)`.
- Group entities by type.

## Required Output File

- Always write a full summary text file that includes all sections exactly as emitted in the response.
- Default output path: [09_COLLABORATION/meetings/summaries](../../09_COLLABORATION/meetings/summaries) with a dated filename such as `YYYY-MM-DD-meeting-summary.md` unless the meeting timestamp supports a more specific filename.
- Link the summary back to the source transcript path when known.

## Extraction Rules

- Do not invent facts.
- If information is absent or weakly supported, use `Unknown`.
- Prefer coverage over polish.
- Keep uncertain items instead of deleting them.
- Normalize time horizons:
  - Use exact dates when present.
  - Otherwise preserve relative timing phrases or convert them relative to the processing date when operationally necessary.
  - If absent, use `Unknown`.

## Detail Depth Constraints

- The detailed description must be lossless with respect to work-relevant content.
- Preserve names, numbers, technical parameters, commitments, and references.
- Lossless coverage also applies to proper nouns and uncertain transcriptions.

## Completeness Gate

Before finalizing:

1. Build a temporary candidate list of named entities from transcript text.
2. Verify every candidate appears in either the detailed description or the named-entities inventory.
3. Add any missing candidate before finalizing.
4. If transcript quality is degraded due to OCR, noisy ASR, or encoding issues, keep uncertain entries with uncertainty tags instead of deleting them.

## Workflow

1. Read the transcript text.
2. If the file is not recognizable as a transcript, stop and return: `The file is not recognized as a trancript, stopping actions.`
3. Identify attendees from roll call, introductions, or explicit mentions.
4. Extract decisions, risks, open questions, and action items.
5. Build the exhaustive named-entity inventory from the transcript text.
6. Run the completeness gate.
7. Emit the summary in the required order and write the output file.
8. Normalize the source transcript location:
   - If a plain-text transcript exists, rename or save it as `meeting-transcript-YYYY-MM-DD-HHhMM.txt` inside [09_COLLABORATION/meetings/raw_notes](../../09_COLLABORATION/meetings/raw_notes).
   - If the source is `.docx` or `.pdf`, preserve the original source file and create the extracted working text with the same timestamped stem as `.txt`.
9. Delete intermediary files. If deletion is not possible, move them into a local `local_bin/` folder.

## Conflict Resolution Applied

The supplied guidance contained two conflicts. This workflow resolves them explicitly:

- Path conflict:
  - Provided guidance used `04_COLLABORATION`.
  - Repository evidence uses `09_COLLABORATION` and [08_DECISIONS/decisions_from_meetings](../../08_DECISIONS/decisions_from_meetings).
- Source-extension conflict:
  - One part of the guidance treated processed transcripts as `.txt`.
  - Another part instructed renaming the original transcript to `.md`.
  - This workflow standardizes normalized transcript text as `.txt` and preserves original binary source extensions for `.docx` and `.pdf`.

## Common Failure Modes To Avoid

- Producing a short detailed description that loses work-relevant information.
- Omitting names, numbers, technical parameters, or proper nouns.
- Mixing decisions with assumptions without marking uncertainty.
- Omitting explicitly mentioned initiatives, projects, systems, or codenames.
- Deleting uncertain names instead of preserving them with uncertainty tags.
