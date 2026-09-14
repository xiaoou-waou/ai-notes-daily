# 2026-09-14｜开放正在分层：NVIDIA 把金牌的账单也开源了，而账单本身就是门槛

> 「开源」不再是布尔值。交出多少账单，决定了你能验证多少——也暴露了你复现不起多少。

**标签**：`#开源` `#后训练` `#可复现性` `#端侧` `#Agent安全`
**生成时间**：2026-09-14 12:08（北京时间）

---

## 一、今日观察

**「开放」这个词今天裂成了三档，而它们恰好是同一件事的三个不同切面。**

过去判断一个模型"开不开源"，看的是权重在不在 Hugging Face 上——一个布尔值。今天这件事变成了一个**成本函数**：你交出的东西越完整，外界能验证的就越多；但账单写得越细，同时也把"复现需要多少钱"写死了。

| 档位 | 今天的主角 | 交出了什么 | 卡在哪 |
|---|---|---|---|
| **第三档：带账单的开放** | NVIDIA Nemotron IMO 金牌配方 | 权重 + 数据 + 代码 + **200 题全新 benchmark** + **GPU 小时账** + 自曝的验证器盲点 | 复现门槛：2 个 specialist checkpoint、训练用 **512 张 GB200** |
| **第二档：诚实的主张** | Princeton 的 Recurrent Looped Transformer | 完整架构 spec + **明确声明"研究目标而非实测结果"** + 79K 参数合成实验 | 从未在真实规模上训练过 |
| **第一档：能真跑的开放** | 元空 Boxer / 原点星辉 StartLux | 35B-A3B 在 **40 TOPS 消费级 PC、<8GB 内存**上断网可跑 | 评测多为自建集，缺第三方复核 |

三档不是好坏之分，而是**可验证性的三种量纲**：第三种让你能"核对"，第二种让你能"理解"，第一种让你能"上手"。真正值得注意的是 NVIDIA 那一档——它把 9-13 那篇里 25 位菲尔兹奖得主要求的"别急着宣布、留出写清楚的时间"，做成了实证：**一周之内，同一个社区里有人交出了带 ablation 和算账的金牌，也有人交出了连一次训练都没跑的架构主张，两者都诚实，但分量完全不同。**

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 NVIDIA 开源 IMO 金牌全栈：30/42 分，附带完整算账单（9-09 上线 arXiv）

NVIDIA 团队（Ivan Moshkov、Stephen Ge、George Armstrong、Wei Du、Sadegh Mahdavi、Igor Gitman）发布技术报告《An Open Recipe for IMO Gold》，系统在 **IMO 2026 拿到 30/42 分**，超过 29 分的金牌线，**全程只用自然语言证明，无形式化定理证明器、无外部工具、无联网**。

关键在释放物的完整度：两个 post-trained specialist checkpoint（OpenMDW-1.1）、SFT 语料 **414,890 条**与 RL 题目 **9,597 道**（CC BY 4.0）、训练与推理代码、实际提交的证明、以及 **Nemotron-IMO-Bench（200 道全新奥赛题，与 Titu Andreescu 合作编写）**。

算账部分（论文正文与表 1）：找到全部 6 道提交证明耗费 **约 7.07 亿 tokens / 1,464 GB200 GPU 小时**；跑完在飞轮次后总计 **约 23.1 亿 tokens / 4,800 GPU 小时**。分题差异极大——P1 只花 11.7 GPU 小时，P6 花 612.9。

