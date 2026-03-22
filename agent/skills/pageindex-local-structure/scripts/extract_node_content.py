import argparse
import json
import sys
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_local_structure as builder


def find_node_by_id(nodes, node_id):
    for node in nodes:
        if node.get("node_id") == node_id:
            return node
        found = find_node_by_id(node.get("nodes", []), node_id)
        if found is not None:
            return found
    return None


def collect_node_text(node):
    parts = []
    text = node.get("text")
    if text:
        parts.append(text)
    for child in node.get("nodes", []):
        child_text = collect_node_text(child)
        if child_text:
            parts.append(child_text)
    return "\n\n".join(parts).strip()


def load_structure(structure_path):
    return json.loads(Path(structure_path).read_text(encoding="utf-8"))


def extract_pdf_node_content(pdf_path, structure, node_id):
    node = find_node_by_id(structure.get("structure", []), node_id)
    if node is None:
        raise ValueError(f"Node not found: {node_id}")

    start_page = node.get("start_page")
    end_page = node.get("end_page")
    if start_page is None or end_page is None:
        raise ValueError(f"PDF node {node_id} is missing page range metadata")

    parts = []
    with fitz.open(pdf_path) as doc:
        for page_number in range(start_page, end_page + 1):
            page = doc.load_page(page_number - 1)
            parts.append(page.get_text("text").strip())

    return {
        "node_id": node_id,
        "title": node.get("title"),
        "content": "\n\n".join(part for part in parts if part).strip(),
        "start_page": start_page,
        "end_page": end_page,
    }


def extract_markdown_node_content(markdown_path, node_id):
    path = Path(markdown_path)
    structure = builder.extract_markdown_structure(
        path.read_text(encoding="utf-8"),
        doc_name=path.stem,
        include_text=True,
    )
    node = find_node_by_id(structure.get("structure", []), node_id)
    if node is None:
        raise ValueError(f"Node not found: {node_id}")

    return {
        "node_id": node_id,
        "title": node.get("title"),
        "content": collect_node_text(node),
        "line_num": node.get("line_num"),
    }


def extract_docx_node_content(docx_path, node_id):
    structure = builder.extract_docx_structure(docx_path, include_text=True)
    node = find_node_by_id(structure.get("structure", []), node_id)
    if node is None:
        raise ValueError(f"Node not found: {node_id}")

    return {
        "node_id": node_id,
        "title": node.get("title"),
        "content": collect_node_text(node),
        "paragraph_index": node.get("paragraph_index"),
    }


def extract_node_content(source_path, source_type, node_id, structure_path=None):
    if source_type == "markdown":
        return extract_markdown_node_content(source_path, node_id)
    if source_type == "docx":
        return extract_docx_node_content(source_path, node_id)
    if source_type == "pdf":
        if structure_path is None:
            raise ValueError("PDF extraction requires --structure")
        structure = load_structure(structure_path)
        return extract_pdf_node_content(source_path, structure, node_id)
    raise ValueError(f"Unsupported source type: {source_type}")


def infer_source_type(path):
    suffix = Path(path).suffix.lower()
    if suffix in {".md", ".markdown"}:
        return "markdown"
    if suffix == ".docx":
        return "docx"
    if suffix == ".pdf":
        return "pdf"
    raise ValueError(f"Unsupported file extension: {suffix}")


def main():
    parser = argparse.ArgumentParser(description="Extract content for a single PageIndex node.")
    parser.add_argument("--source", required=True, help="Source PDF, DOCX, or Markdown file")
    parser.add_argument("--node-id", required=True, help="Node identifier to extract")
    parser.add_argument("--structure", help="Structure JSON path, required for PDFs")
    parser.add_argument("--type", dest="source_type", choices=["pdf", "docx", "markdown"], help="Optional explicit source type")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()

    source_type = args.source_type or infer_source_type(args.source)
    result = extract_node_content(args.source, source_type, args.node_id, structure_path=args.structure)

    output_path = Path(args.output) if args.output else None
    if output_path is None:
        source = Path(args.source)
        output_path = source.with_name(f"{source.stem}_{args.node_id}_content.json")

    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(str(output_path))


if __name__ == "__main__":
    main()
