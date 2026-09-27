# 2026-09-27｜换接口，不换模型：今天所有进展都长在适配层

> 今天能挑出来的进展，没有一条是"模型更强了"——五件事各自改了一段接口，把成本砍掉一个数量级。

**标签**：`#接口设计` `#Agent工程` `#开源工具` `#Agent治理` `#具身智能`
**生成时间**：2026-09-27 13:40（北京时间）

---

## 一、今日观察

今天扫到的料里，最值钱的几条有一个共同点：**被改动的都不是模型，也不是被操作的对象，而是中间那层接口。** 五个互不认识的团队，在同一周做了同一个动作：

| 被适配的对象 | 原来怎么做 | 今天换的接口 | 换来的收益 |
|---|---|---|---|
| **真实机器人** | 训 VLA，每个 embodiment 重训一遍 | 11 个离散语义动作单元 + 解释器 | 前沿 VLM **零样本直控**；小模型单卡 **<2 小时** |
| **桌面应用** | 截图 → 视觉模型猜像素坐标 | 读 OS 无障碍树 | Slack 快照 **30,743 → 383 tokens** |
| **长期记忆** | 切块 → 嵌入 → 向量库 → 相似度检索 | LLM 定时读改写 SQLite | 一整套嵌入管线换成一次定时调用 + 单文件库 |
| **企业存量 agent** | 各平台只监控自己建的 | 原生连接器 + OpenTelemetry 跨 8 平台盘点 | 第一次能回答"我们到底有几个 agent" |
| **没有 API 的遗留系统** | 造 API（造不动） | 录一遍人的操作，之后回放 + 全量日志 | 集成项目退化成宏录制 |

把它们按"**接口粒度**"再排一次，形状更清楚——三组数字讲的是同一件事，而这个旋钮**不花钱**：

| 谁 | 拧了哪个旋钮 | 拧之前 | 拧之后 | 训练成本 |
|---|---|---|---|---|
| Show-Harness | 解释器步长 | 2 cm | 1 cm | **零**（不重训） |
| agent-desktop | 快照层级 | 全量 snapshot | skeleton overview | **零**（不换模型） |
| Always On Memory | 整合时机 | 写入时嵌入 | 每 30 分钟全库整合 | **零**（不换模型） |

Show-Harness 那一组最硬：步长从 2 cm 改到 1 cm，**零样本 60% → 82%、微调 40% → 65%**；而同样演示下的 π₀.₅ 只有 **18%**，补了专门的精细训练也才 **62%**。换句话说：**拧一个解释器参数的收益，超过了给 VLA 加一轮针对性训练。**

这条主线也不是没有反证。接口选错的时候，模型能力补不回来——见下面第三条和事实 1 的符号消融。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. Show-Harness：让 VLM "玩"机器人，接口比模型重要 🟢

NUS Showlab 的具身 harness，把机器人控制压缩成一套离散语义动作单元：`MV_FWD/BACK/LEFT/RIGHT/UP/DOWN`、`ROTATE_CW/CCW`、`GRASP`、`RELEASE`、`DONE`（双臂再加 `STILL`），由 embodiment-specific interpreter **确定性**接地成电机指令，VLM 只负责在这些单位上推理。

