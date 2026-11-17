# 2026-11-17｜进门标价签，出门贴日期

> 发布端把账单当头牌数据，退役端按日历关门，改进端交给 agent——唯独使用方写死的那行模型名，还在手工对齐。

**标签**：`#模型生命周期` `#退役与迁移` `#成本结构` `#自动化科研` `#开源权重`
**生成时间**：2026-11-17 12:10（北京时间）

---

## 一、今日观察

过去 24 小时的新闻放在一起看，会发现模型的"新陈代谢"三个端口都在提速，但提速的方向各不相同：

- **进门（发布）**：阿里 Qwen4-Max 正式版昨天上线。注意它发布的头牌数据不是跑分第一——CodeArena 只排第六——而是**完成单任务平均费用较上代降 58%**、缓存命中 0.5 元/百万 tokens、激活参数比上代少 25%。发布叙事的重心已经从"我多强"挪到了"我省你多少钱"。
- **保养（改进）**：Salesforce 公开的 SFR-AutoR&D 把"改进模型"这件事本身交给 agent 跑：一轮完整实验周期约 80 小时，而人类研究者传统上要几周。基线的更新速度从"人周"换成"机时"。
- **出门（退役）**：今天（11 月 16 日）正是 GitHub Copilot 三个模型（Claude Opus 4.8、Claude Opus 5、GPT-5.6 Terra）从所有 Copilot 体验中退场的生效日。这是六周内第三波，10 月 2 日和 10 月 19 日还各退役过一批。官方退役历史表里，日期列得清清楚楚。

三个端口都在加速，只有一个环节没有变快：**你把模型名写进配置文件的那只手**。CI 里的 `--model` 参数、`.github/copilot/settings.json`、prompt 里 pin 死的模型 ID——这些不会跟着厂商的日历自动改。GitHub 官方的说法是"模型下架后无需任何移除动作"，那是对 picker 而言的；对写死模型名的工作流而言，生效日就是失效日。

| 端口 | 今天谁在动 | 节奏由什么决定 | 落到使用方头上的是什么 |
| :--- | :--- | :--- | :--- |
| **进门** | 阿里 Qwen4-Max 正式版（2.4T 总参 / 71B 激活） | 架构与缓存定价 | 重算预算；等中小尺寸开源 |
| **保养** | Salesforce SFR-AutoR&D（约 80 小时一轮） | agent 实验循环 | 你引用的"基线"自己会动 |
| **出门** | GitHub Copilot 三模型退役生效 | 分发方的日历（六周三波） | 写死的模型名失效 |
| **换血** | Agnes 2.5 Pro Theta / 华为 CloudRobo-WM1.2 开源 | 许可证与权重体积 | 硬件门槛（BF16 约 375.5 GB）与合规评估 |

值得警惕的一点：退役这件事有个容易误读的地方——**11 月 16 日关掉的是 Copilot 这个分发通道，不是模型本身**。Anthropic 自己的退役页把 Opus 5 标为"活跃、不早于 2027-07-24 退役"。模型活着，只是有一条路被指到了别处。对依赖单一分发通道的团队来说，这条路就是全部。

