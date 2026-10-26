# 2026-10-26｜1024 个 agent 对 11.3 倍剪枝：今天两种解法，只有一种报了成本

> 同一道题"让 agent 又强又便宜"，今天分成加量派和减量派；加量派头条拿满，成本一个没报。

**标签**：`#多智能体` `#剪枝` `#推理成本` `#开源权重` `#商业化`
**生成时间**：2026-10-26 12:45（北京时间）

---

## 一、今日观察

今天这批新闻其实在解同一道题：**怎么让 agent 更强、更便宜**。但解题手法分裂成了方向相反的两派——

一派**往上加**：agent 数量加到 1024 个、参数加到 3 万亿、上下文加到 100 万、融资加到 1000 亿。另一派**往下砍**：把输入 token 砍掉九成、把大模型从记忆关键路径上挪走、把 MoE 专家压到 4bit、把 KV cache 从 8bit 压到 4bit。

真正有意思的不是谁更强，而是**两派报数字的方式完全不对称**：

| 这一派动的旋钮 | 今天的代表事件 | 拿到手的数字 | **有没有报成本** |
| :--- | :--- | :--- | :--- |
| **agent 数量 ↑** | Microsoft 开源 **Agensh**（无中心调度） | pandoc 通过率 **33.89% → 55.06%**（1 → 1024 个 agent） | ❌ 官方明说 token 成本与协调开销**未测量** |
| **参数 / 上下文 ↑** | Kimi K3.1 Pro（3 万亿级、1M ctx） | Terminal-Bench 4.0 **65.7%** | ❌ 未报训练/推理成本 |
| **钱 ↑** | DeepSeek 新一轮融资 | 目标 **500 亿 → 约 1000 亿元**，投前估值约 5000 亿 | ❌ 双方均未公开回应 |
| **吞吐 ↑** | MiniMax M3.1 Flash 上线 72 小时 | 真实用户处理 **超 100 万亿 token** | ❌ 厂商自测 |
| **token ↓** | **TokenGate**（Stanford + UC Berkeley） | TTFT **1.4×–11.3×**，峰值内存降 **1.5×–3.4×** | ✅ 报了，连训练开销都报了（**1.8 vs 2.2 A100 小时**） |
| **模型调用 ↓** | **Jev-Mem**（UT Dallas） | 记忆构建 **158s（6.6×）**、查询延迟 **0.93s（−36.7%）** | ✅ 报了，还把竞品全测了一遍 |
| **精度 / 激活 ↓** | MiniMax M3.1 Flash **428B → 23B 激活** | MoE 专家 **W4A4**、KV **Q8KV8 → Q8KV4** | ⚠️ 报了手段，没报省了多少 |
| **单价 ↓** | OpenAI 折扣抢 Anthropic 客户 | Rippling 编程任务占比 **Anthropic 57%→18%、OpenAI 16%→52%** | 🟡 折扣幅度各家口径打架 |

上半张表五行的共同点是**没有一行报成本**；下半张表三行的共同点是**卖点本身就是倍率**。

而最妙的一笔是 **MiniMax 同时出现在上下两半**：428B 参数是加量，W4A4 量化是减量——**它开源出去的是减量之后的结果，不是加量之后的结果**。今天所有"开源"动作，放出来的其实都是砍完的版本。

最后一条外部约束把这张表钉死了：Apollo 首席经济学家 Torsten Slok 10 月 24 日算出，**S&P 493（标普 500 剔除七巨头）的利润率和人均营收都是平的**。加量派之所以还能不报成本，是因为账单暂时有人替他们付——Ramp 数据显示，模型与推理支出 **99.5% 集中在前 10% 的企业**，而 AI 支出最高的前 1% 企业里 **80.4% 是 VC 支持的**（中位数企业只有 13.1%）。**这笔钱不是从主营业务利润里出的。**

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. Microsoft 开源 Agensh：去掉中央调度器，1024 个 agent 自组织 🟢

**关键数据**：10 月 24 日开源（MIT 许可），论文 arXiv 预印本 **2609.26781**（9 月 22 日）。架构上没有 orchestrator——worker 通过共享工作区（**Gitea**）、消息界面（**Mattermost**）和共享上下文（改编自 **DeLM**）异步认领子任务、自验并合并进度，单 agent 循环跑在 **Copilot harness** 上。

