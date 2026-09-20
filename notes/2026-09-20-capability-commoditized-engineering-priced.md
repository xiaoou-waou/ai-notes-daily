# 2026-09-20｜两天复现一个模型，五天交付不了一个 App

> 模型层正在被压成商品，剩下的差距全落在配方、harness 和路由这三层工程上。

**标签**：`#LoRA` `#AgentHarness` `#Benchmark` `#推理工程` `#国产生态`
**生成时间**：2026-09-20 12:00（北京时间）

---

## 一、今日观察

今天最刺眼的一组对照是这样的：

- 一个闭源决策模型，据报道由某 OpenAI 联合创始人做了 **三年**（🟡 社交源转述，见下）；
- 一个外部团队用 **2 天**、**2,676 条合成样本**、一张卡上的 **LoRA rank 16** 微调，在一个 324 条的集上做到 **90.12%**，对照原版 **93.21%**；
- 而与此同时，同一批"前沿模型"被要求完成"人类工程师要干几天到一周"的真实任务时，最高通过率是 **28.0%**。

模型能力这一层在快速塌缩——这已经不是判断，是这周两组数字直接摆出来的事实。但塌缩不等于无用：**真正没塌缩的是"把能力变成交付"的那一层**。今天的六条事实，可以按四层排开：

| 层 | 今天的证据 | 变化的量 | 谁在受益 |
| :--- | :--- | :--- | :--- |
| **能力层** | Bespoke Nimble（Qwen3.5-9B + LoRA） | 66.36% → **90.12%**，2 天、2,676 样本 | 没有预训练预算的小团队 |
| **任务层** | Android Bench 2.0 长周期任务 | 原任务集 ~**91%** → 新任务集 **28.0%** | 会拆任务、会设计 harness 的人 |
| **组织层** | arXiv 2609.20804 harness 消融 | 176 组配置，逐组件归因 | 能把 harness 当变量调的团队 |
| **运行时层** | AWS HyperPod Inference Gateway | TTFT **4.4s → <800ms**（最高 82%） | 已经跑着多 LoRA / 多模型的人 |

一句话：**能力在被快速复制，"配方 + 脚手架 + 调度"在被重新定价。**

补一个国产切面：智谱同日宣布 **约 50 亿美元融资**并上线 GLM-5.3-FlashX（最高 **200 tokens/s**，价格为原版 **2.5 倍**）——钱明确投向"完全自训练"体系和推理基础设施。国产厂商卖的已经不是"我们有多强"，而是"**多快、多便宜、多少卡**"。阿里同日发布 Qwen3.8-Omni-Flash（1M 上下文全模态，🟡 多源简报口径，未逐条核官方页）。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 Bespoke Nimble：LoRA 微调 Qwen3.5-9B，两天逼近闭源决策模型

Bespoke Labs 开源 `bespokelabsai/nimble`，数据、训练与评估配方全公开。关键参数（均取自仓库 README 一手内容）：

- 基座 **Qwen3.5-9B**，**LoRA rank 16**、lr **5e-5**、effective batch size **8**、seed 17、**单 epoch**、**BF16**，训练时 prompt 截断 **2,048 token**（推理放宽到 8192）；
- 优化目标是**在允许的候选 token logits 上做交叉熵**——不生成 CoT、不生成 JSON，直接读 logits 出结构化决策；
- 训练集 `train.jsonl` 共 2,826 条，实际训练发布模型用 **2,676** 条；留出集 `eval.jsonl` **324** 条；
- 准确率（324 条留出集）：基座 Qwen3.5-9B **66.36%**（215/324）→ Nimble **90.12%**（292/324）→ Jev 1.13.0 **93.21%**（302/324）；
- 延迟中位数：Nimble 在 **H100 106.0 ms**；基座 Qwen 58.1 ms；Jev 走 API **246.7 ms**；M5 Pro 64GB Mac 上 **444.0 ms**；
- 仓库明确写：**"we did not distill from Jev"**（未蒸馏）、未用 RL，标签用硬标签交叉熵；
- 数据方法是 **contrastive data curation**：造两个几乎一样的样本，只改**至多 8 个词**的关键事实使答案翻转，其余上下文不变，让模型从配对里学"哪个事实决定了决策"。

