# 2026-10-23｜找到已经免费，修补没有：PHP2Shell 卡住的那六道闸门

> AI 两个月内挖出 PHP 两个 9.2 分 RCE，而同一个缺陷的修复在人类手里停了近两年。

**标签**：`#AI安全` `#开源治理` `#漏洞响应` `#PHP2Shell`
**生成时间**：2026-10-23 12:19（北京时间）

---

## 一、今日观察

一个严重漏洞从「存在于代码里」到「真正从世界上消失」，中间要过六道闸门。今天 PHP2Shell 把这条链路完整地暴露了出来——而 AI 只加速了最上面两道。

| 闸门 | PHP2Shell 的实际情况 | AI 让它变快了吗 |
|---|---|---|
| ① 看见异常 | **2024 年**外部审计中，核心开发者已发现 OOM 处理异常 | — 人先看见的，且没下文 |
| ② 证明能走到 RCE | 2024 只 theorize 无路径；**2026-08-11** Calif 的 Ryan A 交出无条件 RCE | ✅ 这是真正的增量 |
| ③ 决定怎么修 | 多个方案各有代价（破坏兼容 / 引入新 DoS / 要动大量第三方扩展），共识决策下**停滞近两年**，基金会自称 structural failure | ❌ AI 不参与这个决策 |
| ④ 跨四个分支发版 | 08-11 定为最高优先级 → **10-21** 发布 8.5.12 / 8.4.27 / 8.3.36 / 8.2.35 | ❌ 约两个月 |
| ⑤ 全球部署 | 10-21 起；Cloudflare 记录到的尝试在数小时内从数千涨到百万级 | ❌ 反而更挤 |
| ⑥ 老版本与内嵌的 PHP | 只有 7.4–8.1 的**最小源码回移补丁**；设备与老系统里捆绑的 PHP 无人负责 | ❌ 无人认领 |

时间全花在下半张表，而 AI 的战果全在上半张表。更麻烦的是：**上半张表变快，会让下半张表更堵**。PHP 安全团队自 7 月 1 日以来发布了 15 个 CVE，同时处理了 **100 多份**被判为无效、重复或不可复现的报告——发现能力涨价，审核产能没涨。

最锋利的一刀来自 PHP 基金会自己的叙述：他们今年**早就用 Alpha-Omega 联合 Anthropic 的 Claude Mythos 扫过 PHP**。没扫出这个洞。真正打开局面的是有人给出了能走到 RCE 的路径。也就是说，稀缺的不是「读代码的能力」，而是**「证明这条路走得通」+「有权改写引擎的人」**。

---

## 二、事实清单

> 信源等级：🟢 官方/权威媒体　🟡 二手转述，待核实

### 1. 🟢 PHP 发布四个紧急版本，两个未授权 RCE 位于「每个请求都会经过」的地方

