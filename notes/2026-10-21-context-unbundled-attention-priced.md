# 2026-10-21｜上下文在被拆开卖，最后一份按人头计价

> 同一天里有五条互不相干的消息，都在把「上下文」拆下来换更便宜的载体；唯一没人接手的那一层，Anthropic 第一次给出了价格。

**标签**：`#上下文工程` `#Agent` `#开源` `#工程陷阱` `#行业动向`
**生成时间**：2026-10-21 12:08（北京时间）

---

## 一、今日观察

今天的主线不是「又发了个模型」，而是：**过去统统塞进上下文窗口里一起付费的那些活，正在被逐项拆走，每一项都找到了比 token 更便宜的载体——只有一项没有，而它恰好是人类注意力。**

把今天的事按「上下文原本承担的哪一种活」重排，而不是按公司或类别排，表格自己就把观点说完了：

| 上下文原本承担的活 | 今天谁接手 | 换成了什么载体 | 代价记在谁头上 | 今天能不能动手试 |
|---|---|---|---|---|
| 从长文里挑一个**可枚举**的选项（退款还是维修） | Clef / Jev 类决策模型（一次前向） | 你列出的选项 + 校准概率 | 只算输入 token | 能（决策模型已在 Workers AI 上） |
| 从长文里挑一个**不可枚举**的值（金额、日期、时长、清单） | 🟢 **Clairic 抽取模型**（10-19 preview） | 你声明的 schema + 类型化值 + `p_null` + 80% 区间 | 不生成 token，官方称「通常 1 秒内」 | 能（`@cf/cloudflare/clairic`） |
| 记住「上次这个任务发生过什么」 | 🟢 **MemT-1.0 记忆原生基座**（10-20 开源） | 参数化记忆状态，128K 历史下约为完整 KV Cache 的 **1/66** | 训练侧：两阶段训练 + 34B tokens 数据 | 能（HF 权重 + SGLang 起服务） |
| 记住「这类数据一般怎么随时间走」 | 🟢 **Timestral 时序基座**（5M–209M） | 模型自带的时序先验，零样本 | 8 线程 CPU 上 10 ms / 140 ms | 能（HF，Modified MIT） |
| 把结论**写成字** | 🟡 Mercury 3 扩散语言模型（10-19） | 并行去噪，不是逐 token 排队 | 首发价 $0.10 / $0.35 每百万 | 能（OpenAI 兼容 API） |
| **agent 吐出来的东西，由谁来读** | **没有人接手** | —— | 🟢 **非技术员工读完自己 Claude 的全部产出要占掉「半个以上的工作周」；「元工作」占平均员工 Claude 会话的 22%** | 只能自己扛 |

前五行的共同点是：**它们都把「上下文」翻译成了别的东西——schema、参数、先验、并行解码——而且每一行今天你都能亲手跑一遍。** 最后一行没有对应的替代品，于是它成了唯一还在涨价的那一层，也是第一次被明码标价的那一层。

一个副产品观察：今天这几家里，**肯自曝短板的那几句比「第一名」那几句有用得多**（见第三节第 4 条）。

> 🟡 另有一条国产线待核实：多家媒体（网易/快科技，10-20–21）称小米 MiMo-V2.6-Pro 上线 WorkBuddy、Artificial Analysis 智能指数 46 分「全球开源第一」、支持 1M 上下文。但该系列**本身是 9-21 发布并开源**的，10-20 是「上线某平台」，且分数来自转述，**未见一手官方页面核对，暂不作为既定事实**。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 Cloudflare 开出「抽取模型」新品类：Clairic，单次前向、不生成 token

Cloudflare 官方博客（10-19 前后）宣布 System One 类模型下的**第一个抽取模型** Clairic，以 `@cf/cloudflare/clairic` 在 Workers AI 上开启 preview，并称「打算很快以开放权重发布」（**未给日期**）。与决策模型（Clef/Jev）的区别是：决策模型从你**预先列出的选项**里挑一个并给概率；Clairic 处理的是**你没法预先枚举**的值——发票总额、交付日期、迟了几天、维修要多少钱。

