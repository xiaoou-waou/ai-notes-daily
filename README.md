# ai-notes-daily

> 一个每天自己长出来的 AI 笔记本。

每天中午 12:00 生成一篇 AI 相关笔记：联网检索当日真实信息（模型发布、开源项目、Agent/RAG 工程实践、行业动态），交叉验证后写成结构化笔记，写入 `notes/`，并自动更新下面的目录。

**原则：不瞎编。** 每条事实都带可点击的原始来源链接；检索不到可靠信源时，宁可写"今日无可靠新增"，也不编造。

---

## 📚 目录

<!-- NOTES_INDEX_START -->
> 共 **18** 篇 · 覆盖 2026-09-02 → 2026-09-25 · 最新在最上

| 日期 | 标题 | 标签 |
| :--- | :--- | :--- |
| `2026-09-25` | [今天最贵的失败，全都不报错](notes/2026-09-25-silent-failures-and-a-loud-judge.md) | `#评测` `#Agent` `#静默失败` `#工程陷阱` |
| `2026-09-24` | [今天最重要的一篇论文，学科分类不是 AI](notes/2026-09-24-runtime-layer-becomes-the-bottleneck.md) | `#Agent基础设施` `#开源` `#运行时` `#沙箱` |
| `2026-09-23` | [打的是地板，管的是天花板](notes/2026-09-23-fighting-the-floor-governing-the-ceiling.md) | `#价格战` `#推理工程` `#治理` `#Agent安全` `#国产算力` |
| `2026-09-22` | [「默认开启」是今天最贵的一个选项](notes/2026-09-22-defaults-are-the-expensive-option.md) | `#默认值` `#Agent安全` `#开源模型` `#决策模型` `#国产大模型` |
| `2026-09-21` | [「开源」今天被拆成了三道闸门](notes/2026-09-21-openness-splits-into-three-gates.md) | `#开源许可` `#评测` `#Agent安全` `#国产大模型` |
| `2026-09-20` | [两天复现一个模型，五天交付不了一个 App](notes/2026-09-20-capability-commoditized-engineering-priced.md) | `#LoRA` `#AgentHarness` `#Benchmark` `#推理工程` `#国产生态` |
| `2026-09-18` | [把黑箱拆成可归因的一层：从「结果不对」到「哪一步、为什么不对」](notes/2026-09-18-instrumenting-the-process-layer.md) | `#Agent` `#可观测性` `#推理优化` `#AI安全` `#国产生态` |
| `2026-09-17` | [同一张价目表，四倍账单：成本控制从单价转向路由、形态与供给](notes/2026-09-17-list-price-vs-actual-bill.md) | `#推理成本` `#模型路由` `#开源` `#Agent` `#国产生态` |
| `2026-09-16` | [能力收敛成采购参数，过程与责任开始分流](notes/2026-09-16-capability-converges-liability-diverges.md) | `#开源权重` `#Agent治理` `#模型选型` `#训练工程` `#国产大模型` |
| `2026-09-15` | [「数据怎么造」正在取代「模型有多大」](notes/2026-09-15-data-construction-over-parameter-scale.md) | `#微调` `#数据工程` `#Agent` `#开源` `#RSI` |
| `2026-09-14` | [开放正在分层：NVIDIA 把金牌的账单也开源了，而账单本身就是门槛](notes/2026-09-14-openness-splits-into-tiers.md) | `#开源` `#后训练` `#可复现性` `#端侧` `#Agent安全` |
| `2026-09-13` | [中间层：一边被穿透，一边被重建](notes/2026-09-13-middle-layer-penetrated-and-rebuilt.md) | `#蒸馏` `#AI治理` `#垂直化` `#开源` `#工程实践` |
| `2026-09-12` | [Agent 越界成为默认失败模式，行业开始把「审计」当产品卖](notes/2026-09-12-agent-overshoot-and-auditability.md) | `#Agent安全` `#可审计性` `#全双工语音` `#国产大模型` `#工程实践` |
| `2026-09-10` | [引用不等于使用：证据链上的审计缺口，和补它的三种价格](notes/2026-09-10-evidence-cited-but-not-used.md) | `#RAG` `#Agent安全` `#评测基准` `#开源模型` `#行业动态` |
| `2026-09-08` | [当模型不再是瓶颈：检索层、配方与供应链接管了 Agent 的天花板](notes/2026-09-08-agent-bottleneck-shifts.md) | `#Agent` `#RAG` `#开源` `#工程实践` `#国产大模型` |
| `2026-09-05` | [答案在贬值，验证在升值](notes/2026-09-05-verification-premium.md) | `#验证` `#形式化` `#Agent` `#RAG` `#开源` |
| `2026-09-04` | [成本单位从 token 换成 task，开源分发枢纽被买走](notes/2026-09-04-task-pricing-and-open-distribution.md) | `#成本` `#Agent` `#开源` `#分发` `#端侧` |
| `2026-09-02` | [推理成本的三条下降曲线](notes/2026-09-02-inference-cost-curves.md) | `#成本` `#Agent` `#开源` `#量化` `#端侧` |
<!-- NOTES_INDEX_END -->

---

## 说明

### 目录结构

```
ai-notes-daily/
├── README.md          ← 本文件，目录索引自动更新
├── notes/             ← 每日笔记，命名 YYYY-MM-DD-<slug>.md
└── scripts/
    └── update_index.py  ← 扫描 notes/ 重建顶部目录（幂等，可反复运行）
```

### 笔记里有什么

每篇笔记固定包含四块：

| 板块 | 作用 |
| --- | --- |
| **今日观察** | 一条主线观点，把当天散落的事件串起来 |
| **事实清单** | 每条事实 + 关键数据 + 原始来源链接 |
| **为什么值得记** | 判断：这事儿对我意味着什么 |
| **可行动** | 具体下一步，能落地的 checklist |

### 更新机制

由 WorkBuddy 定时任务驱动，每天 12:00（北京时间）：

1. 联网检索近 24–72 小时内的 AI 事实，多源交叉验证
2. 选定当日主线，写成笔记文件放入 `notes/`
3. 运行 `python3 scripts/update_index.py`，扫描 `notes/` 重建顶部由 `NOTES_INDEX` 注释包裹的目录区块（最新在最上）
4. `git commit` + `git push`

> ⚠️ 目录区块由程序维护，手动编辑会被下次生成覆盖。

---

<sub>由 WorkBuddy 自动维护 · 首次创建于 2026-09-02</sub>
