# Agent Skills

**Agent Skills** are an open specification and architectural pattern for packaging modular workflows, domain knowledge, and executable instructions for AI agents.

Rather than overloading an agent's context window with every possible guideline or procedure upfront, Agent Skills function as on-demand **runbooks** or **playbooks** that an agent reads only when needed.

---

## 1. Directory Structure

A skill is encapsulated within its own directory and follows a standardized layout:

```text
skills/<skill-name>/
├── SKILL.md          # Required: YAML frontmatter + procedural instructions
├── scripts/          # Optional: Helper scripts and executable utilities
├── references/       # Optional: In-depth documentation, manuals, or API specs
└── resources/        # Optional: Templates, sample files, or assets
```

---

## 2. Anatomy of a `SKILL.md`

The core file is `SKILL.md`, composed of two parts:

### A. YAML Frontmatter (Metadata & Discovery)

```yaml
---
name: code-reviewer
description: >-
  Reviews code changes for bugs, security vulnerabilities, and style violations.
  Use when reviewing pull requests or checking code quality.
---
```

* **`name`** (required): A unique, lowercase, hyphenated identifier matching the skill's folder name (e.g., `code-reviewer`).
* **`description`** (required): The primary activation trigger. Agents semantically match user prompts against this description to decide whether to activate the skill.
* **`license`** (optional): License identifier or reference to a bundled license file (e.g., `Apache-2.0`).
* **`compatibility`** (optional): Environmental or runtime requirements (e.g., `Requires python3`).
* **`allowed-tools`** (optional): Specific tools pre-approved for use by this skill without prompting.

### B. Markdown Body (Procedural Instructions)

The Markdown body contains structured, step-by-step guidance on how the agent should carry out the task:
* **Explicit Workflows:** Numbered step-by-step instructions and runbooks.
* **Negative Constraints:** Explicit rules stating what the agent *should not* do (e.g., "Do not modify production databases directly").
* **Validation Steps:** Instructions on how the agent can verify success (e.g., running verification commands or checking log output).
* **Relative Links:** Pointers to bundled helper scripts in `scripts/` or documentation in `references/`.

---

## 3. The 3-Tier Progressive Disclosure Model

Agent Skills optimize token consumption and prevent context exhaustion using **progressive disclosure**:

1. **Discovery (Low Context ~100 tokens/skill):**
   At startup, the agent loads *only* the `name` and `description` of all available skills into its prompt.
2. **Activation (On-Demand):**
   When a user task matches a skill's description, the agent dynamically reads the full `SKILL.md` file into context.
3. **Execution (Deep Context):**
   If the workflow requires specialized knowledge or scripts, the agent drills down to read secondary files in `references/` or executes tools in `scripts/`.

---

## 4. How Skills Compare to Other Agent Concepts

| Concept | Purpose | When Active |
| :--- | :--- | :--- |
| **Tools / MCP** | Raw capabilities (e.g., read file, run shell command, call an API) | Always available |
| **Rules / Guidelines** | Global behavioral constraints, coding styles, or directory policies | Always on or path-scoped |
| **Agent Skills** | Higher-level workflows and runbooks explaining *how* to combine tools to accomplish domain-specific tasks | Activated on-demand |
