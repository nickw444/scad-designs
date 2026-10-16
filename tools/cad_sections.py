"""Draw arbitrary orthogonal mesh cross sections as a reproducible SVG or PNG.

Example: python tools/cad_sections.py part.stl --output sections.svg --levels 0,6,20
"""
from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import trimesh

AXES = [('XY',(0,0,1)),('XZ',(0,1,0)),('YZ',(1,0,0))]


def draw(mesh_path: Path, output: Path, levels: list[float]):
    mesh = trimesh.load_mesh(mesh_path, process=False)
    fig, axes = plt.subplots(3, len(levels), figsize=(5*len(levels), 13), squeeze=False)
    for row,(label,normal) in enumerate(AXES):
        coordinate = np.argmax(normal)
        for col,level in enumerate(levels):
            ax = axes[row,col]
            origin = np.zeros(3); origin[coordinate]=level
            section = mesh.section(plane_origin=origin, plane_normal=normal)
            if section is not None:
                planar,_ = section.to_2D()
                for path in planar.discrete:
                    ax.plot(path[:,0],path[:,1],color='#173a5e',linewidth=.8)
            ax.set_title(f'{label} @ {level:g} mm')
            ax.set_aspect('equal',adjustable='box')
            ax.grid(alpha=.2)
            ax.set_xlabel('mm'); ax.set_ylabel('mm')
    fig.tight_layout()
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output)
    plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mesh',type=Path)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--levels',default='0,6,20')
    a=p.parse_args()
    draw(a.mesh,a.output,[float(v) for v in a.levels.split(',')])


if __name__=='__main__':
    main()
