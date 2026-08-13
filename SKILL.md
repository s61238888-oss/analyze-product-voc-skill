---
name: analyze-product-voc
description: Analyze real product reviews and public comments from Excel, CSV, JSON, Amazon, JD, Tmall, YouTube, Xiaohongshu, or similar sources; clean and deduplicate samples; prevent competitor, negation, reply, or search-card misattribution; quantify purchase reasons, satisfaction, pain points, usage scenarios, unmet needs, personas, and requested product dimensions; and deliver editable three-column VOC reports to DingTalk or another document surface. Use when Codex is asked to perform product VOC, review mining, consumer-needs validation, competitor-review analysis, multi-platform comment analysis, or to reproduce this structured yellow-highlighted reporting format.
---

# Analyze Product VOC

Produce evidence-traceable VOC findings from real comments without keyword hallucination or product misattribution.

## Workflow

1. Inspect every source and establish the target product, platform, row unit, text field, review/reply relationship, and available metadata.
2. For `.xlsx`, `.xls`, `.csv`, or `.tsv`, use the Spreadsheets skill to inspect and extract rows. Preserve the source workbook.
3. Clean the sample before analysis:
   - Normalize whitespace and Unicode.
   - Exclude blank/default text and rows outside the target SKU or product.
   - Deduplicate within platform by normalized text.
   - Remove duplicated follow-up text when it is fully contained in the same review card.
   - Retain short comments when they contain a concrete product signal.
   - Run `scripts/audit_review_csv.py` after exporting the relevant sheet to CSV when a deterministic audit is useful.
4. Record the effective sample size by platform and the exact exclusion reasons.
5. Code themes as multi-label. Count each review at most once per theme.
6. Manually verify every row assigned to a pain point. For large datasets, automation may propose candidates, but the final negative count must be based on explicit product-specific negative meaning.
7. Generate the report using the requested dimensions plus the six standard VOC groups:
   - 用户购买原因
   - 满意点
   - 不满意点（痛点）
   - 使用场景
   - 未被满足的需求
   - 用户画像
8. Separate sources whose evidence strength differs. Do not merge marketplace purchase reviews with social search cards, promotional summaries, questions, or creator replies.
9. Render or write the deliverable, verify it, and leave it editable.

## Evidence Rules

Read `references/evidence-and-counting.md` before classifying negatives, competitor comparisons, social posts, or ambiguous rows.

Apply these gates to every claimed signal:

1. **Subject**: Is the statement about the target product?
2. **Polarity**: Is it actually positive, negative, neutral, hypothetical, or negated?
3. **Experience**: Is it a real usage report, a question, a feature claim, a recommendation, or a search-card summary?
4. **Specificity**: Does the text support this exact category?

Never:

- Convert “其他耳机不舒服，所以买了本产品” into a pain point for the target product.
- Convert “本机不疼”“没有漏音”“连接不断” into the opposite pain point.
- Attribute a reply, quotation, or comparison subject to the target product without resolving the subject.
- Treat a promotional feature list as user satisfaction.
- Invent demographics, motivations, or unmet needs not supported by the text.

Derive unmet needs only from an explicit failure, limitation, workaround, requested improvement, or clearly stated tradeoff. Phrase weak signals as directional rather than definitive.

## Counting Contract

- Use unique effective reviews/posts as the denominator.
- Calculate `提及占比 = unique rows mentioning theme / corresponding effective sample`.
- Allow one row to contribute to multiple themes; state that percentages do not sum to 100%.
- Use separate denominators when evidence layers differ, such as all social cards for topic attention versus full-text posts for satisfaction and pain.
- Show both percentage and count: `12.3%（37/301）`.
- For a combined positive/negative dimension, calculate the union of row IDs. Do not add bucket counts without removing overlaps.
- Keep an internal evidence table with sample ID, platform, product subject, polarity, theme, and decision. Do not expose original comments unless the user asks.

## Report Structure

Read `references/report-and-delivery.md` before generating a document or writing to DingTalk.

Default structure:

1. Title and date
2. Yellow sample-scope callout
3. Yellow counting/anti-hallucination callout
4. One main section per evidence source or source group
5. Requested product-dimension validation table
6. Six standard VOC tables
7. Cross-source real-demand conclusions

Use exactly three columns per table:

`主题 | 提及占比 | 原因/洞察`

Adapt the first and third headers to the section. Omit the original-comment/evidence column unless explicitly requested. Use yellow background and bold text for section titles, table headers, and key conclusions.

Use `scripts/render_voc_html.py` when a reusable rich-text fragment is helpful. Paste the generated HTML fragment plus its plain-text fallback into the destination.

## DingTalk Delivery

Before browser work, search for a purpose-built DingTalk/document connector. If none can perform the edit, use the available Browser or Chrome skill.

1. Open or claim the exact user-specified document.
2. Switch the document to `编辑 → 可编辑文档`.
3. Paste structured rich text rather than a screenshot or flattened file.
4. Confirm the document contains all sections, has no unwanted evidence column, and shows yellow bold headers.
5. Confirm saved state.
6. Leave the document open in editable mode with font, size, bold, text color, and highlight controls available.

Do not change sharing permissions, publish externally, or replace unrelated existing content without explicit authorization.

## Final Quality Gate

Do not finish until all checks pass:

- Effective sample totals reconcile with exclusions.
- Every pain count has passed subject and polarity review.
- Social cards are not used as experience evidence.
- Percentages use the declared denominator and row-level deduplication.
- User portraits remain evidence-based.
- The report uses platform/source sections and three-column tables.
- Yellow bold emphasis is present.
- The original-comment column is absent unless requested.
- The destination is saved and editable.
