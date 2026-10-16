# AGENTS.md

## Slide deck conventions

### Slide Headings
- Do **NOT** use badges, pills, or tags (e.g., `<span class="...rounded...">` or `badge-*` classes) in slide titles or headers. Keep slide headings clean:
  ```html
  <div class="flex items-center gap-3 mb-6">
    <h2 class="text-2xl font-bold m-0">Title</h2>
  </div>
  ```

### Comparison & Concept Lists
- Prefer clean, numbered lists over multi-card grids for high-density conceptual comparisons:
  ```html
  <ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
    <li>
      <strong class="text-white">Topic / Feature Title</strong>
      <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
        <li>Primary high-signal takeaway or mechanism</li>
        <li>Secondary context or contrast</li>
      </ul>
    </li>
  </ol>
  ```

### Speaker Notes
- Every slide must include conversational presenter notes in an HTML comment (`<!-- ... -->`) explaining the narrative flow and talking points behind each bullet.

## Agent skills

### Issue tracker

Local markdown files in `.scratch/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical roles mapped 1:1 (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context (`GLOSSARY.md` + `docs/adr/` at repo root). See `docs/agents/domain.md`.
