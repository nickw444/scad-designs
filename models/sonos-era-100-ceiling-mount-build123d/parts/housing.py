"""Ceiling flange and separate speaker shell."""
from __future__ import annotations
from math import ceil, cos, radians, sin, sqrt
from build123d import Circle, Pos, Rectangle, Rot, loft
from speaker import (SPEAKER_X, SPEAKER_Y, SPEAKER_DEPTH, SPEAKER_FRONT_Z,
                     SPEAKER_REAR_RADIUS, CURVE_CENTRE_Z)
from geometry import cylinder, cone, rectangular_prism, rounded_prism, polygon_xz, radial_profile


# Dimensions owned by this part (millimetres).
PLAN_CLEARANCE = 2.0
REAR_CLEARANCE = 8.0
SIDE_WALL = 4.5
ROOF_WALL = 7.0
ROOF_SHOULDER_HALF_WIDTH = 10.0       # virtual apex before the flat truncation
ROOF_VERTICAL_WALL = 10.0             # 7.1 mm normal thickness on 45° faces
ROOF_CENTRE_CLEARANCE = 5.0           # dummy speaker rear apex to inner flat
FLANGE_RADIUS = 122.5                 # Ø245; preserves 4 mm land beyond cutout
FLANGE_THICKNESS = 6.0
RETAINER_SEAT_DEPTH = FLANGE_THICKNESS  # open channel: retainer passes through the flange
RETAINER_CENTRE_HEIGHT = SPEAKER_FRONT_Z - 0.8  # full beam reaches front-contact height
RETAINER_CENTRE_LENGTH = 123.0         # 0.5 mm clearance each side within 124 mm cavity
RETAINER_BAR_WIDTH = 14.0             # widened load-bearing span
RETAINER_CAPTURE_OVERHANG = 3.0       # outer-end flange bearing, beyond the bar
RETAINER_CAPTURE_ROOT = 0.5          # overlap into bar for a single solid
RETAINER_CAPTURE_PAD_HEIGHT = 2.0    # flat bearing tab; flange pocket uses supports
RETAINER_CAPTURE_XY_CLEARANCE = 0.2
CLIP_LIP_TOP_Z = 0.68
CLIP_SHOULDER_TOP_Z = 0.78
CLIP_RECESS = 0.7
MAGNET_DIAMETER = 10.2                 # 0.2 mm diameter clearance for Ø10 magnets
MAGNET_POCKET_DEPTH = 1.80            # 1.7 mm magnet + 0.1 mm adhesive; 2.2 mm roof
ASSUMED_PLUG_DIAMETER = 30.0           # owner estimate; measure factory plug before final print
CABLE_HOLE_DIAMETER = 32.0             # 1 mm radial clearance around estimated plug
CABLE_EXIT_Y = -69.0                   # provisional; check power-port location
CAVITY_X = SPEAKER_X + 2 * PLAN_CLEARANCE
CAVITY_Y = SPEAKER_Y + 2 * PLAN_CLEARANCE
CAVITY_R = 2.0
OUTER_X = CAVITY_X + 2 * SIDE_WALL
OUTER_Y = CAVITY_Y + 2 * SIDE_WALL
OUTER_R = CAVITY_R + SIDE_WALL
ROOF_TANGENT_X = SPEAKER_REAR_RADIUS / sqrt(2)
INNER_SHOULDER_APEX_Z = float(ceil(CURVE_CENTRE_Z + ROOF_TANGENT_X +
                                   REAR_CLEARANCE + ROOF_TANGENT_X -
                                   ROOF_SHOULDER_HALF_WIDTH))
OUTER_SHOULDER_APEX_Z = INNER_SHOULDER_APEX_Z + ROOF_VERTICAL_WALL
INNER_APEX_Z = SPEAKER_FRONT_Z + SPEAKER_DEPTH + ROOF_CENTRE_CLEARANCE
OUTER_APEX_Z = INNER_APEX_Z + ROOF_WALL
INNER_FLAT_HALF_WIDTH = (ROOF_SHOULDER_HALF_WIDTH +
                         INNER_SHOULDER_APEX_Z - INNER_APEX_Z)
