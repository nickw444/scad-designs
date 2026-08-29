#!/usr/bin/env python3
"""Compare STL meshes independently of facet and vertex ordering."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from pathlib import Path


Point = tuple[float, float, float]
Triangle = tuple[Point, Point, Point]


def read_triangles(path: Path) -> list[Triangle]:
    data = path.read_bytes()
    if len(data) >= 84:
        triangle_count = struct.unpack_from("<I", data, 80)[0]
        if 84 + triangle_count * 50 == len(data):
            triangles = []
            offset = 84
            for _ in range(triangle_count):
                values = struct.unpack_from("<12fH", data, offset)
                triangles.append((values[3:6], values[6:9], values[9:12]))
                offset += 50
            return triangles

    vertices = []
    for line in data.decode("ascii").splitlines():
        fields = line.split()
        if fields[:1] == ["vertex"]:
            vertices.append(tuple(map(float, fields[1:4])))
    if len(vertices) % 3:
        raise ValueError(f"{path}: malformed ASCII STL")
    return [tuple(vertices[index:index + 3]) for index in range(0, len(vertices), 3)]


def subtract(a: Point, b: Point) -> Point:
    return tuple(a[index] - b[index] for index in range(3))


def cross(a: Point, b: Point) -> Point:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def dot(a: Point, b: Point) -> float:
    return sum(left * right for left, right in zip(a, b))


def metrics(triangles: list[Triangle]) -> dict[str, object]:
    points = [point for triangle in triangles for point in triangle]
    bounds = tuple(
        value
        for axis in range(3)
        for value in (min(point[axis] for point in points), max(point[axis] for point in points))
    )
    area = 0.0
    signed_volume = 0.0
    canonical = []
    for a, b, c in triangles:
        normal = cross(subtract(b, a), subtract(c, a))
        area += math.sqrt(dot(normal, normal)) / 2
        signed_volume += dot(a, cross(b, c)) / 6
        canonical.append(tuple(sorted((a, b, c))))
    digest = hashlib.sha256(repr(sorted(canonical)).encode()).hexdigest()
    return {
        "triangles": len(triangles),
        "bounds": bounds,
        "area": area,
        "volume": abs(signed_volume),
        "topology": digest,
    }


def close(left: float, right: float, tolerance: float) -> bool:
    return math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path, help="Reference STL or geometry manifest")
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--model", help="Model key when reference is a JSON manifest")
    parser.add_argument("--tolerance", type=float, default=1e-8)
    args = parser.parse_args()

    if args.reference.suffix == ".json":
        if not args.model:
            parser.error("--model is required with a JSON reference manifest")
        expected = json.loads(args.reference.read_text())[args.model]
    else:
        expected = metrics(read_triangles(args.reference))
    actual = metrics(read_triangles(args.candidate))
    print(f"reference: {expected}")
    print(f"candidate: {actual}")

    scalar_keys = ("area", "volume")
    equivalent = expected["triangles"] == actual["triangles"]
    equivalent &= all(
        close(left, right, args.tolerance)
        for left, right in zip(expected["bounds"], actual["bounds"])
    )
    equivalent &= all(
        close(expected[key], actual[key], args.tolerance) for key in scalar_keys
    )
    equivalent &= expected["topology"] == actual["topology"]
    if equivalent:
        print("equivalent: exact triangle set, bounds, area, and volume match")
        return 0

    print("equivalent: no")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
