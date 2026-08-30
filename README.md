# SCAD designs

Parametric OpenSCAD source for printable designs, with reusable geometry kept separate from model-specific dimensions.

## Layout

```text
models/                      Project families and printable entry points
  10-inch-rack/              Rack projects and their shared geometry
  stitch-guides/             Entries and their project-local shared geometry
  */build/                   Committed STL outputs beside each project
```

Model entry points own their measured dimensions, MakerWorld-facing parameters, preview orientation, and final render call. Shared geometry stays beside its project or project family unless it genuinely serves unrelated designs. Ready-to-print STL exports are committed in each project's local `build/` directory and can be regenerated with `make render`.

## Models

| Model | Entry point | Rendered outputs |
| --- | --- | --- |
| [NBN NTD rack mounts, 0/1/4/6 keystones](https://makerworld.com/en/models/3237154-nbn-ntd-10-inch-rack-mount-with-keystones-cm8200b) | `models/10-inch-rack/nbn-ntd/` | four unnumbered mount variants |
| [UCG Ultra + four keystones](https://makerworld.com/en/models/3237102-1u-ucg-ultra-max-10-inch-rack-mount-4x-keystones) | `models/10-inch-rack/ucg-ultra-4-keystone/ucg-ultra-4-keystone.scad` | assembled STL |
| [Numbered ten-port ⅔U patch panel](https://makerworld.com/en/models/3237051-10-port-2-3u-keystone-patch-panel-for-10-inch-rack) | `models/10-inch-rack/10-port-two-thirds-u-patch-panel/10-port-two-thirds-u-patch-panel.scad` | panel and label STLs |
| [Parametric sous-vide pot lid](https://makerworld.com/en/models/3072514-sous-vide-pot-lid-cover-for-240mm-pot) | `models/sous-vide-pot-lid/sous-vide-pot-lid.scad` | pot-lid STL |
| Sewing stitch guides | `models/stitch-guides/` | four labelled guide STLs |
| [UniFi G5 PTZ soffit mount](https://makerworld.com/en/models/3095613-unifi-g5-ptz-soffit-ceiling-mount#profileId-3488652) | `models/unifi-g5-ptz-soffit-mount/unifi-g5-ptz-soffit-mount.scad` | three carriers and ceiling flange |
| [Tesla trunk hook with M6 nut trap](https://makerworld.com/en/models/3237225-tesla-trunk-hook-with-captured-m6-nut) | `models/tesla-hook/tesla-hook.scad` | nut-retained trunk hook |

Open an entry point in OpenSCAD to use the Customizer. For numbered designs, choose `assembled` for previewing or export `panel` and `labels` separately for aligned multi-material parts.

## Render

OpenSCAD 2021.01 or newer is required.

```sh
make render
make preview
```

These commands render all production STLs and compact project-local PNG previews. Running `make` produces both. Set `OPENSCAD=/path/to/OpenSCAD` when the executable is not on `PATH`; the Makefile also detects the standard macOS application bundle.

## Adding a model

1. Create `models/<project-name>/` with the printable entry point and project-local helpers.
2. Move a helper to the project-family root only when multiple related projects consume it.
3. Keep measured dimensions and documented Customizer controls in that entry point.
4. Add a deterministic render target before publishing.

The initial rack geometry came from Spencer Owen's [10-Inch-Rack-OpenSCAD](https://github.com/spuder/10-Inch-Rack-OpenSCAD) project. It has been specialised and rewritten around these three designs, while retaining the upstream attribution and MIT license in `LICENSES/10-inch-rack-openscad-MIT.txt`.
