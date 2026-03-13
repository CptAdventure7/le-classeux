# Agent Instructions

Read `README.md` in this folder before drafting or browsing history entries.

## Entry Creation

- Create a new file for each update using `AAAA-MM-DD-HHhMM.json`.
- Write a JSON object, not markdown prose.
- Include keys for `new_information`, `impact_on_existing_information`, `source_type`, `source_links`, and `time`.
- Treat history entries as append-only notes that explain change, not as replacements for the parent folder's main documents.

## Example Output

File: `2026-03-11-14h30.json`

```json
{
  "new_information": "The validation plan now requires thermal cycling before final performance measurement.",
  "impact_on_existing_information": "This changes the interpretation of the current test sequence in the parent folder. Any protocol or result summary that assumes room-temperature-only testing must be updated or cross-linked to this note.",
  "source_type": "meeting_decision",
  "source_links": [
    "../validation_plan/2026-03-11-thermal-cycling-update.md",
    "../meetings/2026-03-11-validation-review.md"
  ],
  "time": "2026-03-11-14h30"
}
```

## Browsing Rules

- Browse history only when there is strong evidence that historical change context is linked to the request.
- Prefer the parent folder's current documents first; consult history only to resolve conflicts, provenance, or evolution.
- When history changes the interpretation of a current document, add explicit cross-links between the history note and the affected current artifact.
