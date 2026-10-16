# Modular Act-by-Act Slidev Multi-File Structure

Type: task
Status: resolved
Blocked by: none

## Question

How should the monolithic `slides/slides.md` deck be decomposed into modular files to simplify editing and content maintenance while preserving Slidev hot-module reloading and build reproducibility?

## Answer

Leverage Slidev's native `src:` frontmatter imports to split the presentation into 7 Act-level markdown files under `slides/acts/`, retaining `slides/slides.md` as the master manifest:

- `slides/acts/01-primer.md`: Slides 1–11 (S01–S11)
- `slides/acts/02-the-hook.md`: Slides 12–20 (S12–S20)
- `slides/acts/03-way-1-library-review.md`: Slides 21–34 (S21–S34)
- `slides/acts/04-way-2-dfu-operational.md`: Slides 35–46 (S35–S46)
- `slides/acts/05-way-3-hardware-discovery.md`: Slides 47–62 (S47–S62)
- `slides/acts/06-experiment-and-conclusion.md`: Slides 63–72 (S71–S80)

The master `slides/slides.md` maintains global presentation metadata (theme, background, highlighter, info, transitions) with `hide: true` on the headmatter block to prevent empty slide insertion or frontmatter pollution, followed by clean `src: ./acts/NN-*.md` imports. Slidev parser verification confirms all 80 slide tags, frontmatters, notes, and titles match 100%, and `npm run build` compiles with zero warnings or errors.
