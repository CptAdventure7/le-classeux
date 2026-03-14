---
name: reference-ingestion
description: Ingest a source document into the selected project context bank by updating canonical artefacts, writing a local ingestion summary, and optionally mapping the document for future consultation.
---

# Reference Ingestion

## Overview

Use this skill to ingest a source document into the selected project context bank. Extract the relevant project information, update canonical artefacts, create a persistent local summary near the document's main topic area, and optionally generate a page-index JSON for future consultation.

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
- keep one persistent ingestion summary near the document's main topic area
- ask whether the user wants future consultation support through page indexing
- create the page-index JSON near the same topic area only when the user approves it

## Required Workflow

1. Resolve the source document path or URL.
2. Identify the narrowest relevant active folder in the selected project.
3. Read that folder's local `README.md` before going deeper.
4. Re-read the local `README.md` for any folder that will be edited.
5. Extract the source content from the original file.
6. Reduce heavy documents to repository-relevant working analysis when needed.
7. Compare extracted facts against current canonical artefacts in the topic area and adjacent impacted sections.
8. Update canonical artefacts first when the source changes durable project context.
9. Create one local ingestion summary near the same topic area.
10. Ask whether the document should be mapped for future consultation.
11. If approved, invoke the page-index workflow and write the paired JSON file next to the summary.
12. Delete temporary extraction artefacts before finishing.
13. Update `<project>/00_GOVERNANCE/change_log/change_log.md` when the ingestion changes repository state or guidance.
14. Verify links, filenames, source traceability, and topic placement.

## Naming Convention

Use paired filenames that sort together:

- Summary: `YYYY-MM-DD-<document-stem>-ingestion-summary.md`
- Page index: `YYYY-MM-DD-<document-stem>-ingestion-summary.page-index.json`

## Failure Modes To Avoid

- Treating the source document itself as the canonical record.
- Writing a disconnected summary while skipping canonical updates.
- Creating a page-index JSON without explicit user approval.
- Leaving OCR or extraction working files in the repository.
- Silently ignoring conflicts between the source and current project artefacts.
