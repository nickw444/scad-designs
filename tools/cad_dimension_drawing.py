"""Annotated 2D section drawings measured from native build123d solids.

The model is sectioned by Open Cascade. SVG outlines are sampled from the
resulting B-rep wires, while dimension numbers use exact wire bounding boxes
or specified points; the sampled outline never supplies the measurements.
"""
from __future__ import annotations

from dataclasses import dataclass
from html import escape
from math import hypot
from pathlib import Path
from typing import Iterable

from build123d import GeomType, Plane, section


PLANES = {'xy': Plane.XY, 'xz': Plane.XZ, 'yz': Plane.YZ}


def point2(point, plane: str) -> tuple[float, float]:
    if plane == 'xy':
        return (point.X, point.Y)
    if plane == 'xz':
        return (point.X, point.Z)
    if plane == 'yz':
        return (point.Y, point.Z)
    raise ValueError(f'Unknown plane: {plane}')


@dataclass(frozen=True)
class Bounds2D:
    min_u: float
    min_v: float
    max_u: float
    max_v: float

    @property
    def width(self) -> float:
        return self.max_u - self.min_u

    @property
    def height(self) -> float:
        return self.max_v - self.min_v


def bounds2(shape, plane: str) -> Bounds2D:
    box = shape.bounding_box()
    a, b = point2(box.min, plane), point2(box.max, plane)
    return Bounds2D(*a, *b)


@dataclass(frozen=True)
class LinearDimension:
    start: tuple[float, float]
    end: tuple[float, float]
    offset: float
    prefix: str = ''
    suffix: str = ' mm'
    decimals: int = 2

    @property
    def value_mm(self) -> float:
        return hypot(self.end[0] - self.start[0],
                     self.end[1] - self.start[1])

    @property
    def label(self) -> str:
        return f'{self.prefix}{self.value_mm:.{self.decimals}f}{self.suffix}'

    def endpoints(self):
        x1, y1 = self.start
        x2, y2 = self.end
        length = self.value_mm
        if length <= 0:
            raise ValueError('Dimension endpoints coincide')
        normal = (-(y2 - y1) / length, (x2 - x1) / length)
        delta = (normal[0] * self.offset, normal[1] * self.offset)
        return ((x1 + delta[0], y1 + delta[1]),
                (x2 + delta[0], y2 + delta[1]), normal)


def span_dimension(box: Bounds2D, axis: str, *, side: str,
                   offset: float, prefix='', suffix=' mm', decimals=2):
    """Dimension one exact projected bounding span of a shape or wire."""
    if axis == 'u':
        v = box.min_v if side == 'min' else box.max_v
        start, end = (box.min_u, v), (box.max_u, v)
    elif axis == 'v':
        u = box.min_u if side == 'min' else box.max_u
        start, end = (u, box.min_v), (u, box.max_v)
    else:
        raise ValueError("axis must be 'u' or 'v'")
    return LinearDimension(start, end, offset, prefix, suffix, decimals)


@dataclass(frozen=True)
class Leader:
    anchor: tuple[float, float]
    label_at: tuple[float, float]
    text: str


@dataclass(frozen=True)
class RoundHole:
    centre: tuple[float, float]
    diameter_mm: float


class SectionDrawing:
    """An exact planar cut and helpers for feature measurements."""

    def __init__(self, shape, plane: str, level_mm: float):
        if plane not in PLANES:
            raise ValueError(f'Unknown section plane: {plane}')
        self.shape = shape
        self.plane = plane
        self.level_mm = level_mm
        self.cut = section(shape, section_by=PLANES[plane].offset(level_mm))
        if not self.cut.faces():
            raise ValueError('Section plane does not intersect the part')

    @property
    def section_bounds(self) -> Bounds2D:
        return bounds2(self.cut, self.plane)

    @property
    def overall_bounds(self) -> Bounds2D:
        return bounds2(self.shape, self.plane)

    def inner_wires(self):
        return [wire for face in self.cut.faces() for wire in face.inner_wires()]

    def largest_opening(self) -> Bounds2D:
        wires = self.inner_wires()
        if not wires:
            raise ValueError('Section has no enclosed opening')
        return bounds2(max(wires, key=lambda wire: wire.bounding_box().size.length),
                       self.plane)

    def round_holes(self, *, min_diameter=0., max_diameter=float('inf')) -> list[RoundHole]:
        """Find circular through openings in the cut, measured from B-rep wires."""
        found = []
        for wire in self.inner_wires():
            edges = wire.edges()
            if len(edges) != 1 or edges[0].geom_type != GeomType.CIRCLE:
                continue
            b = bounds2(wire, self.plane)
            if abs(b.width - b.height) > 0.01:
                continue
            diameter = (b.width + b.height) / 2
            if min_diameter <= diameter <= max_diameter:
                found.append(RoundHole(((b.min_u + b.max_u) / 2,
                                        (b.min_v + b.max_v) / 2), diameter))
        return found

    def horizontal_levels_at(self, u: float, *, tolerance=1e-5) -> list[float]:
        """Exact heights of horizontal straight boundary edges crossing a view U value."""
        levels = []
        for edge in self.cut.edges():
            if edge.geom_type != GeomType.LINE:
                continue
            b = bounds2(edge, self.plane)
            if b.height <= tolerance and b.min_u - tolerance <= u <= b.max_u + tolerance:
                level = (b.min_v + b.max_v) / 2
                if not any(abs(level - seen) <= tolerance for seen in levels):
                    levels.append(level)
        return sorted(levels)


