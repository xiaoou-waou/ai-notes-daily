# 2026-10-09｜同一个判断，四种数字

> 决策模型把"答案"压成了一个概率；今天所有证据都在说，这个概率还站不稳。

**标签**：`#决策模型` `#校准` `#Agent工程` `#开源生态` `#评测方法`
**生成时间**：2026-10-09 12:12（北京时间）

---

## 一、今日观察

两周内长出一个新品类：**决策模型（decision model / "System One"）**。它不生成 token——读入一段 state 加若干带类型的问题，一次前向传播，返回每个候选答案的概率。9-15 TypeSafe 的 Jev 首发，半个月内 OpenAI、Perplexity、Cloudflare、AWS、Liquid AI、上海 AI Lab、StartLux 全部入局。

真正的变化不是"多了一种模型"，而是**错误的形态变了**。生成式模型答错时，你能从文字里看出来；决策模型返回 `0.83` 时，你无法判断该不该信——除非你手里有一条"置信度 → 实际正确率"的曲线。于是这类模型的全部价值押在一个数字的稳定性上，而今天的证据显示：这个数字在四种变动下都会变。

| 变动什么 | 同一判断变成了什么 | 幅度 | 信源 |
| --- | --- | --- | --- |
| **换提问类型** | OpenAI Decisions API 上，一枚 70/30 偏硬币：用 `predicate` 问 1000 次 → 正面 **70%**；同一个问题改 `choice` 问 → 正面 **98%** | 0.70 → 0.98，后验塌成 argmax | 🟡 官方论坛用户自测 |
| **换任务是否见过** | Strands Decider：训练过的任务 `noul` **0.961** / `choice` **0.960**；6,000 条未见过的短任务 **0.650**。仓库并明文写"未见过的任务上 `score` 题型不可用" | −31 个点 | 🟢 官方仓库评测文件 |
| **换模型尺寸** | Cloudflare 官方 changelog 表格：CLINC150+OOS macro-F1，Clef(27B) **97.43** vs Clef-flash(9B) **66.77** | −30.66 点 | 🟢 官方 changelog |
| **换一次重训** | 同一配方重训 6 次：159 / 160 / 162 / 165 / 165 / 167（均值 163.0，**SD 3.2**）；任意两次在 231 题里有 **10–19 题**结论相反 | ±约 1.4% 绝对分 | 🟢 官方仓库评测文件 |

第 4 行最值得停一下：AWS 自己在同一份文件里写下"**v17 相对 v16 的 +1 是噪声**"。一家厂商公开宣布自己在排行榜上的进步是噪声——这比任何外部批评都更能说明这张榜的分辨率有多粗。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. OpenAI Decisions API 进公测，官方论坛里第一个复现实验就翻了车
🟢 `POST /v1/decisions`，**2026-10-06** 公测；仅支持 `gpt-6-luna`；三种题型 `predicate` / `choice` / `score`；文本 + inline base64 图片，**不接受**图片 URL、file id、音频、function call、非 user role，单请求最多 128 个图片 part；**$0.10 / 100 万输入 token**，不收 output、cache-read、cache-write 费（另一位用户追问，"目前确实没有缓存"，被官方社区确认）。

🟡 官方开发者社区里用户 *platypus* 的偏硬币实验：`predicate` 问法下正面 70%（与真实偏置一致），改 `choice` 问法后正面 **98%**——"**it's not estimating the true posterior at all**"；并追加"**choice order changes the probabilities**"（选项顺序会改变概率）。其结论原文："**My verdict right now is don't use choice questions.**" 该实验为**单人自测、未经复现**，不作为既定事实，但它是目前唯一公开的、可复现步骤清晰的同类测试。

🟡 同帖另一位用户自测（数百道词游戏 + 一个对话游戏题）：`judgment` 类问题上 Luna 的"自信错答"约为 Jev 的 **3 倍**；多轮对话中位单轮 Jev **0.3s** vs Luna **1.6s**；同等题量成本 **2–3 倍**；窄事实判断上两者相当。OpenAI 自己的建议是"**用你自己应用的标注样本来选阈值**"。

