# 产品 VOC 分析 Skill

[English](README.md) · [Skill 定义](SKILL.md) · [MIT 许可证](LICENSE)

这是一个面向 Codex 的开源产品 VOC（消费者之声）分析 Skill。它可以处理 Amazon、京东、天猫、YouTube、小红书等来源的评论数据，经过清洗、去重、证据分层与人工核验后，输出结构化、可编辑的产品洞察报告。

## 它解决什么问题

传统关键词统计很容易造成错误归因。例如，“AirPods 戴久了疼，所以换了这款产品”描述的是竞品痛点和本产品购买原因，不能算作目标产品的痛点；“这款不漏音”也不能被关键词规则反向统计为漏音投诉。

因此，本 Skill 在接受任何信号前都会检查四个证据条件：

1. **主体**：这句话实际描述的是哪个产品？
2. **极性**：它是正向、负向、中性、假设，还是包含否定？
3. **体验类型**：它是真实使用、提问、回复，还是营销文案？
4. **具体性**：原文是否足以支撑当前分类？

## 核心能力

- 使用可审计脚本规范化、清洗并去重评论样本。
- 区分电商购买评价、完整社交帖子、回复、搜索卡片与宣传内容。
- 使用多标签编码，每条评论在单一主题下只计一次。
- 要求对所有产品痛点候选进行人工逐条复核。
- 输出带统一黄色强调样式的可编辑三列表格报告。
- 覆盖购买原因、满意点、痛点、使用场景、未满足需求、用户画像和自定义产品维度。
- 内置工具只依赖 Python 标准库。

## 项目结构

```text
.
├── SKILL.md                         # 主工作流与最终质量门槛
├── agents/openai.yaml               # 展示信息和默认提示词
├── references/
│   ├── evidence-and-counting.md     # 证据分层与计数规范
│   └── report-and-delivery.md       # 报告结构与交付规范
├── scripts/
│   ├── audit_review_csv.py          # CSV/TSV 清洗与审计
│   └── render_voc_html.py           # 可编辑三列表格 HTML 渲染器
├── examples/                        # 完全脱敏的合成演示数据
└── tests/                           # 命令行回归测试
```

## 安装

把仓库克隆到 Codex Skills 目录：

```bash
git clone https://github.com/s61238888-oss/analyze-product-voc-skill.git ~/.codex/skills/analyze-product-voc
```

如果没有立即识别到该 Skill，请重启 Codex。

## 在 Codex 中使用

提供评论数据后，可以输入：

```text
使用 $analyze-product-voc 分析这些产品评论。请按平台拆分证据，说明有效样本量和排除原因，并生成可编辑的三列表格 VOC 报告。
```

当环境中提供表格、文档或浏览器能力时，本 Skill 会调用相应能力完成数据读取和文档交付。

## 直接运行配套工具

清洗并审计 CSV：

```bash
python3 scripts/audit_review_csv.py examples/reviews.example.csv \
  --text-col review \
  --platform-col platform \
  --id-col review_id \
  --output-dir /tmp/voc-audit
```

生成可编辑 HTML 片段和纯文本备用内容：

```bash
python3 scripts/render_voc_html.py examples/report-spec.example.json \
  --html /tmp/voc-report.html \
  --text /tmp/voc-report.txt
```

运行测试：

```bash
python3 -m unittest discover -s tests -v
```

## 分析口径

- 分母是对应证据层中去重后的有效评论或帖子数。
- 每条评论在同一主题下最多计数一次，但可以进入多个不同主题。
- 合并正负维度时使用评论 ID 并集，不能直接相加两个分组。
- 社交平台搜索卡片和宣传摘要只能支持话题关注度分析，不能证明满意点或痛点。
- 未满足需求必须来自明确失败、限制、替代方案、改进要求或取舍。
- 用户画像必须有文本证据，不虚构年龄、性别、收入或职业。

## 隐私说明

仓库中不包含真实消费者评论、公司内部文件或专有产品数据。示例数据全部为合成内容，仅用于展示工作流。

## 许可证

本项目采用 [MIT License](LICENSE) 开源。
