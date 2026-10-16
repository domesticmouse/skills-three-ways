# Context Economics & Cognitive Design for Agent Skills

How Agent Skills manage context windows, prevent cognitive overload, and eliminate agent failure modes.

---

## 1. The Three-Tier Progressive Disclosure Model

Loading dozens of complete runbooks into an agent's initial prompt triggers attention dilution, instruction drift, and runaway token costs. Skills resolve this by dividing content across three disclosure tiers:

| Tier | Payload | Timing | Token Footprint | Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Catalog** | `name` & `description` | Session boot / initialization | ~50–100 tokens per skill | Injected into system prompt or activation tool schema |
| **Tier 2: Instructions** | `SKILL.md` body | On skill activation (matching request) | < 5,000 tokens | File-read or `activate_skill` tool call |
| **Tier 3: Resources** | Files in `references/`, `scripts/` | On-demand during step execution | Variable (only what is executed or read) | Agent calls file tools on relative links |

---

## 2. Context Pointers

A **context pointer** is a reference held in the agent's working memory that names out-of-context material and encodes the exact condition for reaching it.

- In a skill, the frontmatter `description` is the primary top-level context pointer.
- Inside `SKILL.md`, a relative markdown link to a file in `references/` is a secondary pointer.

### Three Rules of Pointer Writing:
1. **Front-load the leading trigger word**: Place the high-signal verbs or operational nouns at the front of the description.
2. **One trigger per distinct branch**: Allocate one explicit trigger condition per functional branch. Avoid redundant synonyms.
3. **Strip identity the body carries**: Do not waste pointer tokens explaining internal implementation details that the agent will read upon loading the body.

---

## 3. Balancing the Two Loads

Every instruction system spends one of two budgets:
- **Context Load**: The token and attention cost on the LLM's active working memory *on every single turn* (e.g. system prompt rules, always-loaded catalogs).
- **Cognitive Load**: The memory and indexing cost on the *human operator*, who must remember that a tool exists and know when to reach for it.

### Invocation Strategy:
- **Model-Invoked** (default): Pays modest context load (~80 tokens for the catalog description) to give the agent autonomous discovery capability.
- **User-Invoked** (`disable-model-invocation: true`): Pays zero context load. Hides the skill completely from the agent until the user explicitly triggers its slash command (e.g., `/deploy`). Best for dangerous, infrequent, or human-decided actions.
- **Router Skill**: A single user-invoked skill that acts as an interactive index recommending which specialized user-invoked skill to run next.

---

## 4. Defending Against Premature Completion

The most pervasive agent failure mode is **premature completion**: halting execution before verifying edge cases or running tests because the visible steps ahead exert a psychological pull to rush toward "done."

### Defenses:
1. **Sharpen the Bound First**: Replace fuzzy criteria (*"ensure tests pass"*) with checkable, observable assertions (*"execute `npm test`; verify exit code 0 and 0 failing suites in test summary"*).
2. **High Legwork**: Require exhaustive proof (*"inspect every exported interface in `src/index.ts` and confirm each has a corresponding test file in `tests/`"*).
3. **Context Boundary**: If premature completion persists despite sharp criteria, split steps across a subagent delegation boundary so the later steps are hidden from view until the current phase passes.

---

## 5. Authoring Levers: Leading Words, Negation, and Pruning

- **Leading Words**: Use dense, pre-trained terminology (`tight`, `red`, `tracer bullet`, `rollback`) rather than inventing custom jargon. Pretrained words recruit existing latent representations for zero token cost.
- **Avoid Negation**: Steering an agent by prohibition (*"Do not write console.log"*) drags the banned concept into active attention. Prompt the positive target behavior (*"Route all logging exclusively through the structured `logger.info()` interface"*).
- **Hunt No-Ops**: If an agent obeys an instruction by default (*"Write clean code"*), it is a no-op that wastes tokens. Delete it.
- **Environment as Cache**: Never duplicate information already present in `package.json`, `--help`, or directory structures. Instruct the agent to inspect the environment dynamically.
