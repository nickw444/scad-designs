"""Regenerate the underside M3 head-clearance drawing beside this script."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from views.common import dimensioned_view
from cad_dimension_drawing import Leader, SectionDrawing
from parts import housing


def render():
    drawing=SectionDrawing(housing.ceiling_flange(), 'xy', 2.0)
    bores=drawing.round_holes(min_diameter=5.7,max_diameter=5.9)
    if len(bores)!=4:
        raise ValueError('Expected four M3 head counterbores')
    side=max(bores,key=lambda hole:hole.centre[0])
    end=max(bores,key=lambda hole:hole.centre[1])
    side_land=(side.centre[0]-housing.CAVITY_X/2-side.diameter_mm/2)
    end_land=(end.centre[1]-housing.CAVITY_Y/2-end.diameter_mm/2)
    dimensioned_view(
        __file__,drawing,title='Ceiling flange · M3 head clearance',
        dimensions=[],
        leaders=[
            Leader(side.centre,(92,65),f'Side inner land: {side_land:.2f} mm'),
            Leader(end.centre,(-95,130),f'End inner land: {end_land:.2f} mm'),
        ],
        notes=[
            'Underside section at Z = 2.0 mm shows four Ø5.8 mm counterbores.',
            f'Counterbore depth: {housing.JOINT_COUNTERBORE_DEPTH:.1f} mm in a {housing.FLANGE_THICKNESS:.1f} mm flange.',
            'Clearances are measured from each counterbore edge to the inner speaker opening.',
        ],
    )


if __name__=='__main__':
    render()
