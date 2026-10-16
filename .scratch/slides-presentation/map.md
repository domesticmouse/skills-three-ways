## Destination

A complete technical architecture, presentation structure, and content specification for the "Skills Three Ways" slide deck by Brett Morgan, built with Slidev in `slides/`, integrating embedded asciinema recordings, and configured for deployment to GitHub Pages.

## Notes

- Domain: Technical presentation, Developer Relations, Agent Skills, embedded hardware reverse-engineering (Daisy Seed 2 DFM, LibDaisy, DaisySP, Gamma mini synth).
- Presenter: Brett Morgan, Developer Relations Engineer with Google Cloud.
- Framework: Slidev (Markdown + Vue 3 / Vite) located in `slides/`.
- Terminal sessions: Embedded via `asciinema-player` playing `.cast` files.
- Deployment: GitHub Actions building static output to GitHub Pages.
- Relevant skills: `asciinema`, `agent-skills`, `writing-for-agents`, `codebase-design`.
- Related repository context: https://github.com/domesticmouse/reverse-engineering-gamma

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->
- [Integrate asciinema-player with Slidev](issues/01-asciinema-slidev-integration.md): Package asciinema-player v3 as a custom Vue 3 component in `slides/components/` with client dynamic import (`onMounted`), Vite SSR exclusion (`noExternal`), `BASE_URL` resolution for GitHub Pages subpaths, and `ResizeObserver` container scaling.


## Not yet specified

- Visual theme and custom styling (styling Slidev with clean dark mode, monospace terminal accents, Google Cloud brand alignment).
- Reusable slide layout templates (split-pane terminal player + narrative bullet points).
- Live audio sample playback or audio wave preview for synth sounds during the presentation.
- Production custom domain configuration (if needed beyond `<user>.github.io/<repo>/`).

## Out of scope

- Direct implementation of embedded C++ firmware for the Gamma mini synth (belongs in `domesticmouse/reverse-engineering-gamma`).
- Creating physical hardware modifications for the Gamma mini synth.