- **CVE-2026-109618**（OOM 内存破坏）：请求恰好在 PHP 内部数据未初始化完成时触发 `memory_limit`，把半成品状态当有效数据用。Apache + mod_php 下**在应用代码执行之前**即可触发，默认设置下已验证完整 RCE。
- **CVE-2026-109619**（陈旧全局状态）：致命错误留下指向已释放内存的全局状态，同一 worker 处理下一个请求时 use-after-free；mod_php 与 FPM 均已验证 RCE。
- 两者 **CVSS v4.0 均为 9.2**；受影响范围 `< 8.2.35 / < 8.3.36 / < 8.4.27 / < 8.5.12`。
- 官方措辞很硬：**升级是唯一完整缓解**。能临时做的只有 `memory_limit=-1`（618）、`session.upload_progress.enabled=0` 与 PHP 8.5 上的 `fatal_error_backtraces=0`（619），且**都不是完整缓解**，改完必须重启每一个 worker；**不要用 `RLIMIT_AS` / `RLIMIT_DATA`**，那会让 `mmap()` 失败、反而走进脆弱的 `longjmp()` 路径。
- 来源：[PHP Foundation 官方博客（10-21）](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/) ｜ [GHSA-w8hw-w9fx-j79w](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w) ｜ [GHSA-6wmf-4rv5-p3rp](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp) ｜ [php.net 发布公告](https://www.php.net/archive/2026.php#2026-10-21-5)

### 2. 🟢 两条独立路径、两套 AI 工具，指向同一个根因

- **Calif**（安全公司）于 **7 月 30 日**开始审计 PHP，**8 月 11 日**由研究者 Ryan A 报告了与 2024 年 OOM 问题同源的无条件 RCE；OpenAI 独立报告了同一根因，并于 **9 月 18 日**追加攻击路径；**Wiz 于 8 月 24 日**独立报告了相关问题。Trail of Bits 也在审计 PHP。
- OpenAI 口径：Calif 是在其 **Patch the Planet** 计划下**使用 GPT-5.6 Sol** 发现的；Wiz 独立发现并报告了**两个**漏洞（Wiz 的研究中用了自家的 Wiz Atlas、Gemini 4 Argon 与 GPT-5.6 Sol 组合，🟡 组合细节来自媒体转述）。
- OpenAI 提出 **Defender's Window**（防御者窗口）：前沿 AI 在攻击者之前发现漏洞，为维护者争取准备修复的时间。同时宣布 **10 亿美元**补贴性质的 Daybreak 访问（Daybreak for Frontline Defenders），并开源了 [php2shell-checker](https://github.com/openai/php2shell-checker)（一个 Codex skill，用于识别可能受影响的 PHP 版本）。
- OpenAI 自己也写了那一句：**「同样的能力也能帮助攻击者快速开发攻击工具与漏洞利用程序」**。
- 来源：[OpenAI 官方博客（10-21）](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/) ｜ [Patch the Planet](https://patchtheplanet.org/) ｜ PHP Foundation 上述公告

### 3. 🟢 「结构性失败」：这个洞在 2024 年就被看见过，然后停了两年

- 2024 年 PHP 接受了多年来第一次外部安全审计：由**德国主权技术局（Sovereign Tech Agency）资助**、经 **OSTIF** 组织、**Quarkslab** 执行。修复 Quarkslab 提交的问题时，一名基金会聘用的核心开发者发现了 CVE-2026-109618 背后 OOM 问题的**最初迹象**。
- 当时只做了理论推测，没找到具体可利用路径；而几个修复方案分别会破坏向后兼容、引入新的 DoS 风险，或要求大量第三方扩展同时改动。安全团队按**共识决策**运行，迟迟无法在几个高风险方案间拍板。
- 基金会原话：**「the delay was a structural failure, caused by both the security team's decision process and its lack of resources」**（延误是一次结构性失败，源于决策流程和资源不足两方面）。目前已在改成多数决。
- 来源：[PHP Foundation 官方博客](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/) ｜ [2024 审计结果](https://thephp.foundation/blog/2025/04/10/php-core-security-audit-results/)

### 4. 🟢 15 个 CVE 背后是 100 多份无效报告：AI 提高了发现，也提高了噪音

- PHP 安全团队自 **2026 年 7 月 1 日**以来发布了 **15 个 CVE**，同时处理了 **100 多份**最终被判为无效、重复或不可复现的报告。
- 基金会的表述值得抄下来：AI 帮助团队**验证**报告并把同源报告**归类**，但**「a person makes every call and works on every patch」**（每一个判断都由人做出，每一个补丁都由人来写）。
- 基金会在文末直接开口要钱：PHP 撑着政府服务、电商、银行与媒体网站，但安全仍依赖少数基金会雇工与少量志愿者；**「今天这样（懂整个 PHP 代码库的）工程师太少了」**。
- 来源：[PHP Foundation 官方博客](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/) ｜ [How the PHP Security Team Handles Your Reports（10-14）](https://thephp.foundation/blog/2026/10/14/how-the-php-security-team-handles-your-reports/)

### 5. 🟢 披露流程自己成了攻击面：最危险的两步都是防御方迈出的

按基金会公布的 UTC 时间线：

| 时间 | 事件 |
|---|---|
| **10-17** | AWS 威胁情报在 MadPot 蜜罐网捕获一次 PHP2Shell 利用尝试，**比补丁发布早 4 天**，来源为商业匿名网络的 IP；AWS 称无法确认对方如何提前获知 |
| 10-20 ~15:00 | 两个 CVE 编号在论坛与社媒流传，附带错误的发布时间与**错误的 CVSS 10.0** |
| 10-20 19:30 | PHP 提前发布预警，把发布从 10-22 14:00 UTC 提前到 **10-21 14:00 UTC**（发行版还没打包完，立刻发会让多数人无处可升） |
| 10-20 ~20:00 | **Calif 误发**了一段 PoC 演示视频，删除前已被转存，加速了各种 PoC 的开发 |
| 10-21 02:00 起 | AWS 观察到多批来自不同匿名基础设施的尝试，载荷各异，判断不止一个攻击者 |
| 10-21 **07:41** | **Chainguard 单方面打破 embargo**，提前 6 小时发布含修复的镜像——攻击者可以先逆向二进制，而其他用户还在等发布。其 CEO Dan Lorenc 称理由是漏洞已在野外被利用（🟡 其援引的报告未公开证据） |

- Cloudflare 在公开前默认给所有 WAF 用户（含免费档）部署了规则，并强调这只是 **stopgap**。CEO Matthew Prince 称公开前 10 小时内观测到数千次尝试，公开后 45 分钟内涨到数万、2 小时内数十万，此后进入**百万级**；攻击者还在根据被拦结果不断改载荷试图绕过（🟡 具体量级为 Cloudflare 高管口述）。
- AWS 建议：**排查要从至少 10 月 17 日开始**，而不是从披露日开始。
- 来源：[The Register（10-22）](https://www.theregister.com/cyber-crime/2026/10/22/hackers-pile-on-php2shell-as-aws-reveals-attacks-began-before-disclosure/) ｜ [Tenable FAQ](https://www.tenable.com/blog/php2shell-cve-2026-109618-cve-2026-109619-frequently-asked-questions-about-critical-php-remote) ｜ PHP Foundation 上述公告

### 6. 🟢 另一条路：不找漏洞，而是让代码够不着

- Anthropic Frontier Red Team 于 **10-20** 发布研究：用 Claude 对 **25 个**开源项目（**500 万+ 行**，含 C/C++/Java/PHP/Python）做攻击面削减，清点 **17,000+ 个**配置选项（其中 **3,842** 个与安全控制相关），共报出 **493** 个问题。
- 三类方法：默认配置下不必要的可达代码、早期可达性（跑在认证/协议状态转换之前的代码）、配置交互。后者发现 **162 个**既不报错也不警告、且无文档说明的组合，其中 **94 个**会**静默关闭**一个安全控制；有一个冲突配置在软件里存在了 **21 年**。
- OpenSSH 案例：10.4 中约 **4,500 行**实验性 ML-DSA-44 后量子签名代码可被未认证客户端在默认配置下触达，占 sshd 自身前认证代码的 **16%**；10.5 把检查前移但 Claude 又指出两个缺口，**10.6** 才最终修好，移除了默认构建中未认证客户端可触达代码的**约五分之一**。
- Anthropic 自己给的限定很实在：这些技术**不移除漏洞**，只是让它更难被够到；且**「任何会改变非默认配置的 gate 都被搁置，交由人类决定」**。该方法已做成可复用的 Claude skill（对代码库跑三遍），正集成进 OSS-Scanner。
- 来源：[Anthropic 官方研究（10-20）](https://www.anthropic.com/research/attack-surface-reduction)

---

## 三、为什么值得记

1. **「Defender's Window」的真实大小，不取决于谁先发现，取决于维护者有多少人。** OpenAI 造了个好听的词，但 PHP 基金会给的账是反过来的：一个 2024 年就被看见的缺陷，因为没人敢在几个高风险方案间拍板，躺了近两年。AI 把「发现」压缩到接近零，只是让这道闸门前的队伍排得更长——15 个 CVE 旁边躺着 100 多份无效报告。

2. **AI 安全的稀缺资源已经从「读代码」转移到「给出可利用路径」和「有权改写引擎的人」。** PHP 基金会今年就用 Claude Mythos 扫过一遍 PHP，没扫出这个洞；打开局面的是有人交出了一条能走到 RCE 的路。所以评估「用 AI 审代码」的效果时，该问的不是它读了多少行，而是**它有没有把路径走完，以及走完之后谁有权改**。

3. **「让代码够不着」和「把漏洞修掉」是两条成本完全不同的曲线，选型时该分开算。** 前者可以按部署裁剪、能自动化（Anthropic 那 493 个问题里，94 个只需要改配置组合）；后者必须改设计，只能靠懂引擎的人。PHP 这次的洞恰恰落在「几乎每个请求都经过的内存管理与错误处理」——**削不掉**。但它顺手给了个反例：`session.upload_progress` 这个很少用也很少被测的功能，官方建议**即使打了补丁也保持关闭**。能关掉的，就别留着。

4. **披露流程本身正在成为攻击面，而且最危险的两步都是防御方自己迈的。** 这次时间线上两个真正的加速点——CVE 编号提前泄露、Chainguard 提前 6 小时放出含修复的二进制——都不是攻击者干的。 embargo 假设「公开日 = 攻击起点」，而 AWS 的蜜罐数据是 10 月 17 日。**以后做应急响应，起点要从「最早可疑活动时间」倒推，而不是从公告日期。**

---

## 四、可行动

- [ ] **先盘 PHP 运行时版本，不是盘 WordPress/插件版本**：所有对外服务的 PHP 安装都在范围内（PHP-FPM、Apache mod_php、php-cgi、FrankenPHP、LiteSpeed）。目标是 8.2.35 / 8.3.36 / 8.4.27 / 8.5.12 或发行版提供的已验证 backport；托管环境直接找服务商要「运行版本 + 包构建号 + 打完补丁的时间」。
- [ ] **跑一遍 `php2shell-checker`**（[openai/php2shell-checker](https://github.com/openai/php2shell-checker)，Codex skill）做存量盘点，并按 [CISA BOD 26-04](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk) 的暴露度排序决定先补哪批。
- [ ] **暂时升不了的，按 CVE 分别做局部缓解并重启每一个 worker**：618 侧把 `memory_limit=-1` 以应用无法覆盖的方式设上；619 侧设 `session.upload_progress.enabled=0`，PHP 8.5 再加 `fatal_error_backtraces=0`。**不要**用 `RLIMIT_AS` / `RLIMIT_DATA`。注意这些都不是完整缓解，只是拖时间。
- [ ] **日志回溯从 10 月 17 日开始查**，重点看：multipart POST 里带 `PHP_SESSION_UPLOAD_PROGRESS` 的请求、PHP worker 起的异常子进程、web 目录里的新文件、请求开始前重复出现的 warning/deprecation。同时注意「日志里没错误 ≠ 安全」——619 的 INI 诊断路径在 PHP 决定是否记录之前就已经访问了陈旧状态，改 `error_reporting` 挡不住。
- [ ] **给自己维护的项目做一次三遍式攻击面削减**：默认配置下有没有不必暴露的代码 / 有没有跑在认证之前的复杂代码 / 有没有「组合起来静默关掉安全控制」的配置对。第三类最容易漏，也最容易修。

---

## 五、术语卡

| 术语 | 解释 |
|---|---|
| **Defender's Window（防御者窗口）** | OpenAI 提出的概念：前沿 AI 在攻击者之前发现漏洞，从而为维护者与安全厂商争取到在公开披露前准备修复与防护的时间窗口。本次 PHP2Shell 是它的首个大规模案例。 |
| **协调披露（Coordinated Disclosure）** | 发现方先把细节交给维护者，约定一个统一公开日，让补丁、发行版打包与防护规则同步就位，再公开细节。本次原定 10-22 14:00 UTC，因 CVE 编号泄露提前一天。 |
| **embargo / 打破 embargo** | 协调披露中约定的「公开前不得透露」期限。Chainguard 在 10-21 07:41 UTC 提前发布含修复的镜像，被 PHP 基金会指为单方面打破 embargo——因为二进制本身可以被逆向出漏洞位置。 |
| **攻击面削减（Attack Surface Reduction）** | 不逐个找漏洞，而是把「不该被够到」的代码挪到认证之后、显式 opt-in 之后或协议状态机更深处，从而降低**尚未被发现**的漏洞的严重性。 |
| **longjmp / OOM 路径** | PHP 历史上用 `longjmp()` 处理内存耗尽，直接从当前上下文跳出。若此时请求内存尚未初始化完成，就会留下无效状态供后续 shutdown 处理。本次补丁移除了 `longjmp()`，改为在 VM 安全点延迟触发软 OOM，或在达到更高阈值时用 `_exit()` 硬退出。 |
| **backport（源码回移补丁）** | 把针对新版本的修复移植回旧版本。PHP 只为自行编译 7.4–8.1 的用户提供**最小**回移补丁，8.1 及以下不再有官方常规修复，只能依赖发行版或 LTS 厂商。 |

---

<sub>由 WorkBuddy 自动生成 · 事实均附来源，🟡 项待核实</sub>
