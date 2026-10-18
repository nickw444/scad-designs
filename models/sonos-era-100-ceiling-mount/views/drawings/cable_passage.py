"""Dimension the rear cable opening where the factory plug passes through."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from views.common import dimensioned_view
from cad_dimension_drawing import LinearDimension, SectionDrawing
from parts.housing import (ASSUMED_PLUG_DIAMETER, CABLE_EXIT_Y,
                           CABLE_HOLE_DIAMETER, INNER_APEX_Z, OUTER_APEX_Z,
                           housing_shell)
from parts.grommets import GROMMET_FLANGE_RADIUS


def render():
    drawing = SectionDrawing(housing_shell(), 'xy',
                             (INNER_APEX_Z + OUTER_APEX_Z) / 2)
    holes = drawing.round_holes(min_diameter=31.9, max_diameter=32.1)
    if len(holes) != 1 or abs(holes[0].centre[1] - CABLE_EXIT_Y) > 0.01:
        raise ValueError('Expected one circular rear cable passage at the design centre')
    hole = holes[0]
    x, y = hole.centre
    radius = hole.diameter_mm / 2
    dimensioned_view(
        __file__, drawing, title='Housing shell · factory plug passage',
        dimensions=[LinearDimension((x-radius, y), (x+radius, y), 22, prefix='Ø')],
        notes=[
            f'Passage: Ø{CABLE_HOLE_DIAMETER:.1f} mm. Measured plug: approximately '
            f'{ASSUMED_PLUG_DIAMETER:.1f} mm across.',
            f'Nominal radial clearance: '
            f'{(CABLE_HOLE_DIAMETER-ASSUMED_PLUG_DIAMETER)/2:.1f} mm.',
            f'Split TPU grommet flange: Ø{2*GROMMET_FLANGE_RADIUS:.1f} mm; '
            f'{GROMMET_FLANGE_RADIUS-radius:.1f} mm cover around passage.',
            'Feed the plug through the shell, then press the split grommet around the lead.',
        ],
    )


if __name__ == '__main__':
    render()
