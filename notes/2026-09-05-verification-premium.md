# 2026-09-05｜答案在贬值，验证在升值

> Claude 11 天写出 1300 万行 Lean 证明，陶哲轩却警告黑盒答案会污染数学：价值正从生成移向验证。

**标签**：`#验证` `#形式化` `#Agent` `#RAG` `#开源`
**生成时间**：2026-09-05 23:20（北京时间）

---

## 一、今日观察

今天最有意思的不是任何一个新模型，而是**同一天里出现的两组互为镜像的事件**：一边是 Anthropic 把 AI 生成的数学证明交给了机器检查器，1300 万行代码被逐条验证、站得住脚；另一边是 OpenAI 高调公布一个新的数论界值 186，却被数学界集体判定为"尚未成立"。

区别不在答案本身，而在**有没有一个独立于生成方的校验层**。

| 事件 | 生成方 | 有没有外部校验层 | 结果 |
| :--- | :--- | :--- | :--- |
| Claude 形式化费马大定理 | Anthropic | ✅ Lean kernel 逐条检查 + comparator 对齐 Mathlib 定理陈述 | 帝国理工 Kevin Buzzard 背书，成果可复用 |
| GPT-6 素数间距 186 | OpenAI | ❌ 仅自评，无独立人类语义审查 | 数学界不认账，陶哲轩公开批评 |
| WeKnora v0.8.0 | 腾讯开源 | ✅ 审计日志 + Langfuse OTel 全链路追踪 | 企业敢往里放私有文档 |
| Xiaomi-TabLDM | 小米开源 | ✅ 权重/代码/技术报告全公开 | 榜单可被第三方复现或推翻 |

一句话：**当"生成"的成本趋近于零，"可被验证"就从辅助环节变成了产品本身。** 谁把 AI 输出变成可机器校验、可复现、可审计的证据，谁才拿得到下一轮预算。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 Claude 用 11 天写出费马大定理首个端到端机器验证证明

