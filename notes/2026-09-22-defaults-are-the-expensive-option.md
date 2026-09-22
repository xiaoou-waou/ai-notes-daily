# 2026-09-22｜「默认开启」是今天最贵的一个选项

> 数据、模型、身份、判断——四件看似无关的事，今天都在改同一个东西：默认值归谁。

**标签**：`#默认值` `#Agent安全` `#开源模型` `#决策模型` `#国产大模型`
**生成时间**：2026-09-22 12:06（北京时间）

---

## 一、今日观察

今天真正发生变化的不是又发布了什么模型，而是**四件事同时把「默认值」从厂商那一侧搬走了**。

先看一组对照。Artificial Analysis 综合智能指数上，**小米 MiMo-V2.6-Pro 拿到 46 分，xAI Grok 4.7 也是 46 分**。同一个数字，一个被称作「开放权重第一」，一个在总体榜上排第 16。而价格相差四到七倍：小米 Pro 每百万 token 输入 **$0.435**、输出 **$0.87**；Grok 4.7 是 **$2 / $6**。分数相同的时候，剩下能比的就只有架构和默认值了——Pro 是稀疏 MoE，**1.02T 总参数里每次只激活 42B**，Grok 4.7 是 2.1T 稠密。这不是「谁更聪明」的问题，是「你默认要为多少没被叫醒的参数付钱」的问题。

但今天更值钱的是另外三次默认值搬家，而且方向一致：**把「相信我们」换成「你自己验」**。

| 层 | 旧的默认值 | 今天被改成 | 谁在搬 |
| :--- | :--- | :--- | :--- |
| **数据** | 客户端默认上传整仓代码 + 完整 Git 历史，界面无开关、用户无法解密 | 客户端/后端/CLI 全面开源 + 两家第三方审计，交给社区验 | 智谱（被动） |
| **模型** | Copilot 新模型**默认自动启用**，管理员不关就进 IDE | 开关交给企业策略，渐进放量 | GitHub |
| **身份** | 购物代理默认「像人一样」浏览，不自报家门 | 必须公开身份、允许站点 opt-out | Amazon（强制） |
| **判断** | 分类/路由默认调大模型，然后丢掉它生成的整段文字 | 本地可训的 0.8–9B 决策模型，一次前向直出概率 | 社区（Kev） |

四次搬家，三件是被事故或外部压力推着走的，只有最后一件是主动的。**而那件主动的，恰恰是今天唯一你能直接拿去用的东西。**

还有一个反例值得一起记：智谱 9 月 20 日晚在 MaaS 上线的「数据内容不留存」机制，**需要用户主动申请开通**，且 Batch API / File API 不在覆盖范围内，涉及法律法规或违规核查时平台仍可留存 **30 天以上**。也就是说，整改到今天这一步，「不留存」依然不是默认值——默认值还是留存，只是多了一个申请入口。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 智谱 ZCode 完成整改，客户端/后端/Agent CLI 全面开源，两家第三方机构出审计结论 🟡

事件起点是 9 月 18 日技术博主 ferstar 的个人博客：他清理磁盘时发现，ZCode 桌面客户端在登录状态下会自动把整个工作区打包加密上传到阿里云 OSS。据其逆向分析，包内不仅有当前项目源代码，还包括**完整 Git 版本历史、LFS 大文件缓存、reflog 记录及部分全局开发配置**；该行为**默认开启**，设置界面找不到关闭选项；加密用的 RSA 公钥由服务端动态下发，**私钥仅保存在云端，用户无法解密自己生成本地包**。澎湃新闻另报道，有开发者发现即便在设置里手动关闭开关，后台进程仍在上传。

智谱的响应共四步：9-18 声明致歉（归因于「代码库索引」功能默认开启，称数据仅用于生成 Repo Wiki 随后销毁）；9-19 推修复版本；9-20 晚 MaaS 上线「数据内容不留存」（需申请，Batch/File API 不覆盖，合规情形可留存 30 天以上）；**9-21 宣布完成整改，将客户端、后端及 Agent CLI 代码全面开源至 GitHub**。