OUTER_FLAT_HALF_WIDTH = (ROOF_SHOULDER_HALF_WIDTH +
                         OUTER_SHOULDER_APEX_Z - OUTER_APEX_Z)
MAGNETS = [
    (sx * 94.0, sy * 36.0) for sx in (-1, 1) for sy in (-1, 1)
] + [
    (sx * 18.0, sy * 112.0) for sx in (-1, 1) for sy in (-1, 1)
]
CEILING_SCREW_RADIUS = 110.5
CEILING_SCREW_HOLE_RADIUS = 2.0       # Ø4.0 clearance for nominal Ø3.5 6g thread
CEILING_COUNTERSINK_RADIUS = 3.8     # Ø7.6 fits heads up to about Ø7.1
CEILING_COUNTERSINK_DEPTH = 2.05     # ~82° included angle; leaves 3.95 mm flange
CEILING_SCREWS = [
    (CEILING_SCREW_RADIUS * cos(radians(angle)),
     CEILING_SCREW_RADIUS * sin(radians(angle)))
    for angle in (90, 150, 210, 270, 330, 30)
]
RETAINER_Y = 82.0                       # bring end bosses inward for ceiling seal land
RETAINER_FIXINGS = [(sx * 67.2, sy * RETAINER_Y)
                    for sx in (-1, 1) for sy in (-1, 1)]
RETAINER_BOSS_X = 10.2                 # M3 seat clears swept speaker envelope
RETAINER_BOSS_Y = 12.8                 # 1.4 mm wall around full-width socket
RETAINER_BOSS_OUTWARD_OFFSET = 0.0
RETAINER_BOSS_RAMP_RISE = 8.0          # rear-down print: <45° outward growth
RETAINER_PAD_CLEARANCE_WIDTH = 7.65   # outer edge meets the seat end; no bridge island
RETAINER_PAD_CLEARANCE_LENGTH = 10.0  # local fixing pad is narrower than the full beam
RETAINER_PAD_OUTWARD_OFFSET = 0.475   # preserves gasket clearance at inner edge
RETAINER_PAD_TOP_Z = FLANGE_THICKNESS + 1.7
RETAINER_INSERT_BODY_RADIUS = 2.2      # measured Ø4.4 M3 insert
RETAINER_INSERT_TIP_RADIUS = 1.95      # measured Ø3.9 lead-in
RETAINER_INSERT_PILOT_RADIUS = 2.0     # Ø4.0 heat-set pilot
RETAINER_INSERT_PILOT_DEPTH = 9.0     # clears 10 mm bolt measured under head
M3_THREAD_RADIUS = 1.45               # measured Ø2.9 thread
M3_HEAD_RADIUS = 2.75                 # inventory Ø5.5 cap head
M3_HEAD_HEIGHT = 3.0
M3_BOLT_UNDER_HEAD_LENGTH = 10.0
M3_CLEARANCE_RADIUS = 1.65           # Ø3.3 through-hole
M3_COUNTERBORE_RADIUS = 2.9          # Ø5.8 for head clearance
JOINT_SIDE_FIXINGS = [(sx * 66.2, 0.0) for sx in (-1, 1)]
JOINT_END_FIXINGS = [(0.0, sy * 96.5) for sy in (-1, 1)]
JOINT_FIXINGS = JOINT_SIDE_FIXINGS + JOINT_END_FIXINGS
JOINT_BOSS_RADIUS = 4.0               # 2 mm wall around Ø4 insert pilot
JOINT_BOSS_TOP_Z = FLANGE_THICKNESS + 10.0
JOINT_BOSS_RAMP_RISE = 8.5             # rear-down print: <45° outward growth
JOINT_INSERT_BODY_RADIUS = RETAINER_INSERT_BODY_RADIUS
JOINT_INSERT_TIP_RADIUS = RETAINER_INSERT_TIP_RADIUS
JOINT_INSERT_HOLE_RADIUS = RETAINER_INSERT_PILOT_RADIUS
JOINT_INSERT_DEPTH = 9.0
JOINT_BOLT_CLEARANCE_RADIUS = M3_CLEARANCE_RADIUS
JOINT_BOLT_UNDER_HEAD_LENGTH = M3_BOLT_UNDER_HEAD_LENGTH
JOINT_COUNTERBORE_RADIUS = M3_COUNTERBORE_RADIUS
JOINT_COUNTERBORE_DEPTH = 4.0         # 1 mm recess for the 3 mm cap head
RETAINER_BAR_LENGTH = 143.0           # full-height base reaches both fixing bores