需要交代两句撞题：Qwen4-Max 的 preview 版（1M 上下文、39.3 万输出预算、限时供应）我在 11-12《快不是算得快，是少算几遍》写过，本轮写的是正式 GA 的新增信息；"cost per task"作为计价思路 09-04《任务计价与开放分发》讨论过，本轮的增量是**它第一次被厂商拿来做发布会的头牌数据**；"配置层变更不通知你"是 10-26 那篇的主线，本轮不同之处在于——退役是**有日期、有 changelog、提前一个月通知**的配置变更，是配置层变化里最体面的一种，剩下的静默替换才是常态。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 Qwen4-Max 正式发布：发布会的头牌数据是省钱，不是跑分
11 月 16 日，阿里巴巴发布新一代基座大模型 Qwen4-Max：**总参数 2.4T、每 token 激活 71B**（较上代少 25%），采用基于 Qwen 稀疏注意力（QSA）的全新 MoE 架构，原生视觉能力，百万上下文。在 Terminal-Bench 4.0 编程评测中，**每次尝试平均 token 用量从 289K 降至 151K（约 −48%）**，评测得分升至 **48.5 分**（媒体对上代基线分口径略有出入，一说 38.9、一说 37.9）。已上线千问 AI 平台 API：**缓存命中 0.5 元/百万 tokens，完成单任务平均费用较 Qwen3.8-Max 降 58%**。全球前端编程盲测 CodeArena 排名第六。阿里同时宣布 Qwen4 系列中小尺寸模型将陆续开源。
来源：[上海证券报·中国证券网](https://www.cnstock.com/commonDetail/828899)｜[澎湃新闻](https://m.thepaper.cn/newsDetail_forward_34489096)｜[新京报贝壳财经](https://news.qq.com/rain/a/20261116A08BZ500)｜[南方都市报](https://www.163.com/dy/article/LBU3S20N05129QAF.html)

### 2. 🟢 GitHub Copilot 三个模型今天退役生效，六周内第三波
GitHub 官方 changelog（10-15 发布）：**11 月 16 日起，Claude Opus 4.8、Claude Opus 5、GPT-5.6 Terra 从所有 Copilot 体验（Chat、行内编辑、ask/agent 模式、代码补全）退场**。指定替代：Opus 系列换 Claude Opus 5.5，Terra 换 GPT-6.1 Sol 或 GPT-6 Luna。唯一例外：**年费个人订阅者保留 Opus 4.8**。官方文档的退役历史表显示 10-02 已退役 Opus 4.7、Gemini 3.5/3.6 Flash、Kimi K2 等一批，10-19 又退役 Gemini 3.7 Flash、GPT-5.4、GPT-5.5 等。注意：退役的是 Copilot 内的分发通道——Anthropic 官方页显示 Opus 5 本体活跃至"不早于 2027-07-24"。
来源：[GitHub 官方 Changelog](https://github.blog/changelog/2026-10-15-upcoming-deprecation-of-selected-github-copilot-models-in-mid-november/)｜[GitHub 官方文档·退役历史表](https://docs.github.com/en/copilot/reference/ai-models/supported-models)

### 3. 🟢 Salesforce 公开 SFR-AutoR&D：agent 自己跑研发循环，一轮约 80 小时
11 月 11 日 Salesforce AI Research 发布 SFR-AutoR&D：给定目标、系统和算力预算，agent 自动提出假设、实现方法、对照基线跑受控实验，**只在证据支持时保留改动**。把它指向开源模型 EmbeddingGemma 2 产出 SFR-Embedding v4，在 MTEB 十项公开检索任务上 **nDCG@10 提升 6.13 分**（研究检查点 51.07 → 57.21，公司自报、非官方榜单排名）；另一轮约 9 小时的效率优化带来**吞吐 +36%、延迟 −17%**。工程侧还改了 pandas（可空类型归约最高 1.84×，经 134,064 个差分测试，已提上游 PR）、hnswlib、USearch。首席科学家 Silvio Savarese："科学方法仍是准则，只是整个循环跑得更快了。"
来源：[Unite.AI 中文详述](https://www.unite.ai/zh-cn/salesforces-sfr-autor-and-d-automates-model-research-and-validation)｜[TSNMedia（引官方 newsroom）](https://tsnmedia.org/sfr-autornd)｜[AI Affairs（引 salesforce.com）](https://www.aiaffairs.com/technology/salesforce-sfr-autord-embedding-models)

### 4. 🟢 华为云发布并开源昇腾原生具身世界模型 CloudRobo-WM1.2，11-30 开放权重
11 月 16 日发布会宣布：首款昇腾原生具身世界模型 CloudRobo-WM1.2，基于世界模型原生 DualAct 架构把"看懂物理世界"和"生成动作"放进同一个模型，称在 RoboTwin 2.0、LiberoPro 2.0 两基准均排名第一（厂商口径）。针对真机数据贵（每小时 500–2000 元）的问题，采用"多粒度监督数据自适应预训练"，让残缺数据也能参与训练；跨本体泛化靠保留机器人 96 维、人类 168 维原生物理语义。**11 月 30 日起开放权重、推理与后训练代码**。
来源：[中国青年报](https://www.163.com/dy/article/LBST30E10514CDBK_pdya11y.html)｜[每经·数智早参](https://news.qq.com/rain/a/20261117A02VJ800)｜[财闻·发布会详述](https://www.163.com/dy/article/LBSJ8DDR0550WHYR.html)

### 5. 🟢 新加坡 Agnes AI 开源 187.8B 多模态 MoE，Apache 2.0（分数为厂商自报）
11 月 15 日在 Hugging Face 发布 Agnes 2.5 Pro Theta：**总参数约 187.8B、512 路专家 top-10 路由 + 共享专家、上下文 262,144 tokens、Apache 2.0**。BF16 权重约 375.5 GB，建议 4×H200 起步。模型卡自报 GPQA Diamond 92.9、LiveCodeBench v6 90.5，**未经独立验证**。另：llm-releases 目录显示 11-16 正式版 Qwen4-Max 定价为 $1.50/$4.50 每百万输入/输出 tokens（缓存输入 $0.075），此为聚合站口径，与人民币官方价的关系待官方页核实。
来源：[LLM Releases 目录](https://llm-releases.com/open-weight-models)｜[Daily AI Brief](https://dailyaibrief.com/news/agnes-ai-publishes-187-8b-multimodal-model-017rSD2L)｜[Hugging Face 模型页](https://huggingface.co/Agnes-AI/Agnes-2.5-Pro-Theta)｜[TechDaily](https://news.techdou.com/)

### 6. 🟡 MiniMax M2.5 / M2.7 将于 11-18 退出按量付费 API
聚合站 Standard Compute 的口径：**11 月 18 日起 M2.5 与 M2.7 从按量付费 API 移除**，同期还有 11-30 Claude Sonnet 4.5 退出 Claude API、Opus 4.8 fast mode 关闭。仅单一聚合源，待官方公告核实。
来源：[Standard Compute](https://standardcompute.com/ai-coding-plan-changes)

---

## 三、为什么值得记

1. **发布会的头牌数据换了。** Qwen4-Max 排 CodeArena 第六，但官方通稿反复强调的是 −58% cost per task 和 0.5 元缓存价。这说明"任务费用"已经从分析框架变成营销主叙事——厂商自己承认，企业买家算的是账单不是榜单。对选型者的直接含义：**比较两个模型时，先对齐"完成我的任务"口径的成本，再看跑分**。

2. **退役是配置层变更里最体面的一种，但它恰恰证明了 10-26 那篇的判断。** GitHub 提前一个月发 changelog、文档里挂着退役历史表、还给了 model policy API——通知机制不可谓不完善。可即便如此，失效的还是那些写死的模型名，因为**通知到达的是"看 changelog 的人"，失效的是"三个月前写下的配置"**。有日期的退役都尚且如此，没有日期的静默替换（10-26 的 Unspecified → Argon）只会更糟。

3. **"改进模型"本身正在变成 agent 的工作。** SFR-AutoR&D 的关键不是 6.13 分，而是它的验证纪律：改动只在证据支持、通过了 13 万多个差分测试后才保留。这给所有"AI 改代码"团队立了个模板——**自动化生成的改动，配得上自动化验证**；只有生成没有验证的 agent 流水线，产出的是负债。

4. **开源的门槛在从许可证问题变成硬件问题。** Agnes 188B 是 Apache 2.0，法律上随便用；但 BF16 权重 375.5 GB、建议 4×H200。对多数团队，真正的准入条件早已不是"能不能下载"，而是"养不养得起这排卡"——这正是昨天 11-16 那篇《开源拆成了两个承诺：能下载，和能复现》的延续。

---

## 四、可行动

- [ ] **今天就把工作流里写死的模型名过一遍**：`grep -r "opus-4.8\|opus-5\b\|5.6-terra\|gpt-5.6"` 扫 CI 脚本、`.github/copilot/settings.json`、`.github/allowed_models.txt`、agent 定义文件和 Copilot CLI 的 `--model` 参数，逐个换成官方指定替代（Opus 5.5 / GPT-6.1 Sol / GPT-6 Luna）。
- [ ] **给模型依赖建一张带到期日的登记表**：每个被 pin 的模型记三列——上游官方退役日期（Anthropic/OpenAI 页）、分发通道退役日期（Copilot/IDE changelog）、替代模型 ID。11-30（Sonnet 4.5 退 API、Opus fast mode 关闭）和 12 月底（Kimi K2 全量退役）是接下来的两个已知节点。
- [ ] **用缓存命中价重算一遍现有工作流的账单**：如果你们的调用有大量重复前缀（system prompt、长上下文、few-shot），把 0.5 元/百万 tokens 的缓存命中价代入——Qwen4-Max 官方那个 −58% 就是从这里来的，你的场景降幅可能同样可观。
- [ ] **换模型必跑一次固定评估集**：替代模型的输出格式、工具调用行为与旧版未必一致（11-02 写过 Kimi K3.1 Pro 默认 max thinking 档位的坑）。迁移前用既有 prompt 和测试集重跑，别等线上出错才发现。
- [ ] **读一遍 SFR-AutoR&D 的验证纪律**：如果你在搭"AI 改进 AI/代码"的内部流程，照它的三件套检查自己——改动是否只在通过 held-out 基准时保留、是否有差分测试兜底、失败是否回退到原实现。

---

## 五、术语卡

| 术语 | 解释 |
| :--- | :--- |
| **激活参数（active params）** | MoE 模型每次前向实际参与计算的参数量。Qwen4-Max 总参 2.4T 但每 token 只激活 71B——算力账单跟着激活量走，而非总参数量。 |
| **缓存命中计价（cached input）** | 对与历史请求重复的前缀部分按折扣价计费。前缀重复率高的工作流（固定 system prompt、长上下文）受益最大，0.5 元/百万 tokens 意味着命中部分约为常规输入价的零头。 |
| **模型退役（deprecation）** | 供应商从某分发渠道移除某模型。注意与"模型下线"区分：Copilot 11-16 退役的是通道，Opus 5 在 Anthropic 官方渠道仍可用至 2027 年年中。 |
| **nDCG@10** | 信息检索质量指标：衡量前 10 条结果里相关内容是否排在靠前位置，越靠前得分权重越高。SFR-AutoR&D 的 +6.13 是分数提升，不是百分比。 |
| **具身世界模型（embodied world model）** | 让机器人不只"看见"画面，还能预测"我动了之后世界怎么变"的模型。华为 WM1.2 的卖点是把它与动作生成合并进同一个模型，省掉两套系统之间的对接模块。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
