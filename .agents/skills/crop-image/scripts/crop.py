#!/usr/bin/env python3
"""
crop.py - Lossless image cropping and whitespace trimming utility.

Supports:
- Transparent margin trimming (autocrop alpha)
- Solid border trimming (matching corner/edge colors like pure white/black)
- Explicit bounding box cropping
- Configurable padding around trimmed subjects
- Pure Python 3 standard library implementation for PNG (zero external dependencies)
- Automatic fallback to Pillow (PIL) when available for JPEG, WebP, and other formats
"""

import argparse
import binascii
import os
import struct
import sys
import zlib

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def decode_png(file_path):
    """
    Decodes an 8-bit RGB or RGBA PNG using standard library zlib and struct.
    Returns: (width, height, channels, list_of_rows_as_bytearray)
    channels: 3 for RGB, 4 for RGBA
    """
    with open(file_path, "rb") as f:
        data = f.read()

    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{file_path} is not a valid PNG file.")

    pos = 8
    idat = bytearray()
    width = height = bit_depth = color_type = interlace = 0

    while pos < len(data):
        if pos + 8 > len(data):
            break
        length, chunk_type = struct.unpack(">I4s", data[pos : pos + 8])
        pos += 8
        chunk_data = data[pos : pos + length]
        pos += length + 4  # skip data + 4-byte CRC

        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, comp, filter_method, interlace = struct.unpack(
                ">IIBBBBB", chunk_data
            )
            if bit_depth != 8:
                raise ValueError(f"Unsupported PNG bit depth: {bit_depth} (expected 8).")
            if color_type not in (2, 6):
                raise ValueError(
                    f"Unsupported PNG color type: {color_type} (expected 2 for RGB or 6 for RGBA)."
                )
            if interlace != 0:
                raise ValueError("Interlaced PNG is not supported by built-in decoder; install Pillow.")
        elif chunk_type == b"IDAT":
            idat.extend(chunk_data)
        elif chunk_type == b"IEND":
            break

    raw = zlib.decompress(bytes(idat))
    channels = 4 if color_type == 6 else 3
    stride = 1 + width * channels
    expected_len = height * stride
    if len(raw) != expected_len:
        raise ValueError(f"Decompressed data size mismatch: {len(raw)} != {expected_len}")

    rows = []
    prev_row = bytearray(width * channels)

    for y in range(height):
        row_bytes = bytearray(raw[y * stride : (y + 1) * stride])
        filter_type = row_bytes[0]
        curr = row_bytes[1:]

        if filter_type == 0:  # None
            pass
        elif filter_type == 1:  # Sub
            for x in range(channels, len(curr)):
                curr[x] = (curr[x] + curr[x - channels]) & 0xFF
        elif filter_type == 2:  # Up
            for x in range(len(curr)):
                curr[x] = (curr[x] + prev_row[x]) & 0xFF
        elif filter_type == 3:  # Average
            for x in range(len(curr)):
                a = curr[x - channels] if x >= channels else 0
                b = prev_row[x]
                curr[x] = (curr[x] + ((a + b) >> 1)) & 0xFF
        elif filter_type == 4:  # Paeth
            for x in range(len(curr)):
                a = curr[x - channels] if x >= channels else 0
                b = prev_row[x]
                c = prev_row[x - channels] if x >= channels else 0
                p = a + b - c
                pa = abs(p - a)
                pb = abs(p - b)
                pc = abs(p - c)
                if pa <= pb and pa <= pc:
                    pr = a
                elif pb <= pc:
                    pr = b
                else:
                    pr = c
                curr[x] = (curr[x] + pr) & 0xFF
        else:
            raise ValueError(f"Unknown filter type {filter_type} at row {y}")

        prev_row = curr
        rows.append(curr)

    return width, height, channels, rows


