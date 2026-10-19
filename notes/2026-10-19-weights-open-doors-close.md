# 2026-10-19｜权重越开越大，能动手的地方越收越紧

> 一周之内四家把几百 B 的权重塞进各种许可证里往外发，同一周 Yelp 到 Schwab 一排网站把 agent 关在门外。

**标签**：`#开源权重` `#Agent` `#许可证` `#长上下文` `#端侧`
**生成时间**：2026-10-19 10:20（北京时间）

---

## 一、今日观察

这一周（10 月 14–18 日）的 AI 新闻如果只看标题，是"开源大模型大爆发"。但如果按**你在哪一环被放开了、在哪一环被收回去**重新排一遍，会看到一条非常整齐的分界线：

| 环节 | 这几天发生了什么 | 方向 |
|---|---|---|
| **权重** | DeepSeek V4.1-Flash-1017（MIT）、Meta Muse Spark Open（Muse Model License）、阶跃 Step 5 Preview（StepFun Model License 1.0） | 放开 |
| **硬件门槛** | NVIDIA 把 120B 的 Super VL 压成 **24GB** 的 Bolt；面壁把 35B 的 MoE 跑进手机 **3GB** 内存 | 放开 |
| **上下文 / 单价** | DeepSeek 同价把 Terminal-Bench 4.0 从 31.2 拉到 42.3；StepFun 把上下文压缩直接训进策略 | 放开 |
| **动作（登录 / 支付 / 提交）** | Yelp、Delta、JPMorgan、Charles Schwab、Amazon、Cars.com、Amtrak 依次关门 | **收紧** |
| **反爬系统** | 为拦诈骗和脚本而建的风控，对 agent 一视同仁地开火——没人专门针对你 | **收紧（且非故意）** |
| **长上下文可靠性** | 分块 KV Cache 压缩带来"相位敏感"：同一条信息换个位置，准确率最多差 **40.2 个百分点** | 放开带来的新坑 |

**上半张表全是好消息，下半张表全是坏消息，而 agent 的价值恰恰全在下半张表。**

这是今天最值得记的一点：**"能不能跑"这一周被彻底解禁了，"能不能动"一个都没解禁。** 你可以把 816B 的模型搬进自家书房（Meta 的说法是两台 M5 Ultra Mac Studio），但搬回家之后它依然订不了一张 Delta 的机票、查不了一次 Schwab 的余额——因为这些门从来不在模型手里，在网站自己手里。

于是自托管的价值要重新定价：它换来的**不是能力，是把"不能动"的损失圈定在只读范围内**。Schwab 给出的方案恰好是这个形状——**只读 MCP server**：余额可以看，研究可以做，钱一分不能动。

按"你被放开了哪一段"把这一周排开：

| 能力层级 | 谁放开的 | 你现在拿得到什么 |
|---|---|---|
| 权重可下载 | DeepSeek / Meta / StepFun | 是的，HF 和 ModelScope 上直接下 |
| 能在本地跑 | NVIDIA（24GB）、面壁（手机 3GB）、Meta（两台 Mac Studio） | 是的，llama.cpp / Ollama / MLX / vLLM 全线支持 |
| 能读到你的数据 | 你自己 | 是的，这是本地最大的收益 |
| **能替你去做事** | **没人** | **不是的，这是一张一张白名单谈出来的** |

前三行这周全变了，第四行没变。而一个 agent 被买来就是为了第四行。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. The Verge：网站正在对 AI agent 关门，而且是成片的 🟢

**10 月 17 日 The Verge 的专题报道**把过去几周用户遇到的拦截汇总成了一张名单：Meta 的 Muse、xAI 的 Grok、OpenAI 的 Dots、Instinct 的 agent 都在撞墙。

- **Yelp** 告诉 TechCrunch，只放行**为它的数据授权计划付费**的 agent；
- **Delta 航空**禁止 agent 代用户订票；
- **JPMorgan Chase** 与 **Charles Schwab** 已确认因安全原因把 agent 挡在账户外；
- **Amazon** 称 Muse 的"持续访问"违反其站点政策，Grok、Dots、Instinct 也有无法使用的报告，马斯克的回应是"也许我该开一家 Amazon 的竞品"；
- 用户反映**此前能用、现在不行**的站点还包括 **Cars.com** 和 **Amtrak**，意味着还有公司在悄悄关门。

