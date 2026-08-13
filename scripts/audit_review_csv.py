#!/usr/bin/env python3
"""Deterministically clean and audit review rows exported to CSV or TSV."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path


DEFAULT_TEXTS = {
    "此用户未填写评价内容",
    "该用户觉得商品非常好，给出5星好评",
    "该用户觉得商品非常好，给出5星好评。",
    "用户未及时作出评价，系统默认好评",
    "系统默认好评",
    "默认好评",
    "no comment",
    "no written review",
    "the user did not write a review",
}


def normalize(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or ""))
    return re.sub(r"\s+", " ", text).strip()


def detect_delimiter(path: Path) -> str:
    if path.suffix.lower() == ".tsv":
        return "\t"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(8192)
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
    except csv.Error:
        return ","


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    delimiter = detect_delimiter(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        if not reader.fieldnames:
            raise ValueError("Input has no header row")
        return list(reader.fieldnames), [dict(row) for row in reader]


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--text-col", required=True)
    parser.add_argument("--platform-col")
    parser.add_argument("--id-col")
    parser.add_argument("--valid-col")
    parser.add_argument("--valid-value", default="有效")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--containment-dedupe", action="store_true")
    args = parser.parse_args()

    fieldnames, rows = read_rows(args.input)
    required = [args.text_col]
    required += [name for name in (args.platform_col, args.id_col, args.valid_col) if name]
    missing = [name for name in required if name not in fieldnames]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")

    kept: list[dict[str, str]] = []
    excluded: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    normalized_defaults = {normalize(item).casefold() for item in DEFAULT_TEXTS}

    def exclude(row: dict[str, str], reason: str, normalized: str) -> None:
        excluded.append({**row, "_normalized_text": normalized, "_exclusion_reason": reason})

    for index, row in enumerate(rows, start=2):
        text = normalize(row.get(args.text_col))
        platform = normalize(row.get(args.platform_col)) if args.platform_col else ""
        if args.valid_col and normalize(row.get(args.valid_col)) != args.valid_value:
            exclude(row, "validity_filter", text)
            continue
        if not text:
            exclude(row, "blank_text", text)
            continue
        if text.casefold() in normalized_defaults:
            exclude(row, "default_boilerplate", text)
            continue
        key = (platform, text.casefold())
        if key in seen:
            exclude(row, "exact_duplicate", text)
            continue
        seen.add(key)
        kept.append(
            {
                **row,
                "_source_row": str(index),
                "_normalized_text": text,
                "_low_information": "yes" if len(text) < 8 else "no",
            }
        )

    if args.containment_dedupe:
        duplicate_indexes: set[int] = set()
        for left_index, left in enumerate(kept):
            left_text = left["_normalized_text"]
            left_platform = normalize(left.get(args.platform_col)) if args.platform_col else ""
            for right_index in range(left_index + 1, len(kept)):
                right = kept[right_index]
                right_text = right["_normalized_text"]
                right_platform = normalize(right.get(args.platform_col)) if args.platform_col else ""
                if left_platform != right_platform or min(len(left_text), len(right_text)) < 40:
                    continue
                if left_text in right_text or right_text in left_text:
                    duplicate_indexes.add(
                        left_index if len(left_text) <= len(right_text) else right_index
                    )
        if duplicate_indexes:
            filtered: list[dict[str, str]] = []
            for index, row in enumerate(kept):
                if index in duplicate_indexes:
                    exclude(row, "contained_followup_duplicate", row["_normalized_text"])
                else:
                    filtered.append(row)
            kept = filtered

    args.output_dir.mkdir(parents=True, exist_ok=True)
    cleaned_fields = fieldnames + ["_source_row", "_normalized_text", "_low_information"]
    excluded_fields = fieldnames + ["_normalized_text", "_exclusion_reason"]
    write_rows(args.output_dir / "cleaned_reviews.csv", cleaned_fields, kept)
    write_rows(args.output_dir / "excluded_reviews.csv", excluded_fields, excluded)

    platform_counts = Counter(
        normalize(row.get(args.platform_col)) if args.platform_col else "all" for row in kept
    )
    exclusion_counts = Counter(row["_exclusion_reason"] for row in excluded)
    summary = {
        "input_rows": len(rows),
        "effective_rows": len(kept),
        "excluded_rows": len(excluded),
        "effective_by_platform": dict(platform_counts),
        "exclusions_by_reason": dict(exclusion_counts),
        "low_information_rows_kept": sum(row["_low_information"] == "yes" for row in kept),
    }
    (args.output_dir / "audit_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
