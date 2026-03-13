# Reference Ingestion Workflow

## Purpose

Use this workflow to ingest a source document into the Maxwell context bank by extracting the relevant project information, updating the canonical repository artifacts that should absorb that information, creating a persistent local summary near the document's main topic area, and optionally generating a page-index JSON for future section-level consultation.

Upstream context:
- [AGENTS.md](../../AGENTS.md)
- [README.md](../../README.md)
- [README.md](../README.md)
- [README.md](./README.md)
- [project_manifest.yaml](../../project_manifest.yaml)

Repository evidence:
- [general-update-workflow.md](./general-update-workflow.md)
- [meeting-summary-workflow.md](./meeting-summary-workflow.md)

Downstream implications:
- Ingested content may update [03_REQUIREMENTS](../../03_REQUIREMENTS), [04_DESIGN_AND_IMPLEMENTATION](../../04_DESIGN_AND_IMPLEMENTATION), [05_EXPERIMENTS_AND_VALIDATION](../../05_EXPERIMENTS_AND_VALIDATION), [07_PROJECT_EXECUTION](../../07_PROJECT_EXECUTION), [08_DECISIONS](../../08_DECISIONS), [10_COMMUNICATION](../../10_COMMUNICATION), or [11_OPERATIONS_AND_HANDOFF](../../11_OPERATIONS_AND_HANDOFF).

## Trigger Conditions

Use this workflow when the user asks to:
- ingest a reference document into the bank
- consume a SharePoint document and integrate its information
- extract relevant information from a long PDF or other heavy document
- create a persistent summary and optionally map a document for future consultation

## Accepted Inputs

- A source document path or link, including SharePoint URLs.
- Common source formats such as `.pdf`, `.docx`, `.pptx`, `.md`, `.txt`, `.html`, or other readable office or text exports.
- A declared or inferable target topic area in the active context bank.

If the topic area is not given explicitly, the agent must infer the narrowest relevant folder from repository evidence before integrating anything.

## Core Repository Rule

The source document is evidence, not the canonical project record.

The workflow must:
- extract and interpret the source
- integrate durable facts into the appropriate canonical bank artifacts
- keep one persistent ingestion summary near the document's main topic area
- ask whether the user wants future consultation support through page indexing
- create the page-index JSON near the same topic area when the user approves it

The workflow must not keep temporary extraction artifacts after the run completes.

## Required Folder Selection

1. Identify the narrowest relevant active folder for the document's main topic.
2. Read that folder's local `README.md` before opening deeper files.
3. If the workflow will edit content in that folder, also read its local `AGENTS.md`.
4. Prefer active sections `00_GOVERNANCE` through `11_OPERATIONS_AND_HANDOFF` over `99_ARCHIVE`.
5. Keep the persistent summary and optional page-index JSON near that main topic area rather than in a centralized reference bucket.

## Persistent Outputs

### 1. Canonical downstream updates

Update existing canonical artifacts when the document introduces durable information such as:
- new or revised requirements
- design constraints or interfaces
- risks, issues, or execution impacts
- validation evidence or protocol-relevant findings
- decisions or decision-support evidence
- operational or communication impacts

### 2. Local ingestion summary

Create one persistent summary artifact near the document's main topic area when the information needs traceable local capture beyond the canonical updates.

The summary must record:
- source document title
- source location
- ingestion date
- document type
- key extracted facts
- what was integrated into canonical artifacts
- what was not integrated and why
- open questions or unresolved ambiguities
- whether page indexing was offered and whether it was accepted

### 3. Optional page-index JSON

If the user approves future consultation support, invoke the `pageindex-local-structure` skill and create a JSON tree near the same topic area as the summary artifact.

The JSON must include at minimum:
- `title`
- `source`
- `created_at`
- `topic_area`
- `document_type`
- `tree`

The `source` value must preserve a resolvable link to the original document. If the source lives in SharePoint, store the SharePoint URL in `source`.

## Naming Convention

The local summary and optional page-index JSON must sort side by side alphabetically.

Use this paired naming pattern:
- summary: `YYYY-MM-DD-<document-stem>-ingestion-summary.md`
- page index: `YYYY-MM-DD-<document-stem>-ingestion-summary.page-index.json`

This convention keeps both artifacts adjacent in directory listings while making the summary the primary human-readable entry point.

## Temporary Artifact Rule

Temporary extraction outputs are allowed only as working files during ingestion.

Examples include:
- OCR output
- extracted plain text
- temporary normalized markdown
- temporary analysis JSON

Before the workflow ends, delete those temporary artifacts. If deletion is impossible, move them into a local non-tracked disposal area only when such a disposal area already exists and is accepted by the local folder guidance. Do not leave temporary extraction files in the context bank as durable artifacts.

## Required Extraction Coverage

For heavy or lengthy documents, extract and evaluate at least:
- high-value claims or conclusions
- requirements-relevant statements
- design-relevant statements
- risks, assumptions, and constraints
- validation evidence, methods, or quantitative results
- decisions already made or candidate decisions implied by the source
- operational impacts
- unresolved questions or conflicts with existing repository evidence

When facts conflict with existing bank artifacts, apply repository source-priority rules and state the conflict explicitly instead of silently overwriting interpretation.

## User Decision Gate For Mapping

After the relevant information has been extracted and triaged, ask the user whether the document should be mapped for future consultation.

Use a direct question equivalent to:

`Do you want me to map this document for future consultation?`

If the user says:
- `yes`: invoke `pageindex-local-structure`, write the JSON tree, and link it from the summary
- `no`: finish the ingestion without mapping and record that mapping was declined

The agent must not silently create a page-index JSON without this explicit user approval.

## Workflow

1. Resolve the source document path or URL.
2. Identify the main topic area in the context bank.
3. Read the local `README.md` for that area before going deeper.
4. Read the local `AGENTS.md` for any folder that will be edited.
5. Extract the source content from the original file.
6. If the document is heavy or lengthy, reduce it to a structured working analysis focused on repository-relevant information.
7. Compare extracted facts against the current canonical artifacts in the topic area and any required adjacent sections.
8. Update canonical artifacts first when the source changes durable project context.
9. Create the local ingestion summary near the same topic area.
10. Ask whether the user wants the document mapped for future consultation.
11. If approved, invoke `pageindex-local-structure` and write the page-index JSON using the paired naming convention.
12. Link the summary and page-index JSON to each other when both exist.
13. Delete temporary extraction artifacts.
14. Add a `~history` note when the new workflow result changes how the folder's current contents should be interpreted.
15. Verify links, filenames, source traceability, and topic placement before completion.

## Cross-Link Expectations

The local ingestion summary should link to:
- the original source document location
- the canonical artifacts updated during ingestion
- the optional page-index JSON when it exists
- related decision, requirement, design, validation, or execution artifacts affected by the source

The page-index JSON should retain the original document link in `source` so future retrieval can always navigate back to the source file.

## Failure Modes To Avoid

- Treating the source document itself as the canonical record.
- Writing a disconnected summary while skipping required updates to canonical artifacts.
- Storing mapped JSON in a centralized folder when the topic area is clear.
- Leaving OCR or extraction working files in the repository after ingestion.
- Creating the page-index JSON without asking the user first.
- Using unrelated filenames that separate the summary and page-index files alphabetically.
- Replacing explicit source links with vague provenance text.
- Silently ignoring conflicts between the source and current bank artifacts.
