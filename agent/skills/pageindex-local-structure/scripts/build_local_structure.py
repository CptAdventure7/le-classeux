import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import fitz

MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
WORD_REL_NS = {"pr": "http://schemas.openxmlformats.org/package/2006/relationships"}
DRAWING_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


TOC_LINE_RE = re.compile(
    r"^\s*(?:(?P<number>\d+(?:\.\d+)*)[\.\)]?\s+)?(?P<title>.*?\S)\s*(?:\.{2,}|\s{2,}|\t)\s*(?P<page>\d{1,5})\s*$"
)


def next_node_id(counter):
    return str(counter).zfill(4)


def count_markdown_images(text):
    if not text:
        return 0
    return len(MARKDOWN_IMAGE_RE.findall(text))


def _finalize_tree_image_metadata(nodes):
    total_count = 0
    for node in nodes:
        own_count = node.pop("_local_image_count", 0)
        child_count = _finalize_tree_image_metadata(node.get("nodes", []))
        node_count = own_count + child_count
        node["has_images"] = node_count > 0
        node["image_count"] = node_count
        total_count += node_count
    return total_count


def extract_markdown_structure(markdown_text, doc_name="document", include_text=False, include_image_metadata=False):
    lines = markdown_text.splitlines()
    entries = []
    in_code_block = False

    for line_number, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", stripped)
        if not match:
            continue

        entries.append(
            {
                "level": len(match.group(1)),
                "title": match.group(2).strip(),
                "line_num": line_number,
            }
        )

    tree = []
    stack = []
    counter = 0

    for index, entry in enumerate(entries):
        counter += 1
        start_line = entry["line_num"]
        end_line = entries[index + 1]["line_num"] - 1 if index + 1 < len(entries) else len(lines)
        node = {
            "title": entry["title"],
            "node_id": next_node_id(counter),
            "line_num": start_line,
            "nodes": [],
        }
        section_text = "\n".join(lines[start_line - 1 : end_line]).strip()
        if include_text:
            node["text"] = section_text
        if include_image_metadata:
            node["_local_image_count"] = count_markdown_images(section_text)

        while stack and stack[-1]["level"] >= entry["level"]:
            stack.pop()

        if stack:
            stack[-1]["node"]["nodes"].append(node)
        else:
            tree.append(node)

        stack.append({"level": entry["level"], "node": node})

    if include_image_metadata:
        _finalize_tree_image_metadata(tree)

    return {"doc_name": doc_name, "structure": tree}


WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def _docx_text_from_paragraph(paragraph):
    parts = []
    for node in paragraph.findall(".//w:t", WORD_NS):
        if node.text:
            parts.append(node.text)
    return "".join(parts).strip()


def _heading_level_from_style(style_value):
    if not style_value:
        return None
    match = re.fullmatch(r"Heading([1-9])", style_value)
    if match:
        return int(match.group(1))
    return None