- **两种模式一个接口**：零样本用 **Gemini-3.1 Pro**（medium thinking）；微调用 **Qwen3.5-2B + rank-64 LoRA**（仅约 **3%** 参数，冻结视觉编码器与 projector），**单张 H200 不到 2 小时**，24GB 级卡可跑。
- **最硬的一组数字**：解释器步长 2 cm → 1 cm，**不重训** —— ZS **60% → 82%**、FT **40% → 65%**；π₀.₅ 同样演示 **18%**，额外精细训练后 **62%**。
- **消融**（真实 Franka，5 个 Plate 任务）：全套 harness **96%** / 平均 30 步；去掉 Subtask Planning → **60%**；去掉 Failure Recovery → **72%**；全程强制 action chunking → **74%**；Visual Prompt 让 handle-aware grasping **40% → 85%**；Situated Planning 让藏物搜索 **35% → 85%**。
- **推理密集型任务**（藏杯找方块 + 把散落字母排成 "SHOW"）：ZS+SP **85%**，FT 单独 **10%**，π₀.₅ 单独 **0%**。
- **符号可读性消融**（2×2）：(A) 语义名 + 书面约定最优；(C) 任意符号 + 约定几乎打平；**(D) 只给任意符号不给说明 → 仅 1/20 成功（5%），且推断出的映射正确率仅 23.3%**。
- **数据**：GUMI 采集 164 条真机 + 230 条仿真 = **394 条 / 约 21.3K 步**；27 类文件。
- **自陈局限**（论文 Sec 6）：只评测了单臂/双臂**平行夹爪**；未扩展到人形机器人或灵巧手；感知侧**缺乏触觉与力反馈**，无法支持接触丰富的精细操作。
- 来源：[arXiv 2609.10522](https://arxiv.org/abs/2609.10522) · [GitHub](https://github.com/showlab/Show-Harness) · [权重](https://huggingface.co/showlab/Show-Harness-VLMs) · [数据](https://huggingface.co/datasets/showlab/Show-Harness-Data)
- ⚠️ 时点说明：arXiv v1 提交于 **2026-09-09**，**9-27** 由新浪科技、网易/机器之心等中文媒体大规模转载；本条按转载日入册，论文日期以 arXiv 为准。

### 2. agent-desktop：不猜像素，读无障碍树 🟢

Rust 写的桌面 computer-use 工具，**Apache-2.0，1,679 stars**，最近一次 push 为 2026-09-26。核心主张：不看截图，直接查 OS 的无障碍 API 拿真实 UI 结构。

- **58 个命令名 / 54 个可操作**；其中 4 个 held-input 名保留给 stateful daemon，在无状态 CLI 里 **fail closed**。
- **token 对比**（README 自带示意图）：Slack 常规 accessibility snapshot **30,743 tokens** vs skeleton overview **383 tokens**（约 -98.8%）。README 正文对密集应用给的是 **78–96%** 削减 —— 示例比宣传区间更狠，按保守口径引用更稳妥。
- **稳定引用**形如 `@s8f3k2p9:e1`，内嵌快照 ID；失效时返回 `STALE_REF` / `AMBIGUOUS_TARGET` 并重取重试，不靠坐标。
- **自陈局限**（README/提交）：**Windows 与 Linux 适配器尚未构建，当前仅 macOS**；`key-down`/`key-up` 返回 `ACTION_NOT_SUPPORTED`；默认 auto-wait 上限 5000 ms。
- 提交历史里还留着两个已修的坑，值得当 checklist：macOS 跨 uid 身份拒绝曾让**整个 inventory 捕获失败并让 snapshot 超时**；AX 写入曾"报告成功但应用未真正改变"，后改为**执行后重新读取验证**。
- 来源：[github.com/lahfir/agent-desktop](https://github.com/lahfir/agent-desktop)

### 3. Always On Memory Agent：把向量库从记忆栈里删掉 🟢

**Shubham Saboo**（Google 高级 AI PM）开源，**MIT**，已并入 `GoogleCloudPlatform/generative-ai` 的 `gemini/agents/always-on-memory-agent/`（该仓库 9-27 01:09 UTC 仍有 push）。

- README 原话定位：**"No vector database. No embeddings. Just an LLM that reads, thinks, and writes structured memory."**
- 三个专职子 agent：**IngestAgent**（抽取 Summary / Entities / Topics / Importance）→ **ConsolidateAgent**（**默认每 30 分钟**，`--consolidate-every MIN` 可调，负责找连接、压缩、生成跨切面洞察）→ **QueryAgent**（综合回答并**引用 memory ID**）。
- 支持 **27 种**文件类型（文本 8 / 图像 7 / 音频 6 / 视频 5 / PDF），丢进 `./inbox` 自动拾取，5–10 秒内入库。
- 栈：Google ADK + **Gemini 3.1 Flash-Lite** + SQLite + aiohttp + Streamlit；HTTP API `:8888`，7 个端点（含 `/delete`、`/clear`）。
- README 自陈的对照表值得抄：Vector DB + RAG「被动，嵌入一次、以后检索」；对话摘要「丢细节、无法交叉引用」；知识图「构建维护昂贵」。
- 🟡 一处待核：有转述称 QueryAgent「reads up to 50 recent memories」，**官方 README 未出现此数字**，不采信为既定事实。
- ⚠️ 口径冲突：官方 README 写 **MIT**；有西语源写成 Apache 2.0，以 README 为准。
- 来源：[官方 README（GoogleCloudPlatform/generative-ai）](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/agents/always-on-memory-agent)

### 4. Dataiku Agent Management：第一次有人盘点企业到底有几个 agent 🟢

官方新闻稿：**2026-09-24** 于 Dataiku Succeed（纽约）发布，**2026 年 10 月 GA**。

- **平台覆盖**：AWS Bedrock、Databricks Agents、Google Vertex、Microsoft Copilot Studio、Azure Foundry、Salesforce Agentforce、Snowflake Cortex、Dataiku 自身，自建环境走 **OpenTelemetry**。
- 不只数数：自动识别每个 agent **依赖的工具与模型**；按自主性 / 数据敏感度 / 业务影响分层；最高风险 agent 保有**认证状态、具名风险、定时重跑测试**的常备记录。
- 引用 IBM "AI in Motion"：**不足五分之一**的组织维护着完整且最新的 AI 系统清单。
- **自家调查最锋利**：《Global AI Confessions Report: CIO Edition, 2026》——685 位 CIO，Harris Poll 于 7 月 9–29 日调研，8 国、年营收 5 亿美元以上企业。**90% 称有完整追踪**，但 **81% 承认对"正规渠道之外建的 agent"缺乏完整监督**；84% 说员工建 agent 的速度快过 IT 的治理能力；76% 认为若 2027 年底前拿不出可衡量收益，自己的职位有风险；72% 预计今年指标未达成预算会被砍或冻结。
- CEO Florian Douetteau 原话：**"Ask a bank how many servers it runs, and you get an answer to the decimal. Ask how many AI agents it's running, and you get a shrug or a guess."**
- 定价：按实例年费 + 监控按 agent 计量。
- 来源：[Dataiku 官方新闻稿](https://www.dataiku.com/company/news/dataiku-agent-management-general-availability)

### 5. Strada：给"从来没有 API"的系统造一层 🟡

保险垂直 AI 公司 Strada 本周上线：agent 在承运商门户 / 遗留 TPA、MGA 后端里**录一遍人的操作**，之后对实时数据回放，每一步全程日志留存，用日志代替 API 本该提供的审计保证。前提是这些门户**从来没发过 API，且造不造不由 Strada 决定**。

- 信源等级 🟡：**仅 smillee.com 单一二手转述，未找到 Strada 官方公告页**，待官方源核实，不作为既定事实陈述。
- 来源：[smillee.com](https://smillee.com/blog/always-on-memory-dataiku-agent-inventory-strada-browser-portals-2026)

### 6. 补充：Nscale 递交 S-1 —— 适配层再往下，是"电力到 token" 🟡

- 9-25 宣布完成 **33.6 亿美元**可转债融资，Third Point 领投，英伟达、Apollo、Citadel、Hudson Bay、阿布扎比投资委员会等参与；首批交割 **23.6 亿美元** + 英伟达承诺追加 **10 亿美元**（预计 2026-11 到账）；IPO 后自动转普通股，英伟达部分转为无投票权股份。
- 已向 SEC 递交 S-1，拟纽交所上市，目标估值最高 **350 亿美元**、募资最高 30 亿美元。
- 招股书：2026 上半年营收 **1.406 亿美元**（同比 **+1252%**）、净亏损 **10.201 亿美元**（同比 **+176%**）；截至 8-31 在用 GPU 约 **2.5 万块**，在用+签约 **46.1 万块**；5 座数据中心投产、12 座签约在建；掌控电力 **超 10 GW**；累计合同订单 **1030 亿美元**。
- 英伟达三重角色：供应商 + 客户 + 投资方（合计约 31 亿美元）。
- 🟡 全部为媒体转述招股书（证券时报 / 界面新闻），**未直连 SEC EDGAR 原始文件**。
- 来源：[证券时报（经今日头条）](https://www.toutiao.com/article/7689815409301783086) · [界面新闻（经网易）](https://dy.163.com/article/L7N0H9JV0534A4SC.html)

### 7. 补充：美团 LongCat-2.5-Preview 🟡

9-25 上线，MoE，总参约 **1.6 万亿**、激活约 **480 亿**，**原生 100 万 token** 上下文；新增图片理解，官方称深度适配 Claude Code / Hermes / OpenClaw / OpenCode / Kilo Code。🟡 IT之家转述官方更新日志，**未直连 LongCat 官方页**。来源：[凤凰网科技/IT之家](https://tech.ifeng.com/c/8wjaOU4jTOX)

---

## 三、为什么值得记

1. **此刻适配层的边际收益高于模型层，而且三组独立证据互相印证。** Show-Harness 不换模型只调解释器步长拿到 **+22 个点**；agent-desktop 不换模型只换观测通道砍掉约 **98%** token；Always On Memory 不换模型只换存储与时机，删掉整个向量栈。共同点是**收益不来自能力增长，来自摩擦消除**——这也是为什么这几条全部"不动 benchmark"。

2. **"接口粒度"是免费旋钮，但发布方往往只把它藏在参数里。** Show-Harness 的步长、agent-desktop 的 skeleton 层级、memory agent 的 `--consolidate-every`——三个都是作者明确暴露成可调参数的东西，也恰好是三份材料里收益最陡的地方。可迁移的做法：拿到任何 harness，先找它把哪些东西做成了可调参数，那通常就是作者知道最敏感、也最没写进标题的地方。

3. **反过来：接口选错，加模型补不回来。** Show-Harness 消融 (D)「只给任意符号不给语义说明」→ 成功率 **1/20（5%）**，推断映射正确率 **23.3%**。VLM 还是那个 VLM，光是符号不可读就崩了。这和 9-22 记的"选项顺序会改变答案"是同一类病：**模型能力无法补偿接口的可读性缺失**。选型时该先审动作空间/工具名是否自解释，再去比模型分数。

4. **盘点的缺口是今天最贵的一个洞。** 90% 的 CIO 自信有完整追踪、81% 承认看不见非正规渠道——**这两句话出自同一份 685 人调查**。Dataiku 把"agent 清单"做成独立产品类别（而不是某个平台的一个功能），本身就说明市场认为这个洞不会由建 agent 的人自己补上。它和 9-26 记的"受影响的人从不持有账本"是同一件事的另一面：**这次连"有几个 agent"这笔账都没人持。**

5. **适配不是免费的，它只是把成本换了个位置。** Always On Memory 用"定时整合"换掉"写时嵌入"，代价是记忆变成**最终一致**（30 分钟窗口内的事实未必被合并去重）；agent-desktop 用无障碍树换掉截图，代价是 **Win/Linux 适配器还没做**、且 macOS 之外连验证路径都没有；Show-Harness 用语义动作换掉连续控制，代价是**触觉与力反馈整个缺席**。凡是"我们删掉了一层"的宣传，先问被删的那层原来负责什么。

---

## 四、可行动

- [ ] **给记忆栈做一次 A/B**：把现有 RAG 检索换成"LLM 直接读结构化 SQLite + 定时整合"，用同一组 20 个跨会话问题对比命中率与每问成本。Always On Memory Agent 是 MIT，架构可直接抄（`GoogleCloudPlatform/generative-ai` 的 `gemini/agents/always-on-memory-agent/`）。重点测它最脆的地方：30 分钟窗口内刚写入的事实能不能被查到。
- [ ] **审计你手上的 harness**：把"哪些参数被暴露成可调"列一张表（步长 / 层级 / 间隔 / 阈值 / 重试次数），逐个做单点消融。Show-Harness 的教训是收益高度集中在 2–3 个参数上，而它们默认不会写进标题。
- [ ] **桌面自动化先测无障碍树再测截图**：mac 上 `npm install -g agent-desktop`，对同一个 Slack / VS Code 窗口分别跑 `snapshot --skeleton --app X -i --compact` 与全量快照，对比真实 token 消耗与任务成功率。注意 Windows / Linux 适配器尚未构建，别贸然上生产。
- [ ] **现在就盘 agent 清单，别等 10 月 GA**：按"是否接触客户数据 / 生产库 / 资金流"给每个 agent 打风险档，同时给自建 agent 接上 OpenTelemetry。Dataiku 与 WSO2 都用它做自定义环境接入，它正在成为 agent 可观测性的事实标准——就像十年前 Prometheus 之于基础设施指标。
- [ ] **测一遍你的动作空间可不可读**：如果工具名 / 动作 token 是缩写或没有语义说明，照 Show-Harness 消融 (D) 的做法——只给符号、不给说明，让模型自己试探映射，看正确率是否接近随机（该实验为 **23.3%**）。

---

## 五、术语卡

| 术语 | 解释 |
|---|---|
| **无障碍树（Accessibility tree）** | 操作系统为每个应用维护的结构化 UI 描述，屏幕阅读器用的就是它。相比截图，它给出带稳定引用的按钮/菜单/文本框，而不是会随字体、主题、位移漂移的像素坐标。 |
| **语义动作单元（Semantic action unit）** | Show-Harness 的机器人动作抽象：`MV_*` / `ROTATE_*` / `GRASP` / `RELEASE` / `DONE` 等离散单位，由 embodiment-specific interpreter 确定性接地成具体电机指令；VLM 只在单位层面推理，不碰连续控制量。 |
| **记忆整合（Consolidation）** | 仿睡眠的后台过程：定期重读未整合的记忆、找连接、压缩、生成跨切面洞察。与"写入时就嵌入、检索时才用"的 RAG 相反——智能发生在周期性的全库推理，而不是逐条写入时。 |
| **Sim-to-real** | 只在仿真演示上训练、直接部署到真机。Show-Harness 的微调模式仅用仿真演示即成功，而可训练的 VLA baseline 在同一条件下失败。 |
| **OpenTelemetry** | 厂商中立的遥测标准（trace / metric / log）。在 agent 治理里正充当"自建 agent 怎么被看见"的通用接口，地位类似十年前 Prometheus 之于基础设施指标。 |
| **VLA（Vision-Language-Action）** | 直接从图像 + 指令回归连续控制量的机器人模型（如 π₀.₅、GR00T），通常需要针对具体 embodiment 做预训练与反复适配。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
