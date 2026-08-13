# Analyze Product VOC Skill

[中文说明](README.zh-CN.md) · [Skill definition](SKILL.md) · [MIT License](LICENSE)

An open-source Codex Skill for evidence-traceable Voice of Customer (VOC) analysis across marketplace reviews and social comments.

It turns Excel/CSV/JSON review data from Amazon, JD, Tmall, YouTube, Xiaohongshu, and similar sources into structured, editable product-research reports while guarding against common analysis errors such as competitor misattribution, negation reversal, duplicated reviews, and promotional-copy contamination.

## Why this Skill exists

Keyword counting is not enough for reliable VOC work. A phrase such as “AirPods hurt, so I switched to this product” describes a competitor pain and a purchase reason—not a pain point of the target product. Likewise, “it does not leak sound” must not be counted as a leakage complaint.

This Skill therefore applies four evidence gates before accepting a signal:

1. **Subject** — Which product is the statement actually about?
2. **Polarity** — Is the meaning positive, negative, neutral, hypothetical, or negated?
3. **Experience** — Is this a real usage report, a question, a reply, or marketing copy?
4. **Specificity** — Does the text support the exact category being claimed?

## Highlights

- Cleans, normalizes, and deduplicates review samples with an auditable Python CLI.
- Separates marketplace reviews, full social posts, replies, and search-card/promotional evidence.
- Supports multi-label coding with row-level deduplication and explicit denominators.
- Requires manual verification of every product pain-point assignment.
- Produces editable three-column VOC reports with consistent visual emphasis.
- Covers purchase reasons, satisfaction, pain points, usage scenarios, unmet needs, personas, and custom product dimensions.
- Uses only the Python standard library for the bundled utilities.

## Repository structure

```text
.
├── SKILL.md                         # Main workflow and quality gates
├── agents/openai.yaml               # Display metadata and default prompt
├── references/
│   ├── evidence-and-counting.md     # Evidence hierarchy and counting rules
│   └── report-and-delivery.md       # Report format and delivery contract
├── scripts/
│   ├── audit_review_csv.py          # Deterministic CSV/TSV cleanup and audit
│   └── render_voc_html.py           # Editable three-column HTML renderer
├── examples/                        # Synthetic, privacy-safe demo inputs
└── tests/                           # CLI regression tests
```

## Install

Clone the repository into your Codex skills directory:

```bash
git clone https://github.com/s61238888-oss/analyze-product-voc-skill.git ~/.codex/skills/analyze-product-voc
```

Restart Codex if the Skill is not detected immediately.

## Use in Codex

Attach or point to a review dataset, then use a prompt such as:

```text
Use $analyze-product-voc to analyze these product reviews. Separate evidence by platform, report the effective sample size and exclusions, and produce an editable three-column VOC report.
```

The Skill is designed to work with spreadsheet/document/browser capabilities when those are available in the Codex environment.

## Run the utilities directly

Audit and clean a CSV:

```bash
python3 scripts/audit_review_csv.py examples/reviews.example.csv \
  --text-col review \
  --platform-col platform \
  --id-col review_id \
  --output-dir /tmp/voc-audit
```

Render an editable HTML report fragment plus a plain-text fallback:

```bash
python3 scripts/render_voc_html.py examples/report-spec.example.json \
  --html /tmp/voc-report.html \
  --text /tmp/voc-report.txt
```

Run the regression tests:

```bash
python3 -m unittest discover -s tests -v
```

## Method contract

- The denominator is the number of unique, effective reviews/posts in the declared evidence layer.
- Each row is counted at most once per theme, while one row may contribute to multiple themes.
- Positive/negative combined dimensions use the union of row IDs rather than summed buckets.
- Social search cards and promotional summaries may support attention analysis, but not satisfaction or pain claims.
- Unmet needs must be derived from explicit failures, limitations, workarounds, requests, or trade-offs.
- Demographic and persona claims must remain evidence-based.

## Privacy

The repository contains no real customer reviews or proprietary product data. All example rows are synthetic and included solely to demonstrate the workflow.

## License

Released under the [MIT License](LICENSE).
