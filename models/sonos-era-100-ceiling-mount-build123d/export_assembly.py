"""Export a selected installed assembly as a multi-solid STEP compound."""
from __future__ import annotations
import argparse
from build123d import export_step
from assembly import GRILLES, GROMMETS, make_assembly
from paths import STEP_EXPORTS


def export(grille='grille', grommet='round-cable-grommet',
           speaker=False):
    assembly=make_assembly(grille=grille,grommet=grommet,
                           speaker=speaker)
    suffix='-speaker-dummy' if speaker else ''
    path=STEP_EXPORTS/f'era-100-assembly-{grille}-{grommet}{suffix}.step'
    STEP_EXPORTS.mkdir(parents=True,exist_ok=True)
    export_step(assembly.compound(),str(path))
    print(f'{len(assembly.components)} components -> {path}')
    return path


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--grille',choices=GRILLES,default='grille')
    parser.add_argument('--grommet',choices=GROMMETS,default='round-cable-grommet')
    parser.add_argument('--speaker-dummy',action='store_true')
    args=parser.parse_args()
    export(args.grille,args.grommet,args.speaker_dummy)
