"""Exact build123d section SVGs from native shapes or STEP imports."""
from __future__ import annotations
import argparse
from pathlib import Path
from build123d import ExportSVG, Plane, Pos, Rot, import_step, section

PLANES = {'xy': Plane.XY, 'xz': Plane.XZ, 'yz': Plane.YZ}


def section_svg(shape, plane_name: str, level: float, output: Path) -> bool:
    """Write one orthographic section; return False if the plane misses it."""
    cut = section(shape, section_by=PLANES[plane_name].offset(level))
    if not cut.faces():
        return False
    flat = (Pos(0, 0, -level) * cut if plane_name == 'xy' else
            Rot(X=-90) * Pos(0, level, 0) * cut if plane_name == 'xz' else
            Rot(Y=-90) * Pos(-level, 0, 0) * cut)
    view = ExportSVG(scale=4, margin=5)
    view.add_layer('Section', fill_color='#d7e7f2',
                   line_color='#173a5e', line_weight=0.8)
    view.add_shape(flat, layer='Section')
    output.parent.mkdir(parents=True, exist_ok=True)
    view.write(str(output))
    return True


def draw(step: Path, output_dir: Path, levels: list[float], axes: list[str]):
    shape = import_step(str(step))
    for name in axes:
        for level in levels:
            path = output_dir / f'{step.stem}-{name}-{level:g}.svg'
            if section_svg(shape, name, level, path):
                print(path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('step', type=Path)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--levels', default='0,6,20')
    p.add_argument('--axes', default='xy,xz,yz')
    a = p.parse_args()
    draw(a.step, a.output_dir,
         [float(x) for x in a.levels.split(',')], a.axes.split(','))


if __name__ == '__main__':
    main()
