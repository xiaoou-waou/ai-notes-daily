# 2026-09-04｜成本单位从 token 换成 task，开源分发枢纽被买走

> OpenAI 官方页首次把"每任务成本"写进发布材料；同一周英伟达买下了开源模型的分发枢纽。

**标签**：`#成本` `#Agent` `#开源` `#分发` `#端侧`
**生成时间**：2026-09-04 12:20（北京时间）

---

## 一、今日观察

昨天到今天，四家厂商的动作拼出了同一张图：**AI 的账本和供应链，同时换了一套算法。**

| 维度 | 事件 | 变化的是什么 |
| --- | --- | --- |
| **计价单位** | OpenAI GPT-6 Astra（9-03） | 官方材料首次以**每任务 API 成本**为主轴做对比，而不是单价表 |
| **降本路径 A** | Astra：贵单价 + 少步数 | $10/$50 每百万 token，但 BenchCAD 每任务成本比 Sol 低约 43% |
| **降本路径 B** | Gemini 3.8 Flash（9-02）：平单价 + 多步数 | 单价与 3.7 持平，但官方明说会**用掉更多 token** |
| **账单结构** | Claude Fable 5.1（9-01） | 缓存读取 $1 → $0.25，官方测算 agentic 负载最高降 45% |
| **供应链** | 英伟达 129.3 亿美元收购 Hugging Face（9-03） | 开源模型的默认分发枢纽易主 |
| **替代路径** | 星火 X2.5 端侧开源（9-01） | 1M 上下文 + Apache 2.0 + 全国产算力，绕过中心化分发 |

一句话：**厂商不再比"每百万 token 多少钱"，而是在比"完成一个任务多少钱"。** 而"开源模型免费"这件事的地基——一个中立的分发平台——在同一周被算力巨头买下了。

---

## 二、事实清单

> 信源等级：🟢 官方发布 / 权威媒体　🟡 二手转述，待官方源核实

### 1. OpenAI 发布 GPT-6 Astra，官方材料按"每任务成本"算账 🟢

- 发布时间：2026-09-03（美国时间），API 名 **`gpt-6-astra`**，另经 AWS / Amazon Bedrock 提供
- 定价：标准档 **输入 $10 / 输出 $50** 每百万 token；Fast mode 2 倍速、**2 倍价**
- **官方页面在多处直接给出"每任务成本"对比**（这是本次发布最不寻常的地方）：
  - BenchCAD：API 成本比 GPT-5.6 Sol 低约 **43%**，比 Fable 5.1 低约 **86%**
  - Terminal-Bench 4.0：每任务成本比 Fable 5.1 低约 **63%**
  - GPQA Diamond（低成本设置）：成本比 Sol 低约 **37%**
  - OSWorld 2.0：每任务耗时比 Sol 少约 **47%**
- 关键分数：FrontierMath Tier 4 **97.6%**（Sol 83.0%）、ARC-AGI-3 **99.9%**（Sol 7.8%）、Terminal-Bench 4.0 **57.9%**（Sol 37.3%）、Agents' Last Exam **59.3%**
- 安全：在 Preparedness Framework 下**首次达到网络安全 Critical 阈值**；发布版**拒绝**为漏洞编写 PoC 等攻击性任务，仅开放安全代码审查与打补丁；后续经 **OpenAI Daybreak** 逐步放行漏洞验证、恶意软件分析等防御工作流。企业租户**默认关闭**，需管理员手动开启