def _docx_relationship_map(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as archive:
            rel_bytes = archive.read("word/_rels/document.xml.rels")
    except KeyError:
        return {}

    root = ET.fromstring(rel_bytes)
    relationships = {}
    for rel in root.findall("pr:Relationship", WORD_REL_NS):
        rel_id = rel.attrib.get("Id")
        rel_type = rel.attrib.get("Type", "")
        target = rel.attrib.get("Target")
        if not rel_id or not target:
            continue
        relationships[rel_id] = {"type": rel_type, "target": target}
    return relationships


def _docx_paragraphs(docx_path):
    relationships = _docx_relationship_map(docx_path)
    with zipfile.ZipFile(docx_path) as archive:
        xml_bytes = archive.read("word/document.xml")

    root = ET.fromstring(xml_bytes)
    body = root.find("w:body", WORD_NS)
    if body is None:
        return []

    paragraphs = []
    paragraph_index = 0
    for paragraph in body.findall("w:p", WORD_NS):
        paragraph_index += 1
        style = paragraph.find("w:pPr/w:pStyle", WORD_NS)
        style_value = None if style is None else style.attrib.get(f"{{{WORD_NS['w']}}}val")
        title = _docx_text_from_paragraph(paragraph)
        image_targets = []
        for node in paragraph.iter():
            embed_id = node.attrib.get(f"{{{DRAWING_REL_NS}}}embed")
            if not embed_id:
                continue
            relationship = relationships.get(embed_id)
            if relationship and relationship["type"].endswith("/image"):
                image_targets.append(relationship["target"])
        paragraphs.append(
            {
                "paragraph_index": paragraph_index,
                "style": style_value,
                "text": title,
                "image_targets": image_targets,
            }
        )
    return paragraphs


def extract_docx_structure(docx_path, include_text=False, include_image_metadata=False, include_image_targets=False):
    paragraphs = _docx_paragraphs(docx_path)
    entries = []
    for index, paragraph in enumerate(paragraphs):
        level = _heading_level_from_style(paragraph["style"])
        if level is None or not paragraph["text"]:
            continue

        entry = {
            "level": level,
            "title": paragraph["text"],
            "paragraph_index": paragraph["paragraph_index"],
        }
        if include_text:
            next_heading_index = None
            for later in paragraphs[index + 1 :]:
                if _heading_level_from_style(later["style"]) is not None:
                    next_heading_index = later["paragraph_index"]
                    break

            content_parts = []
            image_targets = []
            for current in paragraphs[paragraph["paragraph_index"] - 1 :]:
                if next_heading_index is not None and current["paragraph_index"] >= next_heading_index:
                    break
                if current["text"]:
                    content_parts.append(current["text"])
                image_targets.extend(current.get("image_targets", []))
            entry["text"] = "\n".join(content_parts).strip()
            if include_image_metadata or include_image_targets:
                deduped_targets = list(dict.fromkeys(image_targets))
                entry["_image_targets"] = deduped_targets
                entry["_local_image_count"] = len(deduped_targets)
        elif include_image_metadata or include_image_targets:
            next_heading_index = None
            for later in paragraphs[index + 1 :]:
                if _heading_level_from_style(later["style"]) is not None:
                    next_heading_index = later["paragraph_index"]
                    break
            image_targets = []
            for current in paragraphs[paragraph["paragraph_index"] - 1 :]:
                if next_heading_index is not None and current["paragraph_index"] >= next_heading_index:
                    break
                image_targets.extend(current.get("image_targets", []))
            deduped_targets = list(dict.fromkeys(image_targets))
            entry["_image_targets"] = deduped_targets
            entry["_local_image_count"] = len(deduped_targets)

        entries.append(entry)

    tree = []
    stack = []
    counter = 0
    for entry in entries:
        counter += 1
        node = {
            "title": entry["title"],
            "node_id": next_node_id(counter),
            "paragraph_index": entry["paragraph_index"],
            "nodes": [],
        }
        if include_text:
            node["text"] = entry.get("text", "")
        if include_image_metadata:
            node["_local_image_count"] = entry.get("_local_image_count", 0)
        if include_image_targets:
            node["_image_targets"] = entry.get("_image_targets", [])

        while stack and stack[-1]["level"] >= entry["level"]:
            stack.pop()

        if stack:
            stack[-1]["node"]["nodes"].append(node)
        else:
            tree.append(node)

        stack.append({"level": entry["level"], "node": node})

    if include_image_metadata:
        _finalize_tree_image_metadata(tree)

    return {"doc_name": Path(docx_path).stem, "structure": tree}


def parse_toc_lines(lines):
    entries = []
    for raw_line in lines:
        line = " ".join(raw_line.strip().split())
        if len(line) < 4:
            continue

        match = TOC_LINE_RE.match(line)
        if not match:
            continue

        title = match.group("title").strip(" .:-")
        if not title or title.isdigit():
            continue

        number = match.group("number")
        if number:
            level = number.count(".") + 1
        else:
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            level = max(1, indent // 2 + 1)

        entries.append(
            {
                "level": level,
                "title": title,
                "page": int(match.group("page")),
            }
        )

    deduped = []
    seen = set()
    for entry in entries:
        key = (entry["level"], entry["title"], entry["page"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(entry)
    return deduped


def build_toc_tree(entries, total_pages=None, doc_name="document"):
    tree = []
    stack = []
    counter = 0

    for entry in entries:
        counter += 1
        node = {
            "title": entry["title"],
            "node_id": next_node_id(counter),
            "start_page": entry["page"],
            "end_page": total_pages or entry["page"],
            "nodes": [],
        }

        while stack and stack[-1]["level"] >= entry["level"]:
            closed = stack.pop()
            closed["node"]["end_page"] = max(
                closed["node"]["start_page"], entry["page"] - 1
            )

        if stack:
            stack[-1]["node"]["nodes"].append(node)
        else:
            tree.append(node)

        stack.append({"level": entry["level"], "node": node})

    while stack:
        closed = stack.pop()
        closed["node"]["end_page"] = max(
            closed["node"]["start_page"],
            total_pages or closed["node"]["start_page"],
        )

    return {"doc_name": doc_name, "structure": tree}


def outline_to_entries(outline):
    entries = []
    for item in outline:
        if len(item) < 3:
            continue
        level, title, page = item[:3]
        if not title or page is None or page <= 0:
            continue
        entries.append({"level": int(level), "title": str(title).strip(), "page": int(page)})
    return entries


def detect_printed_toc_entries(doc, max_pages=12):
    lines = []
    for page_index in range(min(max_pages, doc.page_count)):
        page = doc.load_page(page_index)
        lines.extend(page.get_text("text").splitlines())

    entries = parse_toc_lines(lines)
    if len(entries) < 3:
        return []
    return entries


def page_heading_candidate(page):
    text_dict = page.get_text("dict")
    best_size = 0.0
    candidates = []

    for block in text_dict.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = " ".join(span.get("text", "").split())
                if not text:
                    continue
                if len(text) > 120:
                    continue
                if re.fullmatch(r"[\d\W]+", text):
                    continue

                size = float(span.get("size", 0))
                if size > best_size + 0.2:
                    best_size = size
                    candidates = [text]
                elif abs(size - best_size) <= 0.2:
                    candidates.append(text)

    for candidate in candidates:
        if len(candidate) >= 3:
            return candidate
    return None


def fallback_page_entries(doc):
    entries = []
    last_title = None
    for page_number in range(1, doc.page_count + 1):
        page = doc.load_page(page_number - 1)
        title = page_heading_candidate(page) or f"Page {page_number}"
        if title == last_title:
            title = f"{title} ({page_number})"
        entries.append({"level": 1, "title": title, "page": page_number})
        last_title = title
    return entries


def _page_image_counts(doc):
    counts = {}
    for page_number in range(1, doc.page_count + 1):
        page = doc.load_page(page_number - 1)
        counts[page_number] = len(page.get_images(full=True))
    return counts


def _annotate_pdf_image_metadata(nodes, page_image_counts):
    for node in nodes:
        start_page = node.get("start_page")
        end_page = node.get("end_page")
        image_pages = []
        image_count = 0
        if start_page is not None and end_page is not None:
            for page_number in range(start_page, end_page + 1):
                count = page_image_counts.get(page_number, 0)
                if count > 0:
                    image_pages.append(page_number)
                    image_count += count
        node["has_images"] = image_count > 0
        node["image_count"] = image_count
        if image_pages:
            node["image_pages"] = image_pages
        _annotate_pdf_image_metadata(node.get("nodes", []), page_image_counts)


def extract_pdf_structure(pdf_path, max_toc_pages=12, include_image_metadata=False):
    doc_name = Path(pdf_path).stem
    with fitz.open(pdf_path) as doc:
        page_image_counts = _page_image_counts(doc) if include_image_metadata else None
        outline = outline_to_entries(doc.get_toc(simple=True))

        if outline:
            result = build_toc_tree(outline, total_pages=doc.page_count, doc_name=doc_name)
            result["source"] = "pdf-outline"
            if include_image_metadata:
                _annotate_pdf_image_metadata(result["structure"], page_image_counts)
            return result

        toc_entries = detect_printed_toc_entries(doc, max_pages=max_toc_pages)
        if toc_entries:
            result = build_toc_tree(toc_entries, total_pages=doc.page_count, doc_name=doc_name)
            result["source"] = "printed-toc"
            if include_image_metadata:
                _annotate_pdf_image_metadata(result["structure"], page_image_counts)
            return result

        page_entries = fallback_page_entries(doc)
        result = build_toc_tree(page_entries, total_pages=doc.page_count, doc_name=doc_name)
        result["source"] = "page-headings"
        if include_image_metadata:
            _annotate_pdf_image_metadata(result["structure"], page_image_counts)
        return result


def main():
    parser = argparse.ArgumentParser(description="Build a local PageIndex-style structure without API keys.")
    parser.add_argument("--pdf", type=str, help="Path to a PDF document")
    parser.add_argument("--markdown", type=str, help="Path to a Markdown document")
    parser.add_argument("--docx", type=str, help="Path to a DOCX document")
    parser.add_argument("--output", type=str, help="Optional output JSON path")
    parser.add_argument("--include-text", action="store_true", help="Include Markdown node text")
    parser.add_argument("--include-image-metadata", action="store_true", help="Add lightweight image metadata to nodes")
    parser.add_argument("--max-toc-pages", type=int, default=12, help="Pages to scan for a printed TOC")
    args = parser.parse_args()

    input_count = sum(bool(value) for value in [args.pdf, args.markdown, args.docx])
    if input_count != 1:
        raise ValueError("Specify exactly one of --pdf, --markdown, or --docx")

    if args.markdown:
        path = Path(args.markdown)
        result = extract_markdown_structure(
            path.read_text(encoding="utf-8"),
            doc_name=path.stem,
            include_text=args.include_text,
            include_image_metadata=args.include_image_metadata,
        )
    elif args.docx:
        result = extract_docx_structure(args.docx, include_image_metadata=args.include_image_metadata)
    else:
        result = extract_pdf_structure(
            args.pdf,
            max_toc_pages=args.max_toc_pages,
            include_image_metadata=args.include_image_metadata,
        )

    output = Path(args.output) if args.output else None
    if output is None:
        source_path = Path(args.markdown or args.pdf or args.docx)
        output = source_path.with_name(f"{source_path.stem}_structure.json")

    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(str(output))


if __name__ == "__main__":
    main()
