# Sonos Era 100 ceiling mount — build123d project

This is a parametric [build123d](https://github.com/gumyr/build123d) ceiling mount for the Sonos Era 100. The source is Python/build123d algebra mode. STL files are print exports; STEP is available as an optional interchange export. XY is the ceiling plane, +Z points into the cavity, and dimensions are in millimetres.

## Project layout

| Location | Responsibility |
| --- | --- |
| `geometry.py` | Import bridge to the shared construction primitives in `../../tools/cad_geometry.py` |
| `parts/` | Independently editable part builders with their own dimensions; each part imports mating dimensions from the part that owns them |
| `parts/__init__.py` | Printable part registry |
| `speaker.py` | Measured/inferred Era 100 dimensions and dummy for fit checks |
| `assembly.py` | Installed positions and grille/grommet variants; uses shared `tools/cad_assembly.py` containers |
| `views/assembly/` | One runnable Python camera definition beside each shaded colour PNG |
| `views/sections/` | One runnable Python cut definition beside each exact section SVG |
| `views/drawings/` | One runnable annotated dimension drawing beside its SVG |
| `views/common.py` | Sonos assembly/part selection and colour palette; delegates output to shared `tools/cad_view_helpers.py` |
| `render_views.py`, `render_sections.py`, `render_drawings.py` | Commands to regenerate all or selected views |
| `regenerate.toml` | Build123d artifact stages used by the repository-root `uv run regen` command |
| `build.py` | Individual part STL exports, with optional STEP export |
| `export_assembly.py` | Selected installed assembly as a multi-solid STEP |
| `validate.py` | Assembly clearance and export checks |
| `paths.py` | Project output paths |

`assembly.make_assembly()` returns separate placed build123d solids as an `Assembly`. Its `compound()` method is suitable for rendering or inspection; it does not fuse the printed parts. The ceiling cutout template is a tool, so it is in the part registry but is not installed in the assembly.

Dimensions live with the part that defines the feature. `speaker.py` owns the measured speaker envelope; `parts/housing.py` owns the shared shell/flange seats and fixing locations; the grille, retainers, grommets and cutout template define their own sizes and import only the mating dimensions they need. There is no global dimensions module.

The shell has a Ø32 mm rear cable passage for the factory plug, measured at approximately 30 mm across. Feed the plug through the shell before pressing a split TPU grommet around the cable. Both round- and flat-cable grommets have Ø40 mm rear flanges that cover the passage; their stems press into it. The [annotated cable-passage section](views/drawings/cable_passage.svg) measures the opening from the CAD solid. The plug allowance is based on an approximate measurement, so check its thickest orientation before printing the replacement shell.

The flange has a 1.3 mm wide, 1.5 mm tall locating lip along the cavity edge. The shell has a 1.55 mm wide, 1.8 mm deep rebate cut from its inner edge, leaving 2.95 mm of continuous outer wall. This gives 0.25 mm clearance at the outer flank and 0.3 mm at the tip, so the PETG face surfaces meet at Z = 6 mm. The [joint section](views/drawings/seam_joint.svg) shows the fit. The lip stops at the retainer openings; widened shell bosses cover the full width of those openings and extend at least 2 mm beyond each side. Both flange and shell must be printed as the mating pair for this revision.

The shell is 142.5 mm high from the flange interface to its rear face. Its straight walls are 4.5 mm thick, flat rear roof is 5.0 mm thick, and 45° shoulders are approximately 4.95 mm thick measured normal to their faces. The lower shoulder ridges and sloped end edges have 3 mm fillets; the flat rear build-plate face has a 1 mm perimeter chamfer. The cavity's flat roof is 5 mm beyond the modeled speaker rear apex; the physical speaker should be measured before treating this as a guaranteed fit.

The retainer's 6 mm base passes through the flange without a bridge over the slot. A flat 2 mm thick tab at each outer end extends 3 mm past the retainer bar. The tabs seat in matching underside pockets and hold the flange against the shell. Print the flange pockets with supports.

The retainer has a provisional 60 mm front-contact radius, also used by the speaker dummy. Its top slopes from the curved contact toward each fixing area within the 14 mm bar width. The flange seat and outer tab pockets have 0.35 mm insertion clearance on each side; the fixing pads have 0.3 mm per side. The [retainer profile drawing](views/drawings/retainer_profile.svg) shows the current section. Physical fit and loaded deflection still need a print test.

The [seated assembly depth section](views/drawings/assembly_depth.svg) measures 136.3 mm from the retainer's centre contact to the shell's inner rear roof. With a 130.7 mm measured speaker depth seated on the retainer, the centreline rear gap is 5.6 mm. The 130.5 mm default dummy was used when sizing the existing shell; the measured-depth envelope is checked separately without moving the shell roof.

The grille uses the perimeter clips; the ceiling flange has no magnet pockets.

## Prototype fasteners

- Four M3 × 10 mm cap-head bolts join the ceiling flange to the shell: two at the side midpoints and one at each end midpoint. Four more M3 × 10 mm cap-head bolts secure the two end retainers.
- The joint head counterbores leave at least 3 mm of flange material to the inner opening: 3.6 mm at the sides and 3.35 mm at the ends. See the [underside head-clearance drawing](views/drawings/flange_head_clearance.svg).
- All eight cap heads are designed for Ø5.5 mm heads, 3.0 mm head height, and Ø5.8 × 4.0 mm counterbores. The M3 insert pilots are Ø4.0 mm for the measured Ø4.4 mm heat-set inserts.
- The four joint bolts extend 8.0 mm past the flange into the insert pilots. The retainer bolts extend 6.3 mm past their pad interface. The 20 mm bolts are too long for these pilots.
- The six ceiling-mount screw holes are sized for 6g screws.

## Rebuild and inspect

From the repository root, create the shared environment and regenerate every declared output:

```sh
uv sync
uv run regen sonos-era-100-ceiling-mount-build123d
```

Use `uv run regen sonos-era-100-ceiling-mount-build123d --only build`, `--only checks`, or `--only views` for one stage. For individual scripts, run from this model directory with the root environment:

```sh
../../.venv/bin/python build.py
../../.venv/bin/python validate.py
../../.venv/bin/python render_views.py
../../.venv/bin/python render_sections.py
../../.venv/bin/python render_drawings.py
../../.venv/bin/python views/assembly/rear_assembly.py
../../.venv/bin/python views/sections/flange_joint.py
../../.venv/bin/python views/drawings/shell_insertion.py
```

Select a part or camera view by name:

```sh
../../.venv/bin/python build.py housing-shell end-retainer
../../.venv/bin/python render_views.py exploded_assembly rear_assembly
../../.venv/bin/python render_sections.py shell_centre_xz flange_joint
../../.venv/bin/python render_drawings.py shell_insertion flange_fixings
../../.venv/bin/python build.py housing-shell --step
../../.venv/bin/python export_assembly.py --grille fine-hex-grille
```

Add a new printable part in `parts/`, then register its builder in `parts/__init__.py`. Copy a view script under `views/assembly/`, `views/sections/` or `views/drawings/` and set its camera, cut plane or measurement spans. Run that script directly to regenerate its adjacent image. The repository's [`tools/`](../../tools/README.md) directory has reusable assembly rendering, measured drawing, and section helpers.

The nine printable STL exports are in `build/`. Optional STEP exports go in `build/step/`. Generated views live beside their scripts under `views/`, while the current assembly-check report goes in `build/reports/`. The Python model is authoritative; STEP is useful when passing editable solids to another CAD application.

## Validation and source

The assembly check covers the speaker dummy at 15 insertion positions, the locating rebate and retainer boss coverage, screw axes, a Ø30 mm plug passage, and cable grommet compression. Design credit: [Sonos One/Play:1 ceiling mount on MakerWorld](https://makerworld.com/en/models/1931421-sonos-one-play1-ceiling-mount#profileId-2073402).

The dummy's front and rear curves are based on owner measurements, not a manufacturer CAD model. Physical insertion, cable fit and grille pull-off force still require print testing.
