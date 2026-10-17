"""Plan section through one retainer's capture tab and flange pocket."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from build123d import Plane, section
from geometry import rectangular_prism
from parts.housing import (ceiling_flange, RETAINER_TAIL_WIDTH,
                           RETAINER_CAPTURE_XY_CLEARANCE)
from parts.retainers import end_retainer


def render():
    cut_level = 1.0
    window = rectangular_prism(18, 20, cut_level-0.05, cut_level+0.05, 67, -82)

    def px(x):
        return 100 + 30 * (x - 58)

    def py(y):
        return 720 - 30 * (y + 92)

    def path_for(shape):
        cut = section(shape & window, section_by=Plane.XY.offset(cut_level))
        paths = []
        for face in cut.faces():
            for wire in [face.outer_wire(), *face.inner_wires()]:
                points = [(p.X,p.Y) for p in wire.positions(deflection=0.06)]
                if len(points) >= 3:
                    paths.append('M ' + ' L '.join(
                        f'{px(x):.2f},{py(y):.2f}' for x,y in points) + ' Z')
        return ' '.join(paths)

    flange = path_for(ceiling_flange())
    retainer = path_for(end_retainer())
    pocket_width = RETAINER_TAIL_WIDTH + 2*RETAINER_CAPTURE_XY_CLEARANCE
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1350" height="850" viewBox="0 0 1350 850">
<rect width="1350" height="850" fill="#f8fafc"/>
<style>.title{{font:700 28px Arial;fill:#17324d}}.text{{font:18px Arial;fill:#334b63}}.dim{{font:700 19px Arial;fill:#087b83}}.part{{stroke:#27445c;stroke-width:1.5;fill-rule:evenodd}}</style>
<text x="65" y="55" class="title">Retainer capture tab · XY section at Z = 1 mm</text>
<path d="{flange}" class="part" fill="#e9bd67"/>
<path d="{retainer}" class="part" fill="#e78d69"/>
<text x="710" y="190" class="text">Gold: ceiling flange</text>
<text x="710" y="225" class="text">Orange: one installed retainer</text>
<text x="710" y="300" class="dim">Tail and outer tab: {RETAINER_TAIL_WIDTH:.2f} mm wide</text>
<text x="710" y="338" class="dim">Underside pocket: {pocket_width:.2f} mm wide</text>
<text x="710" y="376" class="text">Pocket clearance: {RETAINER_CAPTURE_XY_CLEARANCE:.2f} mm per side</text>
<text x="710" y="448" class="text">Left: 14 mm central beam.</text>
<text x="710" y="480" class="text">Right: outer ear with no side wings.</text>
<text x="65" y="810" class="text">The flange closes around the narrower tail; the tab seats in a 2 mm deep underside pocket.</text>
</svg>'''
    Path(__file__).with_suffix('.svg').write_text(svg + '\n')


if __name__ == '__main__':
    render()
