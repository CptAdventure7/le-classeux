import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import extract_node_content as content_helper
import extract_node_images as image_helper


def extract_node_bundle(source_path, node_id, source_type=None, structure_path=None, output_dir=None):
    resolved_type = source_type or content_helper.infer_source_type(source_path)
    content = content_helper.extract_node_content(
        source_path,
        resolved_type,
        node_id,
        structure_path=structure_path,
    )
    images = image_helper.extract_node_images(
        source_path,
        resolved_type,
        node_id,
        structure_path=structure_path,
        output_dir=output_dir,
    )
    return {
        "node_id": node_id,
        "source_type": resolved_type,
        "title": content.get("title"),
        "content": content,
        "images": images,
    }


def main():
    parser = argparse.ArgumentParser(description="Extract both text and images for a single PageIndex node.")
    parser.add_argument("--source", required=True, help="Source PDF, DOCX, or Markdown file")
    parser.add_argument("--node-id", required=True, help="Node identifier to extract")
    parser.add_argument("--structure", help="Structure JSON path, required for PDFs")
    parser.add_argument("--type", dest="source_type", choices=["pdf", "docx", "markdown"], help="Optional explicit source type")
    parser.add_argument("--output-dir", help="Optional output directory for extracted image files")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()

    result = extract_node_bundle(
        args.source,
        args.node_id,
        source_type=args.source_type,
        structure_path=args.structure,
        output_dir=args.output_dir,
    )

    output_path = Path(args.output) if args.output else None
    if output_path is None:
        source = Path(args.source)
        output_path = source.with_name(f"{source.stem}_{args.node_id}_bundle.json")

    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(str(output_path))


if __name__ == "__main__":
    main()
