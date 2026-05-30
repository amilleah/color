#!/usr/bin/env python3
"""
convert colors between LAB space (for math) and RGB (for human-readable outputs).
background: https://en.wikipedia.org/wiki/CIELAB_color_space
"""
import numpy as np

def rgb_to_lab(pixels: np.ndarray) -> np.ndarray:
    p = pixels.astype(np.float32) / 255.0
    linear = np.where(p <= 0.04045, p / 12.92, ((p + 0.055) / 1.055) ** 2.4)
    M = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ], dtype=np.float32)
    xyz = linear @ M.T
    xyz[:, 0] /= 0.95047
    xyz[:, 2] /= 1.08883
    f = np.where(xyz > 0.008856, xyz ** (1 / 3), 7.787 * xyz + 16 / 116)
    return np.stack([
        116 * f[:, 1] - 16,
        500 * (f[:, 0] - f[:, 1]),
        200 * (f[:, 1] - f[:, 2]),
    ], axis=1)


def lab_to_rgb(lab: np.ndarray) -> tuple[int, int, int]:
    L, a, b = float(lab[0]), float(lab[1]), float(lab[2])
    fy = (L + 16) / 116
    fx = a / 500 + fy
    fz = fy - b / 200

    def finv(t):
        return t ** 3 if t > 0.206897 else (t - 16 / 116) / 7.787

    x, y, z = finv(fx) * 0.95047, finv(fy), finv(fz) * 1.08883
    rl =  3.2404542 * x - 1.5371385 * y - 0.4985314 * z
    gl = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
    bl =  0.0556434 * x - 0.2040259 * y + 1.0572252 * z

    def gamma(c):
        c = max(0.0, min(1.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

    return (
        max(0, min(255, int(gamma(rl) * 255 + 0.5))),
        max(0, min(255, int(gamma(gl) * 255 + 0.5))),
        max(0, min(255, int(gamma(bl) * 255 + 0.5))),
    )
