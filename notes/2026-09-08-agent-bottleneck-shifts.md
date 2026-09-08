# 2026-09-08｜当模型不再是瓶颈：检索层、配方与供应链接管了 Agent 的天花板

> 今天真正的变化不在模型智商：2B 模型拿到 Agent 能力并开源配方，检索层换成"整页视觉"，而攻击面已移到 Agent 读取的上下文。

**标签**：`#Agent` `#RAG` `#开源` `#工程实践` `#国产大模型`
**生成时间**：2026-09-08 22:59（北京时间）

---

## 一、今日观察

**主线：Agent 的能力上限，正从"模型够不够聪明"迁移到"检索够不够准、配方能不能复现、供应链干不干净"。**

今天几乎没有一条爆炸性的"模型变强了"的新闻，但把六件事放在一起看，位置关系变了：

| 层 | 今天的事件 | 谁被替代/被补位 |
|---|---|---|
| 模型层 | 面壁 MiniCPM5-2B 开源，2B 参数拿到 Agentic Index **20 分** | 端侧"只能聊天"的小模型 |
| 配方层 | 同批开源 **4 个数据集 + RL 训练栈**，UltraData L0–L4 分级治理 | 只给权重、不给复现路径的"半开源" |
| 检索层 | 腾讯 EVIE-8B/4.5B：不 OCR，**整页当图片检索**，Apache 2.0 | OCR → 切块 → 文本嵌入的传统 RAG 链路 |
| 嵌入层 | 微信 WeMM-Embedding：文/图/视频同一语义空间，微信内**日均 10 亿次调用** | CLIP/SigLIP 主导的单模态/双模态嵌入 |
| 供给层 | DeepSeek V4.1 Flash 内测：原生多模态，用 **Flash 定价**试探替换 V4 Pro | "强能力必须买 Pro"的定价分层 |
| 风险层 | GitSpawn：Agent 只是跑了 `git status`，就被仓库里的 `.git/config` 劫持 | 只在 prompt 层做注入防护的安全模型 |