- **11 天**、基本自主完成；写下 **1300 万行 Lean 代码**（规模超过 Mathlib 的 **5 倍**）
- 过程中证明了 **30,300 个定理**，最终证明使用其中 **29,500 个**
- 架构：基于 **Claude Code 的多智能体 harness**，数十个 agent 通过 **Prove2Me**（哥大 Tianyi Peng 等设计）协作，该平台维护定理陈述的 **DAG**、加速 Lean 编译
- 消耗约 **60 亿输出 token**，底座是"大致相当于 Claude Fable 5.1 的内部研究模型"
- 校验：只使用 **Lean 的三个标准公理**；一个 **comparator** 确认定理陈述与 Mathlib 自身的 FLT 陈述一致
- 一个耐人寻味的细节：早期**失败的尝试贡献了最终证明约 7% 的非样板行**
- 遵循 Darmon–Diamond–Taylor 的简化版 Wiles 证明（不是新证明，是形式化）；帝国理工 **Kevin Buzzard** 评审
- 来源：[Anthropic 官方研究博客](https://www.anthropic.com/research/formalizing-fermats-last-theorem) · [GitHub anthropics/fermats-last-theorem](https://github.com/anthropics/fermats-last-theorem)

### 2. 🟢 陶哲轩警告：AI 黑盒答案会"污染"开放问题

- 发布于 **2026-09-03**，以不可压缩 Navier–Stokes 方程全局正则性问题为例
- 核心机制判断：**负责迭代的那一方如果提前知道最终正确的 ansatz，就会自然抑制对其他路线的探索**——那些看似"死胡同"的路线，其失败方式本身往往最具启发性
- 最坏情形设想：一个**自主 AI harness** 在内部完成全部迭代，而运行它的公司把过程"几乎完全隔绝在公众视野之外"；结果是"数学界最著名的开放问题之一技术上被解决了，但数学几乎没有获得任何新增价值"
- 结论原话：过早地用纯 AI 方法解决问题、且过程不透明，"可能把这个过程污染到实际上对整个数学进展**净负面**"的程度
- 来源：[陶哲轩 Mathstodon 原帖（6 段长帖）](https://mathstodon.xyz/@tao/117207849921390904)

### 3. 🟡 素数间距三方竞速：186 / 188 / 212，数学界不买账

- 转述口径：GPT-6 Astra 宣称把孪生素数连续间距上界从 **246** 推到 **186**，Anthropic、Axiom 同期分别宣布 **188**、**212**
- 陶哲轩形容这是"**令人无语的一幕**"（unedifying spectacle），并庆幸牛津数学家 **Julia Stadlmann** 赶在问题被"污染"前，于 8-31 凭对平滑模数的新估计把上界缩到 **240**
- 关键质疑：环球科学指出 186 目前**审查状态仅为 OpenAI 自评，尚未经过任何独立的人类语义审查**；从 212→188→186 更像同一套方法的不同调参，而非范式突破
- 历史坐标：张益唐 7000 万 → Maynard 600 → 246
- 来源：[量子位转述](https://view.inews.qq.com/a/20260905A063W000) · [今日头条分析](https://www.toutiao.com/article/7681935652455318022/) · 陶哲轩原帖 [mathstodon.xyz/@tao](https://mathstodon.xyz/@tao)
- ⚠️ **未找到 OpenAI 官方论文页，186/188/212 三个数字均为媒体转述，待官方源核实**

### 4. 🟢 腾讯开源 WeKnora v0.8.0：把"可审计"写进 RAG 框架

- 9 月 3 日版本 bump，定位：**RAG 快速问答 + ReAct Agent + 自维护 Wiki（含交互式知识图谱）**三合一
- v0.8.0 新增：Skill sandbox runtime（**Docker / E2B / Cube 会话级持久沙箱**，per-tenant 网络策略）、tenant skill catalog、跨会话长期记忆、进程内 anydoc Office 解析
- 企业侧：4 级 RBAC（Owner/Admin/Contributor/Viewer）+ **per-workspace 审计日志** + per-KB 活动审计轨迹；**Langfuse OTLP/OTel tracing**，带 W3C traceparent 传播
- 检索策略：BM25 / Dense / **GraphRAG** / 父子分块 / HNSW 加速 pgvector(1024-dim)
- 20+ LLM provider，覆盖 DeepSeek、Qwen、混元、豆包等国产模型；技术栈 Go + Rust(anydoc) + Vue
- 来源：[GitHub Tencent/WeKnora](https://github.com/Tencent/WeKnora)

### 5. 🟡 小米开源表格基础模型 Xiaomi-TabLDM

- **70M 参数**，一次预训练 + 统一默认配置，跨数据集直接做分类与回归，**不重训、不调参**
- 预训练数据**全部由结构因果模型（SCM）合成**，非爬取
- 架构三步棋：双流特征分组 → 轻量级 Attention Residual → 稀疏 MoE（共享专家设计借鉴 DeepSeekMoE）
- 榜单：OpenML-CTR23 回归**第一**（平均排名 3.03，TabFM 3.06）、TALENT 二分类第一、BCCO 总体第二、TabArena 回归第二（Elo 1900，每 1K 样本 3.12 秒）
- 效率：训练时间比 TabFM 少 **82%**，预测时间少 **68%**
- 工业场景：材料性能预测精度 +130%、零件重量失误样本 -31%、生产组分平均误差 -54%、新工况仅补约 30 条样本误差再降 62%
- 来源：[GitHub xiaomi-research/xiaomi-tabldm](https://github.com/xiaomi-research/xiaomi-tabldm) · [HuggingFace occams/Xiaomi-TabLDM](https://huggingface.co/occams/Xiaomi-TabLDM) · 技术报告 arXiv:2609.03880 · [快科技](https://www.chinaz.com/2026/0905/1775388.shtml)
- ⚠️ 榜单与工业数据均为小米官方口径，**尚未见第三方独立复现**

### 6. 🟡 腾讯混元 Hy4 preview 开源，770B 参数 / 1M 上下文

- 总参数 **770B**、激活 **49B**、上下文 **1M**；权重已上 HuggingFace，同时接入腾讯云 TokenHub 与 OpenRouter
- OpenRouter 记录的上线日期为 **8-28**；定价约 **$0.834 / 百万输入 token** 起
- 腾讯侧口径：163 名内部专家盲测均分优于 GLM-3 与 Kimi K3
- 来源：[HeadsUpAI 汇总](https://headsupai.io/ai-news-and-updates) · [PromptZone 模型时间线](https://www.promptzone.com/ai-model-releases) · [腾讯公众号](https://mp.weixin.qq.com/s?__biz=MzI4ODI5OTkwMg==&mid=2247709091&idx=1&sn=2fc3d77d02aad4141b37ad07f9ed848e)
- ⚠️ 盲测部分为厂商自述，未见第三方评测

---

## 三、为什么值得记

1. **"可验证"正在取代"更聪明"成为竞争维度。** 费马大定理这条新闻的技术含量不在"AI 会做数学"——模型只是把一个已知的 1995 年证明翻译成了 Lean。真正的突破是：**60 亿 token 的概率生成，被一个确定性的 kernel 收敛成了可复用资产**。这给所有做 Agent 的人指了一条路：与其卷 prompt 让模型少犯错，不如在下游加一层机器可执行的判定器（schema 校验、单测、形式化规约、回放对比）。

2. **陶哲轩指出的是"过程价值"的流失，这对产品设计同样成立。** 他说迭代者不能提前知道最终 ansatz，否则会抑制对死胡同路线的探索。翻译到 AI 产品：如果你把 AI 的输出直接当最终答案交付给用户，**用户就失去了在探索过程中形成判断力的机会**——短期体验更好，长期能力空心化。做 AI Native 产品时，要不要保留"半成品/失败路径"给用户看，是一个真实的设计取舍。

3. **开源不再是情怀，而是验证基础设施。** 小米把权重、代码、技术报告一起放出来，混元把权重挂到 HuggingFace 和 OpenRouter——意味着任何人可以复现或者推翻他们的榜单。反过来，186 之所以不被承认，恰恰因为**唯一的验证方是声明方自己**。在 AI 输出越来越难自证的年代，"可被第三方复现"本身就是产品特性。

4. **WeKnora 的走向值得注意：RAG 框架在向"企业治理"靠拢。** 审计日志、RBAC、per-tenant 网络策略、OTel 链路追踪、Wiki 页面的修订历史与一键回滚——这些都不是检索质量问题，而是**责任归属问题**。企业愿意为 RAG 付费的门槛，从来不是召回率高几个点，而是出事时能不能查到是谁在哪一步做了什么。

---

## 四、可行动

- [ ] **给自己的 Agent 加一层"机器判定器"**：挑一个现有流程（比如报告生成、结构化抽取），在输出端加 schema 校验 + 断言 + 回放对比，统计"生成→校验→修正"的通过率，量化这层校验带来的收益
- [ ] **克隆 anthropics/fermats-last-theorem 看一眼 1300 万行证明长什么样**，重点看 Prove2Me 如何用 DAG 组织定理依赖——这套"把大任务拆成可独立验证的节点"的模式，可以直接迁移到多 Agent 协作的任务编排设计
- [ ] **用 Xiaomi-TabLDM 试一张自己的真实业务表**（`pip` 安装，scikit-learn 兼容接口），拿 XGBoost 做 baseline 对比；特别测试"新工况只补 30 条样本"这个宣称是否成立——这是最容易证伪也最有价值的一点
- [ ] **评估 WeKnora v0.8.0 作为知识库中台的可行性**：重点验证三个企业特性（per-workspace 审计日志、Langfuse tracing、Wiki 回滚），并检查它的 GraphRAG 与现有 chunking 策略能否共存
- [ ] **建立个人"信源分级"习惯**：今天的 186/188/212 三个数字没有任何一个是官方一手可查的。对自己输出的每一条 AI 事实，养成问一句"验证方是不是声明方本人"的习惯

---

## 五、术语卡

| 术语 | 解释 | 为什么今天重要 |
| :--- | :--- | :--- |
| **形式化证明（Formal Proof）** | 用证明助手（如 Lean）的语言把数学推理写成代码，由 kernel 逐条检查每一步是否符合规则，不依赖人类阅读理解 | Claude 的 1300 万行 Lean 就是这种产物——它不是"看起来对"，是"被机器逐条验过" |
| **Autoformalization（自动形式化）** | 把人类用自然语言写的数学证明，自动翻译成证明助手可检查的形式化代码 | 费马大定理项目没有产生新数学，产生的是把一个 1995 年的旧证明变成了可机器验证的形式 |
| **Lean / Mathlib** | Lean 是微软研究院起源的证明助手；Mathlib 是其社区维护的数学定理库。Claude 的证明规模是 Mathlib 的 5 倍以上 | 提供了"外部校验层"的现成基础设施，也是 comparator 能确认定理陈述一致的前提 |
| **Ansatz（拟设）** | 一个有根据的猜测性解的形式/结构，先假定它成立再反推验证 | 陶哲轩论点的核心：如果迭代者提前知道最终正确的 ansatz，就不会去探索那些"失败但富有启发性"的路线 |
| **ICL（In-Context Learning，表格场景）** | 不做梯度更新，把带标签样本作为上下文喂给预训练模型，一次前向传播直接预测新样本标签 | TabPFN / Xiaomi-TabLDM 这条路线的基石，也是"一次预训练、跨数据集免微调"能成立的原因 |
| **GraphRAG** | 在向量检索之外，先从文档抽取实体关系图谱，再基于图结构做检索与归纳 | WeKnora 已内置；适合"跨文档找关联"而非"单段匹配"的查询，是 RAG 从召回走向推理的关键组件 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
