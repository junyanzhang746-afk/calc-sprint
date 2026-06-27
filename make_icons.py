from PIL import Image, ImageDraw
import math

def make_icon(size, path):
    img = Image.new("RGB", (size, size), "#10172A")
    draw = ImageDraw.Draw(img)

    # subtle rounded-square feel isn't needed; OS handles masking.
    # Draw a curve (like x^2 shifted) and a tangent line, echoing the app's signature visual.
    pad = size * 0.18
    w = size - 2 * pad

    def to_px(x, y):
        # x in [-1.3, 1.3], y in [-0.2, 1.6] roughly
        px = pad + (x + 1.3) / 2.6 * w
        py = size - pad - (y + 0.2) / 1.8 * w
        return px, py

    # grid axes
    axis_color = "#3D4A66"
    zx, _ = to_px(0, 0)
    _, zy = to_px(0, 0)
    draw.line([(zx, pad * 0.5), (zx, size - pad * 0.5)], fill=axis_color, width=max(2, size // 120))
    draw.line([(pad * 0.5, zy), (size - pad * 0.5, zy)], fill=axis_color, width=max(2, size // 120))

    # curve y = x^2 * 0.9
    pts = []
    steps = 80
    for i in range(steps + 1):
        x = -1.3 + (2.6 * i / steps)
        y = 0.9 * x * x
        pts.append(to_px(x, y))
    draw.line(pts, fill="#F2EFE6", width=max(3, size // 60), joint="curve")

    # tangent line at x = 0.6, slope = 1.8*0.6 = 1.08
    t = 0.6
    slope = 1.8 * t
    y0 = 0.9 * t * t
    x1, x2 = t - 0.7, t + 0.7
    y1 = y0 + slope * (x1 - t)
    y2 = y0 + slope * (x2 - t)
    draw.line([to_px(x1, y1), to_px(x2, y2)], fill="#E8A33D", width=max(3, size // 55))

    # point marker
    px, py = to_px(t, y0)
    r = max(4, size * 0.035)
    draw.ellipse([px - r, py - r, px + r, py + r], fill="#E8A33D")

    img.save(path)

make_icon(192, "/home/claude/calc-pwa/icons/icon-192.png")
make_icon(512, "/home/claude/calc-pwa/icons/icon-512.png")
make_icon(180, "/home/claude/calc-pwa/icons/apple-touch-icon.png")
print("done")
