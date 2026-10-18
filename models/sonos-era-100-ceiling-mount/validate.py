"""Check the build123d assembly, locating joint, and printable exports."""
from __future__ import annotations
import json
from math import sqrt
from pathlib import Path
import numpy as np
import trimesh
from build123d import Pos
from assembly import make_assembly, grommet_placement
from geometry import cylinder, rectangular_prism
from parts import PARTS
from parts import housing
from parts import retainers as retainer_dims
from parts.grommets import GROMMET_FLANGE_RADIUS, flat_cable_grommet
from parts.template import ceiling_cutout_profile
from paths import BUILD, REPORTS
from speaker import (MEASURED_SPEAKER_DEPTH, SPEAKER_DEPTH, SPEAKER_FRONT_RADIUS,
                     SPEAKER_FRONT_Z, speaker_mockup)

OUT=REPORTS

def overlap(a,b):
    return (a & b).volume

def check(condition, description):
    if not condition:
        raise AssertionError(description)

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    direct=make_assembly()
    flange=direct.get('ceiling-flange'); shell=direct.get('housing-shell')
    speaker=speaker_mockup(); grille=direct.get('grille')
    retainers=[direct.get('retainer-south'),direct.get('retainer-north')]
    reports={}
    for name in PARTS:
        path=BUILD/f'era-100-{name}.stl'
        mesh=trimesh.load_mesh(path)
        check(mesh.is_watertight and len(mesh.split())==1,f'{name}: STL not one closed solid')
        reports[name]={'volume_mm3':float(mesh.volume),'bounds_mm':mesh.bounds.tolist(),
                       'watertight':True}
    check(overlap(flange,shell)<0.001,'flange/shell overlap')
    for offset in ((0.5,0),(0,0.5)):
        check(overlap(flange,Pos(offset[0],offset[1],0)*shell)>10,
              f'locating joint does not constrain {offset} mm offset')
    check(housing.RETAINER_BOSS_X/2+abs(housing.RETAINER_FIXINGS[0][0]) >=
          housing.RETAINER_BAR_LENGTH/2+housing.RETAINER_SEAT_XY_CLEARANCE,
          'retainer boss does not cover the outer end of the flange slot')
    check(housing.RETAINER_BOSS_Y/2 >=
          housing.RETAINER_TAIL_WIDTH/2+housing.RETAINER_SEAT_XY_CLEARANCE+1.4,
          'retainer boss does not cover the narrowed flange tail slot')
    check(abs(housing.SEAM_REBATE_WIDTH-housing.SEAM_LIP_WIDTH-0.25)<1e-6 and
          abs(housing.SEAM_REBATE_DEPTH-housing.SEAM_LIP_HEIGHT-0.3)<1e-6,
          'locating lip/rebate clearance changed')
    check(housing.SIDE_WALL-housing.SEAM_REBATE_WIDTH>=2.9,
          'rebate leaves too little continuous outer wall')
    seam_x=housing.CAVITY_X/2+housing.SEAM_LIP_WIDTH/2
    for y in (-50,0,50):
        tongue_probe=rectangular_prism(0.2,0.2,housing.FLANGE_THICKNESS+0.1,
                    housing.FLANGE_THICKNESS+housing.SEAM_LIP_HEIGHT-0.1,seam_x,y)
        check(overlap(flange,tongue_probe)>0.01 and overlap(shell,tongue_probe)<0.001,
              f'locating lip/rebate missing at y={y}')
        outer_wall_probe=rectangular_prism(0.2,0.2,housing.FLANGE_THICKNESS+0.1,
                          housing.FLANGE_THICKNESS+housing.SEAM_REBATE_DEPTH-0.1,
                          housing.OUTER_X/2-0.7,y)
        check(overlap(shell,outer_wall_probe)>0.01,
              f'continuous outer shell wall missing at y={y}')
    for sy in (-1,1):
        for x in (-70,70):
            for dy in (-housing.RETAINER_TAIL_WIDTH/2-
                       housing.RETAINER_SEAT_XY_CLEARANCE+0.3,
                       housing.RETAINER_TAIL_WIDTH/2+
                       housing.RETAINER_SEAT_XY_CLEARANCE-0.3):
                seal_probe=rectangular_prism(0.3,0.3,housing.FLANGE_THICKNESS+0.1,
                                            housing.FLANGE_THICKNESS+0.5,
                                            x,sy*housing.RETAINER_Y+dy)
                check(overlap(shell,seal_probe)>0.01,
                      'retainer boss leaves uncovered flange-slot edge')
    for sy in (-1,1):
        for sx in (-1,1):
            flange_land=rectangular_prism(0.3,0.3,2.5,3.5,
                           sx*65,sy*housing.RETAINER_Y+6.3)
            check(overlap(flange,flange_land)>0.01,
                  'flange is not closed beside narrowed retainer tail')
            tab_roof=rectangular_prism(0.5,0.5,2.5,3.5,
                         sx*73,sy*housing.RETAINER_Y)
            check(overlap(flange,tab_roof)>0.1,
                  'flange lacks a roof above the retainer capture tab')
    house=flange+shell
    check(overlap(house,speaker)<0.001,'speaker/housing overlap')
    rear_apex = SPEAKER_FRONT_Z + SPEAKER_DEPTH
    check(abs(housing.INNER_APEX_Z-rear_apex-5.0)<1e-6,
          'nominal rear apex clearance must be 5 mm')
    roof_flat_wall=housing.OUTER_APEX_Z-housing.INNER_APEX_Z
    roof_slope_wall=(housing.OUTER_SHOULDER_APEX_Z-
                     housing.INNER_SHOULDER_APEX_Z)/sqrt(2)
    check(abs(roof_flat_wall-housing.SIDE_WALL)<=0.6 and
          abs(roof_slope_wall-housing.SIDE_WALL)<=0.6,
          'roof walls differ too much from straight shell walls')
    for distance in np.linspace(0,SPEAKER_DEPTH,15):
        check(overlap(house,Pos(0,0,-float(distance))*speaker)<0.001,
              f'speaker insertion collision at {distance:.1f} mm')
    check(overlap(grille,house)<0.001,'grille/housing overlap')
    check(overlap(grille,speaker)<0.001,'grille/speaker overlap')
    seated_speaker = Pos(0,0,housing.RETAINER_CENTRE_HEIGHT-SPEAKER_FRONT_Z) * speaker_mockup(
        depth=MEASURED_SPEAKER_DEPTH)
    for name,part in [('shell',shell),('flange',flange),('grille',grille),
                      ('south retainer',direct.get('retainer-south')),
                      ('north retainer',direct.get('retainer-north'))]:
        check(overlap(part,seated_speaker)<0.001,
              f'130.7 mm seated speaker overlaps {name}')
    centre_probe=rectangular_prism(0.02,0.02,0,200,0,housing.RETAINER_Y)
    retainer_contact_z=(direct.get('retainer-north') & centre_probe).bounding_box().max.Z
    measured_rear_z=(seated_speaker & centre_probe).bounding_box().max.Z
    roof_inner_z=(shell & centre_probe).bounding_box().min.Z
    seated_available=roof_inner_z-retainer_contact_z
    seated_rear_gap=roof_inner_z-measured_rear_z
    check(abs(seated_available-MEASURED_SPEAKER_DEPTH-seated_rear_gap)<0.01 and
          seated_rear_gap>=5.0,
          '130.7 mm seated speaker lacks rear roof clearance')
    for i,stop in enumerate(retainers):
        check(overlap(stop,house)<0.001,f'retainer {i}/housing overlap')
        check(overlap(stop,speaker)<0.001,f'retainer {i}/speaker overlap')
        check(overlap(stop,grille)<0.001,f'retainer {i}/grille overlap')
        check(overlap(stop,Pos(0,0,-1)*speaker)>1,f'retainer {i} fails to capture speaker')
    for x in (-58,0,58):
        beam_probe=rectangular_prism(1,1,housing.RETAINER_CENTRE_HEIGHT-0.3,
                                     housing.RETAINER_CENTRE_HEIGHT-0.1,
                                     x,-housing.RETAINER_Y)
        check(overlap(retainers[0],beam_probe)>0.1,
              f'retainer load-bearing beam too thin at x={x}')
    for x in (-63.5,63.5):
        end_probe=rectangular_prism(0.5,1,housing.RETAINER_SEAT_DEPTH-0.4,
                                    housing.RETAINER_SEAT_DEPTH-0.1,
                                    x,-housing.RETAINER_Y)
        check(overlap(retainers[0],end_probe)>0.1,
              f'retainer base does not continue to fixing at x={x}')
    check(abs(housing.FLANGE_THICKNESS-housing.RETAINER_SEAT_DEPTH)<1e-6,
          'retainer channel must pass all the way through the flange')
    for i,stop in enumerate(retainers):
        check(overlap(flange,Pos(0,0,0.5)*stop)>0.1,
              f'retainer {i} outer tabs do not capture flange')
        for sx in (-1,1):
            tip=rectangular_prism(0.5,housing.RETAINER_TAIL_WIDTH-1,0.3,1.7,
                                  sx*(housing.RETAINER_BAR_LENGTH/2+1.5),
                                  -housing.RETAINER_Y if i==0 else housing.RETAINER_Y)
            check(overlap(stop,tip)>1 and overlap(flange,tip)<0.001,
                  f'retainer {i} outer tab {sx} is missing or pocket is blocked')
    capture_outer_overlap=housing.RETAINER_CAPTURE_OVERHANG
    actual_capture=capture_outer_overlap-housing.RETAINER_SEAT_XY_CLEARANCE
    check(actual_capture>=2.5,
          'retainer tab has insufficient flange overlap after adding slot clearance')
    check(housing.RETAINER_TAIL_WIDTH>=2*housing.M3_COUNTERBORE_RADIUS+4.0,
          'narrowed retainer tail lacks material beside the M3 head')
    check(housing.RETAINER_SEAT_XY_CLEARANCE>=0.3,
          'retainer main slot has insufficient insertion clearance')
    for i,stop in enumerate(retainers):
        for dx,dy in ((-0.2,0),(0.2,0),(0,-0.2),(0,0.2)):
            check(overlap(flange,Pos(dx,dy,0)*stop)<0.001,
                  f'retainer {i} binds in flange at offset {(dx,dy)}')
        for x in (-50,50):
            shoulder_probe=rectangular_prism(1,1,12.0,13.0,x,
                                              -housing.RETAINER_Y if i==0 else housing.RETAINER_Y)
            check(overlap(stop,shoulder_probe)>0.5,
                  f'retainer {i} raised shoulder missing at x={x}')
    contact_half=retainer_dims.RETAINER_CONTACT_HALF_WIDTH
    speaker_edge_z=(SPEAKER_FRONT_Z+SPEAKER_FRONT_RADIUS-
                    sqrt(SPEAKER_FRONT_RADIUS**2-contact_half**2))
    retainer_edge_z=(housing.RETAINER_CENTRE_HEIGHT+SPEAKER_FRONT_RADIUS-
                     sqrt(SPEAKER_FRONT_RADIUS**2-contact_half**2))
    contact_gap=speaker_edge_z-retainer_edge_z
    check(0.6<=contact_gap<=1.0,
          'nominal front contact gap outside 0.6–1.0 mm across the retainer')
    check(retainer_dims.RETAINER_HEAD_BORE_DEPTH-retainer_dims.RETAINER_HEAD_HEIGHT>=0.8,
          'M3 cap head does not fully recess in retainer')
    engaged_length = (retainer_dims.RETAINER_HEAD_BORE_DEPTH +
                      retainer_dims.RETAINER_BOLT_UNDER_HEAD_LENGTH -
                      housing.RETAINER_PAD_TOP_Z)
    check(engaged_length>=6.0,'10 mm M3 retainer bolt has insufficient insert engagement')
    for x,y in housing.RETAINER_FIXINGS:
        if y > 0:
            continue
        head_clearance=cylinder(x,y,retainer_dims.RETAINER_HEAD_RADIUS,-0.01,
                                retainer_dims.RETAINER_HEAD_BORE_DEPTH-0.01)
        check(overlap(retainers[0],head_clearance)<0.001,
              f'M3 head recess blocked at {x,y}')
        head_seat=(cylinder(x,y,retainer_dims.RETAINER_HEAD_RADIUS,
                            retainer_dims.RETAINER_HEAD_BORE_DEPTH+0.05,
                            retainer_dims.RETAINER_HEAD_BORE_DEPTH+0.25) -
                   cylinder(x,y,retainer_dims.RETAINER_BOLT_CLEARANCE_RADIUS,
                            retainer_dims.RETAINER_HEAD_BORE_DEPTH,
                            retainer_dims.RETAINER_HEAD_BORE_DEPTH+0.30))
        check(overlap(retainers[0],head_seat)>0.1,
              f'M3 head lacks bearing seat at {x,y}')
    check(len(housing.JOINT_FIXINGS)==4 and len(housing.RETAINER_FIXINGS)==4,
          'expected four shell joins and four retainer bolts')
    side_head_land=(abs(housing.JOINT_SIDE_FIXINGS[0][0])-
                    housing.CAVITY_X/2-housing.JOINT_COUNTERBORE_RADIUS)
    end_head_land=(abs(housing.JOINT_END_FIXINGS[0][1])-
                   housing.CAVITY_Y/2-housing.JOINT_COUNTERBORE_RADIUS)
    check(min(side_head_land,end_head_land)>=3.0,
          'M3 head counterbore is too close to the flange inner opening')
    joint_engagement = (housing.JOINT_COUNTERBORE_DEPTH +
                        housing.JOINT_BOLT_UNDER_HEAD_LENGTH -
                        housing.FLANGE_THICKNESS)
    check(joint_engagement>=8.0 and
          joint_engagement<housing.JOINT_INSERT_DEPTH,
          '10 mm M3 joint bolt does not seat safely in the insert pilot')
    for x,y in housing.JOINT_FIXINGS:
        check(overlap(flange,cylinder(x,y,housing.JOINT_BOLT_CLEARANCE_RADIUS,0.1,5.9))<0.001,
              f'M3 flange bore blocked at {x,y}')
        check(overlap(shell,cylinder(x,y,housing.JOINT_INSERT_HOLE_RADIUS,
                                     housing.FLANGE_THICKNESS+0.1,
                                     housing.FLANGE_THICKNESS+housing.JOINT_INSERT_DEPTH-0.1))<0.001,
              f'M3 insert bore blocked at {x,y}')
        head_clearance=cylinder(x,y,housing.M3_HEAD_RADIUS,-0.01,
                                housing.JOINT_COUNTERBORE_DEPTH-0.01)
        check(overlap(flange,head_clearance)<0.001,
              f'M3 joint head recess blocked at {x,y}')
        head_seat=(cylinder(x,y,housing.M3_HEAD_RADIUS,
                            housing.JOINT_COUNTERBORE_DEPTH+0.05,
                            housing.JOINT_COUNTERBORE_DEPTH+0.25) -
                   cylinder(x,y,housing.JOINT_BOLT_CLEARANCE_RADIUS,
                            housing.JOINT_COUNTERBORE_DEPTH,
                            housing.JOINT_COUNTERBORE_DEPTH+0.30))
        check(overlap(flange,head_seat)>0.1,
              f'M3 joint head lacks bearing seat at {x,y}')
    for x,y in housing.RETAINER_FIXINGS:
        check(overlap(shell,cylinder(x,y,housing.RETAINER_INSERT_PILOT_RADIUS,
                                       housing.RETAINER_PAD_TOP_Z+0.1,
                                       housing.RETAINER_PAD_TOP_Z+8.8))<0.001,
              f'M3 insert bore blocked at {x,y}')
    for x,y in housing.CEILING_SCREWS:
        check(overlap(flange,cylinder(x,y,housing.CEILING_SCREW_HOLE_RADIUS,0.1,5.9))<0.001,
              f'ceiling screw bore blocked at {x,y}')
    cutout=ceiling_cutout_profile(-1,160)
    upper=shell & cylinder(0,0,housing.FLANGE_RADIUS+1,housing.FLANGE_THICKNESS,160)
    check((upper-cutout).volume<0.001,'shell exceeds ceiling cutout')
    plug_radius=housing.ASSUMED_PLUG_DIAMETER/2
    plug_probe=cylinder(0,housing.CABLE_EXIT_Y,plug_radius,
                        housing.INNER_APEX_Z-1,housing.OUTER_APEX_Z+1)
    check(overlap(shell,plug_probe)<0.001,'factory plug envelope blocked by shell')
    check(housing.CABLE_HOLE_DIAMETER-housing.ASSUMED_PLUG_DIAMETER>=2,
          'factory plug needs at least 1 mm radial passage clearance')
    check(GROMMET_FLANGE_RADIUS-housing.CABLE_HOLE_DIAMETER/2>=3,
          'grommet flange lacks sealing land around cable opening')
    check(housing.OUTER_FLAT_HALF_WIDTH-GROMMET_FLANGE_RADIUS>=2,
          'grommet flange overhangs the flat roof shoulder')
    check(housing.OUTER_Y/2-abs(housing.CABLE_EXIT_Y)-GROMMET_FLANGE_RADIUS>=2,
          'grommet flange overhangs the rear shell edge')
    grommet=direct.get('cable-grommet')
    flat_grommet=grommet_placement()*flat_cable_grommet()
    for item in (grommet, flat_grommet):
        check(overlap(item,speaker)<0.001,
              'rear cable grommet intersects nominal speaker envelope')
        bounds=item.bounding_box()
        check(bounds.max.Z>housing.OUTER_APEX_Z+1.4,
              'grommet flange must be on the rear/outside of roof')
        check(bounds.min.Z<housing.INNER_APEX_Z,
              'grommet stem must enter the roof opening')
    round_compression=overlap(house,grommet)
    flat_compression=overlap(house,flat_grommet)
    check(30<round_compression<150,'round grommet compression out of range')
    check(30<flat_compression<150,'flat grommet compression out of range')
    clip_probe=rectangular_prism(0.08,0.2,0.45,0.55,housing.FLANGE_RADIUS+0.24,0)
    check(overlap(grille,clip_probe)>0.0001,'grille lower catch missing')
    reports['assembly']={
        'insertion_positions_checked':15,
        'direct_assembly_collisions_mm3':0,
        'seam_lip_width_mm':housing.SEAM_LIP_WIDTH,
        'seam_lip_height_mm':housing.SEAM_LIP_HEIGHT,
        'seam_rebate_width_mm':housing.SEAM_REBATE_WIDTH,
        'seam_rebate_depth_mm':housing.SEAM_REBATE_DEPTH,
        'seam_outer_flank_clearance_mm':housing.SEAM_REBATE_WIDTH-housing.SEAM_LIP_WIDTH,
        'retainer_boss_span_mm':[housing.RETAINER_BOSS_X,housing.RETAINER_BOSS_Y],
        'retainer_tail_width_mm':housing.RETAINER_TAIL_WIDTH,
        'retainer_capture_tab_width_mm':housing.RETAINER_TAIL_WIDTH,
        'round_grommet_compression_mm3':round_compression,
        'flat_grommet_compression_mm3':flat_compression,
        'nominal_factory_plug_diameter_mm':housing.ASSUMED_PLUG_DIAMETER,
        'cable_passage_diameter_mm':housing.CABLE_HOLE_DIAMETER,
        'nominal_plug_radial_clearance_mm':(housing.CABLE_HOLE_DIAMETER-housing.ASSUMED_PLUG_DIAMETER)/2,
        'grommet_flange_diameter_mm':2*GROMMET_FLANGE_RADIUS,
        'speaker_rear_apex_z_mm':rear_apex,
        'inner_roof_apex_z_mm':housing.INNER_APEX_Z,
        'rear_apex_clearance_mm':housing.INNER_APEX_Z-rear_apex,
        'measured_speaker_depth_mm':MEASURED_SPEAKER_DEPTH,
        'seated_retainer_to_roof_mm':round(seated_available,3),
        'seated_measured_rear_gap_mm':round(seated_rear_gap,3),
        'side_wall_mm':housing.SIDE_WALL,
        'roof_flat_wall_mm':roof_flat_wall,
        'roof_slope_normal_wall_mm':roof_slope_wall,
        'joint_m3_axes_checked':len(housing.JOINT_FIXINGS),
        'joint_side_head_inner_land_mm':side_head_land,
        'joint_end_head_inner_land_mm':end_head_land,
        'retainer_m3_axes_checked':len(housing.RETAINER_FIXINGS),
        'joint_m3_10mm_insert_engagement_mm':joint_engagement,
        'joint_head_counterbore_depth_mm':housing.JOINT_COUNTERBORE_DEPTH,
        'retainer_base_thickness_mm':housing.RETAINER_SEAT_DEPTH,
        'retainer_capture_shoulder_height_mm':housing.RETAINER_CAPTURE_PAD_HEIGHT,
        'retainer_capture_outer_overlap_mm':actual_capture,
        'retainer_centre_beam_height_mm':housing.RETAINER_CENTRE_HEIGHT,
        'retainer_centre_beam_length_mm':housing.RETAINER_CENTRE_LENGTH,
        'retainer_bar_width_mm':housing.RETAINER_BAR_WIDTH,
        'retainer_slot_radial_clearance_mm':housing.RETAINER_SEAT_XY_CLEARANCE,
        'retainer_shoulder_top_at_50mm_min_z_mm':13.0,
        'retainer_contact_half_span_mm':contact_half,
        'retainer_front_radius_mm':SPEAKER_FRONT_RADIUS,
        'retainer_nominal_contact_gap_mm':contact_gap,
        'retainer_head_bore_depth_mm':retainer_dims.RETAINER_HEAD_BORE_DEPTH,
        'retainer_m3_10mm_insert_engagement_mm':engaged_length,
        'ceiling_screws_checked':len(housing.CEILING_SCREWS),
        'speaker_mockup_note':'Rear/front curves inferred from owner measurements; physical fit remains to be tested.'
    }
    out=OUT/'assembly-check.json'; out.write_text(json.dumps(reports,indent=2)+'\n')
    print(f'PASS: nine watertight STL parts, 15 insertion positions, located assembly; {out}')

if __name__=='__main__':
    run()