def render_section_drawing(drawing: SectionDrawing, output: Path, *, title: str,
                           dimensions: Iterable[LinearDimension],
                           leaders: Iterable[Leader] = (), notes: Iterable[str] = (),
                           width=1500, height=1200, curve_deflection=0.12):
    """Write a standalone SVG with shaded cut material and measured dimensions."""
    dimensions, leaders, notes = list(dimensions), list(leaders), list(notes)
    paths = []
    outline_points = []
    for face in drawing.cut.faces():
        face_paths = []
        for wire in [face.outer_wire(), *face.inner_wires()]:
            points = [point2(p, drawing.plane)
                      for p in wire.positions(deflection=curve_deflection)]
            if len(points) < 3:
                continue
            outline_points.extend(points)
            face_paths.append(points)
        paths.append(face_paths)
    extent = list(outline_points)
    for dimension in dimensions:
        a, b, _ = dimension.endpoints()
        extent.extend((dimension.start, dimension.end, a, b))
    for leader in leaders:
        extent.extend((leader.anchor, leader.label_at))
    min_u, max_u = min(p[0] for p in extent), max(p[0] for p in extent)
    min_v, max_v = min(p[1] for p in extent), max(p[1] for p in extent)
    margin, top, bottom = 90, 125, 100 + 28 * len(notes)
    scale = min((width - 2 * margin) / max(max_u - min_u, 1),
                (height - top - bottom) / max(max_v - min_v, 1))
    centre_u, centre_v = (min_u + max_u) / 2, (min_v + max_v) / 2

    def px(point):
        return (width / 2 + (point[0] - centre_u) * scale,
                top + (height - top - bottom) / 2 - (point[1] - centre_v) * scale)

    def pair(point):
        x, y = px(point)
        return f'{x:.2f},{y:.2f}'

    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
                f'height="{height}" viewBox="0 0 {width} {height}">',
                '<rect width="100%" height="100%" fill="#ffffff"/>',
                f'<text x="{margin}" y="62" class="title">{escape(title)}</text>',
                f'<text x="{margin}" y="93" class="subtitle">'
                f'{drawing.plane.upper()} section at {drawing.level_mm:g} mm · dimensions measured from CAD</text>',
                '<style>.title{font:700 31px Arial,sans-serif;fill:#17324d}'
                '.subtitle{font:17px Arial,sans-serif;fill:#5b7084}'
                '.cut{fill:#dceaf4;stroke:#19466c;stroke-width:2;fill-rule:evenodd}'
                '.dim{stroke:#147c82;stroke-width:2;fill:none}'
                '.ext{stroke:#65a9ad;stroke-width:1.5}'
                '.dimtext{font:700 18px Arial,sans-serif;fill:#0b666b}'
                '.leader{stroke:#b45d33;stroke-width:2;fill:none}'
                '.leadertext{font:700 18px Arial,sans-serif;fill:#9a4923}'
                '.note{font:17px Arial,sans-serif;fill:#40566b}</style>']
    for face_paths in paths:
        commands = []
        for points in face_paths:
            commands.append('M ' + ' L '.join(pair(p) for p in points) + ' Z')
        elements.append(f'<path class="cut" d="{" ".join(commands)}"/>')
    arrow = 10
    for dim in dimensions:
        q1, q2, normal = dim.endpoints()
        x1, y1 = px(q1)
        x2, y2 = px(q2)
        ux, uy = (x2 - x1) / hypot(x2 - x1, y2 - y1), (y2 - y1) / hypot(x2 - x1, y2 - y1)
        for start, end in ((dim.start, q1), (dim.end, q2)):
            elements.append(f'<line class="ext" x1="{px(start)[0]:.2f}" y1="{px(start)[1]:.2f}" '
                            f'x2="{px(end)[0]:.2f}" y2="{px(end)[1]:.2f}"/>')
        elements.append(f'<line class="dim" x1="{x1:.2f}" y1="{y1:.2f}" '
                        f'x2="{x2:.2f}" y2="{y2:.2f}"/>')
        for x, y, direction in ((x1, y1, 1), (x2, y2, -1)):
            bx, by = x + direction * ux * arrow, y + direction * uy * arrow
            points = [(x, y), (bx - uy * 4, by + ux * 4),
                      (bx + uy * 4, by - ux * 4)]
            elements.append(f'<polygon fill="#147c82" points="'
                            + ' '.join(f'{a:.2f},{b:.2f}' for a, b in points) + '"/>')
        midx, midy = (x1 + x2) / 2, (y1 + y2) / 2
        if abs(uy) > abs(ux):
            elements.append(f'<text class="dimtext" text-anchor="middle" '
                            f'transform="translate({midx-8:.2f} {midy:.2f}) rotate(-90)">'
                            f'{escape(dim.label)}</text>')
        else:
            elements.append(f'<text class="dimtext" text-anchor="middle" '
                            f'x="{midx:.2f}" y="{midy-9:.2f}">{escape(dim.label)}</text>')
    for leader in leaders:
        ax, ay = px(leader.anchor)
        lx, ly = px(leader.label_at)
        elements.append(f'<circle cx="{ax:.2f}" cy="{ay:.2f}" r="4" fill="#b45d33"/>')
        elements.append(f'<path class="leader" d="M {ax:.2f},{ay:.2f} L {lx:.2f},{ly:.2f}"/>')
        elements.append(f'<text class="leadertext" x="{lx+8:.2f}" y="{ly-6:.2f}">'
                        f'{escape(leader.text)}</text>')
    for i, note in enumerate(notes):
        elements.append(f'<text class="note" x="{margin}" y="{height-bottom+40+i*28}">'
                        f'{escape(note)}</text>')
    elements.append('</svg>')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text('\n'.join(elements) + '\n')
    return output
