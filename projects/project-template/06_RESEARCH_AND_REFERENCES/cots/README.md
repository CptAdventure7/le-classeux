# Cots

Commercial off-the-shelf component comparison artifacts live here.

## Keep Here

- Create one subfolder per component area, subsystem part family, or comparison scope.
- In each component-area subfolder, keep one canonical JSON file that aggregates the specification and sourcing data for the options being compared in that area.
- Add a local `README.md` inside each component-area subfolder to define the exact JSON shape for that area, while preserving the minimum required fields listed below for every option record.
- Keep normalized comparison notes, shortlist rationale, and links to affected requirements, design records, procurement items, decisions, or validation evidence close to that component-area JSON.
- Keep vendor-specific web evidence here when it directly supports a component comparison.

## Minimum Option Fields

Each option entry in the component-area JSON must contain at least these fields:

- `option_name`
- `manufacturer`
- `model`
- `characteristics`
- `price`
- `weight_g`
- `dimensions_mm`
- `country_of_origin`
- `state_province_region_of_origin`
- `internet_reference_links`
- `sharepoint_reference_links`
- `notes`

The local `README.md` inside each component-area subfolder may add context-specific fields, top-level metadata, or normalization rules, but it must not drop the minimum option fields above.

## Keep Elsewhere

- Put general web research that is not tied to a specific COTS comparison in `../web_references`.
- Put procurement execution artifacts such as quote approval flow or purchase timing in `../../07_PROJECT_EXECUTION/procurement`.
- Do not keep original downloaded evidence here. Internet screenshots, PDFs, datasheets, quotes, and other source captures belong in the linked SharePoint location under `03-Design\cots\option_name\model`, using a similar folder structure.
- Keep only the relevant references in this repository, primarily through `internet_reference_links`, `sharepoint_reference_links`, and concise notes.

## Example

`motor-controllers/` containing:

- `README.md` describing the exact JSON contract for motor-controller comparisons
- one canonical JSON file aggregating the candidate data for that component area
- optional supporting notes that explain downselect logic or traceability links

## Local Manifest

- Review `local_manifest.yaml` when entering this folder to quickly see whether any local files are relevant.
- Keep `local_manifest.yaml` up to date whenever files are added, removed, renamed, or materially repurposed.

