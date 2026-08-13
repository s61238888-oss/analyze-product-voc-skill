# Evidence and Counting Rules

## Evidence hierarchy

Use the strongest available evidence for experience claims:

1. Verified-purchase or marketplace review with original text
2. Full social post describing concrete use
3. Top-level video comment describing concrete use
4. Reply whose product subject is explicit
5. Search-card title, snippet, feature list, or promotional copy

Levels 1–4 can support experience claims after subject and polarity checks. Level 5 can support attention or messaging analysis only.

## Subject resolution

Resolve the grammatical subject before coding:

| Text pattern | Correct treatment |
|---|---|
| “AirPods 戴久了疼，所以换了 X8，X8 很舒服” | AirPods pain is a purchase reason; X8 comfort is satisfaction |
| “这款不漏音” | X8 leak-control satisfaction, not a leak pain |
| “评论说会断连，但我没遇到” | Do not count X8 disconnection pain |
| “朋友说通话差” | Third-party report; label separately or exclude from firsthand satisfaction |
| Creator reply recommends another product | Do not attribute that product's property to X8 |

When multiple products occur in one row, split the statement into subject–predicate pairs before assigning themes.

## Polarity and negation

Inspect the full clause, not isolated keywords.

Common false positives:

- 不疼、不会疼、久戴不痛
- 不压耳、无压迫、没有不适
- 不漏音、没感觉到漏音、漏音可控
- 不断连、没有延迟、连接稳定
- 没有杂音、没有误触

Contrast markers such as `但`, `不过`, `就是`, `唯一不足`, `缺点`, `希望`, and `如果` often change polarity. Code each clause independently.

## Experience versus claim

Treat language as a feature claim rather than satisfaction when it only repeats specifications, marketing copy, or broad praise without use context. Concrete details include time, place, device, action, comparison condition, workaround, or observed outcome.

For social sources:

- Use all collected posts/cards to describe topic attention.
- Use complete bodies with concrete experience for satisfaction, pain, scenarios, unmet needs, and personas.
- Flag suspected promotional wording and avoid generalizing its superlatives.

## Standard taxonomy

Use the user's requested categories first. Common product dimensions include:

- AI功能
- 佩戴/耳型适配
- 舒适度
- 音质/音量/调音
- 漏音/隐私
- 续航/充电
- 通话/麦克风/降噪
- 运动稳固/防水/环境感知
- 连接/延迟/多设备
- 操控/APP
- 外观/质感/配色
- 价格/性价比
- 配件/收纳/查找

Keep `佩戴/耳型适配` and `舒适度` separate when the user asks for both. For a combined summary, use the union of review IDs.

## Six VOC groups

- **购买原因**: Explicit decision driver, comparison criterion, replacement motive, gift motive, recommendation source, or problem prompting purchase.
- **满意点**: Positive outcome experienced on the target product.
- **痛点**: Explicit negative outcome experienced on the target product.
- **使用场景**: Concrete context such as commute, office, meetings, calls, sports, travel, study, sleep, or entertainment.
- **未满足需求**: Explicit requested improvement, workaround, limitation, or reliable opportunity derived from a pain.
- **用户画像**: Evidence-based role or need state such as commuter, office worker, runner, sensitive-ear user, glasses wearer, student, creator, or price-sensitive buyer.

Do not infer age, gender, income, occupation, or medical status without evidence.

## Counting

For each theme:

1. Build a set of unique sample IDs.
2. Count the set size.
3. Divide by the declared platform/evidence-layer denominator.
4. Show one decimal place and the raw fraction.

If the same review repeats the same theme, count it once. If it mentions multiple themes, count it once in each theme. If two buckets are merged, use set union rather than adding counts.

Small counts remain valuable when the issue is high risk. Label them as low-frequency, directional, or high-sensitivity rather than claiming broad prevalence.