来源：[arXiv:2609.10712（官方摘要页）](https://arxiv.org/abs/2609.10712) ｜ [arXiv HTML 全文（含表 1 逐题算账）](https://arxiv.org/html/2609.10712v1)

### 2. 🟢 论文自曝盲点：模型陪审打出 32 分，官方只给 30 分

最值得记的一段：**在竞赛截止时间，两个基于模型的验证器都给这批证明打了约 32 分，比官方的 30 分高 2 分**。论文原话指出这个差距"完全集中在第 3 题和第 6 题——两个基于模型的评估都给了分数，而官方阅卷只给 1 分"。

作者把这件事定性为 **"a shared blind spot in model-based verification"（模型验证的共享盲点）**——不是随机噪声，是**系统性的共同偏差**。

配套还有一个反直觉数字：在 16 位评委全票通过才接受的规则下，**false accept 率仅 1.1%，但 false reject 率高达 81.3%**。

来源：[arXiv HTML 全文 §5.3 与表 3](https://arxiv.org/html/2609.10712v1)

### 3. 🟢 消融结论对做微调的人最值钱：第二个 checkpoint > 同一个 checkpoint 加倍采样

论文 Table 4 的采样预算分配实验（30 题开发集，首轮尝试）：

| 配置 | Tokens (B) | 接受问题数 | 全 30 题陪审分 |
|---|---|---|---|
| RL 256（单 checkpoint 加倍采样） | 1.59 | **14** | 139 |
| RL 128 + SFT 128（混合池） | 2.36 | **18** | 159 |

论文结论原文：*"Doubling the RL attempts barely moves the pool… Of the 18 problems the combined RL 128 + SFT 128 pool accepts, six are accepted from both checkpoints, seven only from RL and five only from SFT, and doubling the RL attempts to 256 recovers just one of the five."*

配套的八轮累计分：RL 管线 **180 分**、SFT 165 分、GA 基座 162 分。

来源：[arXiv HTML 全文 §6.2 与 Table 4](https://arxiv.org/html/2609.10712v1)

### 4. 🟢 复现门槛：开放了，但开放给"有 512 张 GB200 的人"

从论文 4.2 节可以读到训练侧的真实开销：**SFT 训练用 512 张 GB200**（TP8/CP32/EP64/PP1）；**RL 训练用 128 训练节点 + 128 推理节点 + 16 裁判节点，每节点 4 张 GB200**。基座为 Nemotron-3-Ultra **550B-A55B** MoE。

🟡 另有二手来源称：两个 specialist checkpoint 各为 **1.12 TB 下载量**，NVIDIA 模型卡建议**至少 8 张 B200、约 1.5 TB 显存**才能推理；HF 集合名为 `nvidia/nemotron-labs-imo-2026`。此项**未能在官方页面上直接核实**（Hugging Face 页面本次不可达），按待核实处理。

还有一个容易被忽略的供应链事实：414,890 条 SFT 数据的初始证明，**是由 DeepSeek-V4-Pro 在 Max 推理模式下生成的**。

来源：[arXiv HTML 全文 §4.1/§4.2](https://arxiv.org/html/2609.10712v1) ｜ 🟡 [dev.to 报道（1.12TB / 8×B200 数据）](https://dev.to/breachprotocol/nvidia-publishes-the-whole-recipe-behind-an-imo-gold-score-weights-and-all-4o49) ｜ 🟡 [OrcaRouter 对 HF 集合的清点](https://www.orcarouter.ai/blog/nemotron-3-labs-ultra-math-rl-imo-2026)

### 5. 🟢 另一端：国产后训练小模型把"能跑"做进了 40 TOPS 的消费级 PC

据新华社报道，9 月初北京大学科学智能学院孵化的**元空 AI 发布端侧模型 Boxer**，**基于阿里 Qwen3.5-35B-A3B 后训练**而来；记者在现场看到，一台 **40 TOPS 算力的消费级 PC** 上，对话延迟接近真人交流，**运行内存占用约 8GB**。同批报道的还有原点星辉 **StartLux-V1.0-27B-Preview**（基于 Qwen3.6-27B，面向工具调用与通用 Agent 后训练），在工信部中国信通院可信 AI 大模型基准测试的 **MCP 专项中综合性能超越多款千亿参数模型**。

🟡 补充细节来自 36 氪与 i黑马的现场报道（**非官方一手规格表，待核实**）：Boxer 在 40 TOPS PC 上可达**预填充 700+ tokens/s、解码 30+ tokens/s，内存占用不到 8GB**，训练数据来自团队长期积累的 Agent Harness 真实任务轨迹；在自建 **WorkArena** 测评集中同尺寸排名第一。**注意：WorkArena 是团队自建集，不是第三方 benchmark。**

来源：[新华网《办公智能体赛道分化 本地大模型加速融入》](https://www.news.cn/tech/20260914/b5a92db7feab4a68baadb3b1ac58ef42/c.html) ｜ 🟡 [36氪报道](https://www.toutiao.com/article/7683150655518704163/) ｜ 🟡 [i黑马现场报道](https://www.iheima.com/article-401697.html)

### 6. 🟢 反面样本也诚实：RLT 提出"无限推理深度"，自己声明"这是研究目标不是实测结果"

普林斯顿研究者 Yifan Zhang 于 **9 月 12 日**发布 Recurrent Looped Transformer（RLT）：把解码器的最终隐状态与逐层滑动窗口缓存**跨 token 传递**，且**在 prompt 与回答的边界不重置**。参考配置为 **48 层编码器 + 48 层解码器（权重共享）**，每个 token 执行 96 个逻辑 block，但处理到第 t 个 token 时累计状态路径已穿过 **48t 个解码器 block**——**单 token 算力固定，结构深度随序列增长**。

README 里的免责声明写得很直白：*"Reasoning improvements, hardware speedups, and RL scaling are research goals rather than measured results in this report."* 且明确澄清"infinite depth"指的是**随序列延伸的计算路径，而非单 token 内的无限算力**。

🟢 更新（9-13 提交）：仓库新增了由 @AradhyeAgarwal 贡献的**合成状态追踪实验**——约 **79K 参数、3 个种子**，训练长度 32 步，外推到 **128 步（4×）**。结果是诚实的双刃剑：RLT 在训练长度上达到约 100%，但外推到 128 步时 Parity 掉到 **60.8%**、五状态转移掉到 **20.7%**（对比 Transformer 的约 48% / 21%）。作者自己也标注：*参数与数据预算对齐了，FLOPs 没有对齐*。

来源：[GitHub 官方仓库 README（Apache 2.0）](https://github.com/yifanzhang-pro/recurrent-looped-tranformer) ｜ [项目主页](https://yifanzhang-pro.github.io/recurrent-looped-tranformer/)

### 7. 🟡 Agent 安全侧：软约束会稀释，硬中断必须"物理切断 API 流"

开源项目 **zero-trust-llm** 提出一套五步状态机约束 Agent：`[HYPOTHESIS] → [IDENTIFY REQUIRED EVIDENCE] → [GROUND VERIFICATION METHOD] → [EXECUTE]（严格只读诊断命令）→ [HARD YIELD TO OPERATOR]`。核心论点是：**在系统提示里加"请谨慎"这类自然语言规则，会随着上下文增长而稀释**；因此在 HARD YIELD 节点，必须由 **Python 中间件 / LangGraph / Semantic Kernel 物理切断 API 流**，执行只读诊断后再把原始输出喂回上下文。仓库提供 AGENTS.md、MANIFESTO.md、失败案例 transcripts 与编排伪代码，**暂无量化评测**。

🟡 此条来自二手报道，**未能直接访问原仓库核实**，按待核实处理。同类思路还有 🟡 Agentwall（在工具函数外层做拦截与审批门，默认 destructive 调用需人工批准，且**审批服务不可用时 fail-closed 拒绝**）。

来源：🟡 [Web Pulse 对 zero-trust-llm 的介绍](https://wpnews.pro/news/a-computational-constitution-to-stop-llm-agents-from-bricking-servers) ｜ 🟡 [Agentwall 作者自述](https://dev.to/tritium007/we-built-a-circuit-breaker-for-ai-agents-heres-why-it-matters-pih)

---

## 三、为什么值得记

**1. "多模型投票"不等于"多模型独立"——这是今天最贵的一条教训。**
NVIDIA 的两个 verifier 都是 Nemotron 的后代，一个 SFT 一个 RL，看起来是不同的检查者。结果它们在 P3、P6 上**犯了同一个错**，一起把 30 分评成 32 分。这对所有做 LLM-as-judge / RAG 多路召回融合的人是当头一棒：**同源模型的分歧会互相抵消，同源模型的偏见会互相放大**。要真正的独立性，得引入**不同基座、甚至非模型**的验证器（编译器、执行器、形式化 kernel、数据库约束）。9-05 那篇讲"验证溢价"，今天这条是它的补丁——**验证器自己也有溢价泡沫**。

**2. 81.3% 的 false reject 说明：严卡的代价被严重低估。**
大家都在优化"别让错的通过"，NVIDIA 的数据却是——16 票全票通过制下，**每 100 个正确解里有 81 个被自己扔掉了**。工程上这意味着：与其继续加严验收阈值，不如**先降低 false reject**。对做 RAG 的人来说特别直接：如果你的重排/网关把 80% 的正确文档挡在外面，再准的生成器也救不回来。

**3. 后训练的方向正在从"更强"转向"更不同"。**
RL 256 → 14 题，RL 128 + SFT 128 → 18 题，而且 18 题里有 7 题只有 RL 能解、5 题只有 SFT 能解、**翻倍 RL 采样只能拿回其中 1 题**。这条 ablation 的价值远超 IMO 本身：**多样性（diversity）比强度（strength）更值钱**。对做 LoRA 微调的人是可直接迁移的结论——与其把同一个 adapter 训得更久、采样更多，不如**再训一个路线不同的 adapter 组成池**（不同数据切片 / 不同 rank / 不同目标），互补收益大概率更高。

**4. "开放"正在从权利变成成本问题。**
NVIDIA 把配方全交了，但 SFT 用 512 张 GB200、RL 用 1088 张 GB200 级节点。这意味着**"开源"保证了你能检查和引用，不保证你能复现**。与此同时，Boxer/StartLux 走的是另一条：**用后训练把 27–35B 塞进 40 TOPS 的 PC**。两条路的分野很清楚——**前者的护城河是算力，后者的护城河是数据和场景**。对个人和小团队来说，可参与的其实只有第二条。

**5. 一个容易被漏掉的张力：开源配方的供应链是闭源的。**
414,890 条 SFT 数据的证明由 **DeepSeek-V4-Pro** 生成。这不是缺点——但它说明"开放模型"这个词描述的是**产出物的许可状态，不是生产过程的自主性**。评估一个开源模型时，值得多问一句：它的训练数据是谁生成的。

---

## 四、可行动

- [ ] **把你现有的多路验证改成"异源"**：如果 RAG 或 Agent 里用了两个模型做交叉验证，检查它们是否同源（同一基座 / 同一家族）。是的话，补一路**非模型**校验（正则、SQL 执行、编译器、数据库唯一约束），并单独统计每路的 false reject 率，而不只是 false accept。
- [ ] **复现 NVIDIA 那条 ablation 的思路，用在你自己的 LoRA 上**：固定总采样预算，对比「单 adapter 加倍采样」vs「两个不同路线的 adapter 各一半」，记录各自能解决、对方解决不了的 case 数。如果两个 adapter 的解集高度重叠，说明你的多样性设计失败了。
- [ ] **去读 arXiv:2609.10712 的 Table 1**：逐题 GPU 小时（P1 11.7 vs P6 612.9）是难得一见的"难题成本分布"公开数据，可以用来校准自己 Agent 任务的算力预算——**先估计你的任务里 P6 占比多少**，再决定要不要上重试+精炼循环。
- [ ] **试跑 RLT 仓库里的合成状态追踪实验**（79K 参数、单卡可跑），重点不是信它的结论，而是**亲手验证"训练长度 32 → 外推 128"的衰减曲线**。这对你评估任何声称"长上下文泛化"的架构都是个可复用的测试模板。
- [ ] **给现有 Agent 加一道 fail-closed 的物理中断**：不要只改系统提示词。用中间件在工具 dispatch 前拦截（参考 Agentwall 的做法），把 destructive 调用挂起等人工确认，并确认**审批服务超时/不可用时是拒绝而不是放行**。顺手验证：把审批服务停掉，看 Agent 是拒绝执行还是照跑。
- [ ] **评估端侧路线时先问评测集来源**：Boxer 的 WorkArena 是团队自建集。真的要选型，拿自己的真实任务集在 40 TOPS 档位的机器上跑一遍，别信任何"同尺寸第一"的自建排名。

---

## 五、术语卡

| 术语 | 解释 | 今天为什么重要 |
|---|---|---|
| **Test-time compute（推理时算力）** | 不在训练时堆参数，而在推理时多采样、多轮验证与精炼来换正确率 | NVIDIA 的 30 分主要是"花算力买来的"：4,800 GPU 小时、23.1 亿 tokens |
| **Unanimity verification（全票通过验证）** | 多个评委独立打分，必须全部给满分才接受该候选 | 16/16 规则换来 1.1% false accept，代价是 **81.3% false reject** |
| **Shared blind spot（共享盲点）** | 多个验证器因同源而产生相同的系统性偏差，分歧不能互相抵消 | 两个 Nemotron verifier 一起把 30 分高估成 32 分 |
| **Post-training（后训练）** | 在基座模型之上做 SFT / RL 等定向训练，不改变架构只改行为 | 今天两端都靠它：NVIDIA 的 specialist、Boxer/StartLux 的小模型 |
| **MoE 激活参数（A55B）** | 混合专家模型中每次前向只激活的部分参数，与总参数量（550B）分离 | 理解"550B 但只需 A55B"才能读懂那份算账单 |
| **滑动窗口注意力（SWA）** | 只保留最近 W-1 条历史 KV 的注意力机制，把显存从随序列平方降为线性 | RLT 把它当作跨 token 传递的"循环记忆"载体 |
| **Fail-closed** | 安全组件失效时默认拒绝而非放行 | Agent 审批门的关键属性，很多实现错在超时即放行 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
