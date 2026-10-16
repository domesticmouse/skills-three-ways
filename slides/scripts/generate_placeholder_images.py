import zlib
import struct
import os

def create_png(width, height, draw_fn, filename):
    # Generates a true uncompressed/zlib 24-bit RGB PNG
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0) # Filter type 0 (None)
        for x in range(width):
            r, g, b = draw_fn(x, y, width, height)
            raw_data.extend((r, g, b))

    compressed = zlib.compress(bytes(raw_data), level=6)

    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    png_bytes = b'\x89PNG\r\n\x1a\n'
    png_bytes += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    png_bytes += chunk(b'IDAT', compressed)
    png_bytes += chunk(b'IEND', b'')

    with open(filename, 'wb') as f:
        f.write(png_bytes)

os.makedirs('slides/public/images', exist_ok=True)

# 1. gamma-promo.png (800x480, dark slate theme with hardware mock diagram)
def draw_promo(x, y, w, h):
    # Background: deep dark slate
    r, g, b = 24, 26, 32

    # Border
    if x < 4 or x >= w - 4 or y < 4 or y >= h - 4:
        return (60, 70, 90)

    # Synth body rectangle (x: 60..740, y: 60..420)
    if 60 <= x <= 740 and 60 <= y <= 420:
        # Inner chassis gradient
        r, g, b = 38, 42, 53

        # Bezel border
        if x in (60, 61, 739, 740) or y in (60, 61, 419, 420):
            return (80, 95, 120)

        # OLED Display (x: 320..480, y: 100..200)
        if 320 <= x <= 480 and 100 <= y <= 200:
            if x in (320, 480) or y in (100, 200):
                return (100, 200, 255)
            # Screen pixel grid simulation
            return (12, 18, 30)

        # 4 Knobs along the top (x: 140, 240, 560, 660, y: 150, radius 25)
        for kx in [140, 240, 560, 660]:
            dx, dy = x - kx, y - 150
            dist_sq = dx*dx + dy*dy
            if dist_sq <= 25*25:
                if dist_sq >= 22*22:
                    return (200, 160, 50) # Amber ring
                return (65, 75, 95)

        # 2 Thumbsticks (x: 170, 630, y: 290, radius 40)
        for sx in [170, 630]:
            dx, dy = x - sx, y - 290
            dist_sq = dx*dx + dy*dy
            if dist_sq <= 40*40:
                if dist_sq >= 36*36:
                    return (52, 211, 153) # Mint ring
                return (50, 58, 72)

        # 14 Keys (2 rows of 7: Chord row y: 250, Note row y: 320)
        # centered around 290..510
        for row_idx, ky in enumerate([240, 310]):
            for col_idx in range(7):
                bx = 305 + col_idx * 30
                if bx <= x <= bx + 22 and ky <= y <= ky + 45:
                    if x in (bx, bx+22) or y in (ky, ky+45):
                        return (120, 140, 180)
                    return (70, 82, 105)

        # Rotary Encoder (x: 400, y: 380, radius 20)
        dx, dy = x - 400, y - 380
        dist_sq = dx*dx + dy*dy
        if dist_sq <= 20*20:
            if dist_sq >= 17*17:
                return (167, 139, 250)
            return (60, 70, 90)

    return (r, g, b)

create_png(800, 480, draw_promo, 'slides/public/images/gamma-promo.png')
print("Created slides/public/images/gamma-promo.png")

# 2. gamma-screws.png (and we will convert to jpg via sips)
def draw_screws(x, y, w, h):
    # Dark industrial chassis rear view
    r, g, b = 28, 30, 36

    if x < 4 or x >= w - 4 or y < 4 or y >= h - 4:
        return (70, 80, 95)

    # Enclosure back plate
    if 80 <= x <= 720 and 50 <= y <= 430:
        r, g, b = 45, 48, 56
        if x in (80, 720) or y in (50, 430):
            return (90, 100, 120)

        # 4 Corner Chassis Screws with bright red/orange target rings
        # Top-left, Top-right, Bottom-left, Bottom-right
        for sx, sy in [(130, 90), (670, 90), (130, 390), (670, 390)]:
            dx, dy = x - sx, y - sy
            dist_sq = dx*dx + dy*dy
            if dist_sq <= 30*30:
                if 22*22 <= dist_sq <= 28*28:
                    return (255, 85, 85) # Red callout ring
                if dist_sq <= 12*12:
                    return (200, 205, 215) # Silver screw head
                return (70, 40, 45) # Warning halo

        # Center informational box (access to Daisy Seed)
        if 280 <= x <= 520 and 170 <= y <= 310:
            if x in (280, 520) or y in (170, 310):
                return (52, 211, 153) # Mint border
            return (35, 40, 48)

    return (r, g, b)

create_png(800, 480, draw_screws, 'slides/public/images/gamma-screws.png')
print("Created slides/public/images/gamma-screws.png")
