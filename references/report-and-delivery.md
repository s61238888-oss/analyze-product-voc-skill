# Report and Delivery Contract

## Three-column tables

Use one table per section. Recommended headers:

| Section | Column 1 | Column 2 | Column 3 |
|---|---|---|---|
| 需求验证 | 需求维度 | 提及占比 | 验证结论 |
| 购买原因 | 用户购买原因 | 提及占比 | 原因/洞察 |
| 满意点 | 满意点 | 提及占比 | 原因/洞察 |
| 痛点 | 不满意点（痛点） | 提及占比 | 负向原因 |
| 使用场景 | 使用场景 | 提及占比 | 场景说明 |
| 未满足需求 | 未被满足的需求 | 提及占比 | 机会说明 |
| 用户画像 | 用户画像 | 提及占比 | 画像说明 |

Do not add `原评论代表摘取`, `证据原文`, or a fourth column unless the user asks.

## Visual style

- Use yellow `#FFE699` for section-title highlights and table headers.
- Use pale yellow `#FFF2CC` for scope, method, caution, and conclusion callouts.
- Bold titles, table headers, and the leading label in each conclusion.
- Keep body copy dark, concise, and left aligned.
- Prefer one decimal place for percentages.
- State sample counts and exclusions near the top.

## Required scope note

Include:

- Platform sample sizes
- Deduplication and boilerplate exclusions
- Denominator definition
- Multi-label warning
- Product-attribution and negation rule
- Social evidence-layer rule when applicable

## Renderer input

`scripts/render_voc_html.py` accepts JSON shaped like:

```json
{
  "title": "产品 VOC 分析",
  "subtitle": "数据截至 2026-07-29",
  "callouts": [
    {"label": "样本口径", "text": "京东 204 条，天猫 286 条。"}
  ],
  "sections": [
    {"kind": "heading", "title": "一、京东 + 天猫"},
    {
      "title": "1. 用户购买原因",
      "base": 490,
      "headers": ["用户购买原因", "提及占比", "原因/洞察"],
      "rows": [
        {"label": "开放式舒适佩戴", "count": 148, "insight": "拒绝入耳和长时佩戴需求明显。"}
      ]
    }
  ],
  "conclusions": [
    {"label": "舒适是第一门槛", "text": "继续优化轻量和耳型覆盖。"}
  ]
}
```

The renderer emits an HTML fragment rather than a full HTML document so a browser paste does not insert a duplicate `<title>` line.

## DingTalk verification

After pasting:

1. Check the title and sample callouts.
2. Scroll through the first marketplace table, the social-source heading, one pain table, and the final conclusions.
3. Verify `原评论代表摘取` is absent.
4. Verify yellow headers visually.
5. Verify the top toolbar exposes font, style, size, bold, text color, and highlight controls.
6. Verify `已保存`.
7. Leave the target document open as the deliverable.
