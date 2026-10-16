# Framework Taxonomy: Agent Skills Across Frameworks

Comparison of skill implementations across major modern agent runtimes.

---

## 1. Comparative Matrix

| Feature / Dimension | Anthropic Claude Code & Open Standard (`agentskills.io`) | Google Antigravity (AGY) | Microsoft Semantic Kernel | OpenAI ChatGPT / Codex Skills | LangChain / AutoGen Tools |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary File Format** | `SKILL.md` (YAML frontmatter + Markdown) | `SKILL.md` in `.agents/skills/` or `skills.json` | C#/Python classes or `skprompt.txt` + `config.json` | YAML / Markdown runbooks | Python classes (`BaseTool` / function decorators) |
| **Encapsulation Concept** | Directory package (`scripts/`, `references/`) | Modular package with scripts, references, rules | Plugins (formerly Skills) containing Native & Semantic functions | Skill runbooks + API schemas | Toolkits and Agent Executors |
| **Discovery Mechanism** | Filesystem walk (`.agents/skills`, `.claude/skills`) | Hierarchical CWD traversal + JSON declarations | Explicit registration in `KernelPluginCollection` | Workspace settings & platform directory | Programmatic binding in agent initialization code |
| **Loading Strategy** | 3-tier progressive disclosure (Catalog -> Body -> Assets) | Progressive disclosure; metadata in context; on-demand load | Eager function schema injection into LLM system prompt | Eager or on-demand catalog matching | Eager JSON schema injection into tool definitions |
| **Execution Engine** | Native agent file-read + shell tool execution | Dedicated activation tool or native file tools | Kernel invocation loop via function calling | Model function calling & sandboxed python | Python interpreter runtime |
| **Locking & Distribution** | `skills-lock.json` via `npx skills` (Vercel Labs) | Workspace project VCS + `skills.json` | NuGet, PyPI, or internal enterprise package registries | Platform Store / Workspace Enterprise Config | Python package manager (`pip`, `uv`, `poetry`) |
| **Distinction from Tools** | Skills *orchestrate* tools and provide SOPs | Skills distinct from MCP servers, rules, and hooks | Plugins *group* tools and prompts together | Skills provide workflow; Actions connect APIs | Tools *are* the primitives; no native "skill" abstraction |

---

## 2. Skills vs. Model Context Protocol (MCP)

A common point of confusion is how Skills relate to MCP servers:

- **MCP is the Muscle and Senses**: MCP exposes APIs, terminal sessions, database connectors, and browser windows as standard JSON-RPC tools and resources. It provides primitive capabilities.
- **Skills are the Playbook and Brain**: Skills provide procedural standard operating procedures (SOPs). They tell the agent *which* tools to call, in *what sequence*, under *what preconditions*, and against *what checkable completion criteria*.

Skills and MCP are complementary: a `SKILL.md` runbook can invoke MCP tools or specify pre-approved access via `allowed-tools: Bash Read`.
