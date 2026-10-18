"""Zoomed XZ section of the inner-edge PETG locating rebate."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from build123d import Plane, section
from geometry import rectangular_prism
from parts import housing


def render():
    window = rectangular_prism(10, 0.2, 3, 10, 64.25, 0)
    scale = 70

    def px(x):
        return 95 + scale * (x - 59.25)

    def py(z):
        return 640 - scale * (z - 3)

    def cut_path(shape):
        cut = section(shape & window, section_by=Plane.XZ)
        contours = []
        for face in cut.faces():
            for wire in [face.outer_wire(), *face.inner_wires()]:
                points = [(point.X, point.Z) for point in wire.positions(deflection=0.04)]
                if len(points) >= 3:
                    contours.append('M ' + ' L '.join(
                        f'{px(x):.2f},{py(z):.2f}' for x, z in points) + ' Z')
        return ' '.join(contours)

    flange = cut_path(housing.ceiling_flange())
    shell = cut_path(housing.housing_shell())
    lip_top = housing.FLANGE_THICKNESS + housing.SEAM_LIP_HEIGHT
    rebate_top = housing.FLANGE_THICKNESS + housing.SEAM_REBATE_DEPTH
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="780" viewBox="0 0 1600 780">
<rect width="1600" height="780" fill="#f8fafc"/>
<style>.title{{font:700 27px Arial;fill:#17324d}}.body{{font:17px Arial;fill:#334b63}}.dim{{font:700 18px Arial;fill:#087b83}}.shape{{stroke:#27445c;stroke-width:1.7;fill-rule:evenodd}}</style>
<text x="60" y="55" class="title">Inner-edge rebate · XZ section at Y = 0</text>
<path d="{flange}" class="shape" fill="#e9bd67"/>
<path d="{shell}" class="shape" fill="#6b95c8"/>
<line x1="60" y1="{py(housing.FLANGE_THICKNESS):.1f}" x2="790" y2="{py(housing.FLANGE_THICKNESS):.1f}" stroke="#087b83" stroke-dasharray="5 5"/>
<text x="810" y="{py(housing.FLANGE_THICKNESS)+30:.1f}" class="dim">PETG faces meet · Z = 6</text>
<text x="810" y="205" class="body">Gold: flange locating lip</text>
<text x="810" y="235" class="body">Blue: shell inner-edge rebate</text>
<text x="810" y="290" class="dim">Lip: {housing.SEAM_LIP_WIDTH:.2f} wide × {housing.SEAM_LIP_HEIGHT:.1f} high</text>
<text x="810" y="322" class="dim">Rebate: {housing.SEAM_REBATE_WIDTH:.2f} into wall × {housing.SEAM_REBATE_DEPTH:.1f} deep</text>
<text x="810" y="354" class="body">Outer-flank clearance: {housing.SEAM_REBATE_WIDTH-housing.SEAM_LIP_WIDTH:.2f}</text>
<text x="810" y="382" class="body">Tip clearance: {rebate_top-lip_top:.2f}; outer wall retained: {housing.SIDE_WALL-housing.SEAM_REBATE_WIDTH:.2f}</text>
<text x="60" y="735" class="body">The inner-edge lip stops at the two retainer slots; widened shell bosses cover those openings.</text>
</svg>'''
    Path(__file__).with_suffix('.svg').write_text(svg + '\n')


if __name__ == '__main__':
    render()
