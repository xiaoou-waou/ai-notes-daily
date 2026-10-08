# 2026-10-08｜一次调用被拆成六个角色，签字的却还没定

> 监督、判断、批量执行、压缩、准入、验收——今天发布的每一件事都在把「一次调用」切成多个可替换的环节，但没人说清每个环节由谁负责。

**标签**：`#职责分离` `#Agent工程` `#定价档位` `#技能供应链` `#合规`
**生成时间**：2026-10-08 12:07（北京时间）

---

## 一、今日观察

今天没有一项发布是"模型更强了"。把它们排在一起看，动作只有一个：**把原本由一次调用一口气干完的事，拆成若干个能单独替换、单独计费、单独审查的环节。**

| 环节 | 今天谁在做 | 怎么接入链路 | 能否单独换掉 / 单独计价 | 出问题算谁的 |
|---|---|---|---|---|
| 干活 | 主 agent（Opus 5.5 / Sonnet 5.5） | 默认路径 | 能换模型 | 调用方 |
| 复核 | **Auto-review**：第二个 agent 只审高风险动作 | 权限菜单里的 "Approve for me" | 免费、不占额度（此前消耗 **2%–10%** 额度） | 没写 |
| 判断 | **Decisions API**：只输出"选哪个模型/工具/动作" | 独立 API，公测 | 延迟约为 Responses 调用的 **1/10** | 调用方 |
| 批量执行 | **Claude Haiku 5.5**：官方定位是 Opus/Sonnet 的 **subagent** | 被主模型派活 | 价格按 prompt 长度分两档 + **effort 档位** | 编排者 |
| 输入压缩 | **Headroom**（开源，Apache-2.0） | `wrap` / proxy / MCP 三种接法 | 本地运行、**可逆**（原文留本地按需取回） | 本地 |
| 技能准入 | **SkillSpector**（NVIDIA 开源） | 安装技能**之前**扫一遍 | 71 种漏洞模式，0–100 风险分，可出 SARIF | 装机的人 |
| 验收 | **mini-ork**（开源） | 复现 bug + 生成不变量攻击补丁 | 返回 **PROVEN / REFUTED / UNVERIFIED** + JSON 证书 | 可举证 |

这张表的每一行单独看都只是个小功能；合起来是一次结构变化：**"一次调用"不再是原子操作了。**

而恰好在同一天，新加坡金管局（MAS）给出了这条链路上唯一一份"归属规则"——**金融机构对自己交付的服务里用的 AI 负责，包括第三方提供的 AI**。技术侧把责任切碎了，监管侧要求有一个名字把它收回去。这个时间差就是今天最值得记的东西。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. Claude Haiku 5.5：便宜是有档位的，档位挂在上下文长度上 🟢

10 月 7 日 Anthropic 发布 Haiku 5.5，官方原话是"the cheapest, fastest, and most capable small model we've ever released"，定位是"high-volume, cost-sensitive tasks"，并且明确写了一句 **"It pairs well with Opus 5.5 and Sonnet 5.5 as a subagent on coding work"**。

价格分两档（每百万 token）：

| | Haiku 5.5 ≤100K | Haiku 5.5 >100K | Haiku 4.5 | Sonnet 5.5 |
|---|---|---|---|---|
| 输入 | **$0.10** | **$0.50** | $1.00 | $2.00 |
| 输出 | **$0.50** | **$2.50** | $5.00 | $10.00 |
| 缓存读 | $0.01 | $0.05 | $0.10 | $0.10 |
| 缓存写 | $0.125 | $0.625 | $1.25 | $2.50 |

即：**≤100K 比 Haiku 4.5 便宜约 90%，>100K 只便宜约 50%，两档之间差 5 倍**。官方称平均运行成本降约 **75%**，并说明约 **90%** 的 Haiku 4.5 请求落在 ≤100K 那一档；两家独立媒体（SiliconANGLE、Unite.AI）都转述了同一条官方脚注：**这个 75% 已计入一个新 tokenizer，而新 tokenizer 完成同样工作会用掉略多的 token**。

另外三点是首次出现：Haiku 系列**第一次带可调 effort 档位**（成本 ↔ 智能的旋钮）；官方给出了自我限定——**"Sonnet 5.5 and Opus 5.5 remain better choices for complex agentic coding tasks"**，Haiku 5.5 适合"compaction, summarization, or subagent work"；速度那句的脚注也自打了折：**标准速度下最快，但 Fast Mode 下不如 Opus**。

同日 Sonnet 5.5 **缓存读价格砍半**（$0.20 → $0.10），官方称"reduces the cost of Sonnet 5.5 on most agentic tasks by around 20%"。

