# Regenerable views

Each view is defined by a Python script beside its generated image. Run a script from this model directory with the repository-root `../../.venv/bin/python`; the image is written next to the script.

```sh
../../.venv/bin/python views/assembly/exploded_assembly.py
../../.venv/bin/python views/sections/shell_centre_xz.py
../../.venv/bin/python views/drawings/shell_insertion.py
```

The assembly scripts set the camera, selected grille, gasket and exploded spacing. `views/common.py` selects Sonos parts and colours, then calls the reusable helpers in `tools/cad_view_helpers.py`. The section scripts set the part, plane and cut location and export exact build123d section SVGs.

The scripts in `drawings/` make annotated SVGs. Dimension numbers come from the actual build123d section wires or overall part bounds; hole diameters and counts are measured from circular cut wires. They are useful for checking a model before printing. The page is fitted to the image, so it is not a 1:1 cutting template. The drawings do not account for printer shrinkage, fit tolerance or hardware variation.

Run `render_views.py`, `render_sections.py` and `render_drawings.py` from the project root to regenerate the complete sets.
From the repository root, `uv run regen sonos-era-100-ceiling-mount-build123d --only views` regenerates all three view groups through the project manifest.