def encode_png(width, height, channels, rows):
    """Encodes raw rows into a PNG bytearray using standard library zlib and struct."""
    def make_chunk(chunk_type, data):
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", binascii.crc32(chunk_type + data) & 0xFFFFFFFF)
        return length + chunk_type + data + crc

    color_type = 6 if channels == 4 else 2
    raw = bytearray()
    for row in rows:
        raw.append(0)  # filter type 0 (None)
        raw.extend(row)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    idat = zlib.compress(bytes(raw), level=9)

    out = bytearray(b"\x89PNG\r\n\x1a\n")
    out.extend(make_chunk(b"IHDR", ihdr))
    out.extend(make_chunk(b"IDAT", idat))
    out.extend(make_chunk(b"IEND", b""))
    return bytes(out)


def find_bounding_box(width, height, channels, rows, alpha_thresh=1, color_match=None, tolerance=0):
    """
    Finds the bounding box [min_x, min_y, max_x, max_y] of subject pixels.
    If channels == 4: checks alpha >= alpha_thresh and not matching color_match.
    If channels == 3: checks not matching color_match.
    """
    min_x, max_x = width, -1
    min_y, max_y = height, -1

    def is_background(r, g, b, a):
        if channels == 4 and a < alpha_thresh:
            return True
        if color_match is not None:
            cr, cg, cb = color_match[:3]
            if (
                abs(int(r) - int(cr)) <= tolerance
                and abs(int(g) - int(cg)) <= tolerance
                and abs(int(b) - int(cb)) <= tolerance
            ):
                return True
        return False

    for y in range(height):
        row = rows[y]
        for x in range(width):
            offset = x * channels
            r = row[offset]
            g = row[offset + 1]
            b = row[offset + 2]
            a = row[offset + 3] if channels == 4 else 255

            if not is_background(r, g, b, a):
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y

    if min_x > max_x or min_y > max_y:
        return None  # entire image is blank

    return min_x, min_y, max_x, max_y


def detect_border_color(width, height, channels, rows):
    """Samples image corner and edge pixels to guess the background color."""
    corners = [
        (rows[0][0], rows[0][1], rows[0][2]),
        (rows[0][(width - 1) * channels], rows[0][(width - 1) * channels + 1], rows[0][(width - 1) * channels + 2]),
        (rows[height - 1][0], rows[height - 1][1], rows[height - 1][2]),
        (
            rows[height - 1][(width - 1) * channels],
            rows[height - 1][(width - 1) * channels + 1],
            rows[height - 1][(width - 1) * channels + 2],
        ),
    ]
    # If corners agree, return that color
    if corners[0] == corners[1] == corners[2] == corners[3]:
        return corners[0]
    return corners[0]


def crop_image_pure(input_path, output_path, crop_box=None, autocrop=False, padding=0,
                    alpha_thresh=1, trim_color=None, tolerance=0):
    width, height, channels, rows = decode_png(input_path)

    if crop_box is not None:
        left, top, right, bottom = crop_box
    elif autocrop:
        bbox = find_bounding_box(
            width, height, channels, rows,
            alpha_thresh=alpha_thresh,
            color_match=trim_color,
            tolerance=tolerance,
        )
        if bbox is None:
            raise ValueError("Image appears completely blank; no subject found.")
        min_x, min_y, max_x, max_y = bbox
        left = max(0, min_x - padding)
        top = max(0, min_y - padding)
        right = min(width - 1, max_x + padding)
        bottom = min(height - 1, max_y + padding)
    else:
        raise ValueError("Must specify either --autocrop or --box.")

    if left > right or top > bottom:
        raise ValueError(f"Invalid crop box: left={left}, top={top}, right={right}, bottom={bottom}")

    new_w = right - left + 1
    new_h = bottom - top + 1

    cropped_rows = []
    for y in range(top, bottom + 1):
        row = rows[y]
        cropped_rows.append(row[left * channels : (right + 1) * channels])

    out_bytes = encode_png(new_w, new_h, channels, cropped_rows)
    with open(output_path, "wb") as f:
        f.write(out_bytes)

    return width, height, new_w, new_h, (left, top, right, bottom)


