# 2026-10-19｜模型之外，三张账单同时到期

> 电、显存、验证：这 48 小时里最有信息量的消息，没有一条在说模型变强了。

**标签**：`#基础设施` `#推理栈` `#vLLM` `#形式化验证` `#算力供给`
**生成时间**：2026-10-19 12:05（北京时间）

---

## 一、今日观察

把 10 月 16–18 日这 48 小时的消息按「它落在模型的哪一层」重新排一遍，会出现一条很整齐的断层：**这一轮最硬的四条消息，全都发生在模型下面**。

| 层 | 这两天发生的事 | 它到底在省什么 / 抢什么 | 期限 | 你自己能不能动手 |
| :--- | :--- | :--- | :--- | :--- |
| **电网** | Anthropic 包租 Point Tupper **20 年**；微软退出 Nscale 的 Essex 项目 | **并网日期**，不是芯片 | 2027 年底 / 2030 年代 | 不能 |
| **显存与带宽** | vLLM v0.32.0 把 KV cache 压到 **NVFP4**；Xolotl 单张 24GB 卡跑 **552B** 模型 | 每个 token 的**显存占用与搬运量** | 立刻（升级即生效） | **能** |
| **验证** | OpenAI 719 篇手稿只有 **~42%** 完成 Lean 形式化；三天后 $1500 万交给基金会 | 人判断「这到底对不对」的**时间** | 没有期限 | 部分能 |

这三层看起来毫无关系，但有一个共同点：**它们都买不到**。电买不到（有钱也排不进并网队列）、显存密度买不到（同一张卡的 HBM 是固定的）、人的核验注意力也买不到（全世界能读懂这些手稿的数学家数量是固定的）。

所以今天真正在发生的事情不是"模型更强了"，而是——**过去靠"买更多"解决的三件事，现在都只能靠换架构解决**：换配电电压、换 KV cache 精度、换验证的组织形式。

还有一个细节值得单独拎出来：这三层的**账期完全不一样**。显存是"今天升级今天就见效"，电网是"签了 20 年才落地"，验证是"根本不知道什么时候结束"。一个工程团队能控制的东西（vLLM 那一行），和它控制不了的东西（并网日期），正在被拉成两个极端。

---

