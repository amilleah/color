#!/usr/bin/env python3
"""
extract colors from images with mean-shift clustering.
background: https://spin.atomicobject.com/mean-shift-clustering/
"""
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.cluster import MeanShift

from colors import lab_to_rgb, rgb_to_lab


def extract_palette(
    path: Path,
    n_colors: int = 5,          #--- output n_colors for palette extraction
    dpi: int = 80,              #--- resolution of input image
    bandwidth: float = 24,      #--- kernel bandwidth for mean shift clustering; larger = more colors
):
    img = Image.open(path).convert("RGB").resize((dpi, dpi), Image.LANCZOS)
    pixels = np.array(img).reshape(-1, 3)

    lab = rgb_to_lab(pixels)
    try:
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, n_jobs=1) # bins of size bandwidth
        ms.fit(lab)
    except ValueError:
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=False, n_jobs=1) # low variance images
        ms.fit(lab)

    counts = np.bincount(ms.labels_)
    order = np.argsort(counts)[::-1][:n_colors]
    centers = ms.cluster_centers_[order]
    weights = (counts[order] / counts.sum()).astype(float)
    rgbs = [lab_to_rgb(c) for c in centers]
    return centers.tolist(), rgbs, weights.tolist()


def render_swatch(              #--- outputs `--palette` sidecar PNG
    rgbs,
    weights,
    out_path: Path,
    *,
    width: int = 512,
    height: int = 64,
):
    weights = np.array(weights, dtype=float)
    widths = np.maximum(1, np.round(weights / weights.sum() * width).astype(int))
    widths[-1] += width - widths.sum()
    img = Image.new("RGB", (width, height))
    x = 0
    for rgb, w in zip(rgbs, widths):
        if w <= 0:
            continue
        img.paste(tuple(rgb), (x, 0, x + w, height))
        x += w
    img.save(out_path, "PNG")