def retainer_boss_xy(x, y):
    return x + (RETAINER_BOSS_OUTWARD_OFFSET if x > 0 else
                -RETAINER_BOSS_OUTWARD_OFFSET), y


def retainer_pad_xy(x, y):
    return x + (RETAINER_PAD_OUTWARD_OFFSET if x > 0 else
                -RETAINER_PAD_OUTWARD_OFFSET), y


def retainer_capture_pocket(x, y):
    sign=1 if x>0 else -1
    cx=sign*(RETAINER_BAR_LENGTH/2+RETAINER_CAPTURE_OVERHANG/2)
    return rectangular_prism(
        RETAINER_CAPTURE_OVERHANG+2*RETAINER_CAPTURE_XY_CLEARANCE,
        RETAINER_BAR_WIDTH+2*RETAINER_CAPTURE_XY_CLEARANCE,
        -0.1,RETAINER_CAPTURE_PAD_HEIGHT,cx,y)


def boss_wall_ramp(x, y, radius, shoulder_z, rise):
    top_radius = 1.0
    top_x = (1 if x > 0 else -1) * (OUTER_X / 2 - top_radius - 0.3)
    lower = Pos(x, y, shoulder_z) * Circle(radius)
    upper = Pos(top_x, y, shoulder_z + rise) * Circle(top_radius)
    return loft([lower, upper], ruled=True)

def retainer_boss_ramp(x, y):
    z = 18.01
    top_x = (1 if x > 0 else -1) * (OUTER_X / 2 - 1.3)
    lower = Pos(x, y, z) * Rectangle(RETAINER_BOSS_X, RETAINER_BOSS_Y)
    upper = Pos(top_x, y, z + RETAINER_BOSS_RAMP_RISE) * Rectangle(2, 3)
    return loft([lower, upper], ruled=True)

def end_joint_ramp(x, y):
    top_y = (1 if y > 0 else -1) * (OUTER_Y / 2 - 1.3)
    lower = Pos(x, y, JOINT_BOSS_TOP_Z) * Circle(JOINT_BOSS_RADIUS)
    upper = Pos(x, top_y, JOINT_BOSS_TOP_Z + JOINT_BOSS_RAMP_RISE) * Circle(1)
    return loft([lower, upper], ruled=True)

def roof_limit(shoulder_apex, cap_z, half_width, bottom):
    flat = ROOF_SHOULDER_HALF_WIDTH + shoulder_apex - cap_z
    side = shoulder_apex - (half_width - ROOF_SHOULDER_HALF_WIDTH)
    return polygon_xz([(-half_width,bottom),(half_width,bottom),
                       (half_width,side),(flat,cap_z),(-flat,cap_z),
                       (-half_width,side)])

