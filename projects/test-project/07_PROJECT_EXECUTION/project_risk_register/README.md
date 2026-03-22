# Project Risk Register

Keep project-level delivery risks here. The canonical artifact is `project_risk_register.json`.

## Risk Entry Shape

Each risk entry should include:

- `id`
- `description`
- `type`
- `status`
- `development_step`
- `contingency_plan`
- `owner`
- `comment`
- `links`
- `requirement_reference`
- `strategy`
- `risk_reduction_actions`
- `occurrence`
- `severity`
- `budget_impact`
- `delay_impact`

Keep `comment` append-only with dated notes. Keep `links` and `risk_reduction_actions` as arrays.

## Example

```json
[
  {
    "id": "RSK-0001",
    "description": "Critical supplier lead time could delay prototype integration.",
    "type": "EXT: Fournisseur/Supplier",
    "status": "open",
    "development_step": "2",
    "contingency_plan": "Approve backup supplier if the primary quote slips again.",
    "owner": "Program Management",
    "comment": [
      "2026-03-21: Waiting on updated delivery estimate."
    ],
    "links": [
      "../procurement/2026-04-sensor-vendor-downselect.md"
    ],
    "requirement_reference": "REQ-001",
    "strategy": "M",
    "risk_reduction_actions": [
      "Collect second-source quote"
    ],
    "occurrence": "medium high",
    "severity": "medium high",
    "budget_impact": "medium low",
    "delay_impact": "high"
  }
]
```

