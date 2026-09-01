# Flush tablet wall mount

This project reproduces the legacy flush tablet mount in `../../tablet-mount/`
as editable OpenSCAD geometry. It contains a shared tablet-side sliding cleat
and two wall-housing variants:

- `round_housing` has a 4 mm power-cable channel.
- `flat_housing` has a 12 mm power-cable/plug channel.
- Both retain the separate 3 mm IR-emitter channel.

The defaults preserve the legacy STL coordinate system, overall dimensions,
fastener locations, cable reservoir, and mating geometry. The cleat is a
100 × 70 × 5 mm dovetail. Its pocket retains 0.25 mm clearance normal to the
45° faces; the corresponding X offset is therefore 0.353553 mm.

## Rendering

From the repository root:

```sh
make models/tablet-mount/build/tablet-mount-round-housing.stl
make models/tablet-mount/build/tablet-mount-flat-housing.stl
make models/tablet-mount/build/tablet-mount-cleat.stl
```

Set `part` in `tablet-mount.scad` to preview a housing, the cleat, or an
assembly in OpenSCAD's Customizer.

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
