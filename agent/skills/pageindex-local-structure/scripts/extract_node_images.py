import argparse
import json
import shutil
import sys
import zipfile
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_local_structure as builder
import extract_node_content as content_builder


def ensure_output_dir(path):
    output_dir = Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_bytes(output_dir, filename, payload):
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / filename
    target.write_bytes(payload)
    return target


def markdown_image_refs(text):
    return builder.MARKDOWN_IMAGE_RE.findall(text or "")


def extract_markdown_node_images(markdown_path, node_id, output_dir):
    node = content_builder.extract_markdown_node_content(markdown_path, node_id)
    source_dir = Path(markdown_path).parent
    output = ensure_output_dir(output_dir)
    images = []

    for index, ref in enumerate(markdown_image_refs(node["content"]), start=1):
        if ref.startswith(("http://", "https://")):
            continue
        source = (source_dir / ref).resolve()
        if not source.is_file():
            continue
        target = output / f"{node_id}_{index}{source.suffix}"
        shutil.copyfile(source, target)
        images.append({"path": str(target), "source": str(source)})

    return {
        "node_id": node_id,
        "title": node["title"],
        "image_count": len(images),
        "images": images,
    }


def extract_pdf_node_images(pdf_path, structure_path, node_id, output_dir):
    structure = content_builder.load_structure(structure_path)
    node = content_builder.find_node_by_id(structure.get("structure", []), node_id)
    if node is None:
        raise ValueError(f"Node not found: {node_id}")

    start_page = node.get("start_page")
    end_page = node.get("end_page")
    if start_page is None or end_page is None:
        raise ValueError(f"PDF node {node_id} is missing page range metadata")

    output = ensure_output_dir(output_dir)
    images = []
    with fitz.open(pdf_path) as doc:
        for page_number in range(start_page, end_page + 1):
            page = doc.load_page(page_number - 1)
            for image_index, image_info in enumerate(page.get_images(full=True), start=1):
                xref = image_info[0]
                extracted = doc.extract_image(xref)
                ext = extracted.get("ext", "bin")
                target = write_bytes(
                    output,
                    f"{node_id}_p{page_number}_{image_index}.{ext}",
                    extracted["image"],
                )
                images.append({"path": str(target), "page": page_number, "xref": xref})

    return {
        "node_id": node_id,
        "title": node.get("title"),
        "image_count": len(images),
        "images": images,
    }


def normalize_docx_target(target):
    cleaned = target.replace("\\", "/").lstrip("/")
    if cleaned.startswith("word/"):
        return cleaned
    return f"word/{cleaned}"


def extract_docx_node_images(docx_path, node_id, output_dir):
    structure = builder.extract_docx_structure(
        docx_path,
        include_image_metadata=True,
        include_image_targets=True,
    )
    node = content_builder.find_node_by_id(structure.get("structure", []), node_id)
    if node is None:
        raise ValueError(f"Node not found: {node_id}")

    output = ensure_output_dir(output_dir)
    targets = list(dict.fromkeys(node.get("_image_targets", [])))
    images = []
    with zipfile.ZipFile(docx_path) as archive:
        for index, target in enumerate(targets, start=1):
            normalized = normalize_docx_target(target)
            ext = Path(normalized).suffix or ".bin"
            payload = archive.read(normalized)
            file_path = write_bytes(output, f"{node_id}_{index}{ext}", payload)
            images.append({"path": str(file_path), "target": normalized})

    return {
        "node_id": node_id,
        "title": node.get("title"),
        "image_count": len(images),
        "images": images,
    }


def infer_source_type(path):
    suffix = Path(path).suffix.lower()
    if suffix in {".md", ".markdown"}:
        return "markdown"
    if suffix == ".docx":
        return "docx"
    if suffix == ".pdf":
        return "pdf"
    raise ValueError(f"Unsupported file extension: {suffix}")


def extract_node_images(source_path, source_type, node_id, structure_path=None, output_dir=None):
    if output_dir is None:
        source = Path(source_path)
        output_dir = str(source.with_name(f"{source.stem}_{node_id}_images"))

    if source_type == "markdown":
        return extract_markdown_node_images(source_path, node_id, output_dir)
    if source_type == "docx":
        return extract_docx_node_images(source_path, node_id, output_dir)
    if source_type == "pdf":
        if structure_path is None:
            raise ValueError("PDF image extraction requires --structure")
        return extract_pdf_node_images(source_path, structure_path, node_id, output_dir)
    raise ValueError(f"Unsupported source type: {source_type}")


def main():
    parser = argparse.ArgumentParser(description="Extract image files for a single PageIndex node.")
    parser.add_argument("--source", required=True, help="Source PDF, DOCX, or Markdown file")
    parser.add_argument("--node-id", required=True, help="Node identifier to extract images for")
    parser.add_argument("--structure", help="Structure JSON path, required for PDFs")
    parser.add_argument("--type", dest="source_type", choices=["pdf", "docx", "markdown"], help="Optional explicit source type")
    parser.add_argument("--output-dir", help="Optional output directory for extracted image files")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()

    source_type = args.source_type or infer_source_type(args.source)
    result = extract_node_images(
        args.source,
        source_type,
        args.node_id,
        structure_path=args.structure,
        output_dir=args.output_dir,
    )

    output_path = Path(args.output) if args.output else None
    if output_path is None:
        source = Path(args.source)
        output_path = source.with_name(f"{source.stem}_{args.node_id}_images.json")

    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(str(output_path))


if __name__ == "__main__":
    main()
