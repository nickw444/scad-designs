"""Regenerate flange section with measured screw-hole callouts."""
from pathlib import Path
from math import hypot
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from views.common import dimensioned_view
from cad_dimension_drawing import Leader, SectionDrawing, span_dimension
from parts.housing import ceiling_flange


def render():
    drawing = SectionDrawing(ceiling_flange(), 'xy', 5)
    section_bounds = drawing.section_bounds
    overall = drawing.overall_bounds
    ceiling_holes = drawing.round_holes(min_diameter=3.9, max_diameter=4.1)
    joint_holes = drawing.round_holes(min_diameter=3.2, max_diameter=3.4)
    if len(ceiling_holes) != 6 or len(joint_holes) != 4:
        raise ValueError('Unexpected flange screw-hole count or diameter')
    ceiling = max(ceiling_holes, key=lambda h: h.centre[0] + h.centre[1])
    joint = max(joint_holes, key=lambda h: h.centre[0] + h.centre[1])
    pcd = 2 * sum(hypot(*h.centre) for h in ceiling_holes) / len(ceiling_holes)
    dimensioned_view(
        __file__, drawing, title='Ceiling flange · fixing section',
        dimensions=[span_dimension(section_bounds, 'u', side='min',
                                   offset=-16, prefix='Ø')],
        leaders=[
            Leader(ceiling.centre, (55, 137),
                   f'6 × Ø{ceiling.diameter_mm:.2f} mm ceiling screws'),
            Leader(joint.centre, (-105, 137),
                   f'4 × Ø{joint.diameter_mm:.2f} mm M3 joins'),
        ],
        notes=[
            f'Overall flange OD: Ø{overall.width:.2f} mm; screw pitch circle: Ø{pcd:.2f} mm.',
            f'Flange thickness: {drawing.shape.bounding_box().size.Z:.2f} mm.',
            'Four M3 × 10 mm cap bolts: Ø5.8 × 4.0 mm head counterbores.',
            'The section outline is slightly inset from the overall OD by the grille clip relief.',
        ],
    )


if __name__ == '__main__':
    render()
