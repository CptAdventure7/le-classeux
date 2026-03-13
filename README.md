# Maxwell Context Bank

This repository is organized as a progressive disclosure context bank. Start broad at the root, then follow each folder's local `README.md` and `AGENTS.md` for deeper guidance.

## Start Here

- Read `project_manifest.yaml` for the authoritative section map and repository conventions.
- Open the folder closest to your question, then read that folder's `README.md`.
- Follow the linked folders in each local guide instead of scanning the entire tree.

## Top-Level Sections

- `00_GOVERNANCE`: Program-level control documents, current state, and operating workflows.
- `01_PROJECT_FOUNDATION`: Why the project exists, who it serves, and the constraints that frame all downstream work.
- `02_SYSTEM_DEFINITION`: Problem framing for the system itself, including how users interact with it and how the architecture is partitioned.
- `03_REQUIREMENTS`: Requirements decomposed from user intent to system and subsystem obligations.
- `04_DESIGN_AND_IMPLEMENTATION`: Design artefacts, interface definitions, code references, prototypes, and technical risk information.
- `05_EXPERIMENTS_AND_VALIDATION`: Verification, validation, experiments, datasets, and analysis evidence.
- `06_RESEARCH_AND_REFERENCES`: External knowledge, standards, prior art, supplier research, and citation support.
- `07_PROJECT_EXECUTION`: Planning, staffing, risk, and change-control artefacts used to steer delivery.
- `08_DECISIONS`: Decision records, trade studies, waivers, and other artifacts that explain why the project evolved.
- `09_COLLABORATION`: Working session artefacts and summarized meeting output.
- `10_COMMUNICATION`: Internal and external project communication artefacts, demos, reports, and visuals.
- `11_OPERATIONS_AND_HANDOFF`: Deployment, installation, training, release, and support material for transition to operations.
- `99_ARCHIVE`: Retired, superseded, or preserved historical artefacts that should remain traceable but inactive.

## Operating Conventions

- Keep one primary concept per file.
- Use date prefixes when chronology matters: `YYYY-MM-DD-topic.md`.
- Prefer links over duplication; summarize nearby, source once.
- Keep governance change logs in an append-only `change_log.md` file within each `change_log` folder, with the most recent entry at the top.
- Use each folder's `~history/` child for timestamped impact notes, except in dedicated `change_log` folders.
- Promote durable decisions to `08_DECISIONS` and archive retired material in `99_ARCHIVE`.

## Project Manifest

The project manifest is the machine-readable map for this structure. Update it if you add, remove, or rename major sections.
