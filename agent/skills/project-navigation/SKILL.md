---
name: project-navigation
description: Use when routing inside a project-template-derived context bank and you want a low-token overview of which top-level sections are worth opening before reading deeper artefacts.
---

# Project Navigation

## Overview

Use this shared skill to navigate a project-template-derived context bank cheaply. Read the project root `README.md`, then `project_manifest.yaml`, then refresh or reuse the cached `runtime_scan_summary.json` with the bundled PowerShell script before descending into section folders.

## When to Use

- The project uses the `runtime_scan` block in `project_manifest.yaml`.
- You want a top-level section summary instead of opening many empty folders.
- You are on Windows or using PowerShell-compatible tooling.

## Implementation

- Generator script: `agent/skills/project-navigation/scripts/generate_runtime_scan_summary.ps1`
- Cache artifact: `00_GOVERNANCE/current_overview/runtime_scan_summary.json`

Run the script with the selected project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\agent\skills\project-navigation\scripts\generate_runtime_scan_summary.ps1 -ProjectRoot .\projects\<project-name>
```

Use `-ForceRefresh` when you need a new cache immediately. Otherwise the script reuses the cache until it is more than 24 hours old.

## Common Mistakes

- Treating `99_ARCHIVE` as normal routing scope. It is history-only unless the query is explicitly historical.
- Opening file contents just to decide whether a section matters. The scan is metadata-only by design.
- Expanding the scan beyond the manifest-opted top-level sections.
