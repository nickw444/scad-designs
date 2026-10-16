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
ROOF_CENTRE_CLEARANCE = 10.0          # dummy speaker rear apex to inner flat
FLANGE_RADIUS = 122.5                 # Ø245; preserves 4 mm land beyond cutout
FLANGE_THICKNESS = 6.0
RETAINER_SEAT_DEPTH = 4.8             # full-length beam; 1.2 mm flange bridge preserves seam
RETAINER_CENTRE_HEIGHT = SPEAKER_FRONT_Z - 0.8  # full beam reaches front-contact height
RETAINER_CENTRE_LENGTH = 123.0         # 0.5 mm clearance each side within 124 mm cavity
RETAINER_BAR_WIDTH = 14.0             # widened load-bearing span
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
JOINT_FIXINGS = [(sx * 66.2, sy * 45.0)
                 for sx in (-1, 1) for sy in (-1, 1)]
JOINT_BOSS_RADIUS = 3.2
JOINT_BOSS_TOP_Z = FLANGE_THICKNESS + 9.0
JOINT_BOSS_RAMP_RISE = 8.5             # rear-down print: <45° outward growth
JOINT_INSERT_BODY_RADIUS = 1.70      # measured Ø3.4 heat-set insert
JOINT_INSERT_TIP_RADIUS = 1.50       # measured Ø3.0 lead-in tip
JOINT_INSERT_HOLE_RADIUS = 1.55      # Ø3.1 pilot; measured Ø3.4 body, Ø3.0 tip
JOINT_INSERT_DEPTH = 7.0
JOINT_BOLT_RADIUS = 0.95             # approximately Ø1.9 measured thread
JOINT_BOLT_CLEARANCE_RADIUS = 1.10   # Ø2.2 clearance for ~Ø1.9 thread
JOINT_HEAD_RADIUS = 1.65             # measured Ø3.3 round cup head
JOINT_HEAD_HEIGHT = 1.30
JOINT_BOLT_UNDER_HEAD_LENGTH = 10.0   # 5.4 mm beyond 6 mm flange
JOINT_COUNTERBORE_RADIUS = 1.80      # Ø3.6 for measured Ø3.3 round cup head
JOINT_COUNTERBORE_DEPTH = 1.4       # 0.1 mm recess for ~1.3 mm head
RETAINER_BAR_LENGTH = 143.0           # full-height base reaches both fixing bores
END_JOINT_FIXINGS = [(sx * 35.0, sy * 96.5)
                     for sx in (-1, 1) for sy in (-1, 1)]
END_JOINT_BOSS_RADIUS = JOINT_BOSS_RADIUS
END_JOINT_INSERT_DEPTH = JOINT_INSERT_DEPTH
END_JOINT_BOSS_TOP_Z = JOINT_BOSS_TOP_Z
END_JOINT_RAMP_RISE = JOINT_BOSS_RAMP_RISE
END_JOINT_COUNTERBORE_DEPTH = JOINT_COUNTERBORE_DEPTH


def retainer_boss_xy(x, y):
    return x + (RETAINER_BOSS_OUTWARD_OFFSET if x > 0 else
                -RETAINER_BOSS_OUTWARD_OFFSET), y


def retainer_pad_xy(x, y):
    return x + (RETAINER_PAD_OUTWARD_OFFSET if x > 0 else
                -RETAINER_PAD_OUTWARD_OFFSET), y


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
    lower = Pos(x, y, END_JOINT_BOSS_TOP_Z) * Circle(END_JOINT_BOSS_RADIUS)
    upper = Pos(x, top_y, END_JOINT_BOSS_TOP_Z + END_JOINT_RAMP_RISE) * Circle(1)
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
    for x,y in JOINT_FIXINGS + END_JOINT_FIXINGS:
        part -= cylinder(x,y,JOINT_BOLT_CLEARANCE_RADIUS,-0.1,FLANGE_THICKNESS+0.1)
        part -= cylinder(x,y,JOINT_COUNTERBORE_RADIUS,-0.1,JOINT_COUNTERBORE_DEPTH)
    return part.clean()

def housing_shell():
    part = monolithic_housing() & cylinder(0,0,FLANGE_RADIUS+1,
                                           FLANGE_THICKNESS,OUTER_APEX_Z+0.1)
    for x,y in JOINT_FIXINGS + END_JOINT_FIXINGS:
        part += cylinder(x,y,JOINT_BOSS_RADIUS,FLANGE_THICKNESS,JOINT_BOSS_TOP_Z)
    for x,y in RETAINER_FIXINGS:
        part += retainer_boss_ramp(*retainer_boss_xy(x,y))
    for x,y in JOINT_FIXINGS:
        part += boss_wall_ramp(x,y,JOINT_BOSS_RADIUS,JOINT_BOSS_TOP_Z,
                               JOINT_BOSS_RAMP_RISE)
    for x,y in END_JOINT_FIXINGS:
        part += end_joint_ramp(x,y)
    for x,y in JOINT_FIXINGS + END_JOINT_FIXINGS:
        part -= cylinder(x,y,JOINT_INSERT_HOLE_RADIUS,FLANGE_THICKNESS-0.1,
                          FLANGE_THICKNESS+JOINT_INSERT_DEPTH)
    return part.clean()