## 二、事实清单
> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. vLLM v0.32.0 发布：结构化判定被塞进推理引擎，低精度 KV cache 全面铺开 🟢
- **814 个 commit、363 位贡献者**（官方 release 页面统计口径以 GitHub 为准）。新增默认开启的 `POST /v1/systemone` 端点，直接在引擎内回答 `choice` / `noul` / `score` 三类结构化问题，**返回各允许选项的概率**，不再走"生成文本 → 解析 JSON"这条路。
- 低精度 KV cache 覆盖面大幅扩展：**NVFP4** 支持到 SM8x / SM90 / SM12x；GLM-5.x 在 SM100 上默认 FP8 KV cache，**每 rank 的 KV 显存减半**，换来吞吐 +2.3–5.5%，代价是 TTFT +7–11%（PR 自带 benchmark）；`fp8_ds_mla` 在 SM90 上给 GLM-5.3-Flash 最高 **+31%** 输出吞吐；ROCm 侧新增约 FP8 两倍密度的 4-bit `ultraquant_4bit`。
- **升级有 breaking changes**：Python 3.10 被弃用（需 3.11+）、`transformers>=5.16.1,<5.20.0`、`cascade attention` 被移除、`mamba_cache_mode="all"` 被移除、`max_tokens` 从"预留"改为"上限"、Responses API 推理流事件改名。同时修了 3 个 GHSA（chat template 资源耗尽 / tokenizer `max_token_id` / P2P ZMQ socket 耗尽），**默认 CORS 不再放行所有 origin**。
- 来源：[GitHub · vllm-project/vllm releases v0.32.0](https://github.com/vllm-project/vllm/releases/tag/v0.32.0)

### 2. OpenAI 数学手稿库：719 篇、372 个族，只有约 42% 完成形式化 🟢
- 官方仓库 README 原文：当前目录包含 **719 篇手稿、372 个 family**，由**一个未发布的内部模型**产出；评测过程中模型被问了约 **4,000 道题**；**平均每个结果消耗相当于 3 小时 ChatGPT Pro 思考算力的计算量**；仓库标注「**约 42% 的 top-line 结果已完成形式化**」，并明说"未形式化的结果可能有问题（could have issues）"。
- 版本策略：更正与修订以**新版本形式追加**，旧版本保留可访问。
- 🟡 补充（**待官方源核实**）：有媒体转述称 OpenAI 已撤回 3 篇、修订 14 篇；该数字来自《Science》相关报道的中译转述，未在官方仓库 README 中直接看到，暂不作为既定事实。不同媒体对手稿总数有 719 / 722 两种说法，以 README 的 719 为准。
- 来源：[GitHub · openai/math README](https://github.com/openai/math)（🟢 主源）；[科学网转述《Science》](https://wap.sciencenet.cn/blog-41174-1556523.html)（🟡 撤回/修订数）

### 3. 验证被单独立项：$1500 万交给基金会，OpenAI 出 500 万 🟢
- 10 月 15 日，**Simons Foundation 联合 Anthropic 与 OpenAI** 宣布合计 **$15M** 的资金与资源投入，用于支持数学界评估近期 AI 辅助产生的结果、学习使用新工具、**形成关于 AI 使用的共同标准**。
- 关键在结构：**基金独家居中管理和发放**，通过 open call 招标；OpenAI 出资 **$5M**；两家公司另向受资助研究者提供 AI 工具与算力，范围超出数学延伸到基础科学。基金会主席 David Spergel 的原话是"**应该由社区来主导这些工具如何被评估、采纳和使用，而不是任何一家公司或机构**"。
- 时间线很说明问题：10 月 6 日发手稿 → 10 月 15 日宣布出一笔**专门用于"检查"**的钱。这不是研究经费，是**核验经费**。
- 来源：[Simons Foundation 官方公告](https://www.simonsfoundation.org/news/simons-foundation-launches-15m-effort-to-help-mathematicians-navigate-ai-era)

### 4. 微软退出 Nscale 的 Essex 数据中心：不是缺芯片，是缺并网日期 🟢
- 《The Telegraph》10 月 18 日报道：微软近期通知 Nscale **终止去年宣布的协议**，退出其位于埃塞克斯郡 **Loughton** 的首个英国数据中心（原为微软对英 **£22bn** 投资承诺的一部分）。
- 站点已部署数千块高端 NVIDIA 芯片，原计划明年投运，但**电网方告知 Nscale，预计要到 2030 年代才能供电**。微软是唯一公开签约客户，约定租用该站点 **23,000 块 NVIDIA AI 芯片**（另有报道口径为 23,040 块 GB300，一期 50MW、可扩至 90MW 🟡）。
- Nscale 总签约收入 **$103bn**，其中 **超过 40% 来自微软**；公司正推进估值最高 **$35bn** 的上市计划。Nscale 发言人称仍推进 Loughton 项目并**寻找替代电源**。
- 关联背景（同一报道）：Gartner 上周称若 AI 热潮未兑现，**到 2030 年可能有 $3.5tn 投资被减记**；CoreWeave、Nebius 等 neocloud 过去一周股价与债券同步下挫。
- 来源：[The Telegraph, 2026-10-18](https://www.telegraph.co.uk/business/2026/10/18/microsoft-axes-ai-deal-setback-uk-data-centre-pioneer/) · [澎湃新闻转述](https://www.thepaper.cn/newsDetail_forward_34275391) · [中新经纬转述 FT](https://m.chinanews.com/wap/detail/cht/zw/jw693067.shtml)

### 5. Anthropic 反向操作：包租 20 年，自己把电和网一起签了 🟢
- 10 月 16 日 EverWind Fuels 宣布在新斯科舍省 **Point Tupper** 投资逾 **C$10bn**（其中逾 C$8bn 建园区、C$2bn 投陆上风电）。CBC / Canadian Press 确认承租方为 **Anthropic**，租期**至少 20 年**，一期 **95MW** 目标 2027 年底投运，二期 325MW 目标 2028 年，满负荷 **420MW**。
- 路透社口径：这是 Anthropic 在**加拿大的第一个数据中心协议**；园区将承载 Claude 的推理需求。
- 最值得记的两句话：一，**EverWind 自建的 650MW 风电赶不上一期 2027 年底投运**，靠省级电网运营商研究认为现有设施可支撑；二，**二期并网取决于尚未完成的系统研究与审批**。同一份公告里，一半是承诺，一半是前置条件。
- 来源：[Canadian Press / AI Business Weekly 转述](https://aibusinessweekly.net/p/anthropic-everwind-nova-scotia-data-centre) · [TSNMedia 汇总（含 Reuters / CBC / Globe and Mail 转引）](https://tsnmedia.org/everwind-point-tupper-campus) 🟡 *Anthropic 官方稿未在公开索引中直接定位到，核心数字以上述权威媒体转述为准*

### 6. 单卡跑 552B：端侧的另一个方向（开发者自测，🟡）
- 有开发者称基于 Strata 的推理引擎在**单张 24GB RTX 4090** 的 PC 上跑 **552B 参数的 DeepSeek-V4.1-Flash**，解码约 **27 tok/s**，prefill 180–320 tok/s，上下文 512K；配置为 Ryzen 7 5700X + 90GB DDR4 + NVMe，权重分布在显存、锁页内存和 NVMe 上，按需加载专家。
- **信源为开发者自述，无独立复现**，速度与任务分数均标 🟡，不要直接拿来做容量规划。
- 来源：[artificialintnews 转述 Xolotl 开发者](https://artificialintnews.site/index.html)（🟡）

---

## 三、为什么值得记

1. **"缺什么"这个问题，答案已经从 GPU 换成了并网日期。** Nscale 的 Essex 站点有芯片、有客户、有 1030 亿美元合同，最后倒在没有电。反过来 Anthropic 愿意签 20 年、自己承担电网接入与升级费用——因为它买的是"**什么时候有电**"这个确定性。评估任何一家算力供应商时，问"GPU 订单多少"已经不如问"**并网日期是哪天、有没有落进协议**"。

2. **验证第一次被单独标价，而且是被"产出方"出钱买的。** $15M 不是用来做研究的，是用来**判断已有产出对不对**的。719 篇手稿里只有 ~42% 完成 Lean 形式化，剩下的 58% 连"机器能不能检查"都还没解决——**这个比率就是今天 AI 产出与人类可用知识之间的缝隙宽度**。而给出钱的是 OpenAI 自己，管理钱的却被推给了基金会：这说明"**谁出钱、谁定标准**"这件事已经被当成问题处理了。

3. **推理引擎正在往应用层挤，边界又一次位移。** vLLM 把 choice/score 判定搬进引擎内部，省掉的是**第二次 prefill**——以前 Agent 要在"先让小模型判断要不要调工具"和"直接上大模型"之间付一次往返税，现在这个判断可以复用同一份 KV cache。这不是加了个 API，是**推理服务器和 Agent 框架之间的分工被重新划了一次线**。

4. **三张账单的账期分别是"立刻 / 十年 / 无限期"，这个差异本身就是风险。** 显存这一层你今天升级就见效；电网这一层你签了 20 年也未必落地；验证这一层根本没有终点。**把三者放在同一张路线图上排期，是今天最容易犯的规划错误。**

---

## 四、可行动

- [ ] **升级 vLLM 前先锁版本**：0.32.0 有 breaking changes（Python 3.10 弃用、`transformers>=5.16.1,<5.20.0`、`cascade attention` 移除、`max_tokens` 从"预留"变"上限"）。若线上有长上下文请求，**升级后必须重跑长上下文准入测试**——旧的长请求此前会被拒绝，现在会被接受。
- [ ] **用 curl 打一遍 `/v1/systemone`**：把 Agent 里"要不要调 shell / 是否安全 / 挂哪个工具 schema"这类判定改成引擎内结构化调用，对比改造前后的 p95 延迟与 JSON 解析失败率。官方示例接口为 `{"model": "...", "prompt": "...", "schema": {"type": "choice", "options": [...]}}`。
- [ ] **若在用 GLM-5.x / GLM-5.3-Flash，试两个开关**：SM100 上 GLM-5.x 默认 FP8 KV cache（每 rank KV 显存减半，吞吐 +2.3–5.5%，TTFT 代价 7–11%）；SM90 上 `fp8_ds_mla`（输出吞吐最高 +31%）。先确认自己的卡属于哪一档 SM 再改。
- [ ] **检查对外暴露的 vLLM 服务**：0.32.0 修了 3 个 GHSA（chat template 资源耗尽、tokenizer `max_token_id`、P2P ZMQ socket 耗尽），且**默认 CORS 不再放行所有 origin**。升级前把前端域名加进白名单，否则会当场打挂。
- [ ] **把"并网日期"写进算力供应商 RFP 的必答项**，并要求写进合同而非 PPT。参考 Essex 案例：有芯片、有客户、有合同，缺的只是电。
- [ ] **本地跑超大 MoE 模型时先做自己的复现**：27 tok/s / 552B 这类数字是开发者自测（🟡），用它做容量规划前，至少在自己的机器上跑一遍 prefill 与解码。

---

## 五、术语卡

| 术语 | 解释 | 为什么今天重要 |
| :--- | :--- | :--- |
| **KV cache** | 保存已处理 token 的注意力中间结果，让生成下一个 token 时不必重算整个上下文；精度越低（FP8 → NVFP4/4-bit）显存占用越小 | vLLM 0.32.0 这轮的核心变化几乎都在这里：KV 显存减半，直接决定单卡能塞多长上下文 |
| **NVFP4** | NVIDIA 的 4-bit 浮点格式（带 scale factor）用于权重/KV cache 存储 | 比 FP8 再压一半，代价是精度与兼容性；部分 checkpoints 目前仍依赖厂商容器而非上游 vLLM |
| **MoE 专家卸载（expert offloading）** | MoE 模型每次只激活少数专家，把不常用的专家放在显存外（锁页内存 / NVMe），按需加载 | Xolotl/Strata 用它在单张 24GB 卡上跑 552B 模型；**用带宽换容量**，速度取决于存储而非算力 |
| **Lean 形式化** | 把数学证明写成 Lean 语言，由内核逐步机器校验；**只能验证"这段代码所陈述的命题"是否成立** | 719 篇手稿只有 ~42% 完成；形式化 ≠ 结论为真，也不等于命题就是论文的主定理 |
| **并网日期（grid connection date）** | 电网运营商承诺为某个项目接入电力的时间，通常以年计且可能晚于项目完工 | Essex 项目有芯片有客户，卡在"2030 年代才有电"；这是今天最容易被忽略、却最不可采购的变量 |
| **neocloud** | 以 AI 算力租赁为主、重度依赖融资与发债扩张的云服务商（CoreWeave、Nebius、Nscale 等） | 其商业模式的脆弱点不是需求，而是**利率 + 交付能力**；本周股价与债券同步下挫 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
