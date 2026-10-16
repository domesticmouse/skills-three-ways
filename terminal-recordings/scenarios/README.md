# Terminal Recordings & Scenario Playbooks

This directory contains the scenario runners, environment setup fixtures, exact AGY prompts, and resulting `.cast` recordings for the 6 terminal sessions in the **Skills Three Ways** presentation.

---

## Recording Checklist & Slide Mapping

| # | Scenario Directory | Cast File | Slide Beat | Purpose / AGY Prompt | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | [`01-what-are-agent-skills/`](./01-what-are-agent-skills/) | `what-are-agent-skills.cast` | S13–S14 | Introduces Agent Skills format, directory anatomy, and progressive disclosure | **Recorded** (~35s) |
| **02** | [`02-libdaisy-skill-creation/`](./02-libdaisy-skill-creation/) | `libdaisy-skill-creation.cast` | S24–S25 | AGY inspects `libDaisy/` repo and authors `libdaisy-guide` skill | Ready to record |
| **03** | [`03-daisysp-skill-creation/`](./03-daisysp-skill-creation/) | `daisysp-skill-creation.cast` | S29–S30 | AGY inspects `DaisySP/` repo and authors `daisysp-guide` skill | Ready to record |
| **04** | [`04-reverse-engineering-plan/`](./04-reverse-engineering-plan/) | `reverse-engineering-plan.cast` | S49–S50 | AGY collaborates to design 6-phase hardware reverse-engineering plan (`PLAN.md`) | Ready to record |
| **05** | [`05-drum-synth-without-skills/`](./05-drum-synth-without-skills/) | `drum-synth-without-skills.cast` | S73–S74 | AGY attempts 7-voice drum synth with NO skills (fails: wrong pins/USB/Makefile) | Ready to record |
| **06** | [`06-drum-synth-with-skills/`](./06-drum-synth-with-skills/) | `drum-synth-with-skills.cast` | S76–S77 | AGY builds 7-voice drum synth with ALL 7 skills (succeeds!) | Ready to record |

---

## Recording Instructions

1. Open your terminal (**Ghostty** recommended, sized to **116 cols x 30 rows** to match `what-are-agent-skills.cast`).
2. Navigate to the scenario directory:
   ```bash
   cd terminal-recordings/scenarios/<scenario-name>
   ```
3. Run the interactive recorder:
   ```bash
   ./record.sh
   ```
   This will:
   - Run `setup.sh` to configure the workspace (clone libraries, copy skills).
   - Display the exact prompt from `PROMPT.md`.
   - Prompt you to press Enter to start `asciinema rec -i 2.0 --overwrite <cast-name>`.
   - Enter `workspace/` and record your session with `agy`.
   - On exit (`Ctrl+D` or `exit`), automatically copy the `.cast` file to `slides/public/casts/`.

---

## Handling Long Sessions (Skips & Playback Tuning)

- For scenarios with extensive research or builds (such as `06-drum-synth-with-skills`):
  - In Slidev, `<AsciinemaPlayer>` is configured by default with `:speed="2.0"` and `:idleTimeLimit="1.0"`.
  - For very long sessions (e.g. 5–10 minutes), you can override the slide props in `slides.md` with a higher speed multiplier (e.g., `:speed="5.0"` or `:speed="8.0"`), or insert chapter markers (`Ctrl+x` during asciinema recording) to skip idle build phases.