官方 README 给出的数字：五道最难的 ProgramBench 任务，GPT-5.6-sol、高推理强度、**6 小时预算、无网络**，平均通过率从 **1 个 agent 的 19.31%** 升到 **128 个的 28.78%**（相对提升约 **49%**）；**pandoc** 上从 **1 个 33.89%** → **128 个 50.94%** → **1024 个 55.06%**；换成 GPT-6.1-sol，pandoc 从 **1 个 56.19%** → **32 个 79.59%**（相对 **+41.64%**）。团队越大，达到同等通过率的时间也越早；官方观察到"自组织的同伴协作、集成流程与专门化角色随团队规模逐渐涌现"。

⚠️ **最该记的一句恰恰是它没有的东西**：README 和转述都**没有给出任何 token 消耗、总成本或协调开销**，MarkTechPost 直接写明 *"token cost and coordination overhead remain unmeasured"*。用 1024 个 agent 换 21 个百分点的通过率，账单是多少，今天没人知道。

来源：[github.com/microsoft/Agensh（官方 README）](https://github.com/microsoft/Agensh) ｜ 论文：[arXiv:2609.26781](https://arxiv.org/abs/2609.26781) ｜ 转述：[MarkTechPost](https://www.marktechpost.com/)

### 2. TokenGate：可学习的 token 剪枝，让模型先"略读"再"精读" 🟢

**关键数据**：**arXiv 2610.26754**，作者 **Liana Patel、Rishabh Ranjan、Ion Stoica、Matei Zaharia、Carlos Guestrin**（Stanford + UC Berkeley），官方代码 `github.com/tokengate-models/TokenGate`，**Apache-2.0**。

核心矛盾是 top-K 选择不可微、堵死端到端训练，解法是借 MoE 路由的思路做 **token-gated attention**：把每个 token 的重要性分数变成 attention logits 上的偏置，梯度就有了回路。前向分三段——gate 层 L 以下照常处理全部 N 个 token；L 层用一个小 MLP 打分、top-K 保留；L 以上只处理这 K 个 token，**被剪掉的连 KV cache 条目都不生成**。只有文档部分可剪，**问题永远不剪**。

论文摘要页核到的口径：**TTFT 快 1.4×–11.3×**，**峰值内存降 1.5×–3.4×**，且"无精度损失"；对比最好的先前剪枝方法，**prefill 最多快 6.4×、峰值内存低 2×**。测试模型 Qwen3-1.7B 与混合注意力的 Qwen3.5-2B，上下文最长 128k，MLP gate + **LoRA（r=16）**。

🟡 正文级数字（来自 MarkTechPost 对论文的报道，摘要页未逐条核）：最佳项是 **NIAH 16k，11.3× TTFT + 3.42× 内存**；2WikiMultihopQA 在保住 95% 全上下文精度时 **3.0× 快、2.7× 省内存**；训练用 4 张 A100、每步比纯 LoRA 慢 1.3×，但**平均 1.8 vs 2.2 A100 小时**收敛；6 个基线是 FastKV、SlimInfer、DASH、GemFilter、FlexPrefill、MInference。作者与转述方都提醒：**最快 11.3× 与最长上下文的 13.0× 口径未对齐、不同测试环境不可直接比较，且 TTFT 快不等于整段响应快**。

来源：[arXiv:2610.26754](https://arxiv.org/abs/2610.26754) ｜ [MarkTechPost（2026-10-25）](https://www.marktechpost.com/2026/10/25/stanford-berkeley-tokengate-learned-token-pruning-llm-prefill/)

### 3. Jev-Mem：把大模型从"记忆关键路径"上挪走，反而更准 🟢

**关键数据**：**arXiv 2609.23986**（2026-09-21 提交，UT Dallas，Dongming Jiang / Yi Li / Bingzhe Li；代码 `github.com/libingzheren/Jev-Mem`）。⚠️ 注：这是 **9 月底的预印本，本周转热**，不是今天新发。

设计借 System-One / System-Two：高频但输出有界的决策（记忆打型、关系判断、查询路由、检索预算分配、图遍历、候选打分、**何时停止检索**）全部交给一个**非生成式的轻量控制器**，System Two 的大模型只在真正需要复杂推理和写最终答案时才被调用。

LoCoMo 上的官方数字：LLM-as-a-Judge 总分 **0.777**，比最强基线相对高 **11.0%**；记忆构建 **158 秒**，比最快的竞品内存系统快 **6.6×**；平均查询延迟 **0.93 秒**，降低 **36.7%**。

最有用的是它把竞品成本也一并测了：**A-MEM 构建 3,636 秒、MemoryOS 3,276 秒、最快的 Nemori 仍要 1,044 秒**；而**把整段对话直接塞进上下文**这个最常见做法，既最慢之一（每查询 1.74 秒）又最差（总分 **0.481**）。作者明说当前控制器只是 System-One 的一种具体实现。局限：**只在 LoCoMo 一个长对话记忆基准上验证过**，尚未推广到编码助手或长程规划。

来源：[arXiv:2609.23986（原文 HTML）](https://arxiv.org/html/2609.23986v1)

### 4. MiniMax 开源 M3.1 Flash：428B 参数，只激活 23B 🟢

**关键数据**：10 月 23 日开源权重，**总参数 428B、激活参数 23B**（模型 10 月 19 日上线）。三项提效手段官方写得非常具体：

- **全模型稀疏注意力**：把**前三个全注意力层**替换为稀疏注意力；
- **量化感知训练（QAT）**：路由 MoE 专家迁到 **W4A4**（共享专家除外），稀疏注意力索引器与主分支从 **Q8KV8 迁到 Q8KV4**；
- **Power-aware scheduling**：对计算卡功耗做精细分配，让卡持续维持高算力。

生态侧：**上线 72 小时内真实用户处理超 100 万亿 token**（厂商自测）；开源首日接入华为昇腾、平头哥、昆仑芯、摩尔线程、壁仞、海光、沐曦、天数、NVIDIA、AMD 等芯片厂商，以及 Together AI、Fireworks、Nebius、Baseten、Modal、DigitalOcean 等平台；vLLM、SGLang、智源 FlagOS、Hugging Face、魔搭同步适配。权重地址：`MiniMaxAI/MiniMax-M3.1-Flash`（HF）与 `MiniMax/MiniMax-M3.1-Flash`（魔搭）。

🟡 待核实：100 万亿 token 为厂商自测口径；三项优化**各自省了多少**官方未给量化结果。

来源：[凤凰网科技 / IT 之家（2026-10-23）](https://tech.ifeng.com/c/8xS2MhhHwsc) ｜ [腾讯新闻转载](https://news.qq.com/rain/a/20261023A0555900) ｜ 权重页：<https://huggingface.co/MiniMaxAI/MiniMax-M3.1-Flash>

### 5. Apollo：S&P 493 的利润率和人均营收都是平的 🟢

**关键数据**：Apollo 首席经济学家 **Torsten Slok** 10 月 24 日《Daily Spark》提出 **"S&P 493"**（标普 500 剔除 Alphabet、Amazon、Apple、Meta、Microsoft、Nvidia、Tesla）。结论：**人均营收与利润率只有七巨头在上升，其余 493 家是平的**；全要素生产率（旧金山联储 Fernald 2014 经产能利用率调整序列）**看不到被 AI 推升的迹象**。

原话：*"Despite massive investments and widespread hype around artificial intelligence, the technology has delivered zero financial payoff to corporate America outside of tech."* 以及 *"AI may be a great calculator, but in business, intelligence is mostly judgment."* 他还指出 AI **不理解问责、信任、文化、不成文规则、伦理权衡与公平**。

更可执行的是他引的 **Ramp 数据**：模型服务与推理支出 **99.5% 集中在前 10% 的企业**；付给 OpenAI 与 Anthropic 的支出 **95.6% 来自前 10%**；AI 支出最高的前 1% 企业中 **80.4% 是 VC 支持**（中位数企业仅 **13.1%**）。他在 10 月 22 日的报告里把这称为 token 支出的"**循环性**"——买最多算力的新创，是拿创投资金而不是本业盈利在付钱。

⚠️ 需谨慎：这是**观点性笔记 + 五张图**，不是新研究；TSNMedia 也提醒"人均营收与利润率是钝指标，不能证明 AI 在 S&P 493 内部什么都没做，只能证明收益还不够大到推动这两个数"。

来源：[TechCrunch（2026-10-25）](https://techcrunch.com/2026/10/25/ai-delivers-zero-financial-payoff-to-most-companies-according-to-apollo-economist/) ｜ [AI Breaking Wire（含 Ramp 数据）](https://www.aibreakingwire.com/news/apollo-economist-no-ai-payoff-for-sp-493-companies)

### 6. OpenAI 用折扣抢 Anthropic 客户：Rippling 的编程任务占比 5 个月反转 🟡

**关键数据**：据 The Information（10-24 报道），OpenAI 通过降价、赠送额度、加强技术支持争夺 Anthropic 的企业客户。**Rippling CEO Parker Conrad** 给出的一组数字最硬：今年 5 月 Anthropic 模型承担其数百名工程师 **57%** 的编程工作、OpenAI 仅 **16%**；现在反转成 **OpenAI 52%、Anthropic 18%**。

机制上有个细节值得抄：**Anthropic 有一条"客户用量触达合同上限后折扣即取消"的规则，据称正是这条让它丢了 Replit 订单**；Replit 侧 reportedly 只用数小时改完代码完成切换。DataCamp CEO 称预计成本可降 **80%–90%**。

🟡 **折扣幅度各家口径冲突，不要引用单一数字**：The Information 写 **40%**、给 Replit 的折扣 **超 30%**、合同年金额 **超 1 亿美元**；The Decoder 标题写 **最高 90%**；北京日报另一篇讲的是 10 月 7 日 Haiku 5.5 定价较 Haiku 4.5 降约 90%（**与本次企业折扣不是同一件事**）。**建议只记住方向（在打价格战）与 Rippling 那一组可核的占比变化，折扣百分比暂不作为事实引用。**

来源：[新浪财经（转 The Information，2026-10-25）](https://finance.sina.cn/2026-10-25/detail-iniwmhuv9940950.d.html) ｜ [新浪财经（转 WSJ，2026-10-25）](https://finance.sina.com.cn/stock/usstock/c/2026-10-25/doc-iniwmanw3213693.shtml) ｜ [The Decoder 转述](https://the-decoder.com/)

---

## 三、为什么值得记

1. **"堆量"的账今天第一次被外部问了。** 1024 个 agent 换来 pandoc 通过率 +21 个百分点，官方连 token 成本都没测；3 万亿参数的模型没人报训练成本；1000 亿融资双方都不回应。而减量派的三项成果，**卖点本身就是倍率**（6.6× / 11.3× / 1.5–3.4×）——因为它们必须证明"省下来了"。**当一家公司用倍率当标题、另一家用百分点当标题时，你知道谁在为成本负责。**

2. **"开源"放出来的从来是砍完的版本，不是堆完的版本。** MiniMax 的 428B 是工程结果，**W4A4 + Q8KV4 + 前三层换稀疏注意力才是它开源的东西**；Nanbeige4.3-33B（Apache 2.0、524,288 上下文、推理默认开启）的定位干脆就是"**teacher 模型**"——官方明说下一步是把它蒸馏成 Nanbeige4.3-3B。**开源发布物 = 减量后的可分发形态**，这条规律比任何一个榜单分数都实用：你要抄的是它砍了什么，不是它堆了多少。

3. **Agensh 最锋利的地方是它没有 orchestrator。** 主流多智能体框架（含今天大多数 coding harness）都假设有一个中心调度器在分解任务、分配、汇总；Agensh 是 worker 到共享 Git 工作区**自己认领**、自己验证、自己合并，协调靠消息板与上下文板。这直接回答了"规模化的瓶颈是调度器还是 worker"这个问题——但同样地，**它没有回答 1024 个 agent 到底烧了多少钱**。在有人补上这个数字之前，1024 只能当上限参考，不能当配置建议。

4. **Apollo 那条数据真正的含义是：加量派的现金流来自 VC，不来自客户。** 99.5% 的推理支出集中在前 10% 企业、前 1% 里 80.4% 是 VC 支持——这意味着**今天"堆量"的可行性建立在融资环境上，而不是建立在客户付费意愿上**。Slok 那句"主流企业开始把 token 支出视为压缩利润率的成本中心"如果成立，第一个受冲击的不是模型厂商，是那些按 token 消耗量收费的 agent 产品。**这也是为什么"减量派"的成果今年会越来越有商业价值：它们卖的是同一个能力、更少的 token。**

---

## 四、可行动

- [ ] **在照抄 1024 之前，先跑一次 N=1 / N=8 / N=32 的成本对照。** Agensh 给了 `REPRODUCE.md` 与 `scripts/launch_single_node.sh`（Docker Compose 单节点）和 `launch_single_agent.py`（单 agent 基线）。跑的时候**一定要把每档的 token 消耗和墙钟时间记下来**——论文没测的正是这个，谁先补上谁就有发言权。
- [ ] **给你的长上下文 pipeline 量一遍 TTFT 与 KV cache 占位的基线。** TokenGate 的思路可以直接照搬成一个自查项：你的 prompt 里**哪一部分是"文档"、哪一部分是"问题"**？如果现在两者混在一起，就没有任何剪枝方案能安全生效。它的接口是 `{state}` 占位符标记可剪文档 + `generate(max_kept_prefill_tokens=...)` 预算，这个"先标文档再给预算"的形态值得直接抄进自己的设计里。
- [ ] **审计 agent 里"每一步都调大模型"的决策点。** 按 Jev-Mem 的清单逐项查：记忆打型、相关性判断、查询路由、检索预算、**什么时候停止检索**。凡是输出只是一个标签或一个分数的，都可以换成分类/打分小模型。对照基准：全量塞上下文在 LoCoMo 上只有 **0.481**，比任何结构化方案都差——**"上下文变长"不能替代"记忆变结构化"**。
- [ ] **评估开源模型时，先看它砍了什么、再看它堆了多少。** M3.1 Flash 的 W4A4 意味着你的推理框架必须支持对应量化路径；Nanbeige4.3-33B 是 dense 33B，BF16 权重约 **66 GB**、官方示例是 **4 卡 tensor-parallel**，且它**纯文本无视觉**。选型表建议新增两列：**量化方案** 与 **推荐部署形态**。⚠️ Nanbeige 的分数全部为**官方自测**，且其对比表中 Muse-Glimmer-30B / Gemma4-31B 的 SWE-Bench Pro 一行看起来与 Meta、Google 自家卡片**对调了**，第三方复核出现前不要据此换栈。
- [ ] **把明年的 AI 预算口径从"每 token 单价"改成"每任务成本"，并标注这笔钱由谁承担。** Apollo 的口径下，主流企业正在把 token 支出重分类为成本中心。如果你所在组织的 AI 支出主要靠预算拨付而非业务增收，那么**减量派的成果（剪枝、结构化记忆、量化）比换更强的模型更直接影响你的续费谈判**。

---

## 五、术语卡

| 术语 | 是什么 | 今天为什么重要 |
| :--- | :--- | :--- |
| **Prefill / TTFT** | Prefill 是模型吞掉整个输入、还没吐出第一个 token 的阶段；TTFT（Time To First Token）就是这段等待。注意力开销随长度平方增长 | TokenGate 砍的就是这一段：TTFT 快 1.4×–11.3×。⚠️ TTFT 快**不等于**整段响应快，长输入场景收益最大 |
| **Token Pruning（token 剪枝）** | 在前向中途按重要性丢掉一部分 token，上层只处理留下的那些；被丢的连 KV cache 都不生成 | 难点是 top-K 不可微。TokenGate 借 MoE 路由把分数变成 attention logits 的偏置，绕开了这一点 |
| **System One / System Two** | 认知心理学的双系统：System One 快、自动、便宜；System Two 慢、 deliberate、昂贵 | Jev-Mem 把它落到工程上：高频有界决策给非生成式控制器，大模型只在最后写答案时出场，于是**又快又更准** |
| **W4A4 / Q8KV4** | 权重 4bit、激活 4bit；KV cache 键 8bit、值 4bit 的量化精度 | M3.1 Flash 把路由 MoE 专家压到 W4A4（共享专家除外）、KV 从 Q8KV8 降到 Q8KV4——**它开源的是量化后的形态**，你的推理栈得跟得上 |
| **蒸馏（Distillation）** | 用大模型（teacher）的输出与轨迹训练小模型（student），让小模型获得自己学不会的行为 | Nanbeige4.3-33B 官方定位就是 teacher，下一步蒸馏出 3B。这是"减量派"最直接的产品化路径 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
