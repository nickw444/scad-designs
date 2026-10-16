"""Printable part registry and canonical names for exports and checks."""
from parts.housing import ceiling_flange, housing_shell
from parts.seals import flat_seam_gasket
from parts.grilles import grille, hex_grille, fine_hex_grille
from parts.retainers import end_retainer
from parts.grommets import cable_grommet, flat_cable_grommet
from parts.template import ceiling_cutout_template

PARTS = {
    "ceiling-flange": ceiling_flange,
    "housing-shell": housing_shell,
    "flat-seam-gasket": flat_seam_gasket,
    "grille": grille,
    "hex-grille": hex_grille,
    "fine-hex-grille": fine_hex_grille,
    "end-retainer": end_retainer,
    "round-cable-grommet": cable_grommet,
    "flat-cable-grommet": flat_cable_grommet,
    "ceiling-cutout-template": ceiling_cutout_template,
}
