"""Compare unchanged grille variants with the prior CAD project.

The first printed prototype intentionally changes the other seven parts.
"""
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
from paths import REPORTS

REFERENCE=HERE.parent/'sonos-era-100-ceiling-mount-2'
HEX={'hex-grille','fine-hex-grille'}
ADAPTED={
    'ceiling-flange':'open retainer slots, outer-end tab pockets, no magnet pockets and four M3 joint holes',
    'housing-shell':'shorter roof, Ø32 cable passage and four M3 joint bosses',
    'flat-seam-gasket':'one-piece joint interface includes the retainer contact areas',
    'end-retainer':'full-depth base, outer-end capture tabs and M3 head recess',
    'round-cable-grommet':'resized for Ø32 cable passage',
    'flat-cable-grommet':'resized for Ø32 cable passage',
    'ceiling-cutout-template':'follows the revised shell bosses',
}
PARTS=['ceiling-flange','housing-shell','flat-seam-gasket','grille',
       'hex-grille','fine-hex-grille','end-retainer',
       'round-cable-grommet','flat-cable-grommet','ceiling-cutout-template']


def run():
    rows={}
    for name in PARTS:
        print(f'Comparing {name}...',flush=True)
        if name in ADAPTED:
            candidate=trimesh.load_mesh(HERE/'build'/f'era-100-{name}.stl')
            if not candidate.is_watertight or len(candidate.split())!=1:
                raise AssertionError(f'{name}: adapted STL not one closed solid')
            rows[name]={'intentional_change':ADAPTED[name],
                        'candidate_mesh':{'watertight':True,
                                          'bounds_mm':candidate.bounds.tolist(),
                                          'volume_mm3':float(candidate.volume)}}
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
    print(f'PASS: three unchanged grille STL comparisons, two complete hex mesh comparisons, '
          f'one exact STEP/native grille comparison, and seven adapted closed meshes; {out}')

if __name__=='__main__':run()
