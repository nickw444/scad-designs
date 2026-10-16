"""Small build123d solid-construction helpers shared by model projects.

All dimensions are millimetres. Z extents are absolute; prisms grow from
``z0`` to ``z1``. The polygon helpers preserve their supplied coordinates.
"""
from __future__ import annotations

from build123d import Align, Axis, Box, Cone, Cylinder, Plane, Polygon, Pos, RectangleRounded, extrude, revolve


def rounded_prism(x, y, radius, z0, z1):
    return Pos(0, 0, z0) * extrude(RectangleRounded(x, y, radius), amount=z1-z0)


def cylinder(x, y, radius, z0, z1):
    return Pos(x, y, z0) * Cylinder(radius, z1-z0, align=(Align.CENTER, Align.CENTER, Align.MIN))


def cone(x, y, lower, upper, z0, height):
    return Pos(x, y, z0) * Cone(lower, upper, height, align=(Align.CENTER, Align.CENTER, Align.MIN))


def rectangular_prism(x, y, z0, z1, cx=0, cy=0):
    return Pos(cx, cy, z0) * Box(x, y, z1-z0, align=(Align.CENTER, Align.CENTER, Align.MIN))


def polygon_xz(points, y0=-250, y1=250):
    section = Plane.XZ * Polygon(*points, align=None)
    return Pos(0, y1, 0) * extrude(section, amount=y1-y0)


def radial_profile(points):
    return revolve(Plane.XZ * Polygon(*points, align=None), axis=Axis.Z)