**来源**：[OpenAI 官方页 GPT-6 Astra](https://openai.com/index/gpt-6-astra/) · [Safety overview: GPT-6 Astra（9-03）](https://openai.com/index/safety-overview-gpt-6-astra/) · [System Card](https://deploymentsafety.openai.com/gpt-6-astra) · [新京报贝壳财经](https://www.163.com/dy/article/L5VK33HQ0512D3VJ.html)

### 2. 英伟达 129.303 亿美元收购 Hugging Face 🟢

- 官方博客 9-03 由黄仁勋署名，金额原文写作 **$12,930,300,000**
- 四条明确承诺（原文可查）：开发者可自选**模型、框架、云与推理服务商、计算平台**；**构建或部署不强制使用 NVIDIA 算力**；继续支持**多云与多加速器**；Hugging Face 团队保留原有 **🤗 品牌**
- 平台规模：**1800 万+** 开发者/研究者/创作者、**300 万+** 模型、**50 万+** 数据集、**100 万+** 应用、**20 万+** 企业使用方
- 英伟达自称是 HF **最大的开放模型与数据贡献方**：已发布 **500+** 模型、**250+** 开放数据集
- Delangue 称是**自己主动**找的黄仁勋，理由是开源 AI 到了转折点，需要更多资源与更大可见度

🟡 待核实：FT 称英伟达希望 2027 年前完成交易、可能面临竞争监管机构审查；交易结构为约 119 亿美元对价 + 最高 10 亿美元员工股权激励。以上来自二手转述。

**来源**：[NVIDIA 官方博客（黄仁勋署名）](https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/) · [澎湃新闻](https://www.toutiao.com/article/7681303038933484068/) · [第一财经](https://www.toutiao.com/article/7681311618243887658/)

### 3. Google 发布 Gemini 3.8 Flash 与 Flash Cyber 🟢

- 9-02 发布，model ID **`gemini-3.8-flash`**，输入上限 **1,048,576** token、输出上限 **65,536** token
- 定价：intro 价 **$0.75 / $3.75** 每百万 token（**至 2026-12-31**）；**2027-01-01 起翻倍至 $1.50 / $7.50**
- **官方主动预警成本风险**：模型在复杂任务上会执行额外推理步骤、迭代调用工具，"**在某些时刻会用掉更多 token**，尤其在更高 effort 档位"。单价没变，账单会涨
- 官方分数：HLE-Verified **54.9%**；DeepSWE v1.1 长程软件工程上称优于多数更大更贵的前沿模型
- Gemini 3.8 Flash Cyber 专攻漏洞发现与自动打补丁，**仅通过新的 Fairwind Program** 向政府、关键基础设施运营方、软件维护者申请开放，无公开价格

**来源**：[Google 官方博客](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) · [Unite.AI](https://www.unite.ai/google-launches-gemini-3-8-flash-with-cybersecurity-variant) · [ET Enterprise AI（成本上升提醒）](https://enterpriseai.economictimes.indiatimes.com/news/industry/gemini-3-8-flash-google-keeps-token-rates-flat-but-usage-costs-could-rise/133732802)

### 4. Claude Fable 5.1 / Mythos 5.1：降的是缓存，改的是 API 🟢（🟡 部分工程细节）

承接 9-02 已记录的内容，补充两条今天才看清的信息：

- 9-01 发布；缓存读取 **$1.00 → $0.25（-75%）**，输入输出维持 $10/$50。官方测算：典型负载成本降约 **25%**，**高度 agentic 的负载最高降 45%**
- Terminal-Bench-Science 0.1 **52.6%**（Fable 5 为 24.7%）
- 🟡 **三个破坏性变更（单一来源，待官方 migration 文档核实）**：`tool_choice` 设为 `any` 或 `tool` 会返回 **400**；thinking blocks 与模型绑定，路由降级到旧模型会丢失推理；编辑早期轮次会使 thinking blocks 失效并报错（2026-08-31 及以后创建的账号强制执行）

**来源**：[Anthropic 公告链接（经二手引用）](https://www.anthropic.com/claude-fable-and-mythos-5-1) · [中国经济新闻网](https://www.cet.com.cn/pd2026/xfpd/10535740.shtml) · [AIBase](https://www.aibase.com/news/30767) · 🟡 [worldprogramming（破坏性变更唯一来源）](https://www.worldprogramming.org/posts/anthropic-releases-claude-fable-51-and-claude-mythos-51-526-on-terminal-bench-science-and-75-cheaper-cache-reads-carngd)

### 5. 讯飞星火 X2.5-4B / 1.7B 开源：端侧首个原生 100 万 token 上下文 🟢

- 9-01 发布，协议 **Apache 2.0**（商用友好）
- 端侧模型中首个原生支持最长 **100 万 token** 上下文；约 **20 万亿 token** 预训练，**全国产算力平台全流程训练**
- 🟡 架构细节：采用混合注意力（一层全量注意力搭配三层滑动窗口注意力），用以削减长上下文的计算开销 —— 此配比仅见于超算互联网模型页，待官方技术报告核实
- 部署：支持 NVIDIA / 华为 / 海光 / 后摩等硬件，兼容 vLLM、SGLang、llama.cpp、MLX，可用 Ollama / LM Studio 一键跑，**并支持 LLaMA-Factory 增量训练**
- 实测：Domux 智能家居测试集端到端执行正确率 **90.3%**，平均响应 **0.85 秒**

**来源**：[人民网安徽（9-01）](https://ah.people.com.cn/BIG5/n2/2026/0901/c227767-41683644.html) · [Hugging Face 权重](https://huggingface.co/collections/XHToken/spark-x25) · [GitHub](https://github.com/XHToken/Spark-X2.5) · [讯飞星辰 MaaS](https://maas.xfyun.cn/modelSquare) · 🟡 [超算互联网模型页](https://www.scnet.cn/ui/aihub/models?keyword=Spark-X2.5)

### 6. 行业面：资本继续向算力与开源生态两端收口 🟡

- 国家人工智能产业投资基金 **14 亿元**入局快手可灵 AI，投后估值约 **1228 亿元**（🟡 每经转述）
- 字节跳动获 **296 亿美元**贷款，为 2026 年亚洲第二大美元贷款；考虑将 2026 资本支出提升至最高 **700 亿美元**（🟡 知情人士 / 第一财经）
- 9-03 ChatGPT、Claude、Grok **近同时宕机**，暂无证据表明三者同因（🟡 The Verge 转述）

**来源**：[投资界 24h](https://m.pedaily.cn/news/568523) · [每日经济新闻转述](https://view.inews.qq.com/a/20260903A0B05300) · 🟡 [AIdapted 日报（宕机）](https://www.aidapted.ro/en/articles/ai-news-september-4-2026-nvidia-astra-anthropic)

---

## 三、为什么值得记

1. **计价单位真的换了，而且是厂商自己承认的。** OpenAI 这次把"每任务 API 成本"直接印进官方对比表（BenchCAD 比 Sol 便宜 43%、比 Fable 5.1 便宜 86%），等于官方承认：**单价表已经不能反映真实成本**。以后选型问的问题不是"每百万多少钱"，而是"我这类任务，一次多少钱"。这是 9-02 那篇"完成任务多少钱"判断的官方盖章版。

2. **"便宜"分裂成了方向相反的两条路。** Astra 是"贵单价 + 少步数"——一次跑完，省的是步数和重放；Gemini 3.8 Flash 是"平单价 + 多步数"——官方自己预警 token 用量会涨。两条路都叫降本，但对不同任务形态结论完全相反：**长任务、多步骤、上下文重的选前者；短平快、批量的选后者**。只看单价表会选错。

3. **开源的"免费"建立在分发中立之上，而这个前提被买走了。** 绝大多数微调工作流是 `LLaMA-Factory → Hugging Face 权重 → vLLM 部署`，HF 是这条链上的默认单点。黄仁勋的四条承诺写得很清楚、也很有约束力——但**承诺不是架构**。对国内开发者还有一层现实：本机直连 `huggingface.co` 本就不通，一直靠 `hf-mirror`；现在"镜像"从加速手段变成了**必需的容灾备份**。

4. **1M 上下文下放到端侧，RAG 的 chunking 第一次有了替代答案。** 星火 X2.5-4B 原生 1M + Apache 2.0 + 支持 LLaMA-Factory，意味着"整本手册直接塞进去"在特定场景可能比"切块 + 检索 + 重排"更省事。但要警惕：**塞得进去 ≠ 检索得准**。长上下文 needle 类测试（如 MRCR v2）必须自己跑，Astra 在 512K–1M 区间的 8-needle 得分也只有 96.3%，不是 100%。

---

## 四、可行动

- [ ] **把成本度量改成"每成功任务成本"**：挑 10 条自己的真实任务，记录 token 总耗、步数、完成率，算出"成功一次花多少钱"，别再看单价表选型。
- [ ] **给 Gemini 3.8 Flash 设 token 预算上限**：`thinking_level` 默认 medium，官方明确说会用更多 token；上生产前在 low/medium/high 三档各跑 20 条，测出实际 token 放大倍数再定档。
- [ ] **备份 Hugging Face 依赖**：把当前在用的模型权重与数据集在本地或魔乐社区留一份镜像，并书面记录 `HF_ENDPOINT` 切到 `hf-mirror` 的完整流程（本机直连 HF 不通，这条已经是硬需求）。
- [ ] **跑一次 1M 上下文对照实验**：用自己最长的真实文档（产品手册 / 会议材料），对比"整本塞入 X2.5-4B" vs "切块检索"的答案质量与耗时，验证能不能砍掉现有 RAG 链路的 chunking 环节。
- [ ] **检查 Fable 5.1 的三个破坏性变更（🟡 待官方核实）**：若 Agent 用到 `tool_choice: any`，或有路由降级到旧模型的逻辑，先改掉再升级。

---

## 五、术语卡

| 术语 | 一句话解释 |
| --- | --- |
| **每任务成本（Cost per Task）** | 完成一个任务所消耗的总 API 费用 = 单价 × 步数 × 上下文重放量。OpenAI 在 Astra 发布材料中直接用它做跨模型对比，取代单价表。 |
| **准备框架（Preparedness Framework）** | OpenAI 用于分级评估前沿模型危险能力的内部框架。网络安全"Critical"为最高等级，会触发额外部署限制与分阶段开放。 |
| **Daybreak** | OpenAI 面向网络安全防御方的定向访问计划。Astra 最激进的安全能力不公开发放，经 Daybreak 逐步向审核过的组织开放。 |
| **Fairwind Program** | Google 面向政府、关键基础设施运营方与软件维护者的定向开放计划。Gemini 3.8 Flash Cyber 仅通过它申请使用，无公开价格。 |
| **混合注意力（Hybrid Attention）** | 全注意力层与滑动窗口注意力层按比例交替的架构，在保留长程建模能力的同时压低长上下文的计算开销。星火 X2.5 采用此架构（具体配比 🟡 待核实）。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
