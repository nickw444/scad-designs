"""Check the build123d assembly at nominal and optional-gasket placements."""
from __future__ import annotations
import json
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
from speaker import SPEAKER_DEPTH, SPEAKER_FRONT_Z, speaker_mockup

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
    gasket_assembly=make_assembly(gasket=True)
    gasket=gasket_assembly.get('flat-seam-gasket')
    reports={}
    for name in PARTS:
        path=BUILD/f'era-100-{name}.stl'
        mesh=trimesh.load_mesh(path)
        check(mesh.is_watertight and len(mesh.split())==1,f'{name}: STL not one closed solid')
        reports[name]={'volume_mm3':float(mesh.volume),'bounds_mm':mesh.bounds.tolist(),
                       'watertight':True}
    check(overlap(flange,shell)<0.001,'flange/shell overlap')
    house=flange+shell
    check(overlap(house,speaker)<0.001,'speaker/housing overlap')
    rear_apex = SPEAKER_FRONT_Z + SPEAKER_DEPTH
    check(abs(housing.INNER_APEX_Z-rear_apex-5.0)<1e-6,
          'nominal rear apex clearance must be 5 mm')
    for distance in np.linspace(0,SPEAKER_DEPTH,15):
        check(overlap(house,Pos(0,0,-float(distance))*speaker)<0.001,
              f'speaker insertion collision at {distance:.1f} mm')
    check(overlap(grille,house)<0.001,'grille/housing overlap')
    check(overlap(grille,speaker)<0.001,'grille/speaker overlap')
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
              f'retainer {i} shoulder does not capture flange')
    capture_side_overlap=(housing.RETAINER_CAPTURE_PAD_Y-housing.RETAINER_BAR_WIDTH)/2
    capture_outer_overlap=(abs(housing.RETAINER_FIXINGS[0][0])+
                           housing.RETAINER_PAD_OUTWARD_OFFSET+
                           housing.RETAINER_CAPTURE_PAD_X/2-
                           housing.RETAINER_BAR_LENGTH/2)
    check(abs(capture_side_overlap-3.0)<0.01 and
          abs(capture_outer_overlap-3.0)<0.01,
          'retainer shoulders must capture 3 mm of flange at sides and outer end')
    check(retainer_dims.RETAINER_HEAD_BORE_DEPTH-retainer_dims.RETAINER_HEAD_HEIGHT>=0.8,
          'M3 cap head does not fully recess in retainer')
    engaged_length = (retainer_dims.RETAINER_HEAD_BORE_DEPTH +
                      retainer_dims.RETAINER_BOLT_UNDER_HEAD_LENGTH -
                      housing.RETAINER_PAD_TOP_Z)
    check(engaged_length>=6.0,'10 mm M3 retainer bolt has insufficient insert engagement')
    gasket_retainer_engagement=engaged_length-gasket.bounding_box().size.Z
    check(gasket_retainer_engagement>=5.5,
          '10 mm M3 retainer bolt has insufficient engagement with optional gasket')
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
    joint_engagement = (housing.JOINT_COUNTERBORE_DEPTH +
                        housing.JOINT_BOLT_UNDER_HEAD_LENGTH -
                        housing.FLANGE_THICKNESS)
    gasket_joint_engagement = joint_engagement - gasket.bounding_box().size.Z
    check(joint_engagement>=8.0 and
          joint_engagement<housing.JOINT_INSERT_DEPTH,
          '10 mm M3 joint bolt does not seat safely in the insert pilot')
    check(gasket_joint_engagement>=7.0,
          '10 mm M3 joint bolt has insufficient engagement with optional gasket')
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
    raised=gasket_assembly.get('housing-shell')
    check(overlap(gasket,flange)<0.001,'gasket/flange overlap')
    check(overlap(gasket,raised)<0.001,'gasket/raised shell overlap')
    check(overlap(raised,flange)<0.001,'raised shell/flange overlap')
    check(overlap(raised,speaker)<0.001,'raised shell/speaker overlap')
    for i,stop in enumerate(retainers):
        check(overlap(raised,stop)<0.001,f'raised shell/retainer {i} overlap')
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
        'optional_flat_gasket_assembly_collisions_mm3':0,
        'round_grommet_compression_mm3':round_compression,
        'flat_grommet_compression_mm3':flat_compression,
        'nominal_factory_plug_diameter_mm':housing.ASSUMED_PLUG_DIAMETER,
        'cable_passage_diameter_mm':housing.CABLE_HOLE_DIAMETER,
        'nominal_plug_radial_clearance_mm':(housing.CABLE_HOLE_DIAMETER-housing.ASSUMED_PLUG_DIAMETER)/2,
        'grommet_flange_diameter_mm':2*GROMMET_FLANGE_RADIUS,
        'speaker_rear_apex_z_mm':rear_apex,
        'inner_roof_apex_z_mm':housing.INNER_APEX_Z,
        'rear_apex_clearance_mm':housing.INNER_APEX_Z-rear_apex,
        'joint_m3_axes_checked':len(housing.JOINT_FIXINGS),
        'retainer_m3_axes_checked':len(housing.RETAINER_FIXINGS),
        'joint_m3_10mm_insert_engagement_mm':joint_engagement,
        'joint_m3_10mm_gasket_engagement_mm':gasket_joint_engagement,
        'joint_head_counterbore_depth_mm':housing.JOINT_COUNTERBORE_DEPTH,
        'retainer_base_thickness_mm':housing.RETAINER_SEAT_DEPTH,
        'retainer_capture_shoulder_height_mm':housing.RETAINER_CAPTURE_PAD_HEIGHT,
        'retainer_capture_side_overlap_mm':capture_side_overlap,
        'retainer_capture_outer_overlap_mm':capture_outer_overlap,
        'retainer_centre_beam_height_mm':housing.RETAINER_CENTRE_HEIGHT,
        'retainer_centre_beam_length_mm':housing.RETAINER_CENTRE_LENGTH,
        'retainer_bar_width_mm':housing.RETAINER_BAR_WIDTH,
        'retainer_head_bore_depth_mm':retainer_dims.RETAINER_HEAD_BORE_DEPTH,
        'retainer_m3_10mm_insert_engagement_mm':engaged_length,
        'retainer_m3_10mm_gasket_engagement_mm':gasket_retainer_engagement,
        'ceiling_screws_checked':len(housing.CEILING_SCREWS),
        'speaker_mockup_note':'Rear/front curves inferred from owner measurements; physical fit remains to be tested.'
    }
    out=OUT/'assembly-check.json'; out.write_text(json.dumps(reports,indent=2)+'\n')
    print(f'PASS: ten watertight STL parts, 15 insertion positions, direct and gasket assemblies; {out}')

if __name__=='__main__':
    run()
