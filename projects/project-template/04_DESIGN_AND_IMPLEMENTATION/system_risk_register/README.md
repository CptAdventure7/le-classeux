# System Risk Register

Store system design and implementation risks here in a single canonical JSON artifact with minimal boilerplate.

## Purpose

When this folder is populated, it should contain exactly one maintained data artifact: `system_risk_register.json`.

That file captures the system risk register for the project.

Use this folder for:
- system-level hazards, failure modes, causes, harms, and affected subsystems
- candidate and applied control measures with residual-risk scoring
- traceability to requirements, reviews, designs, and related evidence

Do not use this folder for:
- project-management risks that belong in `07_PROJECT_EXECUTION/project_risk_register`
- duplicate summaries, parallel drafts, or separate example files
- final decisions without traceability to the design, review, or requirement context that supports them

## Folder Rule

- Keep exactly one JSON data file in this folder: `system_risk_register.json`.
- In the starter project template, do not keep a placeholder JSON file with fake seed content.
- Create `system_risk_register.json` only when the project has real system-risk content to record.
- If it already exists, update it in place.
- Do not create multiple system-risk files in this folder.

## Required JSON Shape

`system_risk_register.json` should contain a JSON object with:
- `schema_version`: version string for the register shape
- `notes`: optional array of register-wide guidance or scoring notes
- `risks`: array of system-risk entries

Each risk entry must include:
- `id`: format `SRSK-0001`
- `hazard_category`: hazard class or domain
- `function_or_subsystem_affected`: string or array; use `multiple` when one risk spans several subsystems
- `failure_mode`: concise statement of how the system can fail
- `potential_causes`: array; use `["multiple"]` only when specific causes are not yet decomposed
- `potential_harm_effects`: array of user, operator, property, mission, or other harms
- `severity`: integer `1` to `5`
- `occurrence`: integer `1` to `5`
- `possible_control_measures`: array of candidate controls not yet committed
- `applied_control_measures`: array of controls implemented or formally accepted for implementation
- `traceability_to_requirement`: array of `REQ-*` identifiers; use an empty array when no requirement link exists yet
- `control_measure_type`: one of `by_design`, `protective_measure`, or `labelling`
- `new_risk_introduced_by_control_measure`: `no` or an `SRSK-*` identifier
- `residual_risk_severity`: integer `1` to `5`
- `residual_risk_occurrence`: integer `1` to `5`
- `date_of_last_review`: ISO date `YYYY-MM-DD`
- `status`: `open`, `mitigated`, `accepted`, or `closed`
- `owner`: person or team responsible for review and updates
- `comments`: append-only dated entries
- `links`: array with zero or more related artifact links

## Example

```json
{
  "schema_version": "1.0",
  "notes": [
    "Higher numeric values represent higher risk."
  ],
  "risks": [
    {
      "id": "SRSK-0001",
      "hazard_category": "Controls",
      "function_or_subsystem_affected": [
        "Imaging",
        "Motion Control"
      ],
      "failure_mode": "The system can capture blurred images when motion settles too late.",
      "potential_causes": [
        "Trigger timing drift",
        "Stage acceleration beyond tuned limits"
      ],
      "potential_harm_effects": [
        "Invalid measurement result",
        "Operator rework"
      ],
      "severity": 3,
      "occurrence": 2,
      "possible_control_measures": [
        "Add capture timing margin analysis",
        "Limit acceleration profiles per recipe"
      ],
      "applied_control_measures": [
        "Recipe validation blocks unsupported acceleration settings"
      ],
      "traceability_to_requirement": [
        "REQ-042"
      ],
      "control_measure_type": "by_design",
      "new_risk_introduced_by_control_measure": "no",
      "residual_risk_severity": 2,
      "residual_risk_occurrence": 1,
      "date_of_last_review": "2026-03-16",
      "status": "mitigated",
      "owner": "Systems Engineering",
      "comments": [
        "2026-03-16: Initial risk captured from motion-imaging integration review."
      ],
      "links": [
        "projects/project-template/04_DESIGN_AND_IMPLEMENTATION/design/README.md"
      ]
    }
  ]
}
```

## Authoring Rules

- Prefer updating `system_risk_register.json` instead of creating new files.
- Treat larger numeric values in `severity`, `occurrence`, `residual_risk_severity`, and `residual_risk_occurrence` as higher risk.
- Prefer arrays for multi-value fields even when there is currently only one value.
- When a control introduces a new risk, create or link the downstream `SRSK-*` entry explicitly instead of embedding that new risk inside the parent record.
- Keep links to upstream inputs, peer artifacts, and downstream consequences current when the register changes.

