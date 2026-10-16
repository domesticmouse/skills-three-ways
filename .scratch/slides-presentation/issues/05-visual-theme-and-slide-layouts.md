# Visual theme, reusable slide layouts, and hardware asset specs

Type: grilling
Status: resolved
Blocked by: 03

## Question

How should the custom Slidev layouts (`cast-full` for 85–90% viewport click-to-play asciinema recordings, skill breakdown zoom-in cards, and hardware photo callout frames), dark terminal styling (`slides/style.css`), and hardware image assets (`gamma-promo.png`, `gamma-screws.jpg`) be specified so the 80-slide deck is ready to author?

## Answer

### 1. Custom Slidev Layouts (`slides/layouts/`)
- **`cast-full.vue`**: Dedicated 85–90% viewport layout for all 6 terminal session recordings. Integrates a compact top header bar (Act breadcrumb, slide title, animated `"Click terminal to play"` pill) and an expansive player container hosting `<AsciinemaPlayer :src="$frontmatter.src" :autoPlay="false" :speed="2.0" :idleTimeLimit="1.0" fit="both" theme="dracula" />`.
- **`skill-breakdown.vue`**: Standardized multi-slide zoom-in layout featuring dynamic category badges and border styling (`border-cyan-500/30`, `border-amber-500/30`, `border-emerald-500/30`, `border-purple-500/30`), skill path tags, and runbook code containers.
- **`hardware-callout.vue`**: 2-column split layout pairing a dark hardware media frame on the left (with floating caption and tag overlays) and annotated hardware discovery specs / pinout bullets on the right.

### 2. Category Color Tokens & Dark Theme (`slides/style.css`)
- **Base Theme**: Deep dark `#121317` slate background with high-contrast Tokyo Night / Dracula terminal contrast.
- **Category Color System**:
  - **Way 1 (Library Review Skills)**: Sky Cyan (`--skill-way1: #38bdf8`, `.badge-way1`)
  - **Way 2 (DFU Operational Skills)**: Amber Gold (`--skill-way2: #fbbf24`, `.badge-way2`)
  - **Way 3 (Hardware Discovery Skills)**: Mint Emerald (`--skill-way3: #34d399`, `.badge-way3`)
  - **The Mashup (`gamma-usb-connectivity`)**: Violet Purple (`--skill-mashup: #a78bfa`, `.badge-mashup`)
- **Typography & Components**: Stylized `<kbd>` keycaps and monospace code typography tuned for slide visibility.

### 3. Hardware Asset Specs (`slides/public/images/`)
- Generated visual stubs with exact layout dimensions:
  - `slides/public/images/gamma-promo.png` (800x480): Visual diagram of the physical Gamma mini synth (1.3" OLED, 4 top knobs, 2 thumbsticks, 14 keys, rotary encoder).
  - `slides/public/images/gamma-screws.jpg` (800x480): Annotated rear chassis view highlighting the 4 outer corner screws for disassembly to access the Daisy Seed 2 DFM.
- Documented drop-in paths for camera photos so Slidev builds with zero broken image errors.
