# Glossary

Store glossary entries here in a single canonical JSON artifact with minimal boilerplate.

## Purpose

When this folder is populated, it should contain exactly one maintained data artifact: `glossary.json`.

That file captures the project vocabulary that needs stable shared definitions.

Use this folder for:
- project-specific terms
- acronyms or abbreviations that need expansion
- domain language that readers may interpret inconsistently

Do not use this folder for:
- long narrative explanations better suited to `project_definition`
- stakeholder information that belongs in `stakeholders`
- duplicate definitions copied from other artifacts without source traceability

## Folder Rule

- Keep exactly one JSON data file in this folder: `glossary.json`.
- In the starter project template, do not keep a placeholder JSON file with fake seed content.
- Create `glossary.json` only when the project has real terms to record.
- If it already exists, update it in place.
- Do not create multiple glossary files in this folder.

## Required JSON Shape

`glossary.json` should contain a JSON array.

Each array item must include:
- `term`: the word, phrase, or acronym being defined
- `definition`: the concise project-relevant meaning
- `source`: where the definition came from

Recommended fields:
- `id`: stable identifier
- `notes`: short clarification if needed
- `aliases`: alternate spellings or synonymous labels
- `related_links`: links to artifacts where the term is used or justified

## Example

```json
[
  {
    "id": "TERM-001",
    "term": "Context bank",
    "definition": "The structured project repository used to store evidence, decisions, requirements, and other traceable project knowledge.",
    "source": "projects/test-project/README.md",
    "related_links": [
      "projects/test-project/project_manifest.yaml",
      "projects/test-project/01_PROJECT_FOUNDATION/project_definition/README.md"
    ]
  }
]
```

## Authoring Rules

- Prefer updating `glossary.json` instead of creating new files.
- Keep definitions concise and specific to the project context.
- Make `source` specific enough that another reader can trace it.
- If a term changes project interpretation, update the affected upstream and downstream artifacts as well.
- Move superseded material to `99_ARCHIVE` rather than deleting traceability.

