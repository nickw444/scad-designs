# Flush tablet wall mount

This project reproduces the legacy flush tablet mount in `../../tablet-mount/`
as editable OpenSCAD geometry. It contains a shared tablet-side sliding cleat
and eight wall-housing variants formed from cable-routing and wall-box options:

- `round_housing` and `australian_round_housing` have a 4 mm power-cable
  channel.
- `flat_housing` and `australian_flat_housing` have a 12 mm power-cable/plug
  channel.
- Both retain the separate 3 mm IR-emitter channel.
- The original housings retain their 40 mm countersunk fixing pattern.
- The Australian housings use horizontal 84 mm fixing centres for an
  electrical box, a counterbored M3.5 dome-head screw pocket, and an unbroken
  rear face plate across the former top cut-down.
- The portrait Australian housings rotate the wall-box fixing pattern to
  vertical 84 mm centres and use a dedicated 70 × 100 mm vertical cleat.
- The combined European/UK housings use horizontal 60.3 mm fixing centres and
  retain the original horizontal cleat.

The defaults preserve the legacy STL coordinate system, overall dimensions,
fastener locations, cable reservoir, and mating geometry. The cleat is a
100 × 70 × 5 mm dovetail. Its pocket retains 0.25 mm clearance normal to the
45° faces; the corresponding X offset is therefore 0.353553 mm.

## Rendering

From the repository root:

```sh
make models/tablet-mount/build/tablet-mount-round-housing.stl
make models/tablet-mount/build/tablet-mount-flat-housing.stl
make models/tablet-mount/build/tablet-mount-australian-round-housing.stl
make models/tablet-mount/build/tablet-mount-australian-flat-housing.stl
make models/tablet-mount/build/tablet-mount-australian-vertical-round-housing.stl
make models/tablet-mount/build/tablet-mount-australian-vertical-flat-housing.stl
make models/tablet-mount/build/tablet-mount-european-uk-round-housing.stl
make models/tablet-mount/build/tablet-mount-european-uk-flat-housing.stl
make models/tablet-mount/build/tablet-mount-cleat.stl
make models/tablet-mount/build/tablet-mount-vertical-cleat.stl
```

Set `part` in `tablet-mount.scad` to preview a housing, the cleat, or an
assembly in OpenSCAD's Customizer.

## Australian electrical-box fixing pattern

The Australian fixing centres are at X = 8 mm and X = 92 mm, giving exactly
84 mm horizontal spacing while remaining centred on the 100 mm cleat pocket.
Both centres are at Y = 35 mm, the vertical centre of the housing's -5 to
75 mm outer bounds.

The intended M3.5 dome-head screw has a nominal 7.35 mm head diameter and
1.93 mm head height. The printable void adds tolerance as follows:

- 4.00 mm through bore (3.50 mm nominal plus 0.50 mm diametral clearance).
- 7.85 mm flat-bottomed head bore (7.35 mm plus 0.50 mm clearance).
- 3.00 mm head-bore depth (1.93 mm head plus 1.07 mm depth allowance).

This leaves 2.00 mm of material beneath the recessed head in the 5 mm back
plate. The cleat pocket and external housing geometry are unchanged, so the
existing cleat is shared by all four landscape housings.

Unlike the legacy housing, each Australian housing omits the through-cut
entry notch from the rear of the upper 25 mm. The dovetail pocket remains open
from the front and top for cleat insertion, but the wall-facing side is a
continuous rounded rectangular plate over the electrical box.

## Portrait Australian electrical-box version

The portrait face plate is 80 × 110 mm, with fixing centres at X = 35 mm and
Y = 8 mm / 92 mm. This gives exactly 84 mm vertical spacing centred on both
plate axes. It uses the same 4.00 mm screw bores and 7.85 × 3.00 mm head bores
as the horizontal Australian plate.

The dedicated vertical cleat is 70 × 100 × 5 mm. Its captured dovetail run,
clearances, depth, and 5 mm lead-in transition match the legacy cleat system,
but its portrait dimensions require the separate cleat. The rear cable
reservoir is centred at X = 35 mm, Y = 50 mm to remain clear of both mounting
screws, and both round- and flat-channel housing variants are provided.

## European and UK electrical-box version

UK BS 4662 single-gang boxes use horizontal 60.3 mm fixing centres with M3.5
screws. Continental European device boxes commonly use horizontal 60.0 mm
centres with M3 screws. The shared European/UK pattern is therefore placed at
X = 19.85 mm and X = 80.15 mm, centred at Y = 35 mm. Its 4.00 mm through bores
leave enough radial clearance for the 0.15 mm-per-side offset of a 60.0 mm
European box, while exactly matching the UK centres.

These variants use the same 7.85 × 3.00 mm flat-bottomed head bores and full
rear plate as the Australian housings. The external 110 × 80 mm geometry and
100 × 70 mm pocket remain unchanged, so the original horizontal cleat is fully
compatible. The plate covers typical 67–68 mm continental openings and UK
boxes up to approximately 75 mm square; at that maximum UK size, the vertical
overlap is approximately 2.5 mm per edge.

Reference dimensions were checked against the current
[BS 4662 listing](https://knowledge.bsigroup.com/products/boxes-for-flush-mounting-of-electrical-accessories-requirements-test-methods-and-dimensions),
[MK box catalogue](https://www.farnell.com/datasheets/1686253.pdf), and a
[JUNG continental wall box](https://www.jung-group.com/en-DE/p/Wall-box-1-gang-depth-66-mm-black/1556-04).

## Legacy-mesh verification

The rendered outputs were compared directly with the three source STLs using
watertight-mesh Boolean intersection and bidirectional surface sampling:

| Part | Bounds | Volume delta | Boolean symmetric difference |
| --- | --- | ---: | ---: |
| Round-channel housing | exact | -0.641 mm³ (-0.00169%) | 1.903 mm³ (0.00503%) |
| Flat-channel housing | exact | -0.649 mm³ (-0.00178%) | 1.751 mm³ (0.00481%) |
| Cleat | exact | 0 mm³ | numerical identity |

Both housing meshes are watertight and have the same Euler characteristic as
their references. Across 100,000 samples in each direction, more than 99.9%
of each housing surface was within 0.01 mm; the RMS separation was below
0.0008 mm. The tiny residual is tessellation of curved and ruled surfaces, not
a change to the measured dimensions or the seated cleat interface.
