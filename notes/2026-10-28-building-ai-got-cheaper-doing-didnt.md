# 2026-10-28｜造模型的门槛塌到一个人，干活的门槛还差十倍

> 同一家公司今天给出两个数：agent 写了 99% 的代码训出模型，而模型在 Terminal-Bench 4.0 只拿到 6.1%。

**标签**：`#模型发布` `#Agent工程` `#开源权重` `#行业动态`
**生成时间**：2026-10-28 12:45（北京时间）

---

## 一、今日观察

今天最值得记的不是任何一个发布，而是**同一份材料里并存的两个数字**。

Mirendil 在 10 月 21 日的官方博客里说：一个研究员、3.5 个月、不到 1000 万美元算力，从空仓库起手训出了 100B–500B 参数的 base 模型，其中 **>99% 的工程代码由 AI agent 编写、运行并自行诊断报错**。五天后（10 月 26 日）同一家公司发布 Fern 0.1，在自己官方页的 benchmark 表里写着：这个**明确为「跑命令、读输出、直到测试通过」而设计的模型**，在 Terminal-Bench 4.0 上只有 **6.1%**——同一张表里 Claude Opus 5.5 是 **66.4%**。

agent 已经能顶替一整个 pretraining 团队，却还顶替不了一个在终端里干活的初级工程师。这两个数出自同一家公司、相隔五天。

把今天的新闻按「一道活儿」重排，而不是按公司排，会看到一条很干净的分界线——**凡是「造 AI」的活，门槛今天都在塌；凡是「用 AI 干活」的活，门槛基本没动。**

| 这道活儿 | 今天谁给了数字 | 门槛 |
|---|---|---|
| 写训练框架、数据管线、算子优化 | Mirendil 官方博客：**>99%** 的工程代码由 agent 编写、运行、自诊断报错 | **塌了**：人只剩「定方向、分配算力、判断结果可信与否」 |
| 从零预训练一个 100B–500B 的 base | 同一项目：**1** 名全职研究员、**3.5 个月**、**<$1000 万**算力（含全部探索实验、agent token 开销与数据处理） | **塌了**：组织门槛从「一支 pretraining 团队」降到「一个人 + 算力」 |
| 拿到可用的开源权重 | Nanbeige4.3-33B（**Apache 2.0**、33B dense、524,288 上下文）已上 Hugging Face；Kimi K3.1 Pro 承诺 **11-4** 前放出完整权重 | **塌了**：权重与许可都不再是瓶颈 |
| 让它在终端里独立干完一个任务 | Mirendil 官方表：Fern 0.1 **Terminal-Bench 4.0 = 6.1%**，同表 Claude Opus 5.5 **66.4%**、GPT-6 Astra **57.9%**、Kimi-K3 **12.6%** | **没塌**：差约 11 倍 |
| 让它在超长上下文里真的「用上」信息 | 同一官方页：RULER 单针检索 32K→10M 全程 **100%**，多跳 HotpotQA 从 **65%** 掉到 **45%**（10M 格只有 20 个样本，其余 100 个） | **没塌**：装得下 ≠ 用得上 |
| 让世界模型实时保持连贯 | DeepMind 官方博客：Genie 4 实时 in-the-loop 由 **Gemini 3.8 Flash** 驱动（旗舰 Argon 只用于机器人实验）；官方自承只能在 **short sessions** 内维持连贯、物体持久性会漂移 | **没塌**：靠降级模型换实时 |
| 让企业敢把生产交给它 | Anthropic S-1：H1 营收 **162.86 亿**美元、算力与基础设施支出 **89.45 亿**、该支出占营收比从 **201% 降到 55%**；但「承诺了多少钱」没有一个数字是招股书自己给的 | **反向抬升**：钱、电、承诺全在加码 |

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 一个人、3.5 个月、不到 1000 万美元，从空仓库训出 100B–500B base 模型

Mirendil 官方博客（**10-21 发布**，《Pretraining at scale without a pretraining team》）：Mirendil-Base 由**一名研究员**在 **3.5 个月**内完成，算力花费 **<$10M**，且这个数字是 all-in——包含全部前期小规模探索实验、agent 的 token 开销和数据处理，**没有蒸馏、没有购买或授权任何额外数据**。原文：*"AI agents wrote over 99% of the code, ran experiments and diagnosed failures, while the researcher decided what to try and what to trust, and intervened when needed."*

外部对照数据（7 个**在模型训练截止后才公开**的仓库，bits per byte，越低越好）：Mirendil-Base **0.222**，Kimi-K3 **0.193**，DeepSeek-V4-Pro-Base **0.243**，GLM-5.3 **0.242**，Nemotron-550B-Base **0.247**。

