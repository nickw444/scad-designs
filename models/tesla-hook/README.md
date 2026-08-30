# Tesla trunk hook with M6 nut trap

[View this model on MakerWorld](https://makerworld.com/en/models/3237225-tesla-trunk-hook-with-captured-m6-nut).

This version preserves the hook arms derived from the supplied
`obj_1_Body1.stl` but replaces
its printed M6×1 internal thread with a loose 7.2 mm bolt passage and a side-loaded
hex pocket for a user-supplied metal M6 nut. The nut is immediately beneath a
2 mm top skin so the short exposed bolt can reach farther into the nut while
retaining a solid printed clamping face.

The source mesh measures 62.401 × 61.052 × 45.000 mm. Mesh inspection found
a 0.99985 mm thread pitch, 5.035 mm minor diameter, 6.147 mm crest diameter,
and roughly 14 mm of modeled thread, identifying it as M6×1.

## Hardware

- One standard M6×1 hex nut (ISO 4032 / DIN 934), nominally 10 mm across flats
  and up to 5.2 mm thick.

The default pocket and aligned insertion slot are 10.7 mm across flats and the
pocket is 5.6 mm high. That provides 0.35 mm clearance per flat and 0.4 mm
thickness clearance. Adjust
`nut_side_clearance` in the OpenSCAD Customizer if the nut fit is too tight or
too loose for a particular printer and filament. The original 20 mm tube is
reinforced to 22 mm. A 25 mm foot begins directly on the build plate and tapers
inward continuously to the straight boss, so there is no unsupported flange.
The three hook arms are widened by 1 mm on each horizontal edge (about 2 mm
overall) for a broader, stronger profile without changing their height. The
completed lower hook body is stored in `source/tesla-hook-arms.stl`, keeping
the model reproducible without relying on the separately supplied original.

The 7.2 mm passage gives a nominal M6 bolt about 0.6 mm radial clearance. The
bolt should not bear against the printed bore; the captured metal nut provides
the threaded connection and transfers the clamp load into the 2 mm top face.

## Printing and installation

Print in the modeled orientation on the original flat underside. Slide the M6
nut flat into the opening near the top of the tube until it seats in the hex
pocket. Place the hook over the Tesla's exposed M6 trunk bolt and rotate the
hook to thread the captured nut onto the bolt. The hex pocket reacts the
tightening torque so the plastic no longer carries the load through printed
threads.

The preserved source mesh is included alongside the model and is imported by
`tesla-hook.scad` when rebuilding the printable STL.
