# Proof of concept: Slidev + asciinema-player on GitHub Pages

Type: task
Status: resolved
Blocked by: 01

## Question

Does a minimal Slidev deck in `slides/` embedding `terminal-recordings/what-are-agent-skills.cast` via `AsciinemaPlayer.vue` and deployed via `.github/workflows/deploy-slides.yml` to `https://domesticmouse.github.io/skills-three-ways/` work cleanly and meet the bar as the presentation stack for "Skills Three Ways"?

## Answer

Yes. The minimal Slidev deck was implemented in `slides/` with Vue 3 component `AsciinemaPlayer.vue`, Vite SSR exclusion in `slides/vite.config.ts`, and cast assets hosted in `slides/public/casts/`. GitHub Pages was enabled via the API with `workflow` build type, and `.github/workflows/deploy-slides.yml` built and deployed the live deck to `https://domesticmouse.github.io/skills-three-ways/` with HTTP 200 responses for both the presentation and `/casts/what-are-agent-skills.cast`. The stack cleanly validates Slidev + asciinema-player for the presentation.
