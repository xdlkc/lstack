# lstack

[English](./README.md) | 简体中文

面向工程研发与个人效率的 Agent Skills 技能栈，参考 [mattpocock/skills](https://github.com/mattpocock/skills) 的组织范式。

以小巧、可组合、Markdown 优先的方式组织技能，适用于 Antigravity、Claude Code、Codex、Gemini CLI、Cursor 以及其他兼容 Agent Skills 规范的运行环境。

## 安装方式

### 本地开发（软链接热更新与全局文档治理）

克隆本仓库后运行安装脚本，即可在各本地 Agent 运行环境中同步启用技能与全局文档/发版规范：

```bash
git clone https://github.com/xdlkc/lstack.git
cd lstack
./scripts/link-skills.sh
```

[`scripts/link-skills.sh`](./scripts/link-skills.sh) 会同时完成两部分配置：

1. **技能软链接热更新**：扫描 `skills/` 下的 `SKILL.md`（自动跳过 `deprecated/`、`misc/` 与 `node_modules/`），确认目标目录未指向仓库内部后，软链接到 `~/.gemini/config/skills`、`~/.claude/skills` 与 `~/.agents/skills`。
2. **全局文档与发版治理**：
   - 将 [`governance/`](./governance/plugin.json) 软链接至 `~/.gemini/config/plugins/lstack-docs-governance`（为 Antigravity 启用全局规则 [`governance/rules/AGENTS.md`](./governance/rules/AGENTS.md) 与确定性 `Stop` 钩子 [`governance/hooks/stop-docs-check.py`](./governance/hooks/stop-docs-check.py)）。
   - 将 `governance/rules/AGENTS.md` 软链接至 `~/.claude/rules/docs-discipline.md`（供 Claude Code 读取）。
   - 若本机存在 `~/.codex` 或 `~/.kl` 目录，自动向 `~/.codex/AGENTS.md` 与 `~/.kl/agent/AGENTS.md` 写入/更新托管规则块。

修改 `SKILL.md` 或规则文件后立即生效；新增、重命名、移动或下线技能后重新运行 `./scripts/link-skills.sh` 即可同步。

对于在独立 `HOME` 沙箱中运行的后台 Worker（如 Nexus 的 Git Worktree 执行环境），可用以下脚本将同一规则块注入目标仓库根目录的 `AGENTS.md`：

```bash
./scripts/inject-repo-rule.sh /path/to/repo
```

### 各运行环境安装

<details>
<summary><strong>通过 skills.sh 安装到任意 Agent</strong>（Cursor、Windsurf、OpenCode、Claude Code 等）</summary>

```bash
npx skills@latest add xdlkc/lstack
```

后续更新：

```bash
npx skills@latest update
```

</details>

<details>
<summary><strong>Claude Code</strong>（插件市场）</summary>

```bash
claude plugin marketplace add xdlkc/lstack
claude plugin install lstack@xdlkc
```

</details>

<details>
<summary><strong>Codex</strong>（插件市场）</summary>

```bash
codex plugin marketplace add xdlkc/lstack
codex plugin add lstack@xdlkc
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

```bash
gemini skills install https://github.com/xdlkc/lstack.git --path skills/engineering
gemini skills install https://github.com/xdlkc/lstack.git --path skills/productivity
```

</details>

<details>
<summary><strong>Antigravity</strong></summary>

在本地克隆仓库后执行 `./scripts/link-skills.sh`，即可将启用技能软链接至 `~/.gemini/config/skills`。

</details>

## 技能目录

技能按触发主体划分为两类：

- **User-invoked（用户显式触发）**：仅在用户明确调用（如 `/grill-me`）时激活，用于编排顶层工作流。需在 `SKILL.md` 中设置 `disable-model-invocation: true`，并在 `agents/openai.yaml` 中配置 `policy.allow_implicit_invocation: false`。用户触发型技能可调用模型触发型技能，但不得调用另一个用户触发型技能。
- **Model-invoked（模型自主 / 显式触发）**：既可由用户直接指定，也可由模型根据 `description` 中的 `Use when...` 条件自主触发，用于封装可复用的工程或思维规范。

### 工程类（Engineering）

| 技能 | 触发方式 | 说明 |
| --- | --- | --- |
| **[cut-release](./skills/engineering/cut-release/SKILL.md)** | `User-invoked` | 核对版本清单、推进 [`CHANGELOG.md`](./CHANGELOG.md) 封版并生成双语 GitHub Release Notes（`/cut-release`）。 |
| **[code-review](./skills/engineering/code-review/SKILL.md)** | `Model-invoked` | 双轴代码审查：独立检查代码规范（`AGENTS.md`、`CLAUDE.md`、结构清晰度）、文档/Changelog 同步性以及需求一致性，按严重级别输出问题。 |
| **[docs-sync](./skills/engineering/docs-sync/SKILL.md)** | `Model-invoked` | 在变更 CLI、端口、配置或架构时同步维护双语 `README.md` / `README.zh-CN.md` 与 `CHANGELOG.md`，并附带 [`verify_docs.py`](./skills/engineering/docs-sync/scripts/verify_docs.py) 校验脚本。 |
| **[tdd](./skills/engineering/tdd/SKILL.md)** | `Model-invoked` | 红-绿-重构测试驱动开发循环，围绕公开边界逐个垂直切片推进实现。 |

### 效率类（Productivity）

| 技能 | 触发方式 | 说明 |
| --- | --- | --- |
| **[grill-me](./skills/productivity/grill-me/SKILL.md)** | `User-invoked` | 顶层需求追问编排：调用 `grilling` 对方案展开穷尽式访谈，在所有决策分支确认前禁止修改代码。 |
| **[grilling](./skills/productivity/grilling/SKILL.md)** | `Model-invoked` | 可复用访谈原语：先查代码再提问，按依赖顺序逐个分支收口计划、设计与需求中的模糊点。 |

## 技能晋升生命周期

`skills/` 下的技能按成熟度分桶管理：

1. **`skills/in-progress/`**（[说明](./skills/in-progress/README.md)）— 处于高频迭代中的实验性 Beta 技能。`./scripts/link-skills.sh` 会将其链接到本地用于日常验证，但不写入顶层 `README.md` 与 `.claude-plugin/plugin.json`。
2. **`skills/engineering/` 与 `skills/productivity/`** — 已稳定的正式技能，纳入 [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json) 对外分发。每次晋升需同步更新顶层 README、对应分桶 README（[`skills/engineering/README.md`](./skills/engineering/README.md) 或 [`skills/productivity/README.md`](./skills/productivity/README.md)）以及 `.claude-plugin/plugin.json`。
3. **`skills/deprecated/`** — 退役技能目录（按需创建）。不会被本地脚本软链接，也从文档与插件清单中移除。

## 仓库结构

```text
.
├── .claude-plugin/
│   ├── marketplace.json        # 插件市场清单（xdlkc）
│   └── plugin.json             # 插件定义与正式技能列表（v0.2.0）
├── governance/                 # 全局规则与 Antigravity Stop 钩子插件包
│   ├── plugin.json             # Antigravity 原生插件清单
│   ├── hooks.json              # Stop 生命周期钩子配置
│   ├── hooks/
│   │   └── stop-docs-check.py  # 确定性双语漂移与断链拦截脚本
│   └── rules/
│       └── AGENTS.md           # 精简常驻文档与发版触发规则
├── scripts/
│   ├── link-skills.sh          # 本地技能软链接与全局治理规则安装脚本
│   └── inject-repo-rule.sh     # 向指定仓库 AGENTS.md 注入托管规则块
├── skills/
│   ├── engineering/            # 正式工程技能（cut-release, code-review, docs-sync, tdd）
│   ├── productivity/           # 正式效率技能（grill-me, grilling）
│   └── in-progress/            # 实验性技能（不纳入插件清单）
├── AGENTS.md                   # 仓库协作规范
├── CHANGELOG.md                # 版本变更记录（Keep a Changelog）
├── CLAUDE.md                   # 规范基准文档
├── README.md
└── README.zh-CN.md
```

## 许可证

MIT（见 [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json) 声明）。
