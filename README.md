# SCAD designs

Parametric OpenSCAD source for printable designs, with reusable geometry kept separate from model-specific dimensions.

## Layout

```text
lib/                         Reusable modules and geometry
  rack/                      Focused shared rack geometry
models/                      One directory and entry point per printable model
build/                       Committed, ready-to-print STL outputs
```

Model entry points own their measured dimensions, MakerWorld-facing parameters, preview orientation, and final render call. Reusable code belongs under `lib/` and does not render by itself. Ready-to-print STL exports are committed under `build/` and can be regenerated with `make render`.

## Models

| Model | Entry point | Rendered outputs |
| --- | --- | --- |
| NBN NTD + six numbered keystones | `models/nbn-ntd-6-keystone/nbn-ntd-6-keystone.scad` | panel and label STLs |
| UCG Ultra + four keystones | `models/ucg-ultra-4-keystone/ucg-ultra-4-keystone.scad` | assembled STL |
| Numbered ten-port ⅔U patch panel | `models/10-port-two-thirds-u-patch-panel/10-port-two-thirds-u-patch-panel.scad` | panel and label STLs |

Open an entry point in OpenSCAD to use the Customizer. For the two numbered designs, choose `assembled` for previewing or export `panel` and `labels` separately for aligned multi-material parts.

## Render

OpenSCAD 2021.01 or newer is required.

```sh
make render
```

This renders all five production STLs. Set `OPENSCAD=/path/to/OpenSCAD` when the executable is not on `PATH`; the Makefile also detects the standard macOS application bundle.

## Adding a model

1. Put shared primitives or generators under a purpose-specific `lib/<domain>/` directory.
2. Create `models/<model-name>/<model-name>.scad` as the printable entry point.
3. Keep measured dimensions and documented Customizer controls in that entry point.
4. Add a deterministic render target before publishing.

The initial rack geometry came from Spencer Owen's [10-Inch-Rack-OpenSCAD](https://github.com/spuder/10-Inch-Rack-OpenSCAD) project. It has been specialised and rewritten around these three designs, while retaining the upstream attribution and MIT license in `LICENSES/10-inch-rack-openscad-MIT.txt`.
