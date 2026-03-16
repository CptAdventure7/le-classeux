# Roadmap

This folder belongs to the project-template context bank.

## What Belongs Here

Artifacts specifically related to Roadmap.

## What Does Not Belong Here

- Unscoped notes that should live in a broader parent folder.
- Duplicate copies of documents that already exist elsewhere in the context bank.
- Final decisions without a link to the originating issue, requirement, or review.

## Cross-Links To Maintain

- Link to the immediate upstream context that justifies the artifact.
- Link to downstream evidence, implementation, or decision records affected by changes here.
- Review adjacent folders when a change affects related material: `07_PROJECT_EXECUTION/work_packages`, `07_PROJECT_EXECUTION/issues`, `07_PROJECT_EXECUTION/milestones`, `07_PROJECT_EXECUTION/change_requests`.

## Detailed Authoring Guidance

The sections below capture the drafting, update, cross-linking, and any folder-specific formatting rules for this folder.

Read `README.md` in this folder before drafting or editing documents.

## Roadmap Format

- Store roadmap content in JSON format.
- Use `roadmap.json` as the canonical roadmap artifact in this folder unless a more specific dated artifact is required.
- Represent the roadmap as one object with these top-level keys: `roadmap_title`, `last_updated`, `source_links`, `items`.
- Use `source_links` as an array of relative paths to upstream or peer artifacts such as `../milestones`, `../work_packages`, `../issues`, or requirement and decision records.
- Use `last_updated` in `YYYY-MM-DD` format.
- Store `items` as an array of roadmap entries with these keys: `id`, `title`, `phase`, `status`, `owner`, `target_date`, `summary`, `dependencies`, `source_links`.
- Use stable roadmap IDs with the `RDM-` prefix.
- Keep `phase` values short and delivery-oriented, such as `Discovery`, `Build`, `Validation`, or `Launch`.
- Keep `status` values constrained to `planned`, `in_progress`, `blocked`, or `done`.
- Use `dependencies` as an array of roadmap item IDs or external artifact references.
- Use `target_date` in `YYYY-MM-DD` format.

## Example

```json
{
  "roadmap_title": "project-template Delivery Roadmap",
  "last_updated": "2026-03-11",
  "source_links": [
    "../milestones",
    "../work_packages",
    "../issues"
  ],
  "items": [
    {
      "id": "RDM-001",
      "title": "Baseline Context Bank Ready",
      "phase": "Build",
      "status": "in_progress",
      "owner": "Program Management",
      "target_date": "2026-04-15",
      "summary": "Finish the initial context-bank structure and align execution artifacts to the canonical templates.",
      "dependencies": [
        "../milestones",
        "../work_packages"
      ],
      "source_links": [
        "../milestones",
        "../issues"
      ]
    }
  ]
}
```

## Drafting Rules

- Create new files only when the concept is meaningfully distinct from existing material.
- Prefer incremental updates that preserve history and traceability.
- Use explicit links to related folders and files instead of restating the same content.

## Update Rules

- When content changes here, check whether linked requirements, decisions, tests, or plans also need updates.
- Rely on linked artifacts, the governance change log, and the final git commit for traceability.
- Record superseded material in `99_ARCHIVE` rather than deleting traceability.
- Keep titles and filenames aligned with the scope of the document.

## Cross-Linking

- Add links to upstream inputs, peer artifacts, and downstream consequences.
- If a document changes requirements, ensure the linked design, validation, and decision records stay consistent.
- If this folder stores summaries, link back to raw notes or source documents when available.