一句话：**上半场比谁的模型强，下半场比谁的检索准、谁的配方能复现、谁的供应链没洞。** 这三件事今天同一天被摆到台面上。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 面壁 MiniCPM5-2B 开源：2B 参数，Agent 能力"断层式领先"　🟢
OpenBMB 官方页公布：**综合评测平均分 53.9**（超过参与对比的全部更大模型，对比组中最高 51.1）；Artificial Analysis 榜单综合能力**23 分**，居 4B 以下开源模型之首；**Agent 能力 20 分**，官方称是同级模型的约 10 倍。后训练 RL 阶段用 critic-based 算法，推理与通用能力平均 **+10.96 分**、Agent 能力平均 **+6.96 分**；OPD 阶段合并 **16 个 RL 专家模型**。同时开源 UltraData-Code、UltraData-SFT-Agent-2609、UltraData-RL-2609、UltraX 四个数据集。
来源：[OpenBMB 官方模型页](https://www.openbmb.cn/model/minicpm5-2b) ｜ [Hugging Face](https://huggingface.co/openbmb/MiniCPM5-2B)
> 注：部分英文日报写"AA Intelligence Index 得 15 分"，与官方页的 23 分不一致，以官方页为准。

### 2. 腾讯 EVIE-8B / 4.5B：把"整页当图片检索"做成 Apache 2.0　🟡
EVIE（Evidence-Vector-Informed Embedding）不把 PDF 转成文本，直接对页面图像排序。官方模型卡：EVIE-8B 在 **ViDoRe V3 上 66.75 nDCG@10**（48 个任务），EVIE-4.5B 为 **66.02**；4.5B 用 **Prefix-MRL**，单一 2048D 投影可在推理时截断到 64/128/256/512/1024 维，**128 维时分数从 66.02 掉到 65.27**（宽度砍 16 倍，只掉 0.75 分）；配合免训练的 HAC 聚类把每页约 750 个向量压到 32 个，索引降至 **3.81 GiB / 百万页**。骨干为 Qwen3.5，许可 Apache 2.0。
来源：[DataNorth 详细解读](https://datanorth.ai/news/tencent-releases-evie-8b-and-evie-4-5b) ｜ [Hugging Face: tencent/EVIE-8B](https://huggingface.co/tencent/EVIE-8B) ｜ [AGI Hunt 摘要](https://agihunt.info/en/p/1a07b51743f012a011b05935474)
> ⚠️ **这些数字全部是腾讯自报**，无第三方复现；且腾讯 8 月的 EVIE-Preview-4.5B 卡曾以 65.36 自称"ViDoRe V3 第一"，在其刷新后的表里已退到第三。评级为 🟡。

### 3. 微信 WeMM-Embedding 开源：MMEB-v2 第一，微信内日均 10 亿次调用　🟡
微信 AI 视觉团队开源通用多模态嵌入模型，含 **2B / 4B / 9B** 三个版本，以 Qwen3.5 多模态架构为骨干，支持文本、图像、视频、视觉文档及任意交错输入；在 **MMEB-v2 榜单综合排名第一**。微信员工称朋友圈搜索、视频号推荐、公众号推荐、微信电商均已接入，**日均调用量 10 亿次**。论文 arXiv:2608.24053，代码 [Tencent/WeMM-Embedding](https://github.com/Tencent/WeMM-Embedding)，权重在 Hugging Face。
来源：[IT之家](https://www.ithome.com/0/999/527.htm) ｜ [AIBase](https://www.aibase.com/news/30895)
> 注：官方宣布开源在 **9 月 4 日**，国内媒体 9 月 8 日集中转述——发布日期 ≠ 报道日期。"日均 10 亿次调用"为员工口径，尚无官方文档佐证，标 🟡。

### 4. DeepSeek V4.1 Flash 开启限时内测：原生多模态，用 Flash 价试探替换 Pro　🟡
9 月 8 日下午，DeepSeek 在官方交流群开启 V4.1 Flash 中间版本内测，模型 ID `deepseek-v4.1-flash-expires-on-0910`（**9 月 10 日到期**）。官方口径为"**新的模型结构 + 原生多模态支持**"，能力更强、速度更快、成本更低；`base_url` 不变、只改模型名即可迁移，计费与 V4 Flash 一致，但**单账号限 20 并发**（正式版 V4 Flash 为 2500）。随附问卷直接询问"**V4.1 Flash 能否全面替换线上的 V4 Pro**"。参照官方 API 价格，V4 Flash 峰值每百万 tokens 输入 **$0.44** / 输出 **$1.32**，V4 Pro 为 **$1.32 / $3.96**（正好 3 倍）。
来源：[腾讯科技](https://news.qq.com/rain/a/20260908A0APR100) ｜ [上海证券报（腾讯新闻转载）](https://news.qq.com/rain/a/20260908A0D5CC00)
> 注：截至发稿 DeepSeek 官网、API 文档与 Change Log **均未列出** V4.1 Flash；官方也未公布技术报告、参数规模与 benchmark，"新架构新在哪"仍是悬念。标 🟡。

### 5. Mistral 完成 30 亿欧元 D 轮："开放权重 + 主权可控"被定价到 210 亿欧元　🟢
9 月 8 日 Mistral AI 宣布完成 **30 亿欧元 D 轮**，投后估值超 **210 亿欧元**（约 240 亿美元），称是欧洲科技公司迄今最大单笔股权融资。**三星电子领投**，EQT 管理的 Scaleup Europe Fund 与老股东 PSG Equity 联合领投——Scaleup Europe Fund 由欧盟委员会出资锚定，这是它的**第一笔投资**。新进投资方含 Advent、贝莱德旗下基金、卢森堡大公国。Mistral 称业务覆盖 20 个国家、**125+ 企业客户**（Airbus、ASML、汇丰）；CFO 称预计年底年化营收达 **10 亿美元**（公司预测，非已实现）。上一轮为 2025 年 9 月 ASML 领投的 17 亿欧元 C 轮，估值 117 亿欧元——**一年翻倍**。
来源：[EU-Startups](https://www.eu-startups.com/2026/09/french-ai-company-mistral-raises-e3-billion-series-d-led-by-samsung-at-over-e21-billion-valuation/) ｜ [The Next Web](https://thenextweb.com/news/mistral-3bn-series-d-samsung-21bn-valuation) ｜ [财联社](https://new.qq.com/rain/a/20260908A0AZUW00)

### 6. GitSpawn：Agent 只跑了 `git status`，就被仓库配置文件劫持　🟢
Manifold Security 于 **9 月 1 日**披露 GitSpawn，共 8 项发现、涉及 7 款 CLI 编码 Agent。原理：Agent 启动时后台跑 `git status` / `git diff` 收集上下文，触发 Git 索引刷新；而 `core.fsmonitor` 允许仓库在自己的 `.git/config` 里指定一个辅助程序，Git 会在刷新时**自动执行它**。该调用发生在 workspace-trust 提示之前，**绕过所有审批流与沙箱**，以当前用户权限执行。**已修**：Claude Code（core.fsmonitor 路径，2.1.196）、Cursor、OpenAI Codex、Goose 1.44.0（CVE-2026-72718，CVSS 7.0）。**9 月 1 日复测仍会执行**：Claude Code 第二条路径（2.1.252，`claude ultrareview`）、Hermes Agent 0.21.0（CVE-2026-71963）、**Qwen Code 0.22.3**、**Grok Build 1.0.13**。投递方式限为 zip / 共享盘 / U 盘等"带 `.git` 的文件交付"，**`git clone` 不受影响**。
来源：[IntelFusions 复盘](https://www.intelfusions.com/news/gitspawn-git-config-ai-coding-agents) ｜ [Writeble 汇总](https://www.writeble.com/2026/09/07/gitspawn-flaw-lets-malicious-git-configs-hijack-claude-codex-cursor-and-other-coding-agents) ｜ [CySecurity News](https://www.cysecurity.news/2026/09/1-folder-was-all-it-took-security.html)

---

## 三、为什么值得记

1. **"开源"的定义正在从权重升级为配方。** MiniCPM5 把数据集、RL 栈、OPD 合并方法一起交出来，意味着小模型的能力不再只能"下载来用"，而是"照着复现"。对做微调的人来说，这比多几个 benchmark 分数有用得多——**可复现的配方是唯一能迁移的东西**。

2. **RAG 的瓶颈早就不是切块，而是"切块那一刻就丢了版面"。** EVIE 的路子是干脆不 OCR，把整页当图片检索，用迟交互保留版面结构。真正值得抄的不是 66.75 这个分（厂商自报、无人复现），而是 **Prefix-MRL 那个"推理时按需截断维度"的设计**：一套索引、多种成本档位，128 维只掉 0.75 分。这是把"存储/精度"从训练期决策变成运行期旋钮——**是所有嵌入系统都该有的能力，跟你用不用 EVIE 无关**。

3. **Agent 的安全边界画错了地方。** 全行业在 prompt 注入上堆了两年防护，GitSpawn 证明致命输入是**Agent 为了理解环境而自动读取的东西**：一个配置文件、一次 `git status`。共同点是——它们都发生在"用户还没说话"之前。任何"先读环境、再问用户"的 Agent 架构，都天然带着这个洞。

4. **Flash 试探 Pro，是定价分层松动的信号，但别急着下注。** DeepSeek 直接在问卷里问"能不能替换 Pro"，说明厂商自己也在试探边界。但这次内测**没有技术报告、没有 benchmark、20 并发、4 天就下线**——它是一次 A/B 测试，不是一次发布。真正的判断要等正式版的价格和能力同时落地。

5. **Mistral 这笔钱买的不是模型，是"控制权"这个 SKU。** 三星 + 欧盟主权基金 + ASML 连续两轮由硬件制造商领投，说明欧洲在买一条"不被断供"的链路。**开放权重只是手段，可审计、可自托管、算力可预测才是商品**——这个定位对国内做私有化交付的团队是现成的商业模板。

---

## 四、可行动

- [ ] **今天就查本机 Git 配置**：`git config --get-all core.fsmonitor`；对 zip/共享盘/U 盘来的仓库，先用 `git -c core.fsmonitor=false status` 打开。注意 `git config --global core.fsmonitor false` **无效**——仓库级配置覆盖全局。
- [ ] **给现有 RAG 加一条 A/B 基线**：挑 50–100 页表格/图表密集的扫描 PDF，对比"OCR + BM25/文本嵌入"与"整页视觉检索（EVIE-4.5B，Apache 2.0 可商用）"的 top-10 召回，先量化差距再谈替换。
- [ ] **把 Prefix-MRL 思路迁到自有嵌入索引**：评估把现有向量截断到 128/256 维后 nDCG@10 掉多少点、索引省多少 GiB——如果能接受 1 个点换 16 倍压缩，存储账就完全不一样。
- [ ] **跑一遍 MiniCPM5-2B 的工具调用**（BFCL v4 / τ²-Bench 类场景），对照你现在端侧/低成本场景用的 7–9B 模型，看 2B 能不能顶上；顺便读它的 UltraData L0–L4 数据治理方案，这对自己做 SFT 数据清洗直接可抄。
- [ ] **等 DeepSeek V4.1 Flash 正式版**（关注 9 月 10 日内测端点下线后的官方 Change Log），重点看两件事：正式定价，以及是否有技术报告解释"新架构"。

---

## 五、术语卡

| 术语 | 一句话解释 | 为什么今天重要 |
|---|---|---|
| **Late Interaction（迟交互 / MaxSim）** | 不把一页压成一个向量，而是存成几百个 token 级向量，检索时对每个查询 token 取最大相似度再求和 | EVIE 保留版面、表格、图表结构靠的就是它，代价是索引体积暴涨 |
| **MRL / Prefix-MRL** | Matryoshka Representation Learning：让一个高维嵌入的前 N 维本身就是可用的低维嵌入，可运行时截断 | 让"存储 vs 精度"从训练期决策变成运行期旋钮，EVIE-4.5B 的核心卖点 |
| **nDCG@10** | 归一化折损累计增益，只看前 10 条结果的排序质量，越接近 1 越好 | 文档检索榜单（ViDoRe、JinaVDR）的通用货币，注意不同榜单不可直接横向比 |
| **ViDoRe** | 视觉文档检索基准，V1/V2/V3 难度递增，V3 含 48 个任务、覆盖 8 个公开领域 | 判断"视觉检索"模型真实水平的当前主榜，也是厂商自报分数最集中的地方 |
| **core.fsmonitor** | Git 的性能选项，允许仓库指定一个外部程序在索引刷新时自动执行以加速大仓库 | GitSpawn 的入口：它把"仓库配置文件"变成了"可执行指令" |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