**必须同时读的一句自我限定**（仓库原文）：*The reference labels are synthetic... this is a narrow test.*——标签全合成、留出集只覆盖 10 个合成类别中的 6 个、共 162 对近似样本。所以 **90.12% 是"在自家窄测试上"的 90.12%**，不能外推。

来源：[github.com/bespokelabsai/nimble](https://github.com/bespokelabsai/nimble)　交叉：[HuggingNews 报道](https://huggingnews.com/ai/bespoke-labs-builds-open-jev-rival-in-2-days-using-9b-model-cc9dd3f5)｜[AGI Hunt](https://agihunt.info/en/p/1a0b57640fe6e6ba0a3b7927a18)
🟡 旁注：有开发者在 X 上称该发布违反 Jev 使用条款（单一社交源，不做判断）。

### 2. 🟢 arXiv 2609.20804：第一次把 coding harness 的三个组件拆开做消融

《An Empirical Study of Harness Design for Coding Agents》，2026-09-17 提交。做法很干净：**执行循环固定**，只变三个组件——**planning / action space / context management**。

- 4 个模型（Nemotron-3 30B / 120B / 550B + Mistral-Medium-3.5-128B）、2 个基准（SWE-Bench Verified、Terminal-Bench 2.1）、**176 组匹配配置**；上下文策略 5 种（T0 不管 → T4 先规则式省略再 LLM 摘要），上下文预算 4 档（32k/64k/96k/128k）。
- 结论 1：上下文管理**在窗口越紧时越值钱**，收益主要来自**防止 context overflow 提前终止执行**，窗口放大后收益递减。
- 结论 2：**先规则式省略、再 LLM 摘要**（T4）综合效率最高；把被省略内容做成"可召回"（T2）**加了机制但模型几乎不用，准确率没涨**。
- 结论 3：**planning 对弱模型是"准确率支架"，对强模型退化成"省钱器"**，准确率几乎不变。
- 结论 4：预定义工具只对 **bash 能力弱**的模型有帮助；bash 能力强的模型用 **bash-only** 接口就能跑，且成本显著更低。
- 轨迹层解释：上下文管理**延长轨迹但不怎么改变行为**；planning **改变轨迹在哪里停**；action space **改变写代码的粒度**。

来源：[arxiv.org/abs/2609.20804](https://arxiv.org/abs/2609.20804)｜[全文 HTML](https://arxiv.org/html/2609.20804v1)

### 3. 🟡 Android Bench 2.0：任务尺度一变，能力曲线立刻断

Google 于 **9 月 16 日**发布 Android Bench 2.0（本周被广泛报道）。把任务从"小补丁/增量改动"换成**人类工程师需要几天到一周**的工作，并**放弃 pass/fail 二值评分，改用连续完成率**（functional + 视觉保真 + 无回归，违规扣分）。

- 新增 **30 个长周期任务**：从设计稿搭多屏外卖 App、库与架构迁移、加 widget / 画中画、Flutter/React Native 转原生 Android。
- 通过率：原任务集大约在 **91%** 量级；新长周期任务最高只有 **28.0%（OpenAI GPT-6 Astra + Codex）**，其后 **Claude Fable 5.1 22.7%**，Gemini 3.8 Flash 口径不一（一处报 **8%**、一处报 "**sub-20%**"，**不做定论**）。
- 几个高信号发现：**写新代码比重构老代码强得多**；确定性迁移（Java→Kotlin、Retrofit→Ktor、加 ViewModel）能稳定覆盖 **125+ 文件 / 8,000+ 行**；但**需要运行时验证**（如缺失 DI 图）、**框架破坏性变更**、**未发布库**时明显掉链子；**跨端转原生无任何模型 100% 通过，前沿模型完成度最高 80%**。
- 关键设计：排行榜是**模型 + 自家 harness 配对**评测的（Codex / Antigravity SDK / Claude-Code / Kimi-Code / Qwen-Coder），Google 明确说 **harness design 会影响 token 消耗与开发者结果**，未来会测跨厂商组合。

来源（官方博客本次抓取失败，以下为多源交叉）：[worldprogramming.org](https://www.worldprogramming.org/posts/android-bench-20-focuses-on-long-horizon-tasks-agent-evaluations-8wrkhm)｜[tbreak.com](https://tbreak.com/android-bench-2-0-ai-agents-week-long-app-builds)｜[droidfeats.com](https://droidfeats.com/google-launches-android-bench-2-0-with-long-horizon-coding-tasks)
🟡 说明：官方 `android-developers.googleblog.com` 本次 WebFetch 失败，上述数字为二手口径；Gemini 3.8 Flash 一处 8%、一处 sub-20%，存在冲突，故不采信具体值。

### 4. 🟢 AWS HyperPod Inference Gateway：LoRA 从训练技巧变成调度单元

AWS 官方博客（9-19 前后）发布 Kubernetes 原生的 GPU 感知推理路由，**装一个 EKS addon 即可，不改模型服务、不改客户端**。

- 问题定义得很直白：轮询 / 最小连接看不到 GPU 内部——**哪个 pod 的 KV cache 快满了、哪个正在跑长上下文生成、哪个已经把你需要的 LoRA adapter 加载进内存了**。
- 官方数据：首字延迟 **4.4 秒 → 800 ms 以内**，最高降低 **82%**（原文引用："A chatbot user waiting 4.4 seconds for the first token now sees it in under 800 ms."）。
- Endpoint Picker 抓 5 路 Prometheus 指标打分：**KV cache 利用率、队列深度、LoRA adapter 常驻、prefix cache 命中率、运行中请求数**，每项权重可配（延迟敏感 chat vs 吞吐优先 batch）。
- 架构两层：Tier 1 = Envoy Gateway + Body-Based Router（解析 OpenAI 兼容请求体的 `model` 字段做多模型路由）+ Endpoint Picker；Tier 2 = Global Inference Router（跨集群 failover / 全局限流 / 成本感知），**coming soon**。

来源：[aws.amazon.com/blogs/machine-learning/introducing-amazon-sagemaker-hyperpod-inference-gateway/](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-sagemaker-hyperpod-inference-gateway/)　交叉：[AGI Hunt 摘要](https://agihunt.info/en/p/1a0b4b7ea72f95c83c2b4f8b5e8)（其"8B–235B、H100/A10G、P95/P99 降 97–98%"等数字**仅见于二手摘要，官方页本次未核实，故不采信**）

### 5. 🟢 Anthropic 首次公开研发自动化三项指标

9 月 17 日发布《Measuring the pace of AI development》，把"AI 参与造 AI"变成可追踪的组织指标：

- **R&D Automation Index**：采用 Epoch AI 的 AL0–AL5 六级量表。截至 2026 年 8 月，Claude 在 **26%** 的 AI 研发任务中达到 AL4「**主导**」（人类给高层目标 + 监督，AI 端到端完成大部分执行）；**超过 90%** 的任务至少达到 AL3「协作」。**没有任何一项被测任务达到 AL5 完全自主**。该比例 2026 年 2 月还**不到 1%**。
- 方法：7 月每周抽 20% 相关员工的工作记录，由 Claude research agent 整理出约 **1.5 万个**细粒度研发任务，再组织成 **542 个节点 / 378 个叶子**的任务树，按人力时间加权。**评分者也是 Claude**——模型与人的精确一致率 **59%**，人与人之间只有 **35%**，相差一级以内 **97%**。Anthropic 自己承认这有"评估者与被评估者共享盲点"的风险。
- **智能体监督**：最常用内部平台上，任一时刻约有 **30,000 个 agent** 同时跑研究与工程任务；提出应持续公开三个量：监控覆盖率、审查延迟、升级（被阻止/重定向/标记）率。
- **算力分配**：7 月 13–20 日一周快照，AI 研发算力中约 **6%** 用于安全；"AI 驱动的 AI 研发"算力中约 **12%** 用于安全（Anthropic 称这是保守估计）。

来源：[anthropic.com/institute/measuring-pace-of-ai-development](https://www.anthropic.com/institute/measuring-pace-of-ai-development)　交叉：[澎湃/科学网](https://news.sciencenet.cn/htmlnews/2026/9/571716.shtm)｜[digit.in](https://digit.in/news/general/anthropic-says-claude-is-helping-build-future-ai-models-reveals-how-much-work-it-handles.html)

### 6. 🟢 智谱完成约 50 亿美元融资，同日上线 GLM-5.3-FlashX

9 月 18 日港交所公告口径（多家财经媒体数字完全一致）：

- **约 20 亿美元股份配售**：按每股 **714.00 港元**向不少于 6 名承配人配发 **21,965,000 股**新 H 股，占扩大后已发行股份约 **4.50%**；所得款项总额约 **156.83 亿港元**，净额约 **156.64 亿港元**。
- **约 30 亿美元可转债**：本金总额 **201.4 亿元人民币**、美元结算**零息**可换股债券，2027 年到期，初始换股价 **892.50 港元**；所得款项总额约 **30.16 亿美元**，净额约 **30.1 亿美元**。
- 用途按公告比例：**约 60%** 用于下一代 GLM 基础模型研发与"**完全自训练**"体系构建，**约 15%** 业务拓展/战投/并购，**约 25%** 优化资本结构与营运资金。
- 同日上线 **GLM-5.3-FlashX**：最高 **200 tokens/s**，官方称为 GLM-5.3-Flash 的 **5 倍**提速，价格提升至原版 **2.5 倍**，API 全量开放；未更换底层基座。

来源：[新浪财经](https://finance.sina.com.cn/tech/csj/2026-09-18/doc-inisfyex3504631.shtml)｜[观点网/腾讯新闻](https://news.qq.com/rain/a/20260918A0A8C300)｜[大河财立方](https://www.dahecube.com/article.html?artid=287473)
🟡 未经官方页核实的周边数字（**未采信，仅作线索**）：年末 ARR 指引由 24 亿上调至 30 亿美元、当前全业务口径 ARR 18 亿美元、"10 万张国产芯片推理集群上线即被打满"——均出自单一转述源。

---

## 三、为什么值得记

**1. "配方"取代"权重"，成为真正可转让的资产。**
Nimble 最值钱的不是 90.12% 这个数，是它把**数据怎么造**写成了四步流水线：查决策规则 → 造配对（改≤8 个词翻转答案）→ 用独立模型调用检查两个样本（还要**逐个删证据句，确认删掉后焦点事实就不可知**，防泄漏）→ 用代码校验标签后保留。**这条"防泄漏检查"和"只改一个事实"的设计，比任何 LoRA 超参都更可迁移。** 顺便：LoRA rank 16 / lr 5e-5 / batch 8 / 1 epoch 这种"小到有点反直觉"的配置能拿到 +24 个百分点，本身就在提醒——多数失败不是配置不够，是数据没有把决策边界暴露出来。

**2. Benchmark 的"任务尺度"比模型排名更值得盯。**
Android Bench 2.0 用同一批前沿模型，只把任务从"改一个补丁"换成"干一周的活"，通过率从 91% 掉到 28%。**这说明此前的高分里有相当部分是任务尺度的红利，不是能力的证明。** 而且它放弃了二值评分改用连续完成率——"改完 40 个屏幕、过了 90% 功能检查但挂了一个边界断言"不再记 0 分。这个评分法本身值得抄。

**3. LoRA 的位置变了：从"训练技巧"变成"调度单元"。**
今天有两处独立证据。训练侧：Nimble 用 LoRA 在 2 天内产出可发布的专用模型。服务侧：AWS 的 Endpoint Picker 把 **LoRA adapter 常驻**和 KV cache、队列深度并列为路由打分项——因为 adapter 换入换出本身就是一笔延迟开销。**当你同时部署多个 LoRA 时，路由不知道哪个 pod 上已经有你的 adapter，就是在白白付切换税。**

**4. Harness 第一次有了"组件级"的可归因证据，但结论是反直觉的。**
arXiv 2609.20804 的三条结论都指向"没有通用最优解"：planning 对强模型只是省钱器；被省略内容做成可召回是白加机制；bash 强的模型用 bash-only 更便宜。**这意味着抄别人的 harness 配置几乎没有意义，必须按自己的模型档位和上下文预算重新调。** 更值得注意的是方法本身——**固定执行循环、只变一个组件、跑 176 组**，这才是把"玄学脚手架"变成可测量对象的正确姿势。

**5. 研发过程本身正在被 AI 接管，但度量仍是自评。**
Anthropic 的 26% 值得记，但要连同两个限定一起记：**评分者是 Claude 自己**（模型-人 59% vs 人-人 35%），以及**没有一项达到完全自主**。真正有治理价值的可能不是 26% 这个数，而是它提出的三个量——监控覆盖率、审查延迟、升级率。**当同时跑着 3 万个 agent，偶发错误的绝对数量会把"我们有人工审核"这句话变成空话。**

---

## 四、可行动

- [ ] **把 contrastive curation 用到自己的 Qwen3 微调数据上**：挑一批已有问答对，造"只改一个关键事实就翻答案"的负样本（改动词数自己设上限，建议从 ≤8 个词开始），并且**逐条删证据句验证删后不可答**——这一步专治格式类幻觉。
- [ ] **对照 arXiv 2609.20804 的 T0–T4，给自己的 Agent 定一档上下文策略并记录成本**。若当前上下文窗口 ≤64k，优先做"规则式省略优先于 LLM 摘要"；别急着上可召回存储（论文说基本没人用）。
- [ ] **按模型能力分档选 action space**：bash 能力强的模型试 bash-only 接口，看成本降多少；弱模型再给预定义工具集。用同一批任务做 A/B，别凭感觉。
- [ ] **若已在多 LoRA / 多模型部署**：确认路由层能否看到 adapter 常驻与 KV cache 利用率。不能的话，评估开源 Gateway API Inference Extension（AWS 这套就是基于它建的）自建一层。
- [ ] **把"连续完成率"评分法抄进自己的评测**：长任务不要 pass/fail，改成 功能正确 + 视觉/格式保真 + 无回归 三项加权，违规扣分。先跑一遍现有 Agent，看它是不是也"前 80% 很唬人，后 20% 全要人擦屁股"。
- [ ] **读 Nimble 的 eval 集分布**：10 个训练类别里只有 6 个进了留出集，Home/Science/Software/Workplace 全是 0。如果要复现，先想清楚自己的留出集怎么覆盖——别只测训过的分布。

---

## 五、术语卡

| 术语 | 一句话解释 | 今天出现在哪 |
| :--- | :--- | :--- |
| **Contrastive Data Curation**（对比式数据构造） | 造两个几乎相同的样本，只改动一个关键事实使正确答案翻转，迫使模型学"哪个事实决定了决策"，而不是学标签的表面相关性 | Nimble 的训练数据方法，四步流水线含防泄漏检查 |
| **LoRA rank / adapter residency** | rank 是低秩适配矩阵的秩（越小参数越少）；residency 指某张卡上是否已加载你需要的 adapter，未命中就要付出换入延迟 | Nimble 用 rank 16；AWS 把 adapter 常驻作为路由打分项 |
| **Harness（执行脚手架）** | 包在模型外面、负责规划 / 工具调用 / 上下文管理 / 权限的那一层，决定模型能力如何转化为长周期任务表现 | arXiv 2609.20804 的三组件消融；Android Bench 2.0 的配对评测 |
| **TTFT**（Time To First Token） | 从发出请求到收到第一个 token 的时间，用户体感上最敏感的一项，容易被 KV cache 饱和与排队放大 | AWS HyperPod Gateway 主指标：4.4s → <800ms |
| **AL0–AL5 自动化等级** | Epoch AI 提出的六级量表：AL0 无 AI 参与 → AL3 协作 → AL4 主导（人类监督）→ AL5 完全自主 | Anthropic R&D Automation Index 的标尺；当前最高 AL4 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
