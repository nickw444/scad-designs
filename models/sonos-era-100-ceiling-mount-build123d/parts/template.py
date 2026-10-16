"""Thin ceiling cutout marking rim."""
from __future__ import annotations
from build123d import Pos
from parts.housing import (OUTER_X, OUTER_Y, OUTER_R, RETAINER_FIXINGS,
    RETAINER_BOSS_X, RETAINER_BOSS_Y, JOINT_FIXINGS, END_JOINT_FIXINGS,
    JOINT_BOSS_RADIUS, retainer_boss_xy)
from geometry import cylinder, rounded_prism


# Dimensions owned by this part (millimetres).
CEILING_CUTOUT_BOSS_CLEARANCE = 1.0
CEILING_CUTOUT_X = OUTER_X + 2 * CEILING_CUTOUT_BOSS_CLEARANCE
CEILING_CUTOUT_Y = OUTER_Y + 2 * CEILING_CUTOUT_BOSS_CLEARANCE
CEILING_CUTOUT_R = OUTER_R + CEILING_CUTOUT_BOSS_CLEARANCE

def ceiling_cutout_profile(z0,z1):
    opening=rounded_prism(CEILING_CUTOUT_X,CEILING_CUTOUT_Y,
                          CEILING_CUTOUT_R,z0,z1)
    for x,y in RETAINER_FIXINGS:
        opening += Pos(*retainer_boss_xy(x,y),0)*rounded_prism(
            RETAINER_BOSS_X+2*CEILING_CUTOUT_BOSS_CLEARANCE,
            RETAINER_BOSS_Y+2*CEILING_CUTOUT_BOSS_CLEARANCE,2,z0,z1)
    for x,y in JOINT_FIXINGS+END_JOINT_FIXINGS:
        opening += cylinder(x,y,JOINT_BOSS_RADIUS+CEILING_CUTOUT_BOSS_CLEARANCE,z0,z1)
    return opening.clean()

def ceiling_cutout_template():
    outer=ceiling_cutout_profile(0,1.5)
    inner=rounded_prism(CEILING_CUTOUT_X-12,CEILING_CUTOUT_Y-12,
                        CEILING_CUTOUT_R-6,-0.1,1.6)
    return (outer-inner).clean()
