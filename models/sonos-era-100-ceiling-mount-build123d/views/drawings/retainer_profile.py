"""Regenerate the exact central XZ section of the current retainer."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from views.common import dimensioned_view
from cad_dimension_drawing import Leader, SectionDrawing, span_dimension
from parts.retainers import end_retainer, RETAINER_CONTACT_HALF_WIDTH
from parts.housing import (RETAINER_CENTRE_LENGTH, RETAINER_SEAT_XY_CLEARANCE,
                           RETAINER_TAIL_WIDTH)


def render():
    drawing=SectionDrawing(end_retainer(),'xz',82)
    bounds=drawing.section_bounds
    dimensioned_view(
        __file__,drawing,title='End retainer · contact and shoulders',
        dimensions=[span_dimension(bounds,'u',side='min',offset=-7),
                    span_dimension(bounds,'v',side='max',offset=12)],
        leaders=[Leader((50,13),(55,29),'Raised shoulder to fixing'),
                 Leader((0,7.2),(-44,32),'R60 speaker contact')],
        notes=[
            f'Exact XZ section at Y = -82 mm; contact ends at X = ±{RETAINER_CONTACT_HALF_WIDTH:.0f} mm.',
            f'Shoulders extend to X = ±{RETAINER_CENTRE_LENGTH/2:.2f} mm within the 14 mm bar width.',
            f'Flange slot now gives {RETAINER_SEAT_XY_CLEARANCE:.2f} mm insertion clearance on each side.',
            f'Only the fixing tails narrow to {RETAINER_TAIL_WIDTH:.1f} mm; central load beam remains 14 mm wide.',
        ],
    )


if __name__=='__main__':
    render()
