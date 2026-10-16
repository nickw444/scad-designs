"""Compare two STL files, or matching STL sets, without relying on source CAD.

Reports dimensions, volume, watertightness and bidirectional sampled surface error.
The sampling detects misplaced features; it is not a proof of mechanical fit.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import trimesh
from trimesh.proximity import closest_point


def compare(a_path: Path, b_path: Path, samples: int = 20000) -> dict:
    a = trimesh.load_mesh(a_path, process=True)
    b = trimesh.load_mesh(b_path, process=True)
    if not isinstance(a, trimesh.Trimesh) or not isinstance(b, trimesh.Trimesh):
        raise ValueError('Expected one mesh per input file')
    # sample_surface uses global NumPy state; seed it for repeatable audits.
    np.random.seed(12345)
    ap, _ = trimesh.sample.sample_surface(a, samples)
    np.random.seed(12345)
    bp, _ = trimesh.sample.sample_surface(b, samples)
    ad = closest_point(b, ap)[1]
    bd = closest_point(a, bp)[1]
    distances = np.concatenate((ad, bd))
    return {
        'reference': str(a_path), 'candidate': str(b_path),
        'reference_volume_mm3': float(a.volume),
        'candidate_volume_mm3': float(b.volume),
        'relative_volume_error': float(abs(a.volume-b.volume)/abs(a.volume)),
        'reference_bounds_mm': a.bounds.tolist(),
        'candidate_bounds_mm': b.bounds.tolist(),
        'maximum_bounds_error_mm': float(np.max(np.abs(a.bounds-b.bounds))),
        'reference_watertight': bool(a.is_watertight),
        'candidate_watertight': bool(b.is_watertight),
        'surface_rms_mm': float(np.sqrt(np.mean(distances**2))),
        'surface_p99_mm': float(np.percentile(distances, 99)),
        'surface_max_mm': float(np.max(distances)),
        'samples_each_direction': samples,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference', type=Path)
    parser.add_argument('candidate', type=Path)
    parser.add_argument('--samples', type=int, default=20000)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.reference.is_dir() and args.candidate.is_dir():
        rows = {}
        for ref in sorted(args.reference.glob('*.stl')):
            cand = args.candidate / ref.name
            if not cand.exists():
                raise FileNotFoundError(cand)
            rows[ref.stem] = compare(ref, cand, args.samples)
    else:
        rows = compare(args.reference, args.candidate, args.samples)
    result = json.dumps(rows, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result+'\n')
    print(result)


if __name__ == '__main__':
    main()
