---
name: pageindex-local-structure
description: Use when turning long PDF, DOCX, or Markdown documents into a local hierarchical JSON structure for navigation or retrieval, without requiring any API key or external service
---

# PageIndex Local Structure

## Overview

Use this skill to reproduce the core PageIndex idea locally: convert a document into a nested structure that acts like a machine-friendly table of contents, then fetch only the relevant node's text or images when needed.

This skill is local-only. It does not call OpenAI or any hosted PageIndex service.

## When to Use

- Long Markdown files with real heading structure
- Word `.docx` files that use heading styles
- PDFs where local bookmarks already exist
- PDFs with printed table-of-contents pages
- Offline or no-credential environments

Do not use this skill when you need LLM-written summaries or semantic section rewriting. This skill only builds the structure tree.

## Workflow

1. For Markdown, run the bundled script directly on the `.md` file.
2. For DOCX, the script reads `word/document.xml` and builds hierarchy from Word heading styles like `Heading1`, `Heading2`, and so on.
3. For PDF, the script tries three local strategies in order:
   - embedded PDF outline/bookmarks
   - printed TOC line parsing from the first pages
   - per-page heading fallback
4. Inspect the emitted JSON and use it as the retrieval/navigation index.
5. When a node looks relevant, extract only that node's content or images instead of loading the full document.
6. If the agent wants one step, use the bundle script to fetch both in a single manifest.

## Commands

Markdown:

```bash
python scripts/build_local_structure.py --markdown /path/to/file.md
```

Markdown with lightweight image metadata:

```bash
python scripts/build_local_structure.py --markdown /path/to/file.md --include-image-metadata
```

Markdown with section text:

```bash
python scripts/build_local_structure.py --markdown /path/to/file.md --include-text
```

PDF:

```bash
python scripts/build_local_structure.py --pdf /path/to/file.pdf
```

PDF with lightweight image metadata:

```bash
python scripts/build_local_structure.py --pdf /path/to/file.pdf --include-image-metadata
```

DOCX:

```bash
python scripts/build_local_structure.py --docx /path/to/file.docx
```

DOCX with lightweight image metadata:

```bash
python scripts/build_local_structure.py --docx /path/to/file.docx --include-image-metadata
```

Explicit output path:

```bash
python scripts/build_local_structure.py --pdf /path/to/file.pdf --output /path/to/output.json
```

Node extraction:

Markdown:

```bash
python scripts/extract_node_content.py --source /path/to/file.md --node-id 0003
```

DOCX:

```bash
python scripts/extract_node_content.py --source /path/to/file.docx --node-id 0003
```

PDF:

```bash
python scripts/extract_node_content.py --source /path/to/file.pdf --structure /path/to/file_structure.json --node-id 0003
```

Node image extraction:

Markdown:

```bash
python scripts/extract_node_images.py --source /path/to/file.md --node-id 0003 --output-dir /path/to/output-images
```

DOCX:

```bash
python scripts/extract_node_images.py --source /path/to/file.docx --node-id 0003 --output-dir /path/to/output-images
```

PDF:

```bash
python scripts/extract_node_images.py --source /path/to/file.pdf --structure /path/to/file_structure.json --node-id 0003 --output-dir /path/to/output-images
```

One-command node bundle:

Markdown:

```bash
python scripts/extract_node_bundle.py --source /path/to/file.md --node-id 0003 --output-dir /path/to/output-images
```

DOCX:

```bash
python scripts/extract_node_bundle.py --source /path/to/file.docx --node-id 0003 --output-dir /path/to/output-images
```

PDF:

```bash
python scripts/extract_node_bundle.py --source /path/to/file.pdf --structure /path/to/file_structure.json --node-id 0003 --output-dir /path/to/output-images
```

## Output Shape

The script writes JSON like:

```json
{
  "doc_name": "example",
  "structure": [
    {
      "title": "Introduction",
      "node_id": "0001",
      "start_page": 1,
      "end_page": 3,
      "nodes": []
    }
  ]
}
```

Markdown output uses `line_num` instead of page ranges. DOCX output uses `paragraph_index`. With `--include-text`, each Markdown node also includes `text`.

With `--include-image-metadata`, nodes also get small image fields:

```json
{
  "has_images": true,
  "image_count": 2
}
```

PDF nodes may also include:

```json
{
  "image_pages": [12, 13]
}
```

The extraction script writes JSON like:

```json
{
  "node_id": "0003",
  "title": "Risk Factors",
  "content": "...only this node's content..."
}
```

The bundle script writes JSON like:

```json
{
  "node_id": "0003",
  "source_type": "pdf",
  "title": "Risk Factors",
  "content": {
    "content": "...selected node text..."
  },
  "images": {
    "image_count": 2,
    "images": [
      {
        "path": "/path/to/output-images/0003_p12_1.png"
      }
    ]
  }
}
```

## Notes

- Best PDF results come from documents that already expose bookmarks or a printed TOC.
- Best DOCX results come from documents that use actual Word heading styles rather than only visual formatting.
- The page-heading fallback is heuristic. It preserves navigation usefulness but is weaker than the original OpenAI-backed pipeline on messy PDFs.
- If a PDF result is poor, convert the PDF to structured Markdown first, then run the Markdown path.
- For targeted retrieval, use `extract_node_content.py` after choosing a promising node from the structure JSON.
- For multimodal retrieval, keep the JSON lightweight and use `extract_node_images.py` only after a node has been selected.
- For agent workflows, prefer `extract_node_bundle.py` so one command returns both the selected node text and the selected node images.