def crop_image_pil(input_path, output_path, crop_box=None, autocrop=False, padding=0,
                   alpha_thresh=1, trim_color=None, tolerance=0):
    with Image.open(input_path) as im:
        orig_w, orig_h = im.size
        has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)

        if crop_box is not None:
            # Pillow uses (left, upper, right, lower) where right and lower are exclusive
            left, top, right, bottom = crop_box
            cropped = im.crop((left, top, right + 1, bottom + 1))
        elif autocrop:
            if has_alpha:
                rgba = im.convert("RGBA")
                alpha = rgba.split()[-1]
                # mask alpha >= alpha_thresh
                mask = alpha.point(lambda p: 255 if p >= alpha_thresh else 0)
                bbox = mask.getbbox()
            elif trim_color is not None:
                # convert to RGB and compare difference
                rgb = im.convert("RGB")
                from PIL import ImageChops
                bg = Image.new("RGB", im.size, trim_color)
                diff = ImageChops.difference(rgb, bg)
                if tolerance > 0:
                    diff = diff.point(lambda p: 0 if p <= tolerance else 255)
                bbox = diff.getbbox()
            else:
                # auto-sample top-left corner
                bg_color = im.getpixel((0, 0))
                if isinstance(bg_color, int):
                    bg_color = (bg_color, bg_color, bg_color)
                bg = Image.new(im.mode, im.size, bg_color)
                from PIL import ImageChops
                diff = ImageChops.difference(im, bg)
                bbox = diff.getbbox()

            if not bbox:
                raise ValueError("Image appears completely blank; no subject found.")

            min_x, min_y, max_x, max_y = bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1
            left = max(0, min_x - padding)
            top = max(0, min_y - padding)
            right = min(orig_w - 1, max_x + padding)
            bottom = min(orig_h - 1, max_y + padding)

            cropped = im.crop((left, top, right + 1, bottom + 1))
        else:
            raise ValueError("Must specify either --autocrop or --box.")

        cropped.save(output_path)
        new_w, new_h = cropped.size
        return orig_w, orig_h, new_w, new_h, (left, top, right, bottom)


