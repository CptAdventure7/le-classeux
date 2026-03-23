# Roadmap

Keep the project roadmap here. `roadmap.json` is the canonical artifact.

The roadmap may span both the current contracted effort and clearly labeled longer-term vision phases. When it does, each item summary must distinguish committed scope from follow-on opportunity or strategic intent.

## Roadmap Shape

The roadmap object should contain:

- `roadmap_title`
- `last_updated`
- `source_links`
- `items`

Each item should include:

- `id`
- `title`
- `phase`
- `status`
- `owner`
- `target_date`
- `summary`
- `dependencies`
- `source_links`

Use `RDM-` IDs. Keep `status` to `planned`, `in_progress`, `blocked`, or `done`.
Use `YYYY-MM-DD` target dates for committed checkpoints and a clear `TBD - <context>` marker only when the item is an uncontracted vision phase.

## Example

```json
{
  "roadmap_title": "project-template Delivery Roadmap",
  "last_updated": "2026-03-11",
  "source_links": [
    "../execution_items"
  ],
  "items": [
    {
      "id": "RDM-001",
      "title": "Baseline Context Bank Ready",
      "phase": "Build",
      "status": "in_progress",
      "owner": "Program Management",
      "target_date": "2026-04-15",
      "summary": "Finish the initial context-bank structure and align execution artifacts.",
      "dependencies": [
        "../execution_items/EXEC-MILESTONE-001-baseline-context-bank-ready.json"
      ],
      "source_links": [
        "../execution_items/EXEC-ISSUE-001-execution-structure-simplification.json"
      ]
    }
  ]
}
```

