---
name: crop-image
description: Crop, trim, and adjust framing of images by removing transparent whitespace margins, trimming solid color borders, or extracting specific pixel bounding boxes. Use when the user asks to crop an image, trim blank space or transparent borders, remove excess margins, or inspect subject dimensions.
compatibility: Python 3.9+ (zero dependencies for PNG; optional Pillow for JPEG/WebP)
---

# Crop Image

Procedural runbook and tooling for inspecting image boundaries, trimming empty margins (transparent or solid color backgrounds), and executing precision crops.

Includes a zero-dependency Python 3 utility ([crop.py](./scripts/crop.py)) for bit-perfect PNG handling and automatic fallback to Pillow when installed.

## Workflows

Choose the matching workflow based on your objective:

1. [Inspect Image & Subject Bounding Box](#1-inspect-image--subject-bounding-box)
2. [Autocrop Transparent Blank Space](#2-autocrop-transparent-blank-space)
3. [Trim Solid Color Borders (White / Black / Custom)](#3-trim-solid-color-borders-white--black--custom)
4. [Crop by Explicit Bounding Box or Dimensions](#4-crop-by-explicit-bounding-box-or-dimensions)
5. [Validate Cropped Asset](#5-validate-cropped-asset)

---

### 1. Inspect Image & Subject Bounding Box

Before modifying an image, inspect its current dimensions, color channels, and where the actual subject pixels reside.

1. Run the inspection command using [crop.py](./scripts/crop.py):
   ```bash
   python3 .agents/skills/crop-image/scripts/crop.py <path/to/image> --inspect
   ```
2. Review the diagnostic output:
   - **Dimensions**: Overall pixel width and height.
   - **Detected Border/Corner Color**: Color sampled from corners.
   - **Alpha Subject Bounding Box**: Coordinate extent `[left, top, right, bottom]` where alpha > 0.
   - **Subject Margins**: Number of blank pixels on left, right, top, and bottom edges.
3. *Completion Criterion*: Bounding box coordinates and margin sizes are printed to stdout without modifying the source image.

---

### 2. Autocrop Transparent Blank Space

Remove excess transparent padding around a subject, optionally preserving a small aesthetic margin (e.g. 8–16 px) so the graphic does not touch container boundaries.

1. Run autocrop with desired padding (default is 0 for tight crop):
   ```bash
   # In-place overwrite with 12px padding around subject:
   python3 .agents/skills/crop-image/scripts/crop.py <path/to/image.png> --autocrop --padding 12 --in-place
   
   # Or output to a new file:
   python3 .agents/skills/crop-image/scripts/crop.py <input.png> -o <output.png> --autocrop --padding 12
   ```
2. For semi-transparent edge artifacts, increase `--alpha-thresh` (e.g. `--alpha-thresh 10`).
3. *Completion Criterion*: Target image exists on disk with reduced dimensions tightly bounding the subject.

---

### 3. Trim Solid Color Borders (White / Black / Custom)

Trim uniform solid background colors (e.g. white borders `255,255,255` or dark borders `0,0,0`):

1. Specify the RGB color to trim and tolerance (0–255):
   ```bash
   # Trim pure white border with tolerance 5 and 10px margin:
   python3 .agents/skills/crop-image/scripts/crop.py <path/to/image> -o <output> --autocrop --color 255,255,255 --tolerance 5 --padding 10
   
   # Trim pure black border:
   python3 .agents/skills/crop-image/scripts/crop.py <path/to/image> -o <output> --autocrop --color 0,0,0 --tolerance 5
   ```
2. *Completion Criterion*: Script reports `Success` with adjusted dimensions matching the bounded subject.

---

### 4. Crop by Explicit Bounding Box or Dimensions

Extract a specific rectangle by pixel coordinates `left,top,right,bottom` (inclusive):

1. Compute or select the target coordinates `left,top,right,bottom`:
   ```bash
   python3 .agents/skills/crop-image/scripts/crop.py <path/to/image> -o <output> --box 100,50,900,650
   ```
2. If working on macOS and only cropping from the center or fixed width/height:
   ```bash
   sips --cropToHeightWidth <targetHeight> <targetWidth> <input> --out <output>
   ```
3. *Completion Criterion*: Output image matches the exact target pixel dimensions `(right - left + 1) × (bottom - top + 1)`.

---

### 5. Validate Cropped Asset

Always verify the cropped image before declaring completion:

1. Query file metadata with `sips` (macOS) or [crop.py](./scripts/crop.py) `--inspect`:
   ```bash
   sips -g pixelWidth -g pixelHeight <path/to/cropped-image>
   python3 .agents/skills/crop-image/scripts/crop.py <path/to/cropped-image> --inspect
   ```
2. Confirm:
   - `pixelWidth` and `pixelHeight` match expected cropped dimensions.
   - The file is readable and not corrupted.
   - For web/slides projects, run local build/linter (e.g. `npm --prefix slides run build`) to ensure layouts using the asset compile cleanly.
3. *Completion Criterion*: Image metadata returns expected dimensions and project build exits with code 0.
