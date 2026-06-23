#!/usr/bin/env python3
"""Regenerate talks.md from original 03_speaking.md HTML."""
import re
from html import unescape
from pathlib import Path
from urllib.parse import urlparse

SRC = Path("/tmp/03_speaking.md")
OUT = Path(__file__).resolve().parent.parent / "_includes" / "content" / "talks.md"


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return unescape(re.sub(r"\s+", " ", text)).strip()


def escape_cell(text: str) -> str:
    """Escape pipe characters so markdown tables stay aligned."""
    return text.replace("|", "\\|")


def link_label(url: str, original: str) -> str:
    host = urlparse(url).netloc.lower().replace("www.", "")
    if "github.com" in host:
        return "Demo"
    if "hashicorp.com" in host or "youtube.com" in host or "youtu.be" in host:
        return "Recording"
    if "speakerdeck.com" in host or original.lower() == "slides":
        return "Slides"
    if original.lower() == "demo":
        return "Demo"
    if original.lower() == "recording":
        return "Recording"
    if original.lower() == "slides":
        return "Slides"
    return original or "Link"


def parse_links(cell: str) -> list[tuple[str, str]]:
    links = []
    seen = set()
    for m in re.finditer(
        r'<a[^>]*href="([^"]*)"[^>]*>[\s\S]*?<span class="label">([\s\S]*?)</span>',
        cell,
        re.I,
    ):
        url = m.group(1).strip()
        original = strip_html(m.group(2))
        label = link_label(url, original)
        key = (label, url)
        if key in seen:
            continue
        seen.add(key)
        links.append((label, url))

    # Deduplicate labels in same row: if two "Demo", keep one (user complaint)
    by_label: dict[str, str] = {}
    order = []
    for label, url in links:
        if label not in by_label:
            by_label[label] = url
            order.append(label)
    return [(label, by_label[label]) for label in order]


def format_links(links: list[tuple[str, str]]) -> str:
    if not links:
        return ""
    return " · ".join(f"[{label}]({url})" for label, url in links)


def parse_table_section(html: str, heading: str) -> list[list[str]]:
    pattern = rf"<h3>{re.escape(heading)}</h3>[\s\S]*?<tbody>([\s\S]*?)</tbody>"
    match = re.search(pattern, html, re.I)
    if not match:
        return []
    rows = []
    for tr in re.finditer(r"<tr>([\s\S]*?)</tr>", match.group(1), re.I):
        if "<th>" in tr.group(1):
            continue
        cells = re.findall(r"<td>([\s\S]*?)</td>", tr.group(1), re.I)
        if not cells or cells[0].strip().startswith("<!--"):
            continue
        rows.append(cells)
    return rows


def main() -> None:
    body = re.sub(r"^---[\s\S]*?---\n", "", SRC.read_text())

    md = "# Speaking\n\n### Upcoming\n\n"
    md += "| Date | Event | Location |\n"
    md += "|------|-------|----------|\n"

    upcoming = parse_table_section(body, "Up Next")
    if upcoming:
        for cells in upcoming:
            date = escape_cell(strip_html(cells[0]))
            event = escape_cell(strip_html(cells[1]))
            title = escape_cell(strip_html(cells[2]))
            location_cell = cells[3] if len(cells) > 3 else ""
            loc_m = re.search(r'<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)</a>', location_cell, re.I)
            if loc_m:
                location = f"[{escape_cell(strip_html(loc_m.group(2)))}]({loc_m.group(1)})"
            else:
                location = escape_cell(strip_html(location_cell))
            event_full = escape_cell(f"{event} — {title}")
            md += f"| {date} | {event_full} | {location} |\n"
    else:
        md += "| | | |\n"

    md += "\n### Past Talks\n\n"
    md += "| Date | Event | Links |\n"
    md += "|------|-------|-------|\n"

    past = parse_table_section(body, "Previous Slides & Recordings")
    if not past:
        past = parse_table_section(body, "Previous Slides")

    for cells in past:
        date = escape_cell(strip_html(cells[0]))
        event = escape_cell(strip_html(cells[1]))
        title = escape_cell(strip_html(cells[2]))
        links_cell = cells[3] if len(cells) > 3 else ""
        event_full = escape_cell(f"{event} — {title}")
        links = format_links(parse_links(links_cell))
        md += f"| {date} | {event_full} | {links} |\n"

    OUT.write_text(md)
    print(f"Wrote {len(past)} past talks to {OUT}")


if __name__ == "__main__":
    main()