来源：[Anthropic 官方页](https://anthropic.com/claude-haiku-5-5) · [SiliconANGLE](https://siliconangle.com/2026/10/07/anthropic-releases-claude-haiku-5-5-small-model-and-halves-sonnet-5-5-cache-read-prices/) · [Unite.AI](https://www.unite.ai/anthropic-releases-claude-haiku-5-5-cutting-small-model-api-prices/)

### 2. Codex「28 天连更」第二天四连发：监督、判断、档位、纪要 🟢

OpenAI 的 Tibo 立了 28 天日更的旗（没更新就做一次用量重置）。第二天一口气四项：

- **Auto-review 免费**：对所有用 ChatGPT 账号登录的用户免费、不再消耗套餐额度；官方文档写明它"uses a separate reviewer to examine eligible actions that would otherwise pause for manual approval"，通过则继续，不通过则走更安全的路径或退回给人。此前开启时它会消耗 **2%–10%** 的套餐额度（视负载而定）。
- **Decisions API 公测**：面向所有开发者，用于"choose models, tools, or actions in near real time"，官方称决策速度比走 Responses API 调 GPT-6 Luna **快 10 倍**。
- **API 付费档位从 5 档简化为 3 档**：Build / Launch / Grow，门槛分别是累计充值 **$5 / $100 / $500**（最高档门槛从 $1,000 降到 $500）；对应月用量上限 $500 / $5,000 / $200,000。
- **Meetings 插件**：macOS 桌面端向 Pro / Business 开放 Beta，用麦克风与系统音频录制（不需要机器人入会），纪要落进 ChatGPT Space；官方称音频生成完纪要后即删除、无法回放，会话满 **4 小时**或长时间无音频会自动停止。企业版在小范围 alpha，Windows / iOS / Android 在计划中。

第一天还有一项：GPT-6 Astra 与 GPT-6.1 Sol 默认速度提升约 **50%**（30 → 50 tokens/秒）。

来源：[OpenAI 开发者社区 28 天跟踪帖](https://community.openai.com/t/28-days-of-shipping-at-openai/1403897) · [AI Industry Today（含 Auto-review 2%–10% 与档位细节）](https://aiindustrytoday.com/news/openai-ships-four-day-2-updates-then-resets-codex-and-work-usage-anyway)

### 3. GPT-6 与 Intelligent UI 推给全部 12 亿周活用户：官方博客与系统卡用了两个基线 🟢

10 月 8 日 OpenAI 宣布 GPT-6 进 ChatGPT（Plus/Pro/Business/Enterprise 用 **GPT-6 Sol**，Free/Go 次日 10 月 9 日用 **GPT-6 Luna**），同时上线 **Intelligent UI**：回答可以是图形、可点击按钮、表单、图表，乃至"能在对话里直接用的工具"（账单分摊、储蓄计算器、小游戏）。官方说明为此建了一套支持流式输出的原生组件库 + 编译器，界面随生成过程逐步呈现。

同一份发布里最该学的是**两个文档、两个基线**：

- 官方博客口径：**相对 GPT-5.6**，越狱抵抗更强、更遵守护栏。
- 系统卡口径：**相对 9 月的 GPT-6 版本**，多轮越狱鲁棒性的点估计**略有下降**（95% 置信区间大幅重叠）；但对 GPT-5.6 Sol，在所有测试的攻击预算下都更强。
- 系统卡还自陈回退：相对各自的 GPT-5.6 版本，GPT-6 Sol（10 月）在 standard self-harm 上**统计显著回退**，GPT-6 Luna（10 月）在 self-harm、gore、sexual content 上**统计显著回退**；官方称人工复核后判定被禁回复"generally low severity"。
- 关键数字：指令层级鲁棒性 **Sol 99.99% / Luna 99.79%**；间接提示注入鲁棒性 **Sol 97.13% / Luna 95.80%**；两份模型在**网络安全**与**生化**两个领域均被判为 **High capability**，AI 自我改进未达 High。

来源：[OpenAI 官方页](https://openai.com/index/gpt-6-for-everyone/) · [Deployment Safety Hub 系统卡](https://deploymentsafety.openai.com/gpt-6-october)（数字转引自 [cellcog.ai 整理](https://cellcog.ai/blog/gpt-6-intelligent-ui)，系统卡原文页较长，逐项数字建议回原文核对）

### 4. 新加坡 MAS《AI 风险管理指引》：把归属规则先写死了 🟢

10 月 7 日 MAS 发布《Guidelines on AI Risk Management》，适用于**所有金融机构、所有形式的 AI**。关键四点：

- **分阶段生效**：2027 年 10 月 7 日起适用第 3–4 节（监督、识别、清单、风险重要性评估），2028 年 10 月 7 日起适用第 5–6 节（生命周期控制、能力与容量）。咨询稿原本只给了 12 个月过渡期，最终改成两段。
- **第三方 AI 仍由金融机构担责**：机构须从供应商取得充分保证、评估其是否适合预期用途，并在保证有缺口时施加补偿性控制；风险无法压进风险偏好时，应考虑**限制、暂停或更换**该服务。
- **先有清单，后有控制**：要求识别 AI 使用场景、维护"适当颗粒度"的清单、评估每个用例的重要性。
- **agentic AI 留了一手**：MAS 表示将在 **2027 年**就"还需要哪些 agentic AI 指引"再开一次咨询——即本次发布的框架并不覆盖自治工作流。

风险重要性的三个维度（Impact / Complexity / **Reliance**，其中 Reliance 衡量授予 AI 的自治程度与人的介入程度）、以及"剩余风险须落在风险偏好之内才可部署"等段落级细节，目前只见到单一法律 commentary 的解读，🟡 待回原文核对。

来源：[The Asian Banker（MAS 新闻稿全文转载）](https://www.theasianbanker.com/press-releases/mas-sets-out-supervisory-expectations-on-responsible-ai-adoption-by-financial-institutions) · [新华网](http://www.chinaview.cn/20261007/63e1c96515a6479f8b265c711352ef9c/c.html) · [AI Policy Desk](https://www.aipolicydesk.com/blog/mas-ai-risk-management-guidelines-singapore-vendor-questionnaire-2026)

### 5. NVIDIA SkillSpector：技能供应链终于有了「安装前」的闸门 🟢

`NVIDIA/SkillSpector`（Python，Apache-2.0，19,657★，10-07 仍在更新，10-08 用 GitHub API 实测）。官方 README 的数据比任何二手报道都硬：

- 在分析的 **31,132 个技能**子集里，**26.1% 含漏洞**、**5.2% 呈现疑似恶意意图**。
- 检测 **71 种**漏洞模式、横跨 17 个类别：提示注入、数据外泄、权限提升、供应链、过度代理（excessive agency）、输出处理、系统提示泄露、记忆投毒、工具滥用、rogue agent、反拒答（anti-refusal）、触发器滥用、危险代码（AST）、污点追踪、YARA 签名、MCP 最小权限、MCP 工具投毒。
- 两阶段分析（静态 + 可选 LLM 语义评估）、0–100 风险分、可输出 **SARIF**、接 OSV.dev 查实时 CVE、支持 baseline/fingerprint 抑制（重扫只看新增问题）。
- 它是 NVIDIA Verified Skills 流水线的一环，通过者才进 NVIDIA 技能目录。

**口径提醒**：中文聚合站写的是"64 种漏洞模式"，官方 README 写 **71 种**——以仓库为准。这类聚合站的 star 数同样不可信（同一天另一处把 Headroom 写成 39k，GitHub API 实测 **74,604**）。

来源：[GitHub README（经 `gh api repos/NVIDIA/SkillSpector/readme` 取原文）](https://github.com/NVIDIA/SkillSpector)

### 6. Headroom：把压缩变成链路里的一个独立环节 🟢

`headroomlabs-ai/headroom`（Python，Apache-2.0，74,604★，10-08 仍在更新）。README 的定位原话：压缩 agent 读的一切——工具输出、日志、RAG 片段、文件、会话历史——**在它进入 LLM 之前**。

三种接法（库 / `headroom proxy` 零改码 / `headroom wrap claude|codex|...`），另有 MCP server（`headroom_compress` / `headroom_retrieve` / `headroom_stats`）。工程上三个点值得留意：**压缩在本地跑，内容不外发**；**可逆（CCR）**，原文缓存在本地按需取回；有 `headroom learn`，会挖失败会话并把修正写进 `CLAUDE.local.md`（默认，gitignored）。

README 给出的样例：55,957 token 的 agent prompt 压到实际发送 **24,340**，且第 67 项的 FATAL 行**逐字节保留**；另一个演示是 10,144 → 1,260 token。宣称"same answers"——**这是项目自述，未见第三方复现，🟡**。

来源：[GitHub README（经 `gh api repos/headroomlabs-ai/headroom/readme` 取原文）](https://github.com/headroomlabs-ai/headroom)

### 补充：验收这一环也有人做了 🟡

`SourceShift/mini-ork`（Apache-2.0，29★，10-07 更新）做一件事：证明 AI 写的修复真的修好了——在你自己的仓库上复现 bug，在 Docker 沙箱里用生成的不变量攻击补丁，返回 **PROVEN / REFUTED / UNVERIFIED** 并附 JSON 证书。star 数极低、无第三方验证，仅作链路完整性的一条线索，不作为能力证据。

---

## 三、为什么值得记

1. **监督第一次被明确定价，而定价方式决定它会不会被执行。** Auto-review 此前占用 **2%–10%** 的套餐额度——这意味着过去用户是在"多花额度"和"自己点批准"之间做选择，也就是说**护栏有一个价格，而且价格随任务变长而上涨**。改成免费，等于厂商承认：让监督跟用量挂钩，会诱导人在长任务里关掉监督。这条比降价本身重要得多。**以后凡遇到"我们提供了安全开关"，先问：这个开关按什么计费？**

2. **每拆出一个角色，就多一条责任真空，而今天的监管已经不打算接受"链条太长所以没人负责"。** Decisions API 只输出判断——判断错了算谁的？Haiku 作为 subagent 干了活——子 agent 造成的外部影响由谁批准？MAS 的回答很干脆：**清单上写谁就是谁，第三方 AI 也还是你的责任**，压不进风险偏好就限制、暂停或更换。**治理文件第一次跑在了技术栈前面：归属规则先定义好，技术再往上长。**

3. **"便宜"已经不是一个数，而是一组档位，比价必须换成自己的分布。** Haiku 5.5 在 ≤100K 便宜 90%、>100K 只便宜 50%，两档差 5 倍；官方的 75% 是把"约 90% 请求在低档"加权算出来的，且**新 tokenizer 会用掉略多 token**。再叠加 effort 档位与上下文档位，同一款模型现在有 **2×N 个价格点**。→ 规矩：**跨模型比价不能比 headline，要比你自己 prompt 长度分布的加权值，并把 tokenizer 变更单独列一项。**

4. **技能供应链的闸门位置终于对了：在安装之前。** 26.1% 的技能含漏洞、5.2% 疑似恶意（NVIDIA 官方数据，样本 31,132）——装一个 skill 等于给 agent 装一段可执行代码，而生态此前是"隐式信任 + 最小审查"。SkillSpector 的价值不在检出率（未知），在于**它把检查点放到了 install 之前，并且能出 SARIF 接 CI**。

---

## 四、可行动

- [ ] 给自己的 agent 链路画一张角色表：干活 / 复核 / 判断 / 压缩 / 验收各由谁承担，每格补两列——「能单独换掉吗」「出问题找谁」。空白格就是责任真空。
- [ ] 打开 Codex 的 Auto-review（权限菜单 → "Approve for me"），并在日志里**把主 agent 的 token 与复核 agent 的 token 分开记**——免费不等于不需要计量，计量才能看出监督覆盖了多大比例的动作。
- [ ] 把路由类判断从主调用里拆出来试 Decisions API：先挪"选哪个模型/走不走工具"这类高频低风险决策，量延迟与成本（官方称约 1/10 延迟）。
- [ ] 装任何 agent skill 之前先跑一遍 `uv tool install git+https://github.com/NVIDIA/skillspector.git` 再 `skillspector` 扫；把 SARIF 接进 CI，用 fingerprint baseline 抑制已知项，只看新增。
- [ ] 按自己的 prompt 长度分布重算 Haiku 5.5 的真实单价，别用 75% 这个 headline：≤100K 是 $0.10/$0.50，>100K 是 $0.50/$2.50，另计新 tokenizer 的额外 token；同时用 effort 档位在成本与质量之间找一个自己的点。
- [ ] 若给金融行业客户供货：按 MAS 的两个日期倒排（**2027-10-07** 第 3–4 节，**2028-10-07** 第 5–6 节），现在就准备两份材料——AI 用例清单，以及每个用例的重要性评估（影响 / 复杂度 / 依赖，其中"依赖"要写明授予 AI 的自治程度与人工介入程度）。

---

## 五、术语卡

| 术语 | 含义 | 今天为什么重要 |
|---|---|---|
| **Decisions API** | 只输出"选哪个模型/工具/动作"这类决策的独立接口，不产出完整回答 | 把决策从主调用里剥离出来单独加速（官方称约 1/10 延迟），代价是决策责任单独落在一处 |
| **subagent** | 由主模型派活、只承担窄范围子任务的模型实例 | Haiku 5.5 的官方定位就是 Opus/Sonnet 的 subagent；这意味着主模型的一次任务会横跨多个模型与多个价格档 |
| **effort 档位** | 同一模型上"成本 ↔ 智能"的可调旋钮 | Haiku 5.5 首次引入；与上下文档位相乘后，单款模型有多个价格点，选型要先固定这两个档再比 |
| **CCR（可逆压缩）** | 压缩后原文仍缓存在本地、可按需取回的机制 | Headroom 的核心；它把"省 token"和"丢信息"解耦，是压缩层能被放进生产链路的前提 |
| **风险重要性（materiality）** | 对每个 AI 用例按影响 / 复杂度 / 依赖评估其重要程度，据此配比例化控制 | MAS 要求先有清单与重要性评估，再谈控制；"依赖"这一维专门衡量 AI 的自治程度 |
| **过度代理（excessive agency）** | agent 被授予了超出任务所需的权限或行动自由度 | SkillSpector 的 17 类漏洞模式之一，也是把责任切碎后最容易出现的失败模式 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