来源：[OpenAI Developer Community - Decisions API is now available in Public Beta](https://community.openai.com/t/decisions-api-is-now-available-in-public-beta/1403877)

### 2. AWS Strands Decider 2B：唯一把"重训噪声"和"校准"写进仓库的一家
🟢 仓库 `strands-labs/strands-decider`，**Apache-2.0**，**534★ / 68 fork**，创建于 2026-09-29（10 天内）。

- README 原文：**"On short classification tasks it has never seen, answers at a confidence of 0.9 or more are right about 95% of the time... below that, confirm or ask a person. Frontier LLM inference APIs do not expose anything equivalent."**（置信度 ≥0.9 的答案在未见过的短分类任务上约 95% 正确；低于此则确认或问人。前沿 LLM 推理 API 不暴露任何等价物。）
- `evaluation/results.md`：JevBench public **176/231**，Brier **0.323**，ECE **0.064**（发布链路）/ 0.074（训练链路）
- **选 seed 的规则在排名前就写死**：对五项指标取六个 seed 的 z-score 平方和，发布距离最小的那个——"**so that the release is a representative seed and not the luckiest one**"
- 延迟：RTX 3090（WSL2）中位 **115ms** / p95 **299ms**；M3 Pro 中位 **234ms** / p95 **2,628ms**（**p95 是中位数的 11 倍**）
- 未见任务：训练过的 `noul` 0.961 / `choice` 0.960 → 6,000 条未见短任务 **0.650**；官方明文 *"On tasks it has never seen, `choice` is useful behind a confidence gate and `score` is not."*

来源：[github.com/strands-labs/strands-decider](https://github.com/strands-labs/strands-decider) · [evaluation/results.md](https://github.com/strands-labs/strands-decider/blob/main/evaluation/results.md)

### 3. Cloudflare Clef / Clef-flash：延迟打 Jev 2.5× / 13×，但官方表格里藏着一处 30 点断层
🟢 官方 changelog（2026-10-01）：Clef 中位 **209.3ms** / p95 238.6ms；Clef-flash **38.8ms** / p95 122.4ms；Jev **524.1ms** / p95 536.0ms。基于 43 次基准运行。宣称"10 项决策基准中 Clef 系列 7 项第一"，TypeSafe 自己的 workflow evals 上 4 项赢 3 项（invoice / customer service / security incidents）。

🟢 同一张官方表里的断层（macro-F1 / case-exact）：

| 基准 | Clef (27B) | Clef-flash (9B) | Jev |
| --- | --- | --- | --- |
| BFCL (case exact) | 98.47 | **98.76** | 95.75 |
| BANKING77 (macro-F1) | **94.20** | 90.93 | 79.74 |
| CLINC150+OOS (macro-F1) | **97.43** | 66.77 | 89.27 |
| Home appliances (case exact) | 82.95 | **97.73** | 52.27 |

"Clef 系列 7 项第一"是把两个尺寸合并计数得出的。**flash 档不是全面小一号，它在 CLINC150+OOS 上比自家 27B 低 30.66 点**——而它恰恰是被推荐放在热路径上的那一档。

- 🟢 Apache 2.0 权重（HF `Cloudflare/clef`、`Cloudflare/clef-flash`）；64K 上下文（Jev 为 32K）；带 vision encoder，单请求最多 4 张图；`noul`/`choice`/`score` 三型，单请求最多 64 个问题
- 🟡 定价 $0.24 / $0.09 per 1M input（Workers AI 模型页，多源转述一致，未直连核实）
- 🟡 **训练数据不公开**（Cloudflare 的 Michelle Chen 对 The Register 明确答复）；本地自托管约需 85GB / 41GB VRAM（同一来源）
- 🟢 内部用例：域名分类 2.2s vs 通用模型 `gpt-oss-120b` 的 4.7s（厂商自测）
- 后训练方法：label-smoothed cross-entropy + **Brier loss（为校准）** + 自命名的 RLCD（Reinforcement Learning for Calibrated Decisions）🟡

来源：[Cloudflare Changelog - Introducing Clef](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/)

### 4. Liquid AI d1-3B / d1-omni-600M：端侧跑通了，但"Open-weight"在自家两处页面上互相打架
🟢 官方博客（10-07）：d1-3B 在 Decision Index v0.2.1 public split 得 **48.57**，<10B 里第一，与 **12 倍大**的 Decider 35B-A3B（47.11）持平；七项文本基准均值 **82.9**（Decider 4B 81.1、Decider 2B 77.1）。d1-omni-600M 得分 **15.95**。

🟢 延迟（单次一问）：RTX 4090 **8ms**、AMD MI325X 9ms、Jetson AGX Thor 16ms、Apple M5 Pro 30ms、Jetson Orin Nano **50ms**。**但 3.4K-token 的 state 在 Orin Nano 上是 1,640ms**——单问 50ms 的 **33 倍**。三问约为一问的 1.3 倍时长。

🔴 **一处必须点出的矛盾**：博客"Get Started"一节写 **"Open-weight — Download, fine-tune, and deploy without restrictions"**；而 Liquid 自己的许可文档写的是 **LFM Open License v1.0**——"**Free if your annual revenue is under $10M USD. Paid license required above that.**"（年收入 1,000 万美元以下免费商用，超过则须另购商业许可；修改与衍生模型同样受此约束）。**"open-weight" 和 "无限制商用" 在同一家公司的两个页面上同时成立。**

🟢 官方自陈边界：Decision Index v0.3 的视觉分区是私有的、本轮不报；d1-omni-600M 是实验性 checkpoint，**官方不发布任何延迟数字**；"**Dedicated audio decision benchmarks are currently an open problem**"（专门的音频决策基准目前是空白）。

来源：[liquid.ai/blog/d1-open](https://www.liquid.ai/blog/d1-open) · [LFM Open License v1.0](https://docs.liquid.ai/lfm/getting-started/model-license)

### 5. 国产侧：七天出货，且几乎全以后训练 Qwen 为底座
🟡 **上海 AI Lab Intern-Decision**（9-28 开源）：0.8B / 2B / 4B 三档。4B 在七项评测套件上平均 **90.02%**，对比 Jev **88.74%**（+1.28），测试共 **10,000+ 行**（含 typed decisions、tool calling、新闻分类、越狱检测）；单张消费级 RTX 4090 上本地请求平均约 **44ms**；微调 Qwen3.5 语言主干、冻结 vision tower 与 projector；**国产 GPU 厂商沐曦（MetaX）完成 Day-0 适配**。**开发者自测**；训练数据与部分私有验证记录未公开。

🟡 **StartLux-Decision**（10-03/04，上海原点星辉）：0.8B–27B 五档，开放代码与权重。Decision Index 0.2.1 上 27B 得 **63.88** vs Jev 1.13 的 **57.91**，38 项基准中 **31 项**更高；在 Intern-Decision 团队那套七项评测上 27B 达 **91.82%**（Jev 88.74% / Intern-Decision-4B 90.02%）。单张 H200、BF16、短请求下：4B 一次答三问 **26ms**，0.8B **12.2ms**，2B **15.5ms**。团队自述"研发与验证全程仅 **3 天**"，由内部 Auto Research（RSI）循环驱动。**以上均为团队自测 + 中文媒体转述，对照的是 2026-09-28 榜单快照。**

🟡 **同一底座现象**：Clef（Qwen3.8-27B）、Clef-flash（Qwen3.5-9B）、Strands Decider（Qwen3.5-2B）、Intern-Decision（Qwen3.5）、Perplexity pplx-decider-v1.1-27b（Qwen3.8-27B）全部以后训练 Qwen 为主干。**这条赛道的"模型层"创新几乎全部发生在同一批国产开源基座之上。**

来源：[Pandaily - Shanghai AI Lab Open-Sources Intern-Decision](https://pandaily.com/shanghai-ai-lab-intern-decision-open-source-0-8b-2b-4b-decision-model) · [文汇报/转述 - StartLux-Decision](https://www.163.com/dy/article/L8J8576I05506BEH.html) · [腾讯新闻 - Jev被请下王座](https://news.qq.com/rain/a/20261003A037YH00)

### 6. 接入层在同一周被一次性补齐（补充）
🟢 **llama.cpp v0.6.0**（10-05）新增 `/v1/systemone` 服务端点，服务端到 **6 个决策模型**，含 Cloudflare Clef 的文本与视觉支持。🟡 SGLang v0.5.21 加 `/v1/decisions`（把已有 LLM/VLM 直接变 classifier + scorer）；Ollama、Pydantic AI（`DecisionModel` / `SystemOneModel`）、Vercel AI SDK（`experimental_decide`）、Vercel AI Gateway（OpenAI 兼容 `/decisions`）均已接入。

> **接口层已经冻结，模型层还没有。** `/v1/systemone` 这个格式名来自 TypeSafe，Cloudflare / AWS / Liquid / Ollama / Pydantic 全线兼容，只有 OpenAI 走自己的 `/v1/decisions`。好消息是替换成本接近零；坏消息是**没有任何一家积累的 calibration 能迁移到另一家**。

来源：[Sentient Foundation - OS AI Field Notes 9 Oct 2026](https://sentient.foundation/news/os-ai-field-notes-october-9-2026)

---

## 三、为什么值得记

1. **这个品类卖的不是智能，是"可动作性"，而可动作性整个建立在概率上。** 生成式模型给你的文字错了，下游代码可能解析失败、可能被人看出来；决策模型给你的 0.83 无论对错都长得一模一样。**错误的可见性被设计掉了**——这是它快的代价，不是免费午餐。

2. **厂商发布的指标和你需要的指标不是同一个。** 厂商发的是准确率（跨基准聚合）与中位延迟；你需要的是**在自己任务分布上、按自己问法、在 p95 下、且知道它会随重训漂移**的那条曲线。Strands 是唯一把这四件事都写出来的厂商——而且它一旦写出来，数字并不好看（未见任务 0.650、Mac p95 是中位 11 倍、+1 分是噪声）。**愿意公布难看数字的那家，反而是当前最值得信的。**

3. **"问法"第一次成了模型行为的一部分。** 同一枚硬币，`predicate` 给 70%、`choice` 给 98%；选项顺序还能再改一次概率。这说明这类模型输出的不是后验，而是**被题型和顺序塑形过的分数**。以后凡调用决策模型，**提问方式要进版本控制和回归测试**，和 prompt 同等对待。

4. **一周内出货五家，说明壁垒不在模型层。** StartLux 自述 3 天完成研发验证；其余各家都是"冻结 Qwen 主干 + LoRA / 分类头 + 少量后训练"。真正的分化发生在别处：Cloudflare 押**边缘托管 + RL 微调服务**（且训练数据不公开），OpenAI 押**托管计费**（且无缓存、比 Jev 贵 2–3 倍 🟡），AWS/Liquid 押**可下载权重**，Liquid 还额外插了一道**年收入 1,000 万美元的商用闸门**。**选型时挑的是交付形态与许可，不是分数。**

---

## 四、可行动

- [ ] **把所有用 LLM 做分类/路由的调用点列出来，改成 `predicate` + 阈值，暂不用 `choice`。** 理由是 OpenAI 论坛那个偏硬币实验：同一语义下 `choice` 的后验会塌向 argmax（`predicate` 70% → `choice` 98%）。若必须用 `choice`，至少做一次"打乱选项顺序看概率是否变化"的回归。
- [ ] **用自有标注样本画一条"置信度 → 实际正确率"曲线，再定阈值。** 参考 AWS 的做法与量级：置信 ≥0.9 时约 95% 正确；低于阈值就转人工或转大模型。**不要沿用厂商在公开基准上给的阈值。**
- [ ] **延迟只记 p95/p99，不记中位数。** M3 Pro 上中位 234ms、p95 2,628ms（11 倍）；Orin Nano 上单问 50ms、3.4K-token state 1,640ms（33 倍）。凡在热路径上放决策模型，先跑一次长 state 与尾部延迟。
- [ ] **核许可，别只看"open-weight"。** Liquid 的 d1 系列用 LFM Open License v1.0：**年收入超过 1,000 万美元免费商用权即终止**，衍生模型同样受限；Cloudflare Clef 是真 Apache-2.0，但训练数据不公开、本地需 41–85GB VRAM 🟡。
- [ ] **用 llama.cpp v0.6.0 的 `/v1/systemone` 端点把 Clef、d1-3B、Strands Decider 三个本地模型接进来，跑同一批自有题目对比。** 接口已统一，替换几乎零成本——这正是做横向对比的最好时机。
- [ ] **给决策调用加审计日志：记录问法类型、选项顺序、返回的完整概率分布与最终采取的分支。** 概率会随重训漂移（AWS 实测两次重训在 231 题上有 10–19 题结论不同），没有日志就无法归因。

---

## 五、术语卡

| 术语 | 解释 | 今天为什么重要 |
| --- | --- | --- |
| **决策模型（Decision Model / System One）** | 不生成 token 的模型。输入一段 state 与若干带类型的问题，一次前向传播返回每个候选答案的概率。三种题型：`noul`（是/否，返回 P(是)）、`choice`（多选一，返回每选项概率 + 置信度）、`score`（按有序标尺打分，返回概率加权分）。 | 两周内从单品变成一个品类，OpenAI/Cloudflare/AWS/Liquid/上海 AI Lab/StartLux 全部入局。 |
| **校准（Calibration）** | 模型给出的概率与实际正确率是否一致。说"0.8 置信"的样本里若真有 80% 正确，就是校准良好。常用 **ECE**（Expected Calibration Error，越小越好）与 **Brier score**（概率评分的均方误差，越小越好）衡量。 | 决策模型的一切价值都押在概率可信上。AWS 报告 ECE 0.064、Brier 0.323；Cloudflare 的训练目标里明写用 Brier loss。 |
| **置信门（Confidence Gate）** | 在概率上设阈值：高过阈值自动执行，低于阈值转人工或转更强的模型。 | AWS 给出的可迁移量级：≥0.9 约 95% 正确；且明确"未见过的任务上 `score` 题型不配用置信门"。 |
| **JevBench / Decision Index** | 决策模型的公开评测集与榜单。JevBench 含 231 道公开任务；Decision Index 当前版本 v0.2.1（v0.3 的视觉分区为私有）。**注意：各厂商分数的对照口径与快照日期并不统一。** | StartLux 的 63.88 对照的是 9-28 榜单快照上的 Jev 1.13（57.91）；Liquid 的 48.57 对照的是 Decider 35B-A3B 的 47.11。**跨家比分数前先比快照日期。** |
| **prefill-only / 零输出 token** | 决策模型只做一次前向（等价于 LLM 的 prefill 阶段），不进入自回归解码，因此 `output_tokens = 0`，也不存在推理 token 等待。 | 这是它快的根本原因，也是定价上"只收输入费"的来源。代价是输出形状被 schema 完全限定。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
