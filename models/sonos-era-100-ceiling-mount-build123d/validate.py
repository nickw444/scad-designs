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
from parts.grommets import GROMMET_FLANGE_RADIUS, flat_cable_grommet
from parts.template import ceiling_cutout_profile
from paths import BUILD, REPORTS
from speaker import SPEAKER_DEPTH, speaker_mockup

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
    for x,y in housing.JOINT_FIXINGS+housing.END_JOINT_FIXINGS:
        check(overlap(flange,cylinder(x,y,housing.JOINT_BOLT_CLEARANCE_RADIUS,0.1,5.9))<0.001,
              f'M2 flange bore blocked at {x,y}')
        check(overlap(shell,cylinder(x,y,housing.JOINT_INSERT_HOLE_RADIUS,6.1,12.9))<0.001,
              f'M2 insert bore blocked at {x,y}')
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
        'm2_axes_checked':len(housing.JOINT_FIXINGS+housing.END_JOINT_FIXINGS),
        'm3_axes_checked':len(housing.RETAINER_FIXINGS),
        'ceiling_screws_checked':len(housing.CEILING_SCREWS),
        'speaker_mockup_note':'Rear/front curves inferred from owner measurements; physical fit remains to be tested.'
    }
    out=OUT/'assembly-check.json'; out.write_text(json.dumps(reports,indent=2)+'\n')
    print(f'PASS: ten watertight STL parts, 15 insertion positions, direct and gasket assemblies; {out}')

if __name__=='__main__':
    run()
