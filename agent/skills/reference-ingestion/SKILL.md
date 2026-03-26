---
name: reference-ingestion
description: Use when ingesting an external source document into a selected project context bank and keeping the repository outputs to markdown summaries plus optional JSON page indexes.
---

# Reference Ingestion

## Overview

Use this skill to ingest a source document into the selected project context bank. Extract the relevant project information, update canonical artefacts, create a persistent local summary near the document's main topic area, and optionally generate a page-index JSON for future consultation. Source files such as Word, DOCX, and PDF documents remain external evidence referenced by path or URL; the repository keeps only the derived `.md` summary and optional `.json` page index.

## Trigger Conditions

Use this skill when the user asks to:
- ingest a reference document into the bank
- consume a SharePoint document and integrate its information
- extract relevant information from a long PDF or other heavy document
- create a persistent summary and optionally map a document for future consultation

## Core Rule

The source document is evidence, not the canonical project record.

The workflow must:
- extract and interpret the source
- integrate durable facts into the appropriate canonical project artefacts
- keep one persistent markdown ingestion summary near the document's main topic area
- ask whether the user wants future consultation support through page indexing
- create the page-index JSON near the same topic area only when the user approves it
- keep repository artefacts to markdown and JSON only
- never copy or preserve source Word, DOCX, or PDF files inside the repository as ingestion outputs

## Required Workflow

1. Resolve the source document path or URL.
2. Identify the narrowest relevant active folder in the selected project.
3. Read that folder's local `README.md` before going deeper.
4. Re-read the local `README.md` for any folder that will be edited.
5. Extract the source content from the original file without copying the source Word, DOCX, or PDF into the repository.
6. Reduce heavy documents to repository-relevant working analysis when needed, but keep that working analysis temporary unless it becomes the final markdown summary or approved page-index JSON.
7. Compare extracted facts against current canonical artefacts in the topic area and adjacent impacted sections.
8. Update canonical artefacts first when the source changes durable project context.
9. Create one local markdown ingestion summary near the same topic area.
10. Ask whether the document should be mapped for future consultation.
11. If approved, invoke the page-index workflow and write the paired JSON file next to the summary.
12. Delete temporary extraction artefacts and any intermediate Word/PDF copies before finishing.
13. Update `<project>/00_GOVERNANCE/change_log/change_log.json` when the ingestion changes repository state or guidance.
14. Verify links, filenames, source traceability, and topic placement.

## Naming Convention

Use paired filenames that sort together:

- Summary: `YYYY-MM-DD-<document-stem>-ingestion-summary.md`
- Page index: `YYYY-MM-DD-<document-stem>-ingestion-summary.page-index.json`

These are the only repository artefacts this workflow should leave behind.

## Failure Modes To Avoid

- Treating the source document itself as the canonical record.
- Writing a disconnected summary while skipping canonical updates.
- Creating a page-index JSON without explicit user approval.
- Copying or preserving source Word, DOCX, or PDF files inside the repository.
- Leaving repository-side ingestion artefacts in formats other than `.md` and `.json`.
- Leaving OCR or extraction working files in the repository.
- Silently ignoring conflicts between the source and current project artefacts.