审计结论（均由智谱转述，未见两家机构原始报告）：中国信通院技术评测确认 **zcode-prod 阿里云 OSS 存储桶状态为云端零数据**；绿盟科技确认该桶内**全部数据对象及存储桶本身已删除**，**ZCode v3.14.0** 已移除 Repo Wiki 入口及生成链路，**未发现可触发本地仓库快照或文件外发的功能路径**。智谱称后续将每月定期公布代码安全审计报告。9-19 太原承明科技已发函要求书面说明数据删除、私钥保管及是否跨境传输，并保留索赔与诉讼权利。9-21 智谱（2513.HK）股价收涨近 2%。

> 🟡 理由：两家机构的审计结论目前只见于智谱对媒体的转述与官方通稿，未核到第三方原件；ferstar 的逆向分析为单一技术博主来源。多源交叉来源：[澎湃新闻](https://www.thepaper.cn/newsDetail_forward_34118714)、[界面新闻](https://www.toutiao.com/article/7687819709601038887)、[证券时报](https://www.toutiao.com/article/7687907233204404745/)、[凤凰科技](https://tech.ifeng.com/c/8waoZ17PMDL)。

### 2. Kev：把「判断」从大模型里拆出来做成 0.8–9B 的可训小模型 🟢

Jared Palmer 发布 **Kev** 决策模型家族（HN 当日第一，367 upvotes / 164 评论），**Apache-2.0**，基于 Qwen3.5-0.8B / 4B / 9B。我直接读了仓库 README，几个关键设计：

- **不是全参微调**：每个 checkpoint 是一个 **rank-16 LoRA adapter + 一个 pointer head**，基座权重冻结。pointer head 拿选项位 `</opt>` 的隐状态去和提问位 `<decide>` 的隐状态打分，softmax 成概率。因为 `<decide>` 在序列最后，它能 attend 到完整选项列表。
- **问题隔离的实现随基座而变**：Qwen3 纯注意力基座用 attention mask；**Qwen3.5 混了 recurrent Gated DeltaNet 层，这些层完全不理会 attention mask**，所以改成每个问题单独一行、服务端缓存共享 state 前缀复用。作者称两种做法在纯注意力模型上概率差 **4e-6** 以内。
- **三种题型可混在一次请求里**：`noul`（是/否）、`choice`（1–255 个选项）、`score`（2–255 级有序评分）。**推理时不生成任何解释性文本**。
- **训练成本极低**：2 epoch、LoRA rank 16、cross-entropy，lr 1e-4（0.8B）/ 5e-5（4B/9B）；数据 `decision-v7` 共 **12,576 条** = 10,000 条来自十个公开数据集 + 896 条生成策略例 + 1,680 条来自 60 个生成规则结构。

README 的评测表（dev / test，Brier 越低越好）：

| 模型 | 新源准确率 | Brier（新源） |
| :--- | :--- | :--- |
| Kev-0.8B | 0.652 / 0.684 | 0.499 / 0.460 |
| Kev-4B | 0.797 / 0.837 | 0.299 / 0.255 |
| Kev-9B | **0.822 / 0.852** | **0.286 / 0.237** |
| Jev Hosted（TypeSafe） | 0.857 / — | 0.211 / — |

**最该看的两列不是准确率**：一是「在 5% 错误预算下可自动化的决策占比」，**Kev 0.45–0.57，Jev 0.70**；二是外部工单集 scienthoon 900 条上，**Kev-9B 路由 0.952 / 语气 0.911，反超 Jev 的 0.897 / 0.914**。作者自陈该对比**非受控**（不知道 Jev 训练数据），且置信度值是模型导出的估计而非实测准确率。

> 🟢 来源：[github.com/jaredpalmer/kev](https://github.com/jaredpalmer/kev)（README 与 model cards 为作者一手材料）。约 **$95** Modal H100 + $0.03 Jev API 的开销、以及「Palmer 在 Cognition 任工程副总裁、用 Devin 协助构建」来自 [theclarity.today](https://theclarity.today/story/jared-palmer-ports-kev-to-qwen3-5-for-roughly-95-in-h100-time-fb25d22c) 🟡。

### 3. 小米 MiMo-V2.6 开源：AA 指数 46 分，MIT 许可，RL 账单 347 万美元 🟡

9 月 22 日凌晨发布并开源，**Pro / Flash 双版本 + Pro-UltraSpeed 加速档**，权重上 Hugging Face 与 ModelScope，**许可是 MIT**（商用无附加门槛）。

- **架构**（模型卡）：Pro 稀疏 MoE，**1.02T 总参 / 42B 激活**，70 层，60 层滑窗注意力交错 10 层全局注意力，**384 个路由专家每 token 激活 8 个**，5 层 MTP 投机解码每次前向预测 7 个 token，另有 681M 参数 ViT、308M AudioTokenizer；**1M 上下文**，原生全模态（文本/图像/视频/音频）。Flash 约 310B 总参 / **15B 激活**（各源在 309B 与 310B 间略有出入）。
- **榜单**：Artificial Analysis 综合智能指数 v4.3.2 **46 分**，与 Grok 4.7 同分，超过 GLM-5.3 的 45 分、Kimi K3 的 44 分；上代 V2.5-Pro 是 26 分。榜首 Claude Fable 5.1 与 GPT-6 Astra 均为 53 分。
- **训练**：<6 天，Pro 与 Flash 各跑 30 步 RL，约 **75 万条轨迹**，每步 1568 个 prompt × 16 次采样、35–37 亿 token；成本 **Pro 约 262 万美元、Flash 约 85 万美元**，合计约 347 万美元；reward-hacking 轨迹 **<2%**。方法上用了 GRS（离线从对比轨迹合成 rubric）+ GAR（在线重排通过轨迹的优势）+ MOPD2 多前缀多教师蒸馏。一并开源 **7000+ RL 任务环境**与基于 verl / mini-swe-agent 的训练框架。
- **价格**：沿用 V2.5，Pro $0.435 / $0.87（每百万输入/输出），缓存命中 $0.0036；Flash $0.14 / $0.28。UltraSpeed 官方称最高 20 倍速、定价为 Pro 的 10 倍；OpenRouter 页面描述为约 10 倍——**两边说法无第三方实测对齐**。

⚠️ 需要警惕的口径差：官方推文称 Pro「在大多数 agent 基准上与 Claude Opus 5、GPT-5.6 Sol 表现相当」，但有第三方按官方自己随权重放出的评测表逐项数过，**双方共同覆盖的 14 项评测里 Pro 有 10 项落后 Claude Opus 5**，差距最大的是 ExploitBench、Terminal-Bench 4.0 与 ProgramBench。官方表上 DeepSWE v1.1 Pro 71.9，仍落后 DeepSeek V4.1 Flash 74.2、Claude Opus 5 74.0、GPT-6 Astra 74.0。

> 🟡 理由：mimo.xiaomi.com 官方页与 HF 模型卡本次未直连核实，以上来自 [Unite.AI](https://www.unite.ai/xiaomis-new-flagship-model-leads-open-weight-rankings-with-a-score-of-46)、[superpowerdaily（引 VentureBeat）](https://superpowerdaily.com/posts/xiaomi-releases-mimo-v2-6-models-as-its-pro-version-tops-an-open-weight-ranking)、[IT之家/网易](https://www.163.com/dy/article/L7E17RL20534A4SC.html) 多源交叉；厂商自评的基准分数（DeepSWE、CyberGym、OSWorld 等）尚未见社区复现。

### 4. xAI Grok 4.7 发布，GitHub Copilot 全 SKU 铺开且「默认自动启用」 🟡

Grok 4.7 于 9 月 22 日（周一）发布，**2.1T 参数**（4.6 为 1.5T），**$2 / $6** 每百万输入/输出 token，**500K 上下文**，可配置推理档位，即刻上线 Grok App、Cursor、Grok Build 与 xAI API。官方主打「同档模型两倍速度、一半价格」。

第三方数据给出另一面：Artificial Analysis 综合指数 **46**（总体第 16），但**输出速度 39.3 tok/s，在 202 个模型中排第 151**，被标注为「notably slow」。厂商自评方面，DeepSWE v1.1 **71.0%**、EEBench **64.0%**（同档领先），但 **Terminal-Bench 38.0%**，明显落后 Claude Fable 5.1 的 57.9%。

同日 GitHub 宣布把 Grok 4.7 加入 Copilot（Pro 至 Enterprise 全 SKU），覆盖 VS Code、Visual Studio、JetBrains、Xcode、Eclipse、Copilot CLI 与 cloud agent，按 provider list price 计入用量计费。关键一句在 changelog：**「defaults auto-enable new models unless explicitly disabled」** —— 管理员需通过 model policy 显式关闭，否则新模型默认进 IDE。

> 🟡 理由：`x.ai/news/grok-4-7` 本次 WebFetch 失败（fetch failed），以上数字来自 [64bit.co.uk daily brief](https://64bit.co.uk/daily-brief-2026-09-22)、[thecontext.dev](https://thecontext.dev/en/briefing/2026-09-22)、[AGI Hunt](https://agihunt.info/en/daily/2026-09-22?f=dr) 与 [GitHub Changelog](https://github.blog/changelog/) 交叉，官方页未直接核实。

### 5. Amazon 封禁 Meta Muse：代理「不自报身份」被定性为违规 🟢

9 月 20 日起，用户通过 Meta 的 Muse 访问 Amazon 时收到弹窗：**「Continued access by an unauthorized AI agent violates Amazon's Conditions of Use, to which our customers have agreed.」**

Amazon 于 9 月 21 日给出的理由有三条，逐条都指向「默认值」：① Meta **未事先告知** Amazon 其代理会访问站点；② Muse 在浏览过程中**不表明自身是 AI 代理**；③ 会**抓取并存储用户凭证与账户数据**，带来安全与隐私风险。官方声明原话：「第三方应用代表用户从其他商家购买时，应当公开运作，并尊重服务提供方是否参与的决定……我们已要求 Meta 将 Amazon 从该体验中移除。」

Meta 于 9 月 8 日上线 Muse，上线一周登顶美国 App Store 免费榜，其发布说明称「Muse 无法看到用户的密码或支付方式，用户共享的凭证进入安全存储」。Amazon 使用条款并未点名 AI 购物助手，但站点访问许可排除了「data mining, robots, or similar data gathering and extraction tools」。此前 Amazon 已就 Perplexity 的 Comet 浏览器提起诉讼（一审胜诉，8 月上诉法院推翻，认为难以证明违反联邦黑客法），并限制过 ChatGPT 与 Gemini 的购物代理；Amazon 自有同类产品 Buy for Me。4 月 Meta 刚与亚马逊签署数十亿美元云芯片采购协议，本次冲突未波及现有商业合作。

> 🟢 来源：[PCMag](https://au.pcmag.com/ai/120005/amazon-blocks-metas-new-ai-agent-from-shopping-its-store)、[PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2026/amazon-bars-meta-muse-ai-agent-from-ecommerce-marketplace/)、[Engadget](https://www.engadget.com/2263659/amazon-bars-metas-muse-ai-agent-from-ecommerce-marketplace/)（均引 Amazon 官方声明原文）；[亿邦动力](https://m.ebrun.com/708892.html) 提供中文交叉。

### 6. Anthropic：Claude 已「主导」26% 的内部 AI 研发，30K agent 实时过审 🟡

Anthropic 于 **9 月 17 日**披露一组新指标（9-18 起媒体扩散，至 9-22 仍在中文简报中流转）：按 Epoch AI 的 **AL0–AL5** 自动化量表，**26% 的内部 AI 研发任务达到 AL4（Claude 主导）**，即由高层提示驱动完成大部分端到端工作、人类只做监督；**今年 2 月时这一比例还不到 1%**。超过 **90%** 的研发已达到「AI 协作」及以上，**尚无任务达到 AL5（全自动）**。约 15,000 个内部研发任务被映射到 378 个类别。

规模与护栏同时披露：**8 月主内部平台常驻约 30,000 个 agent**，每项操作执行前实时过审；当月**逾 10 亿次决策中约 1/47,000（0.002%）被拦截**；离线监控每周标记约 100,000 条 transcripts、约 50 条升级人工复核。7 月采样周中约 **6%** 的 AI 研发算力用于安全工作，若只算 AI 驱动的那部分研发则升至约 **12%**。

一个具体案例：夜间数据管道故障时，工程师没有自己调试，而是把报错交给 Claude —— 它查日志、定位根因、写修复代码、测试、处理新出现的问题、重跑管道、比对结果并写出说明。

⚠️ 需要保留的质疑：AI 研究者 Nathan Lambert 公开指出，Anthropic **没有定义什么算「AI 研发工作」的范围**（"doesn't define what falls in scope of AI R&D work"）。26% 是内部自评，无第三方核。

> 🟡 理由：Anthropic 官方博客本次未直接核实，数字来自 [MarketBrief](https://marketbrief.now/ai/claude-leads-26percent-of-anthropic-ai-randd-tasks-in-jump-from-1percent-c540417a)、[vfuturemedia](https://vfuturemedia.com/ai/anthropic-says-claude-leads-26-of-its-ai-rd-work)、[红星新闻](https://www.toutiao.com/article/7686750283614994990/) 多源交叉，各方数字一致但同源。

---

## 三、为什么值得记

1. **「默认开启」正在从产品特性变成责任归属问题。** ZCode 事件的根因不是「偷数据」，而是产品团队把「索引数据」当成了普通功能特性，没有按数据出域的规格走安全评审。同样的逻辑今天在 Copilot（新模型默认进 IDE）、Muse（代理默认隐身）上再演一遍。**判断一个 AI 功能危不危险，先看它的默认值，再看它的开关在哪一层**——界面上找不到开关的，基本都要出事。

2. **审计的价值不在于结论，在于它把「相信我们」换成了「你可以自己验」。** 智谱这次最有说服力的动作不是道歉，是把客户端/后端/CLI 全部开源。中信建投那句点评很准：开源的意义是**把此前无法验证的安全承诺变成可验证**。但要注意力度边界——审计结论目前仍是**智谱转述**的，「不留存」仍需**主动申请**、Batch/File API 不覆盖、合规可留 30 天以上。**开源解决的是「能不能验」，不是「已经验完」。**

3. **判断层被单独拆出来做成小模型，是今天唯一能立刻用上的东西。** Kev 的价值不在 0.822 这个准确率，而在于它把「用大模型做分类然后丢掉它生成的整段文字」这个荒谬的默认路径换掉了：**rank-16 LoRA + pointer head，12,576 条样本、2 epoch，一次前向直出校准概率**。但同时它暴露了决策模型的真实约束：**5% 错误预算下可自动化决策占比 Kev 只有 0.45–0.57，Jev 0.70**——也就是说，同样的准确率，**超过四成的决策仍然不能无人值守**。这是「能不能上线」的真正指标，比准确率有用得多。

4. **同一个 46 分，两种命运，说明榜单能告诉你的比想象中少。** MiMo-V2.6-Pro 和 Grok 4.7 都拿 46，一个被叫「开放权重第一」，一个排总榜第 16；价格差 4–7 倍；而 Grok 4.7 官方说「两倍速度」，第三方实测输出速度 39.3 tok/s 排在 202 个模型的第 151。**当分数打平时，决定选型的是激活参数、输出速度和许可，不是排名。** 小米这次还有个细节：官方推文说「与 Opus 5 相当」，可它自己随权重放出的表里，14 项共同评测有 10 项落后——**厂商的「持平」通常是有分母的「持平」。**

---

## 四、可行动

- [ ] **审计你正在用的 Coding Agent 的默认值**：重点查三件事——有没有「代码库索引 / 上下文上传」类功能、它是否在设置界面有开关、关掉后后台进程是否仍在传。ZCode 的教训是**界面上找不到开关 ≠ 没在传**。可用 `lsof -i` / Little Snitch 观察客户端的出站连接做粗验。
- [ ] **关掉 IDE 里的「新模型自动启用」**：GitHub Copilot 的 Grok 4.7 是 `defaults auto-enable new models unless explicitly disabled`。进组织级 model policy 显式白名单化，别让新模型在你不知道的情况下进入生产代码路径。
- [ ] **给自家 Agent 加上自报身份**：如果你在写任何会访问第三方站点的代理，按 Amazon 的三条标准自查——是否事先告知、是否在 User-Agent / 交互中表明 AI 身份、是否给了站点 opt-out 的通道。这三条正在被写成事实标准。
- [ ] **把「高频率的分类/路由」从大模型里拆出来跑一遍 Kev**：`pip install` 后按 README 的 `kev.train --init_from` 从你自己的标注 JSONL 起训（rank-16、2 epoch、12,576 条量级的数据就够）。**评估时不要只看准确率，要看「5% 错误预算下可自动化决策占比」这个数**——Kev 自报 0.45–0.57，低于 Jev 的 0.70，这才是能否无人值守的分界线。
- [ ] **用 Kev 前先做两个必测项**：① **选项顺序敏感性**（README 明写 "Changing option order can change an answer"，同一组选项打乱顺序看结果是否翻转）；② **本地服务无认证**（README 原话 "binds to 127.0.0.1 and has no authentication"），且 server 一次只处理一个请求，别直接挂在多租户后面。
- [ ] **重算你的模型账单：按激活参数而不是总参数估。** 同样的 46 分，稀疏 MoE（1.02T/42B 激活，$0.435/$0.87）和 2.1T 稠密（$2/$6）差 4–7 倍。选型表里加一列「每任务成本」，比智能指数更能预测账单。

---

## 五、术语卡

| 术语 | 解释 | 今天的上下文 |
| :--- | :--- | :--- |
| **稀疏 MoE（Mixture of Experts）** | 模型由大量「专家」子网络组成，每个 token 只路由激活其中少数几个。推理算力按**被激活的参数**算，不按总参数算。 | MiMo-V2.6-Pro：1.02T 总参，每 token 激活 42B；384 个路由专家取 8 个。这是它同分却便宜 4–7 倍的直接原因。 |
| **Pointer Head** | 接在冻结基座上的小型读出头：拿每个选项位的隐状态与提问位隐状态做打分，再 softmax 成概率。不生成文本。 | Kev 的每个 checkpoint = rank-16 LoRA adapter + pointer head，一次前向直出校准概率。 |
| **Brier Score** | 概率预测准确度的评分，取值范围 0–1（对多分类做归一化），**越低越好**。它同时惩罚「错了」和「很自信地错了」。 | Kev-9B 新源 Brier 0.286（dev）/ 0.237（test），Jev Hosted 0.211。比准确率更能反映概率能不能真拿来设阈值。 |
| **AL0–AL5 自动化量表** | Epoch AI 定义的 AI 参与度量表：AL0 无 AI 参与 → AL4「AI 主导」（人类只监督）→ AL5 全自动。 | Anthropic 用于给内部研发任务分级：26% 到 AL4，**无一达到 AL5**；>90% 已在「AI 协作」及以上。 |
| **Reward Hacking** | 强化学习中模型钻奖励函数空子、拿到高分却没完成真实目标的行为。 | 小米报 MiMo-V2.6 训练中 reward-hacking 轨迹 **<2%**，并用 GRS/GAR 双层奖励信号（离线评轨迹质量 + 在线把优势往高质量解法上移）来压制。 |
| **Gated DeltaNet** | 一类线性/循环注意力层，用门控状态递推替代全注意力，**不理会 attention mask**。 | Kev 移植到 Qwen3.5 时踩到：原来的 block attention mask 隔离法失效，改成「每个问题独立成行 + 服务端缓存共享 state 前缀」。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
