"""Native build123d placement of the ceiling mount's installed components.

Coordinates match the part modules: XY is the ceiling plane and +Z points into
its cavity. An Assembly is a compound of placed solids; parts are not fused.
"""
from __future__ import annotations
import sys
from pathlib import Path
from build123d import Pos, Rot, Shape

TOOLS = Path(__file__).resolve().parents[2] / 'tools'
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cad_assembly import Assembly, Component
from parts.housing import CABLE_EXIT_Y, OUTER_APEX_Z
from parts.grommets import GROMMET_FLANGE_THICKNESS
from parts.seals import FLAT_GASKET_THICKNESS
from parts import PARTS
from speaker import speaker_mockup

GRILLES = ('grille', 'hex-grille', 'fine-hex-grille')
GROMMETS = ('round-cable-grommet', 'flat-cable-grommet')


def grommet_placement(*, shell_shift=0.0, explode=0.0):
    """Seat the flange outside the rear roof; the stem enters toward the room."""
    return (Pos(0, CABLE_EXIT_Y,
                OUTER_APEX_Z + GROMMET_FLANGE_THICKNESS + shell_shift +
                1.5 * explode) * Rot(X=180))


def make_assembly(*, grille: str = 'grille', gasket: bool = False,
                  grommet: str = 'round-cable-grommet',
                  speaker: bool = False, explode: float = 0.0) -> Assembly:
    """Place one selected grille/grommet and both end retainers.

    `explode` is a view-only separation in millimetres. The gasket raises the
    shell by its 0.6 mm thickness while the grille and retainers stay seated.
    """
    if grille not in GRILLES:
        raise ValueError(f'Unknown grille: {grille}')
    if grommet not in GROMMETS:
        raise ValueError(f'Unknown grommet: {grommet}')
    cache: dict[str, Shape] = {}

    def part(name: str) -> Shape:
        if name not in cache:
            cache[name] = PARTS[name]()
        return cache[name]

    z_shift = FLAT_GASKET_THICKNESS if gasket else 0.0
    placed = [Component('ceiling-flange', 'ceiling-flange', part('ceiling-flange'))]
    if gasket:
        placed.append(Component('flat-seam-gasket', 'flat-seam-gasket',
                                Pos(0, 0, explode / 2) * part('flat-seam-gasket')))
    placed.append(Component('housing-shell', 'housing-shell',
                            Pos(0, 0, z_shift + explode) * part('housing-shell')))
    stop = part('end-retainer')
    placed.extend([
        Component('retainer-south', 'end-retainer', Pos(0, 0, -explode / 3) * stop),
        Component('retainer-north', 'end-retainer',
                  Pos(0, 0, -explode / 3) * Rot(Z=180) * stop),
        Component('grille', grille, Pos(0, 0, -explode) * part(grille)),
        Component('cable-grommet', grommet,
                  grommet_placement(shell_shift=z_shift, explode=explode) * part(grommet)),
    ])
    if speaker:
        placed.append(Component('speaker-dummy', 'speaker-dummy',
                                Pos(0, 0, -explode / 2) * speaker_mockup()))
    return Assembly(tuple(placed))
