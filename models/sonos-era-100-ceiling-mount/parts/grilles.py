"""Plain, large-hex and fine-hex clip-on grille variants."""
from __future__ import annotations
from math import ceil, cos, radians, sin, sqrt
from build123d import Face, Plane, Pos, Wire, extrude
from parts.housing import FLANGE_RADIUS, FLANGE_THICKNESS
from geometry import cylinder, cone, rectangular_prism, rounded_prism, radial_profile


# Dimensions owned by this part (millimetres).
GRILLE_THICKNESS = 1.4
GRILLE_OUTER_RADIUS = FLANGE_RADIUS + 2.0  # Ø249, within X1C's 256 mm bed
GRILLE_FACE_CHAMFER = 0.8               # soften room-facing outside edge
HEX_OPENING_FLATS = 3.0                # original, larger printed hex opening
HEX_WEB = 0.7
FINE_HEX_OPENING_FLATS = 2.0           # smaller cells limit direct sight lines
FINE_HEX_WEB = 1.0                     # robust PETG paths around the apertures
HEX_FIELD_RADIUS = 115.8              # continuous round pattern, 7.4 mm rim
GRILLE_SKIRT_INNER_RADIUS = FLANGE_RADIUS + 0.35
GRILLE_SKIRT_TOP_Z = FLANGE_THICKNESS - 0.1
CLIP_BEAD_INSET = 0.60
CLIP_BEAD_ROOT_RADIUS = FLANGE_RADIUS + 0.4
CLIP_BEAD_LOWER_Z = 0.30
CLIP_BEAD_TIP_Z = 1.35
CLIP_BEAD_UPPER_Z = 2.50
CLIP_PATCH_LENGTH = 20.0

def grille_face():
    face = cylinder(0,0,GRILLE_OUTER_RADIUS,-GRILLE_THICKNESS+GRILLE_FACE_CHAMFER,0)
    face += cone(0,0,GRILLE_OUTER_RADIUS-GRILLE_FACE_CHAMFER,
                 GRILLE_OUTER_RADIUS,-GRILLE_THICKNESS,GRILLE_FACE_CHAMFER)
    return face

def grille_rim_and_clips(face):
    skirt = cylinder(0,0,GRILLE_OUTER_RADIUS,0,GRILLE_SKIRT_TOP_Z)
    skirt -= cylinder(0,0,GRILLE_SKIRT_INNER_RADIUS,-0.1,GRILLE_SKIRT_TOP_Z+0.1)
    face += skirt
    ring = radial_profile([(CLIP_BEAD_ROOT_RADIUS,CLIP_BEAD_LOWER_Z),
                           (FLANGE_RADIUS-CLIP_BEAD_INSET,CLIP_BEAD_TIP_Z),
                           (CLIP_BEAD_ROOT_RADIUS,CLIP_BEAD_UPPER_Z)])
    for sx in (-1,1):
        face += ring & rectangular_prism(4,CLIP_PATCH_LENGTH,0.2,2.6,
                                         sx*FLANGE_RADIUS,0)
    for sy in (-1,1):
        face += ring & rectangular_prism(CLIP_PATCH_LENGTH,4,0.2,2.6,
                                         0,sy*FLANGE_RADIUS)
    return face.clean()

def grille():
    frame = grille_face()-rounded_prism(128,190,4,-GRILLE_THICKNESS-1,1)
    for x in (-40,0,40):
        frame += rectangular_prism(2.2,192,-GRILLE_THICKNESS,0,x,0)
    for y in (-50,0,50):
        frame += rectangular_prism(130,2.2,-GRILLE_THICKNESS,0,0,y)
    return grille_rim_and_clips(frame)

def hex_grille(opening_flats=HEX_OPENING_FLATS, web=HEX_WEB):
    # One planar face with inner wires avoids thousands of independent cuts.
    z0=-GRILLE_THICKNESS
    panel_radius=HEX_FIELD_RADIUS+0.5
    pitch=opening_flats+web
    row_pitch=pitch*sqrt(3)/2
    vr=opening_flats/sqrt(3)
    offsets=[(vr*cos(radians(30+60*k)),vr*sin(radians(30+60*k))) for k in range(6)]
    outer=Wire.make_circle(panel_radius, Plane(origin=(0,0,z0)))
    holes=[]
    for row in range(-ceil(HEX_FIELD_RADIUS/row_pitch)-1,
                     ceil(HEX_FIELD_RADIUS/row_pitch)+2):
        cy=row*row_pitch
        shift=(row%2)*pitch/2
        for col in range(-ceil(HEX_FIELD_RADIUS/pitch)-2,
                         ceil(HEX_FIELD_RADIUS/pitch)+3):
            cx=col*pitch+shift
            points=[(cx+dx,cy+dy,z0) for dx,dy in offsets]
            if all(x*x+y*y<=HEX_FIELD_RADIUS**2 for x,y,_ in points):
                holes.append(Wire.make_polygon(points,close=True))
    panel=extrude(Face(outer,holes),amount=GRILLE_THICKNESS)
    outer_ring=grille_face()-cylinder(0,0,panel_radius-0.2,z0-0.1,0.1)
    return grille_rim_and_clips(outer_ring+panel)

def fine_hex_grille():
    return hex_grille(FINE_HEX_OPENING_FLATS,FINE_HEX_WEB)
