"""Reproduce the reference CAD comparison and fail on geometry drift."""
from __future__ import annotations
import json
import sys
import numpy as np
import trimesh
from scipy.spatial import cKDTree
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from cad_compare import compare as mesh_compare
from build123d import import_step
from parts import PARTS as BUILDERS
from parts.housing import CABLE_EXIT_Y, CABLE_HOLE_DIAMETER, INNER_APEX_Z, OUTER_APEX_Z
from geometry import cylinder
from paths import REPORTS

REFERENCE=HERE.parent/'sonos-era-100-ceiling-mount-2'
HEX={'hex-grille','fine-hex-grille'}
PLUG_ADAPTED={'housing-shell','round-cable-grommet','flat-cable-grommet'}
PARTS=['ceiling-flange','housing-shell','flat-seam-gasket','grille',
       'hex-grille','fine-hex-grille','end-retainer',
       'round-cable-grommet','flat-cable-grommet','ceiling-cutout-template']


def run():
    rows={}
    for name in PARTS:
        print(f'Comparing {name}...',flush=True)
        if name in PLUG_ADAPTED:
            candidate=trimesh.load_mesh(HERE/'build'/f'era-100-{name}.stl')
            if not candidate.is_watertight or len(candidate.split())!=1:
                raise AssertionError(f'{name}: adapted STL not one closed solid')
            row={'intentional_change':'Ø32 factory-plug passage and matching split TPU grommet',
                 'candidate_mesh':{'watertight':True,'bounds_mm':candidate.bounds.tolist(),
                                   'volume_mm3':float(candidate.volume)}}
            if name=='housing-shell':
                reference_step=REFERENCE/f'era-100-{name}.step'
                original=import_step(str(reference_step))
                expected=original-cylinder(0,CABLE_EXIT_Y,CABLE_HOLE_DIAMETER/2,
                                           INNER_APEX_Z-5,OUTER_APEX_Z+2)
                actual=BUILDERS[name]()
                missing=(expected-actual).volume
                extra=(actual-expected).volume
                if missing+extra>0.001:
                    raise AssertionError('housing-shell: geometry changed outside plug passage')
                row['brep']={'reference_step':str(reference_step),
                             'expected':'reference shell minus Ø32 cable cylinder',
                             'missing_volume_mm3':missing,'extra_volume_mm3':extra,
                             'symmetric_difference_mm3':missing+extra}
            rows[name]=row
            continue
        mesh=mesh_compare(REFERENCE/'build'/f'era-100-{name}.stl',
                          HERE/'build'/f'era-100-{name}.stl',12000)
        if not mesh['candidate_watertight'] or not mesh['reference_watertight']:
            raise AssertionError(f'{name}: mesh not watertight')
        if mesh['relative_volume_error']>1e-5 or mesh['maximum_bounds_error_mm']>0.1:
            raise AssertionError(f'{name}: mesh volume/bounds drift')
        if mesh['surface_p99_mm']>0.05 or mesh['surface_max_mm']>0.3:
            raise AssertionError(f'{name}: mesh surface drift')
        row={'mesh':mesh}
        if name in HEX:
            a=trimesh.load_mesh(REFERENCE/'build'/f'era-100-{name}.stl')
            b=trimesh.load_mesh(HERE/'build'/f'era-100-{name}.stl')
            vertex_gap=max(cKDTree(a.vertices).query(b.vertices)[0].max(),
                           cKDTree(b.vertices).query(a.vertices)[0].max())
            if len(a.faces)!=len(b.faces) or vertex_gap>1e-4:
                raise AssertionError(f'{name}: complete mesh vertex/face drift')
            row['complete_mesh']={'reference_faces':len(a.faces),
                                  'candidate_faces':len(b.faces),
                                  'bidirectional_max_vertex_gap_mm':float(vertex_gap)}
        else:
            reference_step=REFERENCE/f'era-100-{name}.step'
            reference_shape=import_step(str(reference_step))
            native_shape=BUILDERS[name]()
            missing=(reference_shape-native_shape).volume
            extra=(native_shape-reference_shape).volume
            exact={'reference_step':str(reference_step),
                   'candidate':'native build123d part',
                   'reference_volume_mm3':reference_shape.volume,
                   'candidate_volume_mm3':native_shape.volume,
                   'missing_volume_mm3':missing,
                   'extra_volume_mm3':extra,
                   'symmetric_difference_mm3':missing+extra,
                   'reference_valid':reference_shape.is_valid,
                   'candidate_valid':native_shape.is_valid}
            if exact['symmetric_difference_mm3']>0.001:
                raise AssertionError(f'{name}: exact geometry drift')
            row['brep']=exact
        rows[name]=row
    out=REPORTS/'replication-validation.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(rows,indent=2)+'\n')
    print(f'PASS: seven unchanged STL comparisons, two complete hex mesh comparisons, '
          f'five unchanged STEP/native B-rep comparisons, one exact shell-only plug cut, '
          f'and two adapted grommet mesh checks; {out}')

if __name__=='__main__':run()
