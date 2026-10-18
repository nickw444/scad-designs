"""Sonos part selection and styling for the individual view scripts."""
from __future__ import annotations
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
TOOLS = PROJECT.parents[1] / 'tools'
for path in (PROJECT, TOOLS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from assembly import make_assembly
from parts import PARTS
from cad_view_helpers import (
    assembly_view as render_assembly_view,
    section_view as render_section_view,
    dimensioned_view,
)

PALETTE = {
    'ceiling-flange': '#e9bd67',
    'housing-shell': '#6b95c8',
    'end-retainer': '#e78d69',
    'grille': '#9dcfbd',
    'hex-grille': '#9dcfbd',
    'fine-hex-grille': '#9dcfbd',
    'round-cable-grommet': '#756fae',
    'flat-cable-grommet': '#756fae',
    'speaker-dummy': '#d7dce2',
}


def assembly_view(script: str, *, camera, title, look_at=(0, 0, 50),
                  grille='grille',
                  grommet='round-cable-grommet', speaker=False, explode=0):
    assembly = make_assembly(grille=grille, grommet=grommet,
                             speaker=speaker, explode=explode)
    return render_assembly_view(script, assembly, camera=camera,
                                look_at=look_at, title=title, palette=PALETTE)


def section_view(script: str, *, part: str, plane: str, level_mm: float):
    return render_section_view(script, PARTS[part](), plane=plane,
                               level_mm=level_mm)
