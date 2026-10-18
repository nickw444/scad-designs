"""Regenerate the shell opening drawing at the speaker insertion depth."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from views.common import dimensioned_view
from cad_dimension_drawing import SectionDrawing, span_dimension
from parts.housing import housing_shell


def render():
    drawing = SectionDrawing(housing_shell(), 'xy', 20)
    outer = drawing.section_bounds
    opening = drawing.largest_opening()
    overall = drawing.overall_bounds
    dimensioned_view(
        __file__, drawing, title='Housing shell · speaker insertion section',
        dimensions=[
            span_dimension(outer, 'u', side='min', offset=-14),
            span_dimension(outer, 'v', side='min', offset=17),
            span_dimension(opening, 'u', side='max', offset=-13),
            span_dimension(opening, 'v', side='max', offset=13),
        ],
        notes=[
            f'Inner opening at this depth: {opening.width:.2f} × {opening.height:.2f} mm.',
            f'Overall shell XY envelope: {overall.width:.2f} × {overall.height:.2f} mm.',
            'Dimensions are measured from the native build123d section and part bounds.',
        ],
    )


if __name__ == '__main__':
    render()
