"""Two removable front end stops; print two identical parts."""
from __future__ import annotations
from math import sqrt
from build123d import Edge, Face, Wire, extrude
from speaker import SPEAKER_FRONT_Z, SPEAKER_FRONT_RADIUS
from parts.housing import (RETAINER_SEAT_DEPTH, RETAINER_BAR_LENGTH, RETAINER_Y,
    RETAINER_FIXINGS, RETAINER_PAD_TOP_Z, RETAINER_PAD_CLEARANCE_WIDTH,
    RETAINER_PAD_CLEARANCE_LENGTH, retainer_pad_xy)
from geometry import cylinder, rectangular_prism


# Dimensions owned by this part (millimetres).
RETAINER_PAD_GAP = 0.8                 # room for a compliant contact pad
RETAINER_CONTACT_HALF_WIDTH = 40.0    # front contact spans X = -40..40
RETAINER_PAD_WIDTH = RETAINER_PAD_CLEARANCE_WIDTH - 0.30  # X fit
RETAINER_PAD_LENGTH = RETAINER_PAD_CLEARANCE_LENGTH - 0.40  # 0.2 mm each Y side
RETAINER_BOLT_RADIUS = 1.45           # measured Ø2.9 thread
RETAINER_BOLT_CLEARANCE_RADIUS = 1.65 # Ø3.3 clearance
RETAINER_HEAD_RADIUS = 2.65           # measured Ø5.3 head
RETAINER_HEAD_HEIGHT = 2.9
RETAINER_HEAD_BORE_RADIUS = 2.8        # Ø5.6 counterbore
RETAINER_HEAD_BORE_DEPTH = 4.5        # deeper seat keeps 10 mm M3 bolt engaged
RETAINER_BOLT_UNDER_HEAD_LENGTH = 10.0

def curved_front_beam(y):
    half = RETAINER_CONTACT_HALF_WIDTH
    centre_z = SPEAKER_FRONT_Z - RETAINER_PAD_GAP
    edge_z = centre_z + SPEAKER_FRONT_RADIUS - sqrt(SPEAKER_FRONT_RADIUS**2-half**2)
    edges = [Edge.make_line((-half,y-5,RETAINER_SEAT_DEPTH),
                            (half,y-5,RETAINER_SEAT_DEPTH)),
             Edge.make_line((half,y-5,RETAINER_SEAT_DEPTH), (half,y-5,edge_z)),
             Edge.make_three_point_arc((half,y-5,edge_z),(0,y-5,centre_z),
                                       (-half,y-5,edge_z)),
             Edge.make_line((-half,y-5,edge_z),(-half,y-5,RETAINER_SEAT_DEPTH))]
    return extrude(Face(Wire(edges)), amount=10, dir=(0,1,0))

def end_retainer_base(z0=0, z1=RETAINER_SEAT_DEPTH):
    return rectangular_prism(RETAINER_BAR_LENGTH,10,z0,z1,0,-RETAINER_Y)

def end_retainer():
    part = end_retainer_base() + curved_front_beam(-RETAINER_Y)
    for sx in (-1,1):
        x,y=sx*abs(RETAINER_FIXINGS[0][0]),-RETAINER_Y
        part += rectangular_prism(RETAINER_PAD_WIDTH,RETAINER_PAD_LENGTH,
                                   RETAINER_SEAT_DEPTH,RETAINER_PAD_TOP_Z,
                                   *retainer_pad_xy(x,y))
    for sx in (-1,1):
        x,y=sx*abs(RETAINER_FIXINGS[0][0]),-RETAINER_Y
        part -= cylinder(x,y,RETAINER_BOLT_CLEARANCE_RADIUS,-0.1,RETAINER_PAD_TOP_Z+0.1)
        part -= cylinder(x,y,RETAINER_HEAD_BORE_RADIUS,-0.1,RETAINER_HEAD_BORE_DEPTH)
    return part.clean()