规模与进度：Base 100B–500B；Base-Large（500B–2T）**约 80%**；Base-XL（2T–10T）**约 19%**，已接近 Large 当前水平。

官方对「递归自我改进」的原话很克制：*"We don't think we have reached fully autonomous recursive self-improvement yet, but we are closer than we have ever been."*

来源：[mirendil.com/news/pretraining-at-scale-without-a-pretraining-team/](https://mirendil.com/news/pretraining-at-scale-without-a-pretraining-team/)

### 2. 🟢 Fern 0.1：为 agent 编码而生，Terminal-Bench 4.0 只有 6.1%

Mirendil 官方页（**10-26 发布**）：Fern 0.1 上下文最高 **10M tokens**（约 23 MB、约 50 万行代码，官方比作 Megatron-LM 规模），参数 **0.1–0.5T**，Access 状态仍是 **Coming soon**（无价格、无权重）。

官方 benchmark 表（pass rate %）关键几行：

| Benchmark | Fern 0.1 | Beam | Kimi-K3 | GLM-5.3 | GPT-6 Astra | Claude Opus 5.5 |
|---|---|---|---|---|---|---|
| **Terminal Bench 4.0** | **6.1** | 3.0 | 12.6 | 41.9 | 57.9 | **66.4** |
| SWE-Bench Verified | 73.4 | 81.6 | 93.4 | 95.4 | 86.0 | 98.2 |
| DeepSWE v1.1 | 44.2 | 43.3 | 67.3 | 66.9 | 74.1 | 74.2 |
| SWE-Pro v2 Hard | 76.5 | 76.5 | 88.2 | 84.3 | 90.2 | 100.0 |

**同一张表里 73.4 与 6.1 属于同一个模型。** 官方对 Fern 的用途描述第一条就是 *"Agentic coding — Runs commands, reads the output and keeps going until the tests pass"*。

长上下文（官方 RULER 表）：单针检索 32K→10M 全 **100%**；多键检索 100→90；变量追踪 100→100；**多跳 HotpotQA 65→45（10M）**，官方注明 10M 格只平均 **20 个样本**（其余 100 个）。预测损失随窗口下降：42.9 MB 自_repo 流上 bits/byte 从 32K 的 **0.246** 降到 23M 的 **0.155**；但同长度下 Kimi-K3 在 1M 处是 **0.140**，Fern 是 **0.165**——**Fern 不是同长度下最好的预测器，它的优势是曲线在别人停下的地方还在继续。**

来源：[mirendil.com/news/introducing-fern/](https://mirendil.com/news/introducing-fern/)

### 3. 🟢 Genie 4：原生音频 + 用轻量模型换实时

Google DeepMind 官方博客（**10-27**，作者 Raia Hadsell、Diego Rivas、Hang Qi）：Genie 4 是 *"our first real-time world model to generate audio natively"*，可同时生成类音乐音频、环境音与实时交互式对话。

分工明确：**Gemini Omni** 锚定真实世界外观与行为；**Gemini 3.8 Flash** 是 in-the-loop 的 guiding agent——*"Gemini 3.8 Flash serves as a guiding agent in the loop"*，负责观察画面、把目标拆成步骤、逐帧核验每步是否成功；**Gemini 4 Argon** 只出现在与 Gemini Robotics 的实验里（示例为 Apptronik Apollo 人形机器人下跳棋），不是通用实时驱动模型。

官方自承的短板：*"While it can maintain coherent environments over short sessions, visual details and object permanence can still shift or drift over time"*；长期一致性、复杂物理交互、可读文字渲染、空间精度仍是 *"active areas of ongoing research"*。所有视频与音频带 **SynthID** 水印。当前为 research preview（trusted testers），将面向 Google AI Ultra 订阅者与 Gemini API / AI Studio 早期伙伴，**官方页未给出任何定价**。

⚠️ **拆开标注**：多家媒体（财联社、Ars Technica）称「模拟最长约 2 分钟、为 Genie 3 的两倍」，**DeepMind 官方博客通篇没有分钟数**，只有 "short sessions" 的定性表述 → 该「2 分钟」标 🟡 待官方核实，本文未采用。

来源：[deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/)

### 4. 🟡 Nanbeige4.3-33B：同一个 Terminal-Bench，2.1 拿 80.9，4.0 只剩 23.8

BOSS 直聘旗下 Nanbeige LLM Lab 于 **10-25 12:11 UTC** 在 Hugging Face 发布 **Nanbeige4.3-33B**：**Apache 2.0**、33B **dense**（非 MoE）、**524,288** token 上下文、BF16 权重，同时放出 Base 检查点。

厂商自测对照 Qwen3.8-27B（同 harness、最高 thinking）：Terminal-Bench **2.1 = 80.9**（Qwen 73.0）；**Terminal-Bench 4.0 = 23.8**（Qwen 6.3）；DeepSWE **65.5**（Qwen 42.5）；SWE-Bench Pro **60.3**（Qwen 61.7，**落后**）；YC-bench 模拟营收 **$1,025,437**（Qwen $641,290）。33B 定位为 teacher，计划蒸馏 3B。

**同一个模型、同一个 benchmark 家族，跨一个大版本掉了 57 分。** 全部为厂商自报，无独立复现。来源为多家二手转述（AI Weekly / AICoder / MarkTechPost 系）对官方模型卡的搬运，口径一致，但**我未直接打开 HF 模型卡原文** → 🟡。

来源：[huggingface.co/Nanbeige/Nanbeige4.3-33B](https://huggingface.co/Nanbeige/Nanbeige4.3-33B)（官方卡）、[AI Weekly 报道](https://aiweekly.co/alerts/nanbeige-opens-33b-model-under-apache-20-with-512k-context)

### 5. 🟡 Anthropic S-1：营收曲线在变好，但「承诺了多少钱」没有一个数字是招股书自己给的

**10-26** 递交 SEC，代码 **ANT**，纳斯达克全球精选市场，高盛与摩根士丹利牵头 24 家承销商，路透称有望 **11 月中旬**挂牌。

多家权威媒体口径一致的已披露数字：H1 营收 **162.86 亿**美元（上年同期 11.63 亿）；净亏损 **807.48 亿**，其中 **723.88 亿**来自可转换票据/衍生负债的公允价值变动（**非现金**）；营业亏损从 21.35 亿收窄至 **6.93 亿**；Q2 首次季度经营利润 **9.74 亿**；经营现金流 **+39.29 亿**（去年同期 −15.13 亿）；现金及短期投资 **1,316.51 亿**；算力与基础设施支出 **89.45 亿**（去年同期 23.3 亿）——**占营收比从 201% 降到 55%**。客户：过去 12 个月付费 ≥10 万美元的 **>11,900** 家（一年前 950 家），≥100 万美元 **>1,900** 家，≥1000 万美元约 **250** 家；净收入留存 **900%**；前两大客户合计约 **23%**。治理：七位联合创始人持有一股 F 类股，锁定 **50.1%** 投票权。

⚠️ **最关键的一条**：PANews 拆解指出，**公开版 S-1 的采购承诺合计金额栏是空白的**，文件未给出合计数。市场流传的「约 6,370 亿」是第三方逐项加总（其中最低支出/租金义务约 4,310 亿、标注「最高可达」或按交付计费的约 2,060 亿，性质不同不宜合并），「约 5,180 亿」来自路透此前对**保密版**文件的报道。→ **本文不引用任何单一「算力承诺总额」数字。**

来源（媒体交叉，未直接核到 SEC EDGAR 原文）：[CGTN](https://news.cgtn.com/news/2026-10-27/Anthropic-files-for-IPO-reveals-soaring-revenue-massive-net-losses-1RzGVHGukKY/p.html)、[PANews 拆解](https://www.panewslab.com/zh/articles/01a17d87-6e2c-717f-9ef2-a5f43c78b4e6)

### 6. 🟡 Kimi K3.1 Pro（对照项）

10-24 发布，总参 2.8T、100 万 token 上下文，官方称 Terminal-Bench 4.0 得 **65.7%**（GPT-6 Astra 58.2%、Claude Opus 5.5 66.4%），完整权重承诺 **11-4** 前放出。**本文仅作对照组引用，不重复展开**（详见本库 10-27 笔记）。来源为每日经济新闻转述官方口径 → 🟡。

---

## 三、为什么值得记

1. **「AI 造 AI」和「AI 干活」是两条独立的曲线，今天第一次被同一家公司画在一张纸上。** Mirendil 的 >99% 和 6.1% 相隔五天出自同一个域名。前者说明工程实现的稀缺性已经消失，后者说明端到端执行能力的稀缺性没有消失。任何用「agent 已经能写代码了」去推断「agent 能独立完成工作」的论证，今天有了直接反例。

2. **benchmark 的版本号比分数重要，而且这一轮代价是 57 分。** Nanbeige4.3-33B 在 Terminal-Bench 2.1 拿 80.9、在 4.0 只剩 23.8；Fern 0.1 在 SWE-Bench Verified 拿 73.4、在 Terminal-Bench 4.0 拿 6.1。**同一个「编码能力」叙事，换个 benchmark 版本就能从「追平闭源」变成「差十倍」。** 以后看到任何「开源追平闭源」的结论，先问版本号，再问 harness，最后才看分数。

3. **「装得下」和「用得上」已经被官方数据明确切开。** Fern 在 10M 上下文里单针检索 100%，多跳推理掉到 45%。这意味着用长上下文替代 RAG 的前提是——你的任务是检索型的还是推理型的。检索型可以，多跳推理型目前不行。这是可以直接指导架构选型的分界线。

4. **成本下降是真的，但下降的是「单位成本」，不是「总承诺」。** Anthropic 算力支出占营收从 201% 降到 55%（这是真实的效率改善），同时它的采购承诺年限延伸到 2045 年、现金 1,316 亿对不上承诺规模。**效率曲线在向下，绝对额曲线在向上，两条同时为真。** 不要把前者当成后者的反驳。

5. **实时性的税，今天由旗舰模型自己付了。** DeepMind 把 Genie 4 的实时 in-the-loop 交给 Gemini 3.8 Flash 而不是 Gemini 4 Argon。**凡是「实时」约束强的 agent 场景，规划/校验这一层几乎必然要用比生成层更轻的模型**——这是一条今天有官方原文背书的架构模式。

---

## 四、可行动

- [ ] **把「agent 写的代码占比」和「agent 独立完成的端到端任务占比」拆成两个指标分开统计。** 今天一家公司身上这两个数是 >99% 与 6.1%，混在一个指标里会让前者掩盖后者。
- [ ] **给自己的评测脚本加一列 benchmark 版本号。** 凡引用 Terminal-Bench / SWE-Bench 类分数，强制记录 benchmark 版本 + harness + 采样次数（Mirendil 官方表就注明了 10M 格只有 20 个样本）。
- [ ] **长上下文上线前跑两组题，不要只跑一组：** 单针检索（Needle）+ 多跳推理。Fern 的官方数据表明这两组在同一模型上能差 55 个百分点。
- [ ] **实时 agent 按「规划层用快模型、执行层用强模型」拆开选型**，照抄 Genie 4 的 Gemini 3.8 Flash in-the-loop 分工（官方博客已给出该模式的原文描述）。
- [ ] **手上有 4 卡以上机器的，可以直接下 Nanbeige4.3-33B 试本地 agent**（Apache 2.0，官方 SGLang / vLLM 配方用 4 路张量并行，复用 qwen3_coder tool parser，agent 任务建议 temperature 1.0、最多 65,536 新 token）——但先接受它是自报分数，用你自己的任务集复现一遍再决定是否入栈。
- [ ] **11-4 关注 Kimi K3.1 Pro 完整权重与许可条款是否如约放出**（本库 10-27 笔记已记该承诺）。

---

## 五、术语卡

| 术语 | 解释 | 为什么今天要懂 |
|---|---|---|
| **bits per byte** | 模型交叉熵损失除以文本字节数。因为不同模型分词器不同，直接比 loss 不公平，折成「每字节多少比特」才能横评。越低越好。 | Mirendil 用它证明自己的 base 模型质量（0.222 vs DeepSeek-V4-Pro-Base 0.243）。注意：**它是预训练质量指标，不是能力 benchmark**，不能写成「打败了 DeepSeek」。 |
| **RULER** | 长上下文标准评测集，含单针检索、多键检索、变量追踪、多跳 QA 等子任务。 | Fern 在它上面暴露了「检索满分、多跳掉分」的分裂，是判断长上下文能否替代 RAG 的直接依据。 |
| **Terminal-Bench** | 在真实终端环境里完成多步任务的 agent 评测，2.x 与 4.0 难度差异极大。 | 今天最刺眼的数字都出自它：Fern 0.1 = 6.1%，Nanbeige4.3-33B 在 2.1 是 80.9、在 4.0 是 23.8。**引用时必须带版本号。** |
| **dense vs MoE** | Dense 每个 token 激活全部参数；MoE 只激活一部分专家，总参大、激活参小。 | Nanbeige4.3-33B 刻意选 dense：**部署更简单、行为更可预测**，代价是没有 MoE 的「总参很大但很省」。本地部署时这是选型分水岭。 |
| **非现金公允价值变动** | 可转换票据等金融工具按公允价值计量，公司估值上升会推高负债账面价值，差额计入当期亏损——**不涉及现金支出**。 | Anthropic H1 净亏 807.48 亿里 723.88 亿属于这一类。看到「史上最亏」的标题先做这个拆分，营业亏损其实只有 6.93 亿且在收窄。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
