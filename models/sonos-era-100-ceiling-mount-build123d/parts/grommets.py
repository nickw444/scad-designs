"""Alternative round and flat lead TPU cable sleeves."""
from __future__ import annotations
from parts.housing import CABLE_HOLE_DIAMETER, INNER_APEX_Z, OUTER_APEX_Z
from geometry import cylinder, rectangular_prism, rounded_prism


# Dimensions owned by this part (millimetres).
NOMINAL_CORD_OD = 6.0                  # measure cable before printing TPU seal
NOMINAL_FLAT_CORD_X = 6.0               # approximate figure-eight cable width
NOMINAL_FLAT_CORD_Y = 3.5               # measured figure-eight cable thickness
ROUND_CORD_COMPRESSION = 0.4            # reduction across full round bore diameter
FLAT_CORD_COMPRESSION = 0.1             # slight TPU squeeze across each full slot dimension
GROMMET_HEIGHT = OUTER_APEX_Z - INNER_APEX_Z + 2.8
GROMMET_FLANGE_THICKNESS = 1.5
GROMMET_FLANGE_RADIUS = CABLE_HOLE_DIAMETER/2 + 4.0  # 4 mm sealing land around roof hole
GROMMET_STEM_RADIUS = CABLE_HOLE_DIAMETER/2 + 0.1   # TPU press fit
GROMMET_SPLIT_LENGTH = 2 * (GROMMET_FLANGE_RADIUS + 2)

def cable_grommet():
    blank=cylinder(0,0,GROMMET_FLANGE_RADIUS,0,GROMMET_FLANGE_THICKNESS)+cylinder(0,0,GROMMET_STEM_RADIUS,
                                          GROMMET_FLANGE_THICKNESS,GROMMET_HEIGHT)
    blank-=cylinder(0,0,(NOMINAL_CORD_OD-ROUND_CORD_COMPRESSION)/2,
                    -0.1,GROMMET_HEIGHT+0.1)
    blank-=rectangular_prism(GROMMET_SPLIT_LENGTH,1,-0.1,GROMMET_HEIGHT+0.9,
                             GROMMET_SPLIT_LENGTH/2,0)
    return blank.clean()

def flat_cable_grommet():
    blank=cylinder(0,0,GROMMET_FLANGE_RADIUS,0,GROMMET_FLANGE_THICKNESS)+cylinder(0,0,GROMMET_STEM_RADIUS,
                                          GROMMET_FLANGE_THICKNESS,GROMMET_HEIGHT)
    slot_x=NOMINAL_FLAT_CORD_X-FLAT_CORD_COMPRESSION
    slot_y=NOMINAL_FLAT_CORD_Y-FLAT_CORD_COMPRESSION
    blank-=rounded_prism(slot_x,slot_y,slot_y/2-0.001,-0.1,GROMMET_HEIGHT+0.1)
    blank-=rectangular_prism(GROMMET_SPLIT_LENGTH,0.6,-0.1,GROMMET_HEIGHT+0.9,
                             GROMMET_SPLIT_LENGTH/2,0)
    return blank.clean()
