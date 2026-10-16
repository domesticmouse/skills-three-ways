---
name: agent-skills
description: Design, author, audit, and validate Agent Skills packages adhering to the agentskills.io standard and Antigravity customization guidelines. Use when creating a new skill, converting research or workflows into skills, writing SKILL.md frontmatter, structuring scripts and references, or validating skill directories.
compatibility: Requires Python 3.9+ (optional PyYAML for deep schema checks)
---

# Agent Skills

Procedural runbook for designing, authoring, packaging, and validating standardized Agent Skills.

## Workflows

Choose the matching workflow based on your objective:

1. [Scaffold a New Skill](#1-scaffold-a-new-skill)
2. [Author Frontmatter & Context Pointers](#2-author-frontmatter--context-pointers)
3. [Write Steps & Checkable Completion Criteria](#3-write-steps--checkable-completion-criteria)
4. [Structure Progressive Disclosure & Supporting Assets](#4-structure-progressive-disclosure--supporting-assets)
5. [Validate & Audit a Skill Package](#5-validate--audit-a-skill-package)
6. [Lock & Distribute Skills](#6-lock--distribute-skills)

---

### 1. Scaffold a New Skill

1. Choose a unique, lowercase, hyphenated identifier (`<skill-name>`).
   - Length: 1 to 64 characters.
   - Allowed characters: `^[a-z0-9]+(-[a-z0-9]+)*$` (no consecutive hyphens, no trailing/leading hyphens).
2. Choose the scope:
   - **Workspace scope** (recommended): `.agents/skills/<skill-name>/`
   - **Global user scope**: `~/.agents/skills/<skill-name>/` or `~/.gemini/config/skills/<skill-name>/`
3. Create the directory layout:
   ```bash
   mkdir -p .agents/skills/<skill-name>/{scripts,references,assets,agents}
   touch .agents/skills/<skill-name>/SKILL.md
   ```
4. *Completion Criterion*: Directory exists and contains a blank `SKILL.md`.

---

### 2. Author Frontmatter & Context Pointers

Every skill begins with YAML frontmatter bounded by `---`. Read [SPECIFICATION.md](SPECIFICATION.md) for full field rules.

```yaml
---
name: <skill-name>
description: >-
  <Front-load leading words>. Use when <trigger condition 1>, <trigger condition 2>,
  or <trigger condition 3>.
compatibility: Optional system requirements or CLI dependencies
---
```

#### Guidelines for Frontmatter:
- **`name`**: Must match the parent directory name exactly.
- **`description`**: This is the skill's **top-level context pointer**.
  - Front-load the leading word (e.g. `Design`, `Audit`, `Record`, `Deploy`).
  - Allocate one explicit trigger condition per distinct branch.
  - State third-person trigger cues: `Use when...`
  - Strip internal details that the markdown body already carries.
- **Invocation Decision**:
  - **Model-invoked** (default): Omit `disable-model-invocation`. The model autonomously triggers the skill when requests match the description.
  - **User-invoked**: Set `disable-model-invocation: true`. The description is stripped from the model catalog (0 context load) and callable only via manual slash command. Use for destructive or infrequent actions.
  - Consult [CONTEXT-ECONOMICS.md](CONTEXT-ECONOMICS.md) for details on context vs. cognitive load.

---

### 3. Write Steps & Checkable Completion Criteria

Author the markdown body of `SKILL.md` following the closing `---`:

1. **Title & Overview**: State what the skill equips the agent to do.
2. **Workflows List**: Numbered index of workflows with internal anchor links.
3. **Sequential Steps**: Linear, actionable runbook steps written directly for an agent.
4. **Enforce Checkable Completion Criteria**:
   - Every major step or workflow must end on an explicit, checkable condition.
   - Guard against **premature completion** (the agent rushing toward "done" before validating edge cases).
   - *Weak*: "Ensure the build succeeds."
   - *Strong*: "Execute `pnpm run build`; confirm the process exits with returncode 0 and `dist/index.js` is generated."
5. **Positive Prompting**:
   - Frame instructions positively around desired behaviors rather than negations.
   - Avoid: "Do not write console.log."
   - Target: "Route all debugging output through `logger.debug()`."
6. **Prune No-Ops**:
   - Delete sentences instructing the agent on general defaults ("Write clean code"). Every sentence must measurably alter behavior.

---

### 4. Structure Progressive Disclosure & Supporting Assets

Prevent context window bloat by strictly separating procedural steps from bulky references:

1. **In-File Steps**: Keep `SKILL.md` focused on the immediate actions and checks (< 5,000 tokens).
2. **Disclosed Reference**:
   - Move API docs, formal specifications, and large lookup tables into sibling files or `references/`.
   - Link them via relative markdown links (e.g. `[Specification](SPECIFICATION.md)`).
   - The agent reads them only when that specific branch executes.
3. **Deterministic Scripts**:
   - Encapsulate fragile, multi-line shell logic or complex parsing into standalone scripts under `scripts/`.
   - Mark scripts executable: `chmod +x scripts/*.sh scripts/*.py`.
   - Instruct the agent to invoke the script rather than generating complex commands from memory.
4. **Interface Declaration**:
   - Add `agents/openai.yaml` to declare display metadata:
     ```yaml
     interface:
       display_name: "<Display Name>"
       short_description: "<One-line human description>"
     ```

---

### 5. Validate & Audit a Skill Package

1. Run the included validation script against the skill directory:
   ```bash
   ./scripts/validate-skill.py .agents/skills/<skill-name>
   ```
2. Inspect the diagnostic output:
   - Verify directory name matches frontmatter `name`.
   - Verify `description` is between 10 and 1024 characters and includes trigger cues.
   - Verify all scripts in `scripts/` are marked executable.
   - Verify presence of checkable completion criteria.
3. *Completion Criterion*: The validator exits with returncode 0 and prints:
   `PASSED: Skill structure, frontmatter, and naming are compliant with specification.`

---

### 6. Lock & Distribute Skills

To ensure reproducible environments across machines and CI/CD:

1. Commit the skill directory into version control:
   ```bash
   git add .agents/skills/<skill-name>
   git commit -m "feat(skills): add <skill-name> skill"
   ```
2. When managing community or external skills, record dependencies in `skills-lock.json` using the skills package manager:
   ```bash
   npx skills add <github-user>/<repo>
   ```
3. Verify cryptographic SHA-256 integrity in `skills-lock.json`. Consult [FRAMEWORK-TAXONOMY.md](FRAMEWORK-TAXONOMY.md) for ecosystem interoperability.