关键设计（均出自官方文档/博客）：
- 字段类型：`text`（返回原文 span + 字符偏移 + 置信度）、`number`（可指定小数位与单位）、`date`/`time`/`datetime`（ISO）、`duration`、`list`、`estimate`（在你声明的 min/max 与 step 网格上给出分布，含中位数与 **80% 区间**）、`forecast`（序列未来最多 **64 步**）。
- 每个标量答案都带 **`p_null`**（输入其实没给出这个值的概率）与置信度；`include_quantiles` 可取全部 99 个分位。
- 可随 state 传**最多 4 张图片**。
- 因为不生成 token，官方称「不会产生打错字式的幻觉」，找不到就返回 `null`——**但它会犯错**。
- 🟡 官方自测对比（厂商数据，无第三方验证）：客服邮件场景下 Clairic 抽值 + Clef 决策 + GLM-5.3 写回复，**19.3 秒**；GLM-5.3 全流程自己做 **61.7 秒**（约 3.2 倍），成本约低 **49%**。
- 🟡 官方称 21 天机场安检客流量预测平均误差 **3.3%**（转述自官方，未在博客摘要中直接核对）。
- **官方明说的限制**：多步计算链尚不可靠，建议「让 Clairic 取值，重计算留在你自己的代码里」。
- **官方未公布**：参数量、上下文窗口、定价、任何抽取准确率 benchmark。

