"""Optional flat TPU gasket at the flange-to-shell joint."""
from __future__ import annotations
from parts.housing import FLANGE_RADIUS, FLANGE_THICKNESS, housing_shell
from geometry import cylinder


# Dimensions owned by this part (millimetres).
FLAT_GASKET_THICKNESS = 0.60          # optional face gasket, three 0.2 mm layers

def flat_seam_gasket():
    z,t=FLANGE_THICKNESS,FLAT_GASKET_THICKNESS
    # A continuous shell-footprint sheet bridges the small assembly clearances
    # beside the removable retainers instead of splitting into loose islands.
    return (housing_shell() & cylinder(0,0,FLANGE_RADIUS+2,z,z+t)).clean()
