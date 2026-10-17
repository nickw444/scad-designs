"""Regenerate the seated-speaker XZ assembly section and insertion dimensions."""
from __future__ import annotations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from build123d import Plane, Pos, section
from assembly import make_assembly
from geometry import rectangular_prism
from speaker import MEASURED_SPEAKER_DEPTH, SPEAKER_FRONT_Z, speaker_mockup
from parts.housing import RETAINER_CENTRE_HEIGHT, RETAINER_Y


SECTION_Y = RETAINER_Y  # opposite the rear cable opening, through the north retainer
PIXELS_PER_MM = 6.0


def render():
    assembly = make_assembly()
    shell = assembly.get('housing-shell')
    retainer = assembly.get('retainer-north')
    seating_shift = RETAINER_CENTRE_HEIGHT - SPEAKER_FRONT_Z
    speaker = Pos(0, 0, seating_shift) * speaker_mockup(depth=MEASURED_SPEAKER_DEPTH)
    probe = rectangular_prism(0.02, 0.02, 0, 200, 0, SECTION_Y)
    contact_z = (retainer & probe).bounding_box().max.Z
    speaker_front_z = (speaker & probe).bounding_box().min.Z
    speaker_rear_z = (speaker & probe).bounding_box().max.Z
    inner_roof_z = (shell & probe).bounding_box().min.Z
    available = inner_roof_z-contact_z
    rear_gap = inner_roof_z-speaker_rear_z
    if abs(speaker_front_z-contact_z)>0.02 or rear_gap<0:
        raise ValueError('Measured speaker is not seated or intersects the rear roof')

    def px(x):
        return 500 + PIXELS_PER_MM*x
    def py(z):
        return 1040 - PIXELS_PER_MM*z
    def path_for(shape):
        cut = section(shape, section_by=Plane.XZ.offset(-SECTION_Y))
        paths = []
        for face in cut.faces():
            for wire in [face.outer_wire(), *face.inner_wires()]:
                points = [(p.X,p.Z) for p in wire.positions(deflection=0.12)]
                if len(points)>=3:
                    paths.append('M '+' L '.join(f'{px(x):.2f},{py(z):.2f}'
                                                   for x,z in points)+' Z')
        return ' '.join(paths)

    components = [
        ('housing shell', shell, '#93b4d6'),
        ('ceiling flange', assembly.get('ceiling-flange'), '#e9c47d'),
        ('grille', assembly.get('grille'), '#a8d6c4'),
        ('end retainer', retainer, '#ec916e'),
        ('measured speaker envelope', speaker, '#cbd5e1'),
    ]
    elements = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1550" height="1200" viewBox="0 0 1550 1200">',
        '<rect width="1550" height="1200" fill="#f8fafc"/>',
        '<text x="75" y="55" class="title">Era 100 · seated assembly depth</text>',
        f'<text x="75" y="85" class="sub">XZ section at Y = {SECTION_Y:g} mm through one end retainer · dimensions in mm</text>',
        '<style>.title{font:700 29px Arial,sans-serif;fill:#17324d}.sub{font:17px Arial,sans-serif;fill:#526779}'
        '.part{stroke:#27445c;stroke-width:1.35;fill-rule:evenodd}.dim{stroke:#147c82;stroke-width:2;fill:none}'
        '.dimtext{font:700 17px Arial,sans-serif;fill:#0b666b}.note{font:16px Arial,sans-serif;fill:#40566b}'
        '.guide{stroke:#7f9caf;stroke-width:1.2;stroke-dasharray:5 5}</style>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto-start-reverse">'
        '<path d="M8 0 L0 4 L8 8" fill="none" stroke="#147c82" stroke-width="1.4"/></marker></defs>',
    ]
    for name, shape, colour in components:
        d = path_for(shape)
        if d:
            elements.append(f'<path class="part" d="{d}" fill="{colour}" fill-opacity="0.84"/>')
    for z in (contact_z, speaker_rear_z, inner_roof_z):
        elements.append(f'<path class="guide" d="M {px(0):.2f},{py(z):.2f} L 1190,{py(z):.2f}"/>')
    for x, lo, hi in ((1000,contact_z,inner_roof_z),
                      (1090,speaker_front_z,speaker_rear_z),
                      (1180,speaker_rear_z,inner_roof_z)):
        elements.append(f'<path class="dim" d="M {x},{py(lo):.2f} L {x},{py(hi):.2f}" '
                        'marker-start="url(#arrow)" marker-end="url(#arrow)"/>')
    elements += [
        f'<text class="dimtext" transform="translate(984,{(py(contact_z)+py(inner_roof_z))/2:.2f}) rotate(-90)" text-anchor="middle">{available:.2f} available from retainer to roof</text>',
        f'<text class="dimtext" transform="translate(1074,{(py(speaker_front_z)+py(speaker_rear_z))/2:.2f}) rotate(-90)" text-anchor="middle">{MEASURED_SPEAKER_DEPTH:.2f} measured speaker depth</text>',
        f'<text class="dimtext" x="1210" y="{py(inner_roof_z)+18:.2f}">{rear_gap:.2f} rear gap</text>',
        f'<text class="note" x="75" y="1105">Seated speaker front: Z = {speaker_front_z:.2f}; rear apex: Z = {speaker_rear_z:.2f}; inner roof: Z = {inner_roof_z:.2f}.</text>',
        f'<text class="note" x="75" y="1132">At the unseated dummy front Z = {SPEAKER_FRONT_Z:.2f}, the same 130.70 mm depth would leave {inner_roof_z-SPEAKER_FRONT_Z-MEASURED_SPEAKER_DEPTH:.2f} mm behind it.</text>',
        '<text class="note" x="75" y="1159">The speaker outline is an inferred envelope, not a scan. Blue shell · gold flange · orange retainer · grey speaker · green grille.</text>',
        '</svg>',
    ]
    Path(__file__).with_suffix('.svg').write_text('\n'.join(elements)+'\n')
    return {'retainer_to_inner_roof_mm':available,
            'measured_speaker_depth_mm':MEASURED_SPEAKER_DEPTH,
            'seated_rear_gap_mm':rear_gap}


if __name__=='__main__':
    print(render())
