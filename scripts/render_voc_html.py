#!/usr/bin/env python3
"""Render a three-column, yellow-highlighted VOC rich-text fragment from JSON."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


YELLOW = "#FFE699"
PALE_YELLOW = "#FFF2CC"
BORDER = "#D9D9D9"


def percentage(count: int, base: int) -> str:
    return f"{count / base * 100:.1f}%（{count}/{base}）"


def render_table(section: dict) -> str:
    headers = section.get("headers", [])
    if len(headers) != 3:
        raise ValueError(f"Section {section.get('title')!r} must have exactly three headers")
    if any("原评论" in str(header) or "证据原文" in str(header) for header in headers):
        raise ValueError("Original-comment columns are disabled by default")
    base = int(section["base"])
    rows = section.get("rows", [])
    body_rows = []
    for row in rows:
        label = html.escape(str(row["label"]))
        insight = html.escape(str(row["insight"]))
        share = html.escape(str(row.get("share") or percentage(int(row["count"]), base)))
        body_rows.append(
            "<tr>"
            f'<td style="border:1px solid {BORDER};padding:8px;vertical-align:top;font-weight:600;">{label}</td>'
            f'<td style="border:1px solid {BORDER};padding:8px;vertical-align:top;">{share}</td>'
            f'<td style="border:1px solid {BORDER};padding:8px;vertical-align:top;">{insight}</td>'
            "</tr>"
        )
    widths = ("23%", "17%", "60%")
    header_cells = "".join(
        f'<th style="width:{width};border:1px solid {BORDER};background:{YELLOW};padding:8px;text-align:left;font-weight:700;">{html.escape(str(header))}</th>'
        for header, width in zip(headers, widths)
    )
    return (
        f'<h3 style="margin:22px 0 8px;font-size:18px;font-weight:700;">'
        f'<span style="background:{YELLOW};padding:2px 6px;">{html.escape(str(section["title"]))}</span></h3>'
        '<table style="width:100%;border-collapse:collapse;table-layout:fixed;margin:0 0 14px;font-size:14px;line-height:1.55;">'
        f"<thead><tr>{header_cells}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"
    )


def render(spec: dict) -> tuple[str, str]:
    title = str(spec["title"])
    subtitle = str(spec.get("subtitle", ""))
    html_parts = [
        '<div style="font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',\'Microsoft YaHei\',Arial,sans-serif;color:#222;max-width:1100px;margin:0 auto;">',
        f'<h1 style="margin:0 0 8px;font-size:26px;font-weight:800;">{html.escape(title)}</h1>',
    ]
    text_parts = [title]
    if subtitle:
        html_parts.append(f'<p style="margin:0 0 12px;color:#666;">{html.escape(subtitle)}</p>')
        text_parts.extend([subtitle, ""])

    for callout in spec.get("callouts", []):
        label = str(callout.get("label", "")).strip()
        text = str(callout["text"])
        html_parts.append(
            f'<div style="background:{PALE_YELLOW};border-left:5px solid #F4B183;padding:12px 14px;margin:0 0 14px;line-height:1.65;">'
            f"<strong>{html.escape(label)}：</strong>{html.escape(text)}</div>"
        )
        text_parts.append(f"【{label}】{text}")
    text_parts.append("")

    for section in spec.get("sections", []):
        if section.get("kind") == "heading":
            heading = str(section["title"])
            html_parts.append(
                f'<h2 style="margin:28px 0 12px;font-size:22px;font-weight:800;">'
                f'<span style="background:{YELLOW};padding:4px 8px;">{html.escape(heading)}</span></h2>'
            )
            text_parts.extend([heading, ""])
            continue
        html_parts.append(render_table(section))
        text_parts.append(str(section["title"]))
        text_parts.append("\t".join(str(value) for value in section["headers"]))
        for row in section.get("rows", []):
            share = str(row.get("share") or percentage(int(row["count"]), int(section["base"])))
            text_parts.append("\t".join([str(row["label"]), share, str(row["insight"])]))
        text_parts.append("")

    conclusions = spec.get("conclusions", [])
    if conclusions:
        conclusion_title = str(spec.get("conclusion_title", "跨平台真实需求结论"))
        html_parts.append(
            f'<h2 style="margin:28px 0 12px;font-size:22px;font-weight:800;">'
            f'<span style="background:{YELLOW};padding:4px 8px;">{html.escape(conclusion_title)}</span></h2>'
            f'<div style="background:{PALE_YELLOW};border-left:5px solid #F4B183;padding:12px 16px;line-height:1.75;">'
        )
        text_parts.extend([conclusion_title])
        for index, item in enumerate(conclusions, start=1):
            label = str(item["label"])
            text = str(item["text"])
            margin = "0" if index == len(conclusions) else "0 0 8px"
            html_parts.append(
                f'<p style="margin:{margin};"><strong>{index}. {html.escape(label)}：</strong>{html.escape(text)}</p>'
            )
            text_parts.append(f"{index}. {label}：{text}")
        html_parts.append("</div>")

    html_parts.append("</div>")
    return "".join(html_parts), "\n".join(text_parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("--html", dest="html_path", type=Path, required=True)
    parser.add_argument("--text", dest="text_path", type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    html_output, text_output = render(spec)
    args.html_path.parent.mkdir(parents=True, exist_ok=True)
    args.text_path.parent.mkdir(parents=True, exist_ok=True)
    args.html_path.write_text(html_output, encoding="utf-8")
    args.text_path.write_text(text_output, encoding="utf-8")
    print(
        json.dumps(
            {
                "html": str(args.html_path),
                "text": str(args.text_path),
                "tables": sum(1 for item in spec.get("sections", []) if item.get("kind") != "heading"),
                "contains_original_comment_column": "原评论代表摘取" in html_output,
                "contains_yellow": YELLOW in html_output,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
