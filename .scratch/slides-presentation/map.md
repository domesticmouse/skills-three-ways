# Skills Three Ways Presentation Architecture

## Destination

A complete technical architecture, presentation structure, and content specification for the "Skills Three Ways" slide deck by Brett Morgan, built with Slidev in `slides/`, integrating embedded asciinema recordings, and configured for deployment to GitHub Pages.

## Notes

- Domain: Technical presentation, Developer Relations, Agent Skills, embedded hardware reverse-engineering (Daisy Seed 2 DFM, LibDaisy, DaisySP, Gamma mini synth).
- Presenter: Brett Morgan, Developer Relations Engineer with Google Cloud.
- Framework: Slidev (Markdown + Vue 3 / Vite) located in `slides/`.
- Terminal sessions: Embedded via `asciinema-player` playing `.cast` files.
- Deployment: GitHub Actions building static output to GitHub Pages.
- PoC Override ("Plan, don't do"): Ticket 02 executes and deploys a minimal live proof-of-concept Slidev deck (embedding `terminal-recordings/what-are-agent-skills.cast`) to GitHub Pages so the stack can be validated before planning the full slide deck.
- Relevant skills: `asciinema`, `agent-skills`, `writing-for-agents`, `codebase-design`.
- Related repository context: https://github.com/domesticmouse/reverse-engineering-gamma

## Decisions so far

- [Integrate asciinema-player with Slidev](issues/01-asciinema-slidev-integration.md): Package asciinema-player v3 as a custom Vue 3 component in `slides/components/` with client dynamic import (`onMounted`), Vite SSR exclusion (`noExternal`), `BASE_URL` resolution for GitHub Pages subpaths, and `ResizeObserver` container scaling.
- [Proof of concept: Slidev + asciinema-player on GitHub Pages](issues/02-slidev-setup-and-github-pages.md): Deploy minimal Slidev deck with `AsciinemaPlayer.vue`, Vite SSR exclusion, and GitHub Actions `deploy-slides.yml` to `https://domesticmouse.github.io/skills-three-ways/`, cleanly validating the presentation stack.
- [Presentation narrative arc and slide-by-slide structure](issues/03-presentation-narrative-and-slide-breakdown.md): Structure as an 80-slide (30s/slide, 35–40 min) deck across 7 Acts built around the three skill buckets (`libdaisy-guide`/`daisysp-guide` Library Review Skills, `gamma-firmware-flash`/`gamma-firmware-restore` DFU Operational Skills, `gamma-pinout`/`gamma-hardware-controls` Hardware Discovery Skills) plus the `gamma-usb-connectivity` Mashup Skill, using 2-slide click-to-play 85–90% viewport `asciinema` beats, multi-slide skill zoom-ins, and a live physical Gamma mini synth demo in Act 7.

## Not yet specified

- Production custom domain configuration (if needed beyond `<user>.github.io/<repo>/`).

## Out of scope

- Direct implementation of embedded C++ firmware for the Gamma mini synth (belongs in `domesticmouse/reverse-engineering-gamma`).
- Creating physical hardware modifications for the Gamma mini synth.
- Embedded browser audio sample playback (superseded by live physical Gamma mini synth hardware demonstration on stage in Act 7).