另一面是有人主动开门：Meta 改为和 **Walmart、Gap、Sephora、Best Buy** 合作，**Shopify** 把自己的店铺网络开放给 agent。Meta 的原话是"拒绝一个私人 agent，就是拒绝它背后的那个客户"。

最关键的一句来自 AI 安全评估机构 EquiStamp CEO **Chris Canal**：

> "There are all kinds of things that are set up not even to block agents, but to block in general bots or programs that are trying to scam or hack. These AI agents trigger those same safeguards."

**这条比任何一条封禁都重要：拦你的那套系统不是为拦你而建的。** 它是为拦诈骗和撞库而建的，而一个以机器速度填表单的 agent 和它长得一模一样。这意味着"被拦"不会随着模型变强而消失。

来源：[The Verge, 2026-10-17](https://www.theverge.com/ai-artificial-intelligence/1013195/ai-agents-blocked-web)

### 2. Schwab 的做法：拦的是"动"，放行的是"看" 🟢

**10 月 16 日**，Charles Schwab CEO **Rick Wurster** 在 Bloomberg 电视访谈中确认公司在主动拦截未经授权的 agent（点名 Meta 的 Muse），并给了一个可直接执行的框架：

> "We don't want someone just giving their password to Muse, and letting Muse come in and take action on that client's behalf. We can't control it, the client can't control it, something could go wrong and who's liable? So we're not allowing it."

具体做法三条：

1. **信息访问与交易权限严格分开**——对外接的大模型，Schwab 部署的是 **MCP server，只读**：能看余额、能做研究，**明确禁止动钱**；
2. 自有助手 **Charley** 只做行政与信息类任务，**不具备下单能力**；
3. Wurster 说他每周收到一份报告，显示 Schwab 每周拦截主要 agent 的尝试在 **"tens and twenties"（几十次）**量级。

JPMorgan CEO **Jamie Dimon** 本周同样确认挡住外部 agent 访问客户账户；CFO **Jeremy Barnum** 把"共享凭证 + 抓屏"直接定性为不安全。

🟡 需说明：Dimon 表态的原始出处为 Bloomberg / 二次转述，The Verge 链接的是自己的前一条报道（JPMorgan Chase is keeping AI agents out）；"tens and twenties"为 Wurster 口述量级，非精确统计。

来源：[Bloomberg 访谈转述 / The Verge](https://www.theverge.com/ai-artificial-intelligence/1013303/charles-schwab-is-blocking-ai-agents-too)　[Forkast 对只读 MCP 方案的详细拆解](https://forkast.news/schwab-and-jpmorgan-block-unauthorized-ai-agents-from-moving-money-as-private-ordering-reaches-financial-core)　[Digital Trends](https://www.digitaltrends.com/computing/us-banks-want-to-block-ai-agents-from-moving-money-well-at-least-thats-one-good-move/)

### 3. DeepSeek V4.1-Flash-1017：MIT 权重，自称"帕累托改进" 🟢 发布 / 🟡 全部数字为厂商自测

**10 月 17 日**发布，是 9 月 10 日 V4.1-Flash 的小版本更新。

- **权重**：Hugging Face / ModelScope，**MIT 许可**，与上代一致；架构与 **763B** 参数量不变，换的是权重不是形状；上下文 **1M token**，最高输出 384K。
- **调用方式不变**：`deepseek-flash` 直接指向新版本，旧名 `deepseek-v4-flash`、`deepseek-v4-flash-vision-exp` 也路由到它，**价格不变**（错峰 **$0.15 / $0.60** 每百万输入/输出，命中缓存输入 $0.003；高峰翻倍）。
- **DeepSeek 自报的基准变化**（全部为官方模型卡 / changelog 数字，第三方尚未测）：

| 基准 | V4.1-Flash（9 月） | V4.1-Flash-1017 |
|---|---|---|
| Terminal-Bench 4.0（Claude Code harness） | 31.2 | **42.3** |
| ProgramBench | 20.3 | **29.1** |
| DeepSWE v1.1 | 74.2 | **77.0** |
| NL2Repo-Bench | 65.4 | **68.2** |
| Automation-Bench v1.0.6 | 54.8 | **60.5** |
| HLE（无工具） | 36.8 | **42.6** |
| Agents' Last Exam | 31.8 | **35.4** |

- DeepSeek 自己的表里，**Claude Opus 5 在 Terminal-Bench 4.0（51.8）和 HLE（56.3）上仍然领先**。
- 官方把这次的能力变化叫做**"许愿式编程"**——用极短提示和很少参考资料从零搭出可运行项目，归因于**带自我反馈的强化学习**。
- 同步开放了自家搜索引擎的 **Search / Fetch API**。🟡 定价 $0.75/千次成功请求的数字来自二手转述，未在官方 pricing 页核实。

⚠️ **两个必须自己核的点**：其一，上述全部是**厂商自测**，截至 10 月 18 日 Artificial Analysis 等第三方榜单尚未测这个 checkpoint；其二，官方明确说模型是针对 **DeepSeek Harness（需 0.2.1-rc.1+）**以及腾讯 CodeBuddy / WorkBuddy 调过的，换 harness 跑出来的分数未必是这个。

来源：[Pandaily（含官方公告转述）](https://pandaily.com/deepseek-v4-1-flash-1017-official-release-mit-weights-terminal-bench-wish-style-programming)　[ArtificialWatch（直读 DeepSeek changelog / HF 仓库）](https://artificialwatch.com/wire/deepseek-v4-1-flash-1017-update)　[The Quantum Dispatch](https://thequantumdispatch.com/articles/deepseek-v4-1-flash-1017-open-weights-search-api)　[腾讯新闻（中文，附蒸馏质疑）](https://view.inews.qq.com/a/20261018A0B16400)

### 4. NVIDIA 把 120B 压进 24GB：本地 agent 的门槛变成了"一张卡" 🟢

**10 月 15 日** NVIDIA 发布 Nemotron 3.5 家族三款开放模型（官方博客可直连）：

| 模型 | 形态 | 内存 | 状态 |
|---|---|---|---|
| **Nemotron 3.5 Super VL** | 120B 总参 / 12B 激活，MoE，多模态（文本/图/图表/PDF/视频），1M 上下文 | BF16 全精度 | 已发布 |
| **Nemotron 3.5 Bolt 74B-A9B** | 74B 总参 / 9B 激活，**由 Super VL 经原生 2-bit 量化压缩而来**，256K 上下文 | **24GB** | 已发布 |
| **Nemotron 3.5 Bolt E4B** | 同系列边缘版 | 4GB | 10 月 23 日 |

- 许可证为 **OpenMDW-1.1**，权重、数据集、训练配方一并开放；支持 llama.cpp / Ollama / LM Studio / Unsloth / vLLM，面向 RTX 与 DGX Spark。
- 训练规模：约 **26 万亿 token** 预训练，后训练约 **380 万**样本，再跨数十个环境做 RL（官方数字）。
- 🟡 **值得留意的一处"官方自己打自己"**：NVIDIA 的 Super VL 模型卡里，Super VL 在 **SWE-bench Verified 71.10 / Terminal-Bench 2.1 66.70 / BrowseComp 78**，被 **DeepSeek V4 Flash（75.4 / 76.8 / 84.2）**和 **GLM-5.3-Flash（79.10 / 82.70 / 86.6）**压过；它的强项是 **AA-Omniscience 幻觉率 30.0%**（DeepSeek V4 Flash 为 95.9%，越低越好）。NVIDIA 博客主推的"同级别最快 / 5×"是吞吐口径，不是精度口径。
- 对照另一端：**面壁智能 MiniCPM-V 4.7**（10 月 14 日，🟡 10 月 18 日才被广泛报道），**35B-A3B**，是 MiniCPM-V 系列第一个 MoE；官方称在 iPhone 17 Pro Max 上**约 3GB 内存、13+ token/s**解码，靠的是 **LES（lookahead expert scheduling，前瞻专家调度）**——处理当前层时预测下一层需要的专家并提前从存储加载，官方称多数情况下 **80%+** 所需专家已提前就位且**不改变输出**。**Apache-2.0**。🟡 全部速度与对比数字为厂商自测，第三方未验证。

来源：[NVIDIA 官方博客](https://blogs.nvidia.com/blog/nemotron-3.5-super-vl/)　[NVIDIA 模型卡对比（第三方整理）](https://cellcog.ai/blog/nemotron-3-5-super-vl-bolt)　[面壁 MiniCPM-V 4.7（Pandaily）](https://pandaily.com/modelbest-minicpm-v-4-7-open-source-35b-a3b-moe-3gb-iphone-on-device)　[面壁 MiniCPM-V 4.7（Momenta Media，含苹果 30 亿参数对照）](https://www.momenta.media/article/modelbest-squeezes-a-35-billion-parameter-ai-model-onto-a-phone)

### 5. "开源"已经不是一个选型依据：同一周出现了四张不同的证 🟢

这一周放出来的权重，四家四种许可，而且**阈值条款是直接对着你的规模写的**：

| 模型 | 许可证 | 关键限制 |
|---|---|---|
| DeepSeek V4.1-Flash-1017 | **MIT** | 基本无限制 |
| MiniCPM-V 4.7 | **Apache-2.0** | 可商用，含商业用途 |
| Meta Muse Spark Open（816B / 42B 激活 / 1M 上下文，10-15） | **Muse Model License** | 官方原话 "with **limited commercial terms**"，具体条款未在博客展开 |
| 阶跃 Step 5 Preview（600B / 27B 激活 / 1M 上下文，10-15） | **StepFun Model License 1.0** | 见下 |

**StepFun Model License 1.0 的三条**（据直读 HF 仓库 LICENSE.txt 的整理，🟡 为二手转述但注明直读原件）：

1. 月活 **>1 亿** 或月收入 **>2000 万美元**的商用产品，必须标注 **"Powered by StepFun AI"**；
2. **设备厂商**（把模型放进手机、汽车、眼镜、机器人）与年收入 **>2000 万美元**的 **MaaS 厂商**需单独取得商用许可——**内部使用豁免**；
3. **在 Step 5 输出上训练到"实质程度"的模型被视为衍生作品**。

第 3 条是这一周最容易被漏掉的一条：**用开源权重蒸馏出来的东西，可能仍然受上游许可约束。** 这和 MIT / Apache 的手感完全不同。

🟡 其余待核实：Muse Spark Open 在 Artificial Analysis 智能指数 **39 分**、Step 5 Preview **44 分**两个数字均来自聚合站转述，未在 Artificial Analysis 官方页核实；Muse Spark Open 官方自述"两台 512GB 的 M5 Ultra Mac Studio 可跑"，NVFP4 需 ≥700GB 显存、BF16 需 2TB。

来源：[Meta 官方研究博客（Muse Spark Open）](https://research.meta.ai/blog/muse-spark-open)　[Meta 开发者博客（部署与许可）](https://developer.meta.com/ai/resources/blog/build-with-muse-spark-open/)　[ArtificialWatch（直读 StepFun LICENSE.txt）](https://artificialwatch.com/wire/stepfun-step-5-preview-open-weights)　[Pandaily（阶跃官方技术博客解读）](https://pandaily.com/stepfun-step-5-preview-open-weights-technical-blog-92-layer-sparse-gqa)

### 6. 长上下文的隐藏坑：同一条信息换个位置，准确率最多差 40.2 个百分点 🟢

字节 Seed 团队的论文 **《Periodic Weak Spots: Phase Sensitivity from Chunked KV-Cache Compression》**（**arXiv:2609.36322**，**2026-09-28 提交**，本周被广泛传播）。arXiv 摘要页可直连核实：

- 分块 KV Cache 压缩把连续 token 按固定步长压成更少的缓存条目，省显存，但引入了一个新的位置坐标——**phase（相位）**，即 token 相对压缩窗口边界的位置。
- **"在采用此类压缩的大型开放权重模型中，长上下文检索准确率在不同相位之间最多可相差 40 个百分点"**（摘要原文："long-context retrieval accuracy can differ by up to 40 percentage points across phases"）。
- 团队从零预训练了一族 Transformer 做因果分析，确认了**相位专业化**：不同注意力组件对不同源相位的检索贡献不对称。
- 摘要的结论句直接给了评测建议：**"Evaluating models with chunked KV-cache compression thus requires measuring across compression phases: high average accuracy can coexist with systematic positional failures."**（高平均分可以与系统性的位置性失败共存）

🟡 媒体转述中出现的更细数字（DeepSeek-V4-Flash-Base 128K 检索波动 40.2 个百分点、V4-Pro-Base 34.8、后训练后收窄到 19.1 / 14.8；自训 Qwen3-0.6B 对照组平均 59.4% vs 全注意力 61.1%、但最差位置组 9.9% vs 58.4%；振荡周期精确等于压缩步长 4/6/8/12）**均未在 arXiv 摘要页出现**，来自中文科技媒体的正文转述，未能打开 PDF 全文核实，按 🟡 处理。论文自己也说尚未给出通用修复方案。

来源：[arXiv:2609.36322 官方摘要页](https://arxiv.org/abs/2609.36322)　[中文转述（含对照组数字，🟡）](https://www.163.com/tech/article/L8QF59UR00097U7T.html)

---

## 三、为什么值得记

**1. "能跑"和"能动"正在反向移动，自托管的价值要重新定价。**
这一周把"能不能跑"彻底解决掉了：24GB 一张卡、3GB 一台手机、两台 Mac Studio 跑 816B。但"能不能动"一个都没解决，而且正在变糟——Yelp 要收数据授权费，Delta 不让订票，银行连看都不给看全。**把模型搬到本地，你换来的是数据不出门和成本可控，换不来动作权限。** 采购自托管方案时如果按"它能不能替我把事办了"来算 ROI，会算错。正确的算法是：**自托管把"不能动"的损失限定在了只读范围内**——这正是 Schwab 那套只读 MCP 的形状。

**2. "开源"这个词已经不能作为选型依据，许可证必须单独核。**
一周四张证：MIT、Apache-2.0、Muse Model License（"limited commercial terms"，条款未公开展开）、StepFun Model License 1.0（MAU/营收双阈值 + 设备厂商条款 + 衍生作品条款）。最容易被漏的是 StepFun 第 3 条——**在它输出上训练到实质程度的模型算衍生作品**。这意味着"用开源权重蒸馏一个自己的小模型"这条路，不是所有开源权重都放行。**选型表上应该有一列叫 LICENSE，而且要在下单前读 LICENSE.txt，不是读博客。**

**3. 平均分会系统性掩盖位置性失败——长上下文的评测口径要改。**
这篇论文真正的杀伤力不在 40 个百分点，而在那个对照：**平均分 59.4% vs 61.1%，只差 1.7 分；最差位置组 9.9% vs 58.4%，差 48.5 分**（🟡 该组数字来自媒体转述）。**只用平均分选出来的模型，可能在你最需要的那类查询上塌掉一半。** 凡是拿长上下文做检索的——合同审阅、代码库问答、日志归因——评测必须按位置分组做扫描，看曲线不看均值。而这一周恰好有一堆人在把 1M 上下文搬到本地，这个坑会集中爆发。

**4. agent 的可用性不由模型决定，由入口白名单决定，而且拦你的系统不是冲你来的。**
Chris Canal 那句话值得抄在工位上：那些风控"不是为拦 agent 建的"，是为拦诈骗和脚本建的，agent 只是撞在同样的一组特征上。**这推导出一个反直觉的结论：模型变强不会让你更容易被放行。** 同时 Meta 的应对给了一条路——不做对抗做合作（Walmart / Gap / Sephora / Best Buy / Shopify），代价是要一家一家谈。所以"我的 agent 能不能用"这个问题的答案，未来是**一张按站点维护的白名单表**，而不是一个模型版本号。

**5.（旁证）治理侧出现了同构的形状：给访问，不给否决。**
**10 月 15 日 Anthropic 宣布给非营利评估机构 METR 的 6 名员工"员工级访问"**：公司硬件、工位、与自家风险评估团队大致相当的内部系统权限；客户数据、律师-客户特权信息、模型架构三类除外。发布权上，Anthropic **不能否决 METR 发布**，但可要求窄范围删减，而 **METR 可以公开质疑删减是否正当**。Anthropic 的类比是银行监管里的驻场检查员。这与 Schwab 的只读 MCP 是同一个形状：**把"看"的权限给足，把"改"的权力留着。** 差别在于，一个是对外部审计的主动开放，一个是对外部 agent 的被动设限——**方向相反，用的是同一把尺子**。

---

## 四、可行动

- [ ] **给本地 agent 加一条硬边界**：涉及登录态、支付、表单提交、任何不可逆动作的工具，一律要求人工确认；只读工具（检索、读取、导出）自动放行。照抄 Schwab 的"读/写二分"，不要在 prompt 里写，要在工具层的权限上做。
- [ ] **挑一个你最高频的外部站点，把它包成只读 MCP server**，把"看"和"动"拆成两个工具集、两套权限。用这个结构反向检查你现有的 agent：有没有哪个工具同时具备读和写的能力？
- [ ] **选型前先读 LICENSE.txt**，把三行抄进评估表：① 规模阈值（MAU / 营收，触发署名或另签）② 设备厂商条款（是否会挡住"端侧部署"这条路）③ **衍生作品定义**（用它的输出训练出来的模型算谁的）。这一周的 StepFun 三条是全的，MIT / Apache 两条空。
- [ ] **给长上下文检索加一个"位置扫描"测试**：固定 needle 内容，只把它在上下文里平移 0…N 个 token，记录每个位置的准确率，画出曲线；**报告"最差位置组"而不是平均值**。先拿你现在在用的模型跑一遍，看看你的平均分里藏了多少。
- [ ] **用 24GB 这一档跑一遍自己真实的 agent 任务**（Bolt 74B-A9B 走 llama.cpp / Ollama / LM Studio 即可），但记录的是**每一步工具调用的成功率**，不是任务总分。理由很硬：每步差 2 个百分点，20 步之后 0.98²⁰ ≈ 67%，就是三十几个百分点的差距（此为算术推算，非测量结果）——**agent 任务是乘法，benchmark 是加法**。

---

## 五、术语卡

| 术语 | 是什么 | 为什么今天要在意 |
|---|---|---|
| **分块 KV Cache 压缩**（Chunked KV-Cache Compression） | 把连续 token 按固定步长压成更少的缓存条目，降低长上下文的显存与注意力开销 | 它是百万上下文能跑得起的代价所在，也是"相位敏感"的成因 |
| **相位 / Phase** | 一个 token 相对压缩窗口边界的位置 | 同一条信息落在不同相位，检索难度可以差 40 个百分点；**长上下文的"位置"是一个此前没人测的维度** |
| **只读 MCP server** | 用 Model Context Protocol 暴露接口，但只提供查询、不提供写操作 | Schwab 拿它当 agent 接入的唯一通道：**能看余额，不能动钱**。是目前最可复用的 agent 授权模式 |
| **原生 2-bit 量化** | 训练后（或带量化感知）直接以约 2 bit/权重表示，而非事后压到 2 bit | NVIDIA 靠它把 120B 的 Super VL 塞进 24GB。**参数量从此不再是能力的代理变量，bit/权重才是** |
| **LES（Lookahead Expert Scheduling）** | 模型算当前层时，预测下一层需要哪些 MoE 专家并提前从存储加载 | 面壁靠它在 3GB 内存的手机上跑 35B MoE，官方称 80%+ 命中且**不改变输出**——把"显存放不下"变成了"存储带宽"问题 |
| **反爬误伤** | 为拦诈骗/脚本而建的风控把 agent 一并拦下 | 它解释了为什么"模型变强"解决不了"进不去"：**拦截系统不是冲 agent 设计的** |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
