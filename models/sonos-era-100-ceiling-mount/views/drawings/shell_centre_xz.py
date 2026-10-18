"""Regenerate the housing shell centreline profile drawing."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from views.common import dimensioned_view
from cad_dimension_drawing import LinearDimension, SectionDrawing, span_dimension
from parts.housing import housing_shell
from speaker import SPEAKER_DEPTH, SPEAKER_FRONT_Z


def render():
    drawing = SectionDrawing(housing_shell(), 'xz', 0)
    profile = drawing.section_bounds
    overall = drawing.overall_bounds
    roof_levels = drawing.horizontal_levels_at(0)
    inner_roof = max(z for z in roof_levels if z < profile.max_v - 0.1)
    insertion_depth = inner_roof - profile.min_v
    nominal_available = inner_roof - SPEAKER_FRONT_Z
    dimensioned_view(
        __file__, drawing, title='Housing shell · centreline profile',
        dimensions=[
            span_dimension(profile, 'u', side='min', offset=-18),
            span_dimension(profile, 'v', side='min', offset=20),
            LinearDimension((0, profile.min_v), (0, inner_roof), 0,
                            prefix='Insertion depth '),
        ],
        notes=[
            f'Overall shell height: {overall.height:.2f} mm; maximum XY width: '
            f'{drawing.shape.bounding_box().size.X:.2f} mm.',
            f'Shell mouth to inner roof: {insertion_depth:.2f} mm. '
            f'From nominal speaker front: {nominal_available:.2f} mm.',
            f'Nominal speaker depth: {SPEAKER_DEPTH:.2f} mm; '
            f'rear clearance at this position: {nominal_available-SPEAKER_DEPTH:.2f} mm.',
            'Profile is the exact cut through Y = 0; its width differs from the maximum shell width.',
        ],
    )


if __name__ == '__main__':
    render()
