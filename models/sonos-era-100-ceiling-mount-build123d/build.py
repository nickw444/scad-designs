"""Export printable STLs; optionally export neutral STEP interchange files."""
import argparse
from build123d import export_step, export_stl
from paths import BUILD
from parts import PARTS


def build(names, *, steps=False):
    BUILD.mkdir(exist_ok=True)
    if steps:
        (BUILD/'step').mkdir(exist_ok=True)
    for name in names:
        print(f'Building {name}...', flush=True)
        shape=PARTS[name]()
        if not shape.is_valid or len(shape.solids())!=1:
            raise ValueError(f'{name}: expected one valid solid')
        box=shape.bounding_box()
        spans=(box.size.X,box.size.Y,box.size.Z)
        if max(spans)>256.001:
            raise ValueError(f'{name}: exceeds 256 mm print envelope')
        stl=BUILD/f'era-100-{name}.stl'
        export_stl(shape,str(stl),tolerance=0.08,angular_tolerance=0.2)
        if steps:
            export_step(shape,str(BUILD/'step'/f'era-100-{name}.step'))
        print(f"{name}: {' x '.join(f'{s:.2f}' for s in spans)} mm; "
              f'{shape.volume:.1f} mm³ -> {stl.name}', flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('parts',nargs='*',help='part names; defaults to all')
    parser.add_argument('--step',action='store_true',help='also export STEP under build/step/')
    args=parser.parse_args()
    unknown=set(args.parts)-set(PARTS)
    if unknown:
        parser.error(f"unknown parts: {', '.join(sorted(unknown))}")
    build(args.parts or list(PARTS),steps=args.step)
