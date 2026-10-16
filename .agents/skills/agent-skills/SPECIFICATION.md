# Agent Skills Open Specification Reference

Formal reference for the Agent Skills open standard (`agentskills.io/specification`), governing packaging, frontmatter schema, naming constraints, and lifecycle discovery.

---

## 1. Directory Structure

A compliant Agent Skill is packaged as an isolated directory whose folder name matches the skill's `name` property:

```text
<skill-name>/
├── SKILL.md              # Mandatory: YAML frontmatter + procedural runbook
├── scripts/              # Optional: Deterministic executable scripts (Bash, Python, etc.)
│   ├── run.sh
│   └── test.py
├── references/           # Optional: Heavy on-demand reference material (APIs, schemas)
│   ├── SPEC.md
│   └── schema.json
└── assets/               # Optional: Static seed files, boilerplate, or scaffolding fixtures
    └── template.yaml
```

---

## 2. YAML Frontmatter Specification

The `SKILL.md` file must begin with YAML frontmatter enclosed between `---` delimiters.

```yaml
---
name: database-migration
description: >-
  Executes relational schema migrations, generates rollback scripts, and
  validates data integrity constraints against PostgreSQL databases.
license: Apache-2.0
compatibility: Requires psql, pg_dump, and Python 3.11+
metadata:
  author: enterprise-data-team
  version: "2.1.0"
allowed-tools: Bash(psql:*) Read Edit
disable-model-invocation: false
---
```

### Field Definitions & Constraints

| Field | Type | Required | Max Length | Description & Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `name` | String | **Yes** | 64 chars | Lowercase alphanumeric (`a-z`, `0-9`) and hyphens (`-`). Cannot start or end with a hyphen; no consecutive hyphens (`--`). **Must match the parent directory name exactly**. |
| `description` | String | **Yes** | 1024 chars | Non-empty description. Functions as the **top-level context pointer**. Must state what the skill does and list the explicit trigger conditions when the agent should activate it. |
| `license` | String | No | - | SPDX license identifier (e.g., `MIT`, `Apache-2.0`) or reference to bundled license file. |
| `compatibility` | String | No | 500 chars | Operating system, external binary, runtime, or network prerequisites (e.g. `Requires Docker 24+, jq, Python 3.11+`). |
| `metadata` | Map | No | - | Key-value pairs for arbitrary author, version, or team metadata. |
| `allowed-tools` | String | No | - | Space-separated list of approved tool calls (e.g. `Bash(psql:*) Read Edit`) to reduce interactive execution prompts. |
| `disable-model-invocation` | Boolean | No | - | When `true`, hides the skill description from the model's catalog. Makes the skill strictly **user-invoked** (slash command only). |

---

## 3. Markdown Instruction Body Standards

The body following frontmatter contains procedural runbooks written for an AI agent:
1. **Linear Workflows**: Numbered, deterministic actions the agent follows sequentially.
2. **Checkable Completion Criteria**: Precise observable conditions (commands, outputs, exit codes) proving step completion before advancing.
3. **Execution Scripts**: Offload complex multi-command sequences into `scripts/` rather than prompting the model to generate fragile inline bash strings.
4. **Relative Links**: Link internal reference docs and scripts using relative file paths (e.g. `[verify.sh](./scripts/verify.sh)`).

---

## 4. Scope & Discovery Priority

Agent runtimes scan hierarchically at startup:

1. **Workspace Scope** (Highest Priority):
   - `.agents/skills/<skill-name>/SKILL.md` (Universal standard)
   - `.claude/skills/<skill-name>/SKILL.md` (Claude-specific)
2. **Global / User Scope**:
   - `~/.agents/skills/<skill-name>/SKILL.md`
   - `~/.gemini/config/skills/<skill-name>/SKILL.md`
3. **Built-in Scope** (Lowest Priority):
   - Application-bundled skills mounted by name.

*Precedence Rule*: A skill in a higher-priority scope with an identical `name` completely shadows any skill with that name in lower scopes.
