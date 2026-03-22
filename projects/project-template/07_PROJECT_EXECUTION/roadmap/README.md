# Roadmap

Keep the project roadmap here. `roadmap.json` is the canonical artifact.

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
      "summary": "Finish the initial context-bank structure and align execution artifacts.",
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