def inspect_image(input_path, alpha_thresh=1, tolerance=0):
    is_png = input_path.lower().endswith(".png")

    if is_png and not HAS_PIL:
        width, height, channels, rows = decode_png(input_path)
        border_col = detect_border_color(width, height, channels, rows)
        alpha_bbox = find_bounding_box(width, height, channels, rows, alpha_thresh=alpha_thresh)
        color_bbox = find_bounding_box(width, height, channels, rows, color_match=border_col, tolerance=tolerance)
        mode = "RGBA" if channels == 4 else "RGB"
        return {
            "width": width,
            "height": height,
            "mode": mode,
            "engine": "pure-python",
            "border_color": border_col,
            "alpha_bbox": alpha_bbox,
            "color_bbox": color_bbox,
        }
    elif HAS_PIL:
        with Image.open(input_path) as im:
            orig_w, orig_h = im.size
            has_alpha = im.mode in ("RGBA", "LA")
            alpha_bbox = None
            if has_alpha:
                rgba = im.convert("RGBA")
                alpha = rgba.split()[-1]
                mask = alpha.point(lambda p: 255 if p >= alpha_thresh else 0)
                b = mask.getbbox()
                if b:
                    alpha_bbox = (b[0], b[1], b[2] - 1, b[3] - 1)

            corner = im.getpixel((0, 0))
            return {
                "width": orig_w,
                "height": orig_h,
                "mode": im.mode,
                "engine": "pillow",
                "border_color": corner,
                "alpha_bbox": alpha_bbox,
                "color_bbox": None,
            }
    else:
        raise ValueError(
            f"Pillow is required to inspect non-PNG image: {input_path}. Install Pillow with: pip install pillow"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Lossless image cropping and whitespace trimming utility."
    )
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("-o", "--output", help="Path to output image (required unless --inspect or --in-place)")
    parser.add_argument("--in-place", action="store_true", help="Overwrite input image directly")
    parser.add_argument("--inspect", action="store_true", help="Inspect image dimensions, mode, and subject bounds")
    parser.add_argument("--autocrop", action="store_true", help="Trim blank/transparent/solid borders automatically")
    parser.add_argument("--box", help="Manual crop box as left,top,right,bottom (inclusive pixel coordinates)")
    parser.add_argument("--padding", type=int, default=0, help="Padding in pixels to leave around subject (default: 0)")
    parser.add_argument("--alpha-thresh", type=int, default=1, help="Alpha threshold (0-255) for transparency (default: 1)")
    parser.add_argument("--color", help="Trim matching solid color as R,G,B (e.g. 255,255,255)")
    parser.add_argument("--tolerance", type=int, default=5, help="Color match tolerance (0-255, default: 5)")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        sys.stderr.write(f"Error: file not found: {args.input}\n")
        sys.exit(1)

    if args.inspect:
        info = inspect_image(args.input, alpha_thresh=args.alpha_thresh, tolerance=args.tolerance)
        print(f"File: {args.input}")
        print(f"Dimensions: {info['width']}x{info['height']} px")
        print(f"Color Mode: {info['mode']} (engine: {info['engine']})")
        print(f"Detected Border/Corner Color: {info['border_color']}")
        if info["alpha_bbox"]:
            ab = info["alpha_bbox"]
            w = ab[2] - ab[0] + 1
            h = ab[3] - ab[1] + 1
            print(f"Alpha Subject Bounding Box: left={ab[0]}, top={ab[1]}, right={ab[2]}, bottom={ab[3]}")
            print(f"Alpha Subject Size: {w}x{h} px (margin: {ab[0]} left, {info['width'] - 1 - ab[2]} right, {ab[1]} top, {info['height'] - 1 - ab[3]} bottom)")
        if info.get("color_bbox"):
            cb = info["color_bbox"]
            w = cb[2] - cb[0] + 1
            h = cb[3] - cb[1] + 1
            print(f"Color Subject Bounding Box: left={cb[0]}, top={cb[1]}, right={cb[2]}, bottom={cb[3]} ({w}x{h} px)")
        sys.exit(0)

    if not args.autocrop and not args.box:
        sys.stderr.write("Error: Must specify --autocrop, --box <left,top,right,bottom>, or --inspect.\n")
        sys.exit(1)

    output_path = args.output
    if args.in_place:
        output_path = args.input
    elif not output_path:
        sys.stderr.write("Error: Output path not specified. Use -o <path> or --in-place to overwrite.\n")
        sys.exit(1)

    crop_box = None
    if args.box:
        try:
            parts = [int(p.strip()) for p in args.box.split(",")]
            if len(parts) != 4:
                raise ValueError()
            crop_box = tuple(parts)
        except Exception:
            sys.stderr.write("Error: --box must be 4 comma-separated integers: left,top,right,bottom\n")
            sys.exit(1)

    trim_color = None
    if args.color:
        try:
            parts = [int(p.strip()) for p in args.color.split(",")]
            if len(parts) != 3:
                raise ValueError()
            trim_color = tuple(parts)
        except Exception:
            sys.stderr.write("Error: --color must be 3 comma-separated integers: R,G,B (e.g. 255,255,255)\n")
            sys.exit(1)

    is_png = args.input.lower().endswith(".png")
    use_pure = is_png and not HAS_PIL

    try:
        if use_pure:
            orig_w, orig_h, new_w, new_h, box = crop_image_pure(
                args.input,
                output_path,
                crop_box=crop_box,
                autocrop=args.autocrop,
                padding=args.padding,
                alpha_thresh=args.alpha_thresh,
                trim_color=trim_color,
                tolerance=args.tolerance,
            )
        else:
            orig_w, orig_h, new_w, new_h, box = crop_image_pil(
                args.input,
                output_path,
                crop_box=crop_box,
                autocrop=args.autocrop,
                padding=args.padding,
                alpha_thresh=args.alpha_thresh,
                trim_color=trim_color,
                tolerance=args.tolerance,
            )

        print(f"Success: {args.input} ({orig_w}x{orig_h}) -> {output_path} ({new_w}x{new_h})")
        print(f"Crop coordinates (inclusive): left={box[0]}, top={box[1]}, right={box[2]}, bottom={box[3]}")
    except Exception as e:
        sys.stderr.write(f"Error during cropping: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
