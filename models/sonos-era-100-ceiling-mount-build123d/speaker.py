"""Measured and inferred Era 100 dummy used for assembly checks."""
from __future__ import annotations
from math import sqrt
from build123d import Edge, Face, Wire, extrude
from geometry import rounded_prism


# Dimensions owned by this part (millimetres).
SPEAKER_X = 120.0
SPEAKER_Y = 182.5
SPEAKER_DEPTH = 130.5
SPEAKER_FRONT_Z = 8.0
SPEAKER_FRONT_RADIUS = 60.0           # nearest full-width circular proxy for ≈3 mm end gap
SPEAKER_REAR_RADIUS = 66.3
CURVE_CENTRE_Z = SPEAKER_FRONT_Z + SPEAKER_DEPTH - SPEAKER_REAR_RADIUS

def speaker_mockup():
    half = SPEAKER_X/2
    front_side = SPEAKER_FRONT_Z + SPEAKER_FRONT_RADIUS - sqrt(SPEAKER_FRONT_RADIUS**2-half**2)
    rear_side = CURVE_CENTRE_Z + sqrt(SPEAKER_REAR_RADIUS**2-half**2)
    y = -SPEAKER_Y/2
    edges = [Edge.make_three_point_arc((-half,y,front_side),(0,y,SPEAKER_FRONT_Z),
                                       (half,y,front_side)),
             Edge.make_line((half,y,front_side),(half,y,rear_side)),
             Edge.make_three_point_arc((half,y,rear_side),
                                       (0,y,SPEAKER_FRONT_Z+SPEAKER_DEPTH),
                                       (-half,y,rear_side)),
             Edge.make_line((-half,y,rear_side),(-half,y,front_side))]
    side = extrude(Face(Wire(edges)), amount=SPEAKER_Y, dir=(0,1,0))
    return side & rounded_prism(SPEAKER_X,SPEAKER_Y,0.5,SPEAKER_FRONT_Z-1,
                                SPEAKER_FRONT_Z+SPEAKER_DEPTH+1)