def monolithic_housing():
    shell = rounded_prism(OUTER_X,OUTER_Y,OUTER_R,0,OUTER_APEX_Z)
    shell &= roof_limit(OUTER_SHOULDER_APEX_Z,OUTER_APEX_Z,OUTER_X/2,-1)
    blank = shell + cylinder(0,0,FLANGE_RADIUS,0,FLANGE_THICKNESS)
    for x,y in RETAINER_FIXINGS:
        blank += rectangular_prism(RETAINER_BOSS_X,RETAINER_BOSS_Y,
                                   FLANGE_THICKNESS,18,*retainer_boss_xy(x,y))
    cavity = rounded_prism(CAVITY_X,CAVITY_Y,CAVITY_R,-1,INNER_APEX_Z+1)
    cavity &= roof_limit(INNER_SHOULDER_APEX_Z,INNER_APEX_Z,CAVITY_X/2,-1)
    blank -= cavity
    blank -= cylinder(0,CABLE_EXIT_Y,CABLE_HOLE_DIAMETER/2,
                      INNER_APEX_Z-5,OUTER_APEX_Z+2)
    for x,y in MAGNETS:
        blank -= cylinder(x,y,MAGNET_DIAMETER/2,-0.1,MAGNET_POCKET_DEPTH)
    for x,y in CEILING_SCREWS:
        blank -= cylinder(x,y,CEILING_SCREW_HOLE_RADIUS,-0.1,FLANGE_THICKNESS+0.1)
        blank -= cone(x,y,CEILING_COUNTERSINK_RADIUS,CEILING_SCREW_HOLE_RADIUS,
                      0,CEILING_COUNTERSINK_DEPTH)
    seat = rectangular_prism(RETAINER_BAR_LENGTH,RETAINER_BAR_WIDTH,-0.1,RETAINER_SEAT_DEPTH,
                             0,-RETAINER_Y)
    blank -= seat
    blank -= Rot(Z=180)*seat
    for x,y in RETAINER_FIXINGS:
        blank -= rectangular_prism(RETAINER_PAD_CLEARANCE_WIDTH,
                                   RETAINER_PAD_CLEARANCE_LENGTH,
                                   RETAINER_SEAT_DEPTH-0.1,RETAINER_PAD_TOP_Z,
                                   *retainer_pad_xy(x,y))
        blank -= cylinder(x,y,RETAINER_INSERT_PILOT_RADIUS,
                          RETAINER_PAD_TOP_Z-0.1,
                          RETAINER_PAD_TOP_Z+RETAINER_INSERT_PILOT_DEPTH)
    relief = radial_profile([(FLANGE_RADIUS,CLIP_LIP_TOP_Z),
                             (FLANGE_RADIUS+1,CLIP_LIP_TOP_Z),
                             (FLANGE_RADIUS+1,FLANGE_THICKNESS+0.1),
                             (FLANGE_RADIUS-CLIP_RECESS,FLANGE_THICKNESS+0.1),
                             (FLANGE_RADIUS-CLIP_RECESS,CLIP_SHOULDER_TOP_Z)])
    return blank - relief

def ceiling_flange():
    part = monolithic_housing() & cylinder(0,0,FLANGE_RADIUS+1,-0.1,FLANGE_THICKNESS)
    for x,y in RETAINER_FIXINGS:
        part -= retainer_capture_pocket(x,y)
    for x,y in JOINT_FIXINGS:
        part -= cylinder(x,y,JOINT_BOLT_CLEARANCE_RADIUS,-0.1,FLANGE_THICKNESS+0.1)
        part -= cylinder(x,y,JOINT_COUNTERBORE_RADIUS,-0.1,JOINT_COUNTERBORE_DEPTH)
    return part.clean()

def housing_shell():
    part = monolithic_housing() & cylinder(0,0,FLANGE_RADIUS+1,
                                           FLANGE_THICKNESS,OUTER_APEX_Z+0.1)
    for x,y in JOINT_FIXINGS:
        part += cylinder(x,y,JOINT_BOSS_RADIUS,FLANGE_THICKNESS,JOINT_BOSS_TOP_Z)
    for x,y in RETAINER_FIXINGS:
        part += retainer_boss_ramp(*retainer_boss_xy(x,y))
    for x,y in JOINT_SIDE_FIXINGS:
        part += boss_wall_ramp(x,y,JOINT_BOSS_RADIUS,JOINT_BOSS_TOP_Z,
                               JOINT_BOSS_RAMP_RISE)
    for x,y in JOINT_END_FIXINGS:
        part += end_joint_ramp(x,y)
    for x,y in JOINT_FIXINGS:
        part -= cylinder(x,y,JOINT_INSERT_HOLE_RADIUS,FLANGE_THICKNESS-0.1,
                          FLANGE_THICKNESS+JOINT_INSERT_DEPTH)
    return part.clean()
