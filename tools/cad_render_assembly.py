"""Camera-based technical assembly render using build123d's native projection.

Manifest: [{"file":"part.step", "translation":[0,0,0]}]. The CAD camera
produces SVG with visible and optional hidden edges. PNG uses CairoSVG solely
to rasterize that SVG; no second 3D renderer is involved.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from build123d import Compound, ExportSVG, LineType, Pos, Rot, import_step


def render(manifest: Path, output: Path, camera=(350,-450,280),
           look_at=(0,0,50), hidden=False, width=1400):
    items=json.loads(manifest.read_text())
    shapes=[]
    for item in items:
        shape=import_step(str((manifest.parent/item['file']).resolve()))
        shapes.append(Pos(*item.get('translation',[0,0,0]))*Rot(Z=item.get('rotation_z',0))*shape)
    assembly=Compound(children=shapes)
    return render_shape(assembly, output, camera=camera, look_at=look_at,
                        hidden=hidden, width=width)


def render_shape(shape, output: Path, camera=(350,-450,280),
                 look_at=(0,0,50), hidden=False, width=1400):
    """Project an already-built build123d Shape or Compound from a CAD camera."""
    visible, occluded=shape.project_to_viewport(camera,look_at=look_at)
    edges=list(visible)+list(occluded)
    span=max(Compound(children=edges).bounding_box().size) if edges else 1
    svg=ExportSVG(scale=width/span,margin=12)
    svg.add_layer('Visible',line_color='#172c42',line_weight=1.0)
    svg.add_shape(visible,layer='Visible')
    if hidden:
        svg.add_layer('Hidden',line_color='#aab5c0',line_weight=0.45,
                      line_type=LineType.ISO_DOT)
        svg.add_shape(occluded,layer='Hidden')
    output.parent.mkdir(parents=True,exist_ok=True)
    svg_path=output if output.suffix.lower()=='.svg' else output.with_suffix('.svg')
    svg.write(str(svg_path))
    if output.suffix.lower()=='.png':
        import cairosvg
        cairosvg.svg2png(url=str(svg_path),write_to=str(output),background_color='white')
    return svg_path


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest',type=Path); p.add_argument('--output',type=Path,required=True)
    p.add_argument('--camera',type=float,nargs=3,default=(350,-450,280))
    p.add_argument('--look-at',type=float,nargs=3,default=(0,0,50))
    p.add_argument('--hidden',action='store_true')
    a=p.parse_args(); render(a.manifest,a.output,a.camera,a.look_at,a.hidden)


if __name__=='__main__':
    main()
