"""Optional flat TPU gasket at the flange-to-shell joint."""
from __future__ import annotations
from build123d import Pos, Rot
from parts.housing import FLANGE_RADIUS, FLANGE_THICKNESS, ceiling_flange, housing_shell
from parts.retainers import end_retainer
from geometry import cylinder


# Dimensions owned by this part (millimetres).
FLAT_GASKET_THICKNESS = 0.60          # optional face gasket, three 0.2 mm layers

def flat_seam_gasket():
    z,t=FLANGE_THICKNESS,FLAT_GASKET_THICKNESS
    shell_face = housing_shell() & cylinder(0,0,FLANGE_RADIUS+2,z,z+t)
    stop=end_retainer()
    mating_face=ceiling_flange()+stop+Rot(Z=180)*stop
    flange_face = Pos(0,0,t)*(mating_face & cylinder(0,0,FLANGE_RADIUS+2,z-t,z))
    return (shell_face & flange_face).clean()
