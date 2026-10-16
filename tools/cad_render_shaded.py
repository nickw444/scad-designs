"""Portable orthographic, colour shaded renders of build123d assemblies.

Uses the build123d B-rep tessellation and Pillow's polygon rasterizer. This
avoids requiring an X server or GPU when regenerating views in CI or macOS.
"""
from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont


DEFAULT_COLOUR = '#7e9bbd'


def component_name(item):
    """Accept a named component with either ``part_name`` or ``name``."""
    return getattr(item, 'part_name', None) or item.name


def render_assembly(assembly, output: Path, *, camera, look_at=(0, 0, 50),
                    title='', width=1600, height=1200,
                    palette: Mapping[str, str] | None = None):
    """Render an assembly with ``.components`` containing named ``.shape`` items.

    Colours can be supplied by a project palette or a component's ``color``
    attribute. Unknown names use a neutral default colour.
    """
    palette = palette or {}
    eye = np.asarray(camera, dtype=float)
    target = np.asarray(look_at, dtype=float)
    forward = target - eye
    forward /= np.linalg.norm(forward)
    right = np.cross(forward, [0., 0., 1.])
    if np.linalg.norm(right) < 1e-6:
        right = np.cross(forward, [0., 1., 0.])
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)
    basis = np.stack((right, up, forward), axis=1)
    light = np.array([0.35, -0.45, 0.82])
    light /= np.linalg.norm(light)
    meshes = []
    all_xy = []
    for item in assembly.components:
        vertices, triangles = item.shape.tessellate(0.10, 0.25)
        if not triangles:
            continue
        xyz = np.array([(v.X, v.Y, v.Z) for v in vertices], dtype=float)
        projected = (xyz - target) @ basis
        faces = np.asarray(triangles, dtype=np.int32)
        meshes.append((item, xyz, projected, faces))
        all_xy.append(projected[:, :2])
    bounds = np.concatenate(all_xy)
    lo, hi = bounds.min(axis=0), bounds.max(axis=0)
    usable_w, usable_h = width - 180, height - 330
    scale = min(usable_w / max(hi[0] - lo[0], 1),
                usable_h / max(hi[1] - lo[1], 1))
    centre = (lo + hi) / 2
    pixels = np.empty((height, width, 3), dtype=np.uint8)
    pixels[:] = (248, 250, 252)
    zbuffer = np.full((height, width), np.inf, dtype=np.float32)
    for item, xyz, projected, faces in meshes:
        tri_xyz = xyz[faces]
        normals = np.cross(tri_xyz[:, 1] - tri_xyz[:, 0],
                           tri_xyz[:, 2] - tri_xyz[:, 0])
        lengths = np.linalg.norm(normals, axis=1)
        good = lengths > 1e-10
        normals[good] /= lengths[good, None]
        # Back faces of the closed solids must not paint across their front.
        good &= (normals @ forward) < -1e-6
        intensity = np.clip(0.67 + 0.30 * (normals @ light), 0.35, 1.0)
        colour = palette.get(component_name(item), getattr(item, 'color', DEFAULT_COLOUR))
        base = np.array(tuple(bytes.fromhex(colour.lstrip('#'))), dtype=float)
        colours = np.clip(base[None, :] * intensity[:, None], 0, 255).astype(np.uint8)
        xy = projected[:, :2]
        xy = (xy - centre) * scale
        xy[:, 0] += width / 2
        xy[:, 1] = height / 2 - 5 - xy[:, 1]
        vertex_depth = projected[:, 2]
        for index in np.flatnonzero(good):
            pts = xy[faces[index]]
            x0 = max(0, int(np.floor(pts[:, 0].min())))
            x1 = min(width, int(np.ceil(pts[:, 0].max())) + 1)
            y0 = max(0, int(np.floor(pts[:, 1].min())))
            y1 = min(height, int(np.ceil(pts[:, 1].max())) + 1)
            if x0 >= x1 or y0 >= y1:
                continue
            a, b, c = pts
            denom = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if abs(denom) < 1e-7:
                continue
            yy, xx = np.ogrid[y0:y1, x0:x1]
            px, py = xx + 0.5, yy + 0.5
            w0 = ((b[1] - c[1]) * (px - c[0]) + (c[0] - b[0]) * (py - c[1])) / denom
            w1 = ((c[1] - a[1]) * (px - c[0]) + (a[0] - c[0]) * (py - c[1])) / denom
            w2 = 1 - w0 - w1
            inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            d0, d1, d2 = vertex_depth[faces[index]]
            z = w0 * d0 + w1 * d1 + w2 * d2
            region = zbuffer[y0:y1, x0:x1]
            draw_here = inside & (z < region)
            region[draw_here] = z[draw_here]
            pixels[y0:y1, x0:x1][draw_here] = colours[index]
    image = Image.fromarray(pixels, 'RGB')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=28)
    small = ImageFont.load_default(size=19)
    if title:
        draw.text((64, 40), title, font=font, fill='#20344d')
    legend = []
    legend_colours = {}
    for item in assembly.components:
        name = component_name(item)
        if name not in legend:
            legend.append(name)
            legend_colours[name] = palette.get(name, getattr(item, 'color', DEFAULT_COLOUR))
    x, y = 64, height - 115
    for name in legend:
        label = name.replace('-', ' ')
        draw.rounded_rectangle((x, y, x + 23, y + 23), radius=4,
                               fill=legend_colours[name])
        draw.text((x + 32, y + 2), label, font=small, fill='#34465c')
        x += max(155, len(label) * 11 + 60)
        if x > width - 235:
            x, y = 64, y + 38
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    return output
