"""Two removable front end stops; print two identical parts."""
from __future__ import annotations
from math import sqrt
from build123d import Edge, Face, Wire, extrude
from speaker import SPEAKER_FRONT_Z, SPEAKER_FRONT_RADIUS
from parts.housing import (RETAINER_SEAT_DEPTH, RETAINER_CENTRE_HEIGHT,
    RETAINER_CENTRE_LENGTH, RETAINER_BAR_LENGTH, RETAINER_BAR_WIDTH,
    RETAINER_TAIL_WIDTH, RETAINER_Y,
    RETAINER_FIXINGS, RETAINER_PAD_TOP_Z, RETAINER_PAD_CLEARANCE_WIDTH,
    RETAINER_PAD_CLEARANCE_LENGTH, RETAINER_CAPTURE_OVERHANG,
    RETAINER_CAPTURE_ROOT, RETAINER_CAPTURE_PAD_HEIGHT,
    M3_THREAD_RADIUS, M3_CLEARANCE_RADIUS,
    M3_HEAD_RADIUS, M3_HEAD_HEIGHT, M3_BOLT_UNDER_HEAD_LENGTH,
    M3_COUNTERBORE_RADIUS, retainer_pad_xy)
from geometry import cylinder, polygon_xz, rectangular_prism


# Dimensions owned by this part (millimetres).
RETAINER_PAD_GAP = SPEAKER_FRONT_Z - RETAINER_CENTRE_HEIGHT
RETAINER_CONTACT_HALF_WIDTH = 40.0    # front contact spans X = -40..40
RETAINER_PAD_WIDTH = RETAINER_PAD_CLEARANCE_WIDTH - 0.60  # 0.3 mm each X side
RETAINER_PAD_LENGTH = RETAINER_PAD_CLEARANCE_LENGTH - 0.60  # 0.3 mm each Y side
RETAINER_BOLT_RADIUS = M3_THREAD_RADIUS
RETAINER_BOLT_CLEARANCE_RADIUS = M3_CLEARANCE_RADIUS
RETAINER_HEAD_RADIUS = M3_HEAD_RADIUS
RETAINER_HEAD_HEIGHT = M3_HEAD_HEIGHT
RETAINER_HEAD_BORE_RADIUS = M3_COUNTERBORE_RADIUS
RETAINER_HEAD_BORE_DEPTH = 4.0        # 1 mm head recess; 10 mm bolt still engages insert
RETAINER_BOLT_UNDER_HEAD_LENGTH = M3_BOLT_UNDER_HEAD_LENGTH

def curved_front_beam(y):
    half = RETAINER_CONTACT_HALF_WIDTH
    centre_z = SPEAKER_FRONT_Z - RETAINER_PAD_GAP
    edge_z = centre_z + SPEAKER_FRONT_RADIUS - sqrt(SPEAKER_FRONT_RADIUS**2-half**2)
    y0 = y - RETAINER_BAR_WIDTH / 2
    bottom_z = RETAINER_CENTRE_HEIGHT - 0.3  # overlap avoids a zero-thickness arc tip
    edges = [Edge.make_line((-half,y0,bottom_z),
                            (half,y0,bottom_z)),
             Edge.make_line((half,y0,bottom_z), (half,y0,edge_z)),
             Edge.make_three_point_arc((half,y0,edge_z),(0,y0,centre_z),
                                       (-half,y0,edge_z)),
             Edge.make_line((-half,y0,edge_z),(-half,y0,bottom_z))]
    return extrude(Face(Wire(edges)), amount=RETAINER_BAR_WIDTH, dir=(0,1,0))

def end_retainer_base(z0=0, z1=RETAINER_SEAT_DEPTH):
    base=rectangular_prism(RETAINER_CENTRE_LENGTH,RETAINER_BAR_WIDTH,
                           z0,z1,0,-RETAINER_Y)
    tail_start=RETAINER_CENTRE_LENGTH/2-0.5
    tail_end=RETAINER_BAR_LENGTH/2
    for sx in (-1,1):
        base += rectangular_prism(tail_end-tail_start,RETAINER_TAIL_WIDTH,
                                  z0,z1,sx*(tail_start+tail_end)/2,-RETAINER_Y)
    return base


def contact_shoulder(sign):
    """Fill the unused space between the curved contact and each fixing end."""
    half=RETAINER_CONTACT_HALF_WIDTH
    start=half-1.0  # 1 mm overlap beneath the curved contact
    end=RETAINER_CENTRE_LENGTH/2
    centre_z=SPEAKER_FRONT_Z-RETAINER_PAD_GAP
    def arc_z(x):
        return centre_z+SPEAKER_FRONT_RADIUS-sqrt(SPEAKER_FRONT_RADIUS**2-x*x)
    profile=[(start,RETAINER_SEAT_DEPTH),(end,RETAINER_SEAT_DEPTH),
             (end,RETAINER_CENTRE_HEIGHT),(half,arc_z(half)-0.2),
             (start,arc_z(start)-0.2)]
    if sign<0:
        profile=[(-x,z) for x,z in reversed(profile)]
    return polygon_xz(profile,-RETAINER_Y-RETAINER_BAR_WIDTH/2,
                      -RETAINER_Y+RETAINER_BAR_WIDTH/2)


def capture_pad(x,y):
    sign=1 if x>0 else -1
    cx=sign*(RETAINER_BAR_LENGTH/2+
             (RETAINER_CAPTURE_OVERHANG-RETAINER_CAPTURE_ROOT)/2)
    return rectangular_prism(RETAINER_CAPTURE_OVERHANG+RETAINER_CAPTURE_ROOT,
                             RETAINER_TAIL_WIDTH,0,RETAINER_CAPTURE_PAD_HEIGHT,cx,y)

def end_retainer():
    part = end_retainer_base()
    part += rectangular_prism(RETAINER_CENTRE_LENGTH,RETAINER_BAR_WIDTH,
                              RETAINER_SEAT_DEPTH,RETAINER_CENTRE_HEIGHT,
                              0,-RETAINER_Y)
    part += curved_front_beam(-RETAINER_Y)
    part += contact_shoulder(-1)
    part += contact_shoulder(1)
    for sx in (-1,1):
        x,y=sx*abs(RETAINER_FIXINGS[0][0]),-RETAINER_Y
        part += capture_pad(x,y)
        part += rectangular_prism(RETAINER_PAD_WIDTH,RETAINER_PAD_LENGTH,
                                   RETAINER_SEAT_DEPTH,RETAINER_PAD_TOP_Z,
                                   *retainer_pad_xy(x,y))
    for sx in (-1,1):
        x,y=sx*abs(RETAINER_FIXINGS[0][0]),-RETAINER_Y
        part -= cylinder(x,y,RETAINER_BOLT_CLEARANCE_RADIUS,-0.1,RETAINER_PAD_TOP_Z+0.1)
        part -= cylinder(x,y,RETAINER_HEAD_BORE_RADIUS,-0.1,RETAINER_HEAD_BORE_DEPTH)
    return part.clean()