来源：[Cloudflare 博客 — Introducing Clairic](https://blog.cloudflare.com/clairic-extraction-model/) · [Cloudflare Changelog 2026-10-19](https://developers.cloudflare.com/changelog/post/2026-10-19-clairic-workers-ai/)

### 2. 🟢 Anthropic 发布内部就业研究：agent 工时 6:1，人类的注意力成了瓶颈，第一次被量化

Anthropic 官方研究页《How employment is changing at Anthropic》，**发布于 2026-10-16**，本周（10-19/20）被媒体大量转述。数据基于内部就业、AI 使用、产出指标、员工调查、日历与招聘记录，并辅以 17 位员工访谈。

硬数字（全部出自官方页）：
- 技术部门初级员工占比 **21% → 14%**（自 2025 年初）；初级技术岗**新招聘占比 27% → 9%**；初级岗位 postings 自 **2025 年 12 月**起锐减。技术部门占全公司人数 **61% → 56%**。
- **2026 年 3 月** agent 工时总和首次超过人类；**2026 年 8 月**「员工直接指挥的交互式 agent」工时为人类 **6:1**。
  - 口径必须记住：agent 工时 = 运行时长（含推理与工具调用，**排除超过 30 分钟的等待**）；人类工时 = 人头 × **每周 40 小时**假设。这不是生产力换算系数。
- 「元工作」（给 agent 写 spec、让一个 agent 审另一个的输出、搭监控流水线）占平均员工交互式 Claude 会话的比例，从 2025 年秋的 **10%** 升到 2026 年春的 **22%**（基于对 2,000 条单行会话摘要的自动编码估算）。
- 非技术员工：读完自己全部 Claude agent 的产出，要占掉「**半个以上的工作周**」——换算口径是 0.75 词/token、250 词/分钟，即每周 20 小时以上。官方该图标题就叫 *Reading Claude as a full-time job*。
- 人均代码提交量约为六个月前的 **5 倍**；非技术员工的编码型 agent 会话从 2025-08 的 **2 次/月** 涨到 2026-05 的 **90 次/月**；管理者提交量**翻倍**；工程师与 PM 比例约 **17:1**。
- 质量检验：对比同一员工、同月、同目录下 agent 写的代码与人写的代码，在「90 天内被删除或回滚的行数比例」等指标上**没有差异**。
- 公司层面应对：建立岗位级「早期预警系统」+ 内部转岗优先。

> ⚠️ 更正一处流传中的误传：多家聚合站把「元工作」写成「占员工 **1/4** 的工作时间」。**官方原文是占「平均员工的交互式 Claude 会话」的 10% → 22%**，不是占总工时。请以官方页为准。

来源：[Anthropic — How employment is changing at Anthropic](https://www.anthropic.com/research/employment-at-anthropic) · [配套报告：Expectations for the future](https://www.anthropic.com/research/expectations-for-the-future)

### 3. 🟢 记忆张量 MemT-1.0：把记忆从「外挂」做成模型内生，10-20 开源——但 LICENSE 是陷阱

中国团队记忆张量（MemTensor）10-20 发布 MemT-1.0，称业内首个「记忆原生」基座模型：在选定 Transformer 模块旁并行一个 **Native Memory Block**，让历史被编码成**持续存在、可更新的内部状态**，而不是每次重新注入上下文。GitHub 仓库 10-20 两个 commit 发布，含 `tech_report.pdf`（arXiv 2610.26825）。

官方 README 的硬数字：
- **MemT-1.0-Nano**：骨干 Qwen3.6-35B-A3B，总参 **36B**、激活 **3B**、可训练记忆参数 **451M**、动态记忆状态 **10M**。
- **MemT-1.0-Flash**：骨干 DeepSeek-V4-Flash，总参 **288B**、激活 **17B**、可训练记忆参数 **3.61B**、动态记忆状态 **336M**。
- 架构：Local Memory Block（跨交互步演化的多通道记忆矩阵）+ Hyper Memory Block（可训练的读/写/遗忘门）；段末由 **Gated DeltaNet-2 (GDN-2)** 做逐 token 稳定更新；另有 **Mixture-of-Storage (MoS)** 扩容。
- **状态大小恒定，128K 历史长度下存储约为完整上下文 KV Cache 的 1/66**（官方 README 原文约 66×）。
- 训练：两阶段流水线，**34B tokens** 数据。
- 部署：`inference/` 下 `uv pip install '.[server]'`，SGLang 起服务，记忆快照存 `./memt-state`，`save_state()` / `state=` 可跨会话恢复（恢复后明文对话长度为 0，记忆还在）。

🟡 未在官方 README 中直接看到、仅见媒体转述的数字（环球网/量子位/36氪，10-20）：11 项记忆基准上 Flash / Nano 平均 **50.6 / 47.0**；Nano 在 SWE-bench Verified 500 项上平均成功率 **66.07% → 69.73%**、三次全成功比例 **54.00% → 62.80%**；128K / 256K 下端到端推理速度为完整上下文的 **1.86× / 3.99×**。（其中 1.86× 与 1/66 与官方 README 的 66× 方向一致，但基准分数**暂按 🟡 处理**。）

⚠️ **官方自曝的短板（比「第一名」更值得记）**：官方 README 明写——在 11 项记忆基准上 Flash/Nano 位列**已评测的参数化记忆方法**第一、第二，但「**强文本记忆系统总体上仍然领先，尤其是在需要详细证据检索的长历史上**」。

🚨 **许可陷阱（最实用的一条）**：官方 README 的 License 段写得很清楚——
- **仓库软件（含 SGLang 集成）采用 PolyForm Noncommercial License 1.0.0，明确禁止商用**；商用授权需联系作者。
- 技术报告与论文材料为 **CC BY-NC-SA 4.0**（非商用 + 相同方式共享）。
- **模型权重、数据集、benchmark 资产不在上述许可范围内，条款随各自发布另行提供。**
→ 媒体标题里的「开源」≠ 可商用。上生产前必须单独确认权重条款。

来源：[GitHub — MemTensor/MemT-1.0](https://github.com/MemTensor/MemT-1.0) · [Hugging Face — MemTensor/memt-1 collection](https://huggingface.co/collections/MemTensor/memt-1) · [arXiv 2610.26825](https://arxiv.org/abs/2610.26825) · 🟡 [量子位 10-20](https://www.qbitai.com/2026/10/504456.html)

### 4. 🟢 Mistral Timestral：209M 参数、纯 CPU 推理的时序基础模型，官方 10-15 发布，本周转热

Mistral 官方 10-15 发布首个时序基础模型（TSFM）家族 Timestral，**四个尺寸：5M / 28M / 123M / 209M**，共享同一架构与训练配方。⚠️ 注意日期：**官方发布是 10-15，10-20 前后是 HN 与媒体讨论扩散**，不是「今天发布」。

官方口径：
- 209M 模型在 **GIFT-Eval、TIME、fev-bench** 三个主要公开榜单位列**预训练零样本模型第一**（五项指标全部第一），且只用此前 SOTA **约三分之二的参数**；结果来自**单个 checkpoint，未做集成**。
- **不需要 GPU**：8 线程标准服务器 CPU 上，从三周 15 分钟粒度历史预测未来一天，5M 模型 **10 ms**、209M 模型 **140 ms**。
- 28M 模型在 GIFT-Eval 与 TIME 上击败**大约 4 倍于它**的 Chronos-2；209M 以更少参数击败 TimesFM-3 与 Falcon-2.0。
- 技术要点：Decoupled Horizon Forecasting（DHF）、covariate-aware attention（区分目标变量 / 仅过去协变量 / **已知未来协变量**，信息只从协变量流向目标）、合成数据为主。
- 规格（🟡 来自第三方对 HF 模型卡与 README 的整理）：上下文最多 **32,768** 时间步，一次前向最多预测 **1,024** 步，输出 **21 个分位数**；209M 的 fp32 权重 **837 MB**；GIFT-Eval MASE **0.658**、fev-bench SQL skill score **50.39**。
- 许可：**Modified MIT**；权重在 Hugging Face（`mistralai/Timestral-209M`）与 GitHub，可用 Mistral Forge 在自有数据上微调（支持 on-prem / VPC / 气隙部署）。

🟡 **反向核实（值得警惕）**：社区对官方图表与许可的质疑集中在两点——有人指出图表呈现「让 0.03 的改进看起来像 5 倍差距」；官方基准**未与 Nixtla TimeGPT 对比**。🟡 另有第三方称 Modified MIT 中含「月收入条款」，**未在官方公告中直接核对，选型前请自行读 LICENSE**。官方与模型卡均称**完整技术报告稍后发布**，方法细节目前无法完全验证。

来源：[Mistral 官方 — Timestral](https://mistral.ai/news/timestral) · 🟡 [HN/社区讨论转述（ai0.news 10-20 digest）](https://ai0.news/posts/2026-10-20-daily-digest) · 🟡 [第三方对模型卡与 LICENSE 的整理](https://braindetox.kr/en/posts/timestral_mistral_time_series_model.html)

### 5. 🟡 Inception Mercury 3：扩散式 LLM 跑进 1,068 tok/s，但分数全是自测、无权重

Inception 10-19 发布 Mercury 3（Business Wire 通稿），定位「迄今最强的扩散式 LLM」。

- 速度：**NVIDIA GPU 上 1,068 tokens/秒**，官方称比同档快 **4–8 倍**；上下文 **1M**（Mercury 2.5 为 260K）。
- 规模：**超过 Mercury 1 的 40 倍**参数；官方称智能相对 Mercury 1 提升约 3 倍，以此论证**扩散模型的 scaling law 与自回归一致**。联合创始人 Stefano Ermon 原话：「扩散模型的扩展上限是算力与数据，不是根本性算法障碍。」
- 价格：列表价 **$0.20 / $0.70**（每百万输入/输出），**首发五折 $0.10 / $0.35**，缓存输入再打一折；新账户 1 亿免费 token。OpenAI API 兼容，模型串 `mercury-3`，已在 Inception API、OpenRouter、Baseten、Vercel 上线。**未发布权重**。
- 🟡 官方自测（12 项中领先 8 项，中等设置）：SWE-Bench Atlas **51.08**（Haiku 5.5 32.26 / Luna 33.33）、IFBench **76.84**、GPQA Diamond **89.23**；但 **Haiku 5.5 在 DeepSWE v1（46.31 vs 51.62）与 MRCR v2（75.50 vs 78.40）上领先**——长上下文检索与长程编码仍是弱项。
- 🟡 客户自述（非独立评测）：TinyFish 在 50 个真实 Mind2Web 网页导航任务中**完成 50%**（一半失败），官方称优于 GPT-6.1-Sol 但未给对方数字；Octen AI 眼镜搜索中位生成 0.9 秒 / 端到端 2.2 秒。
- 官方未披露：参数量、架构细节、速度测试所用 GPU 型号。

来源：[Business Wire / AOL 通稿 2026-10-19](https://www.aol.com/articles/inception-launches-mercury-3-setting-164800000.html) · 🟡 [深度整理（含对手分数对照）](https://www.depthgrid.in/2026/10/inception-mercury-3-diffusion-llm-1m-context-pricing-benchmarks.html)

### 6. 🟡 融资面：CoreWeave 债券跌入困境区，同期 Tenstorrent 融了 15 亿

两条同一周发生的反向信号（**均为媒体转述，交易细节待核实**）：

- **CoreWeave**：🟡 上周债券进入困境区间——无抵押债券（2031/2032 到期）成交价跌至面值 **76.5–81 美分**，收益率升至 **15–16%**；五年期 CDS 利差突破 **1000 个基点**（盘中报 1194.5bp），隐含五年违约概率约 **60%**；股价单周跌逾 **20%**（10-14 单日跌 15.46%）。Chamath Palihapitiya 公开质疑 AI 基建是否已是「私人信贷泡沫」。🟡 资产负债口径（截至 2026-06）：有息债务约 **356 亿美元**，经营租赁负债约 **163 亿美元**，另有约 **355 亿美元**已签未执行的未来租金承诺，现金约 **55 亿美元**；积压订单约 **1040 亿美元**（🟡 媒体口径，另有源写「逾 1000 亿」）。**2026 年底前约有 44 亿美元到期**。
- **Tenstorrent**：🟡 完成 **15 亿美元**融资，投后估值 **62 亿美元**（较 2024 年底翻倍以上），Jim Keller 称资金用于 Galaxy 服务器扩展与 AI IP 授权，**明确拒绝出售**（称曾拒 Intel 与 Qualcomm 收购意向）。

来源：🟡 [The Gist — Compute & Infrastructure, 2026-10-20](http://aigist.co/digests/1120) · 🟡 [Crypto Briefing — CoreWeave 债务](https://cryptobriefing.com/?p=396759) · 🟡 [ai0.news 10-20 digest](https://ai0.news/posts/2026-10-20-daily-digest)

---

## 三、为什么值得记

1. **「上下文」这个词今天开始分层了，而唯一没被替换掉的那层是人类注意力——它还第一次被标了价。** Anthropic 用官方口径给出了两个数：非技术员工读完自己 agent 的全部产出要占掉**半个以上的工作周**，元工作占平均员工 Claude 会话的 **22%**。这不是抱怨，这是把「人的注意力」写进了成本表。凡是今天还在按 token 算账的团队，都少算了这一项。

2. **「单次前向」正在从「决策」扩张到「抽取」，模型选型的最小单位从「模型」变成了「格子」。** Cloudflare 官方那张表把 System One 拆成了 Extract / Decide 两格，System Two 留给写作与推理，并明说「LLM 处理第三类」。含义是：一条流水线里同一个问题可以拆给三四种不同机制的模型。**但 Clairic 目前参数量、上下文、定价、准确率 benchmark 全部未公布**，只有自测的 19.3s vs 61.7s——所以今天它只能当**架构参考**，不能当**选型依据**，等开放权重和独立评测。

3. **记忆从「外挂」变「内生」是路线变化，成本只是换了个地方记。** MemT 把推理侧的状态压到完整 KV Cache 的 **1/66**，代价是训练侧两阶段 + 34B tokens，且**仓库代码是 PolyForm Noncommercial（禁止商用）、权重条款另行发布**。媒体标题的「开源」和 LICENSE 文件里的「非商用」是两件事——这条如果只看标题，很可能在上生产时踩雷。

4. **今天最有信息量的三句话，全是厂家自己说的短板，不是他们说的第一名。** Anthropic：agent 写的代码与人写的代码在「90 天内被删除/回滚比例」上**没有差异**（所以别拿代码量当质量证据）。MemTensor 官方 README：**强文本记忆系统在需要详细证据检索的长历史上仍然领先**（所以参数化记忆不是万能替换）。Inception 自家表格：Haiku 5.5 在 **DeepSWE v1 与 MRCR v2** 上领先（所以扩散路线的弱项在长上下文检索）。**凡看到「第一」，先去官方源找它自己承认输在哪。**

5. **钱没有退潮，只是在换手。** 同一周里 CoreWeave 债券跌进困境区、CDS 隐含五年违约概率约六成，而 Tenstorrent 拿到史上非 NVIDIA 芯片挑战者的最大单笔融资。这说明市场不是在否定算力需求，而是在**重新给「谁借钱建的」这件事定价**。对你的实际影响是：选型时供应商的**融资结构**（而不仅仅是单价）开始值得看一眼。

---

## 四、可行动

- [ ] **拆一条现有抽取流水线试 Clairic**：把现在用 LLM + JSON Schema 做的结构化抽取，改成 `env.AI.run("@cf/cloudflare/clairic", { state, fields })`，用返回的 `p_null` 与置信度做分流（高于阈值才自动放行，否则转人工），**把多步计算留在自己的代码里**（官方明说长链计算不可靠）。先只上一个字段类型（比如 `date`）验证收益。
- [ ] **读 MemT-1.0 的 LICENSE 再决定能不能上生产**：`github.com/MemTensor/MemT-1.0` 的 License 段写明仓库软件为 **PolyForm Noncommercial 1.0.0（禁止商用）**、论文材料为 CC BY-NC-SA 4.0、**权重条款另行提供**。商用前必须单独确认权重授权，别信「开源」标题。
- [ ] **给自己的时序预测加一个 CPU 基线**：拉 `mistralai/Timestral-209M`（fp32 约 837 MB），在 8 线程 CPU 上跑一遍自己的数据（32,768 步历史 / 1,024 步预测 / 21 个分位数），跟现有基线比 MASE 与 CRPS，**不要只看 GIFT-Eval 的 0.658**——那个数是官方榜、单 checkpoint、且未与 TimeGPT 对比。
- [ ] **给团队的 agent 产出算一笔「阅读预算」**：按 Anthropic 的换算口径（0.75 词/token、250 词/分钟、每周 40 小时）估算你们每周要花多少小时读完 agent 输出；**超过 20 小时就该上 dashboard / 自动摘要**，而不是继续加 agent。同时用「元工作占比」自查：如果你的会话里超过两成是在给 agent 写 spec 和做监控，说明编排层该重构了。
- [ ] **如果你把长上下文记忆当 KV Cache 成本在算，用 66× 这个数量级重估状态预算**——但记住官方 README 的自曝：需要**详细证据检索**的长历史场景，文本记忆仍然更强。两者是分工不是替代：精确原文走外挂检索，可复用的执行经验走内生记忆。

---

## 五、术语卡

| 术语 | 一句话解释 | 今天出现在哪 |
|---|---|---|
| **System One / System Two 模型** | 借 Kahneman《思考，快与慢》的分法：System One 模型**一次前向、不出 token、快且类型化**（如 Clairic 抽取、Clef/Jev 决策）；System Two 模型逐 token 生成、可深思（GPT / Claude / Gemini）。分工思路是「事实与选择交给小模型，写字交给大模型」 | Cloudflare Clairic 官方博客 |
| **抽取模型（extraction model）** | 与决策模型的区别：决策模型从**你预先列出的选项**中选一个并给概率；抽取模型处理**无法预先枚举**的值（金额、日期、时长、清单），返回类型化结果 | Clairic |
| **`p_null`** | 「输入其实没有给出这个值」的概率，与置信度一起返回；用于决定这条结果能不能自动放行、还是要转人工复核。Clairic 找不到时返回 `null` 而不是编一个 | Clairic |
| **记忆原生 / 参数化记忆** | 把历史编码成模型内部**持续存在、可更新的状态**，而不是反复注入上下文。MemT-1.0 在骨干注意力旁并行 Native Memory Block，由 Gated DeltaNet-2 做逐 token 更新，状态大小恒定（128K 历史下约为完整 KV Cache 的 1/66） | MemT-1.0 |
| **时序基础模型（TSFM）** | 在大规模多样语料上预训练、可对**没见过**的序列做**零样本**预测的模型，替代「每条序列各训一个 ARIMA/PatchTST」。Timestral 四档 5M–209M，纯 CPU 可跑 | Mistral Timestral |
| **扩散语言模型（dLLM）** | 不逐 token 排队生成，而是先起草整段答案再并行去噪细化若干轮，从而提高吞吐上限。Mercury 3 报 1,068 tok/s，但**权重未开放、分数为自测** | Inception Mercury 3 |
| **CDS 利差 / 困境债** | CDS 利差是为债务买「违约保险」的年化成本，1000bp 意味着约为面值的 10%/年，通常被视为**困境**门槛；无抵押债券跌破面值 80 美分亦为同类信号 | CoreWeave |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
