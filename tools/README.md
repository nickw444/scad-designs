# CAD inspection tools

These scripts are general purpose and independent of any one model.

- `cad_compare.py`: compares STL pairs or matching directories by closed-mesh status, bounds, volume, and bidirectional sampled point-to-surface distance. Use STEP booleans or physical fit tests when certification is required; sampling can miss a small unsampled feature.
- `cad_compare_step.py`: exact STEP symmetric-difference volume using build123d/OCCT booleans; useful for resolving mesh-sampling uncertainty.
- `cad_sections_build123d.py`: creates exact cross-section SVGs using `build123d.section()` and `ExportSVG`; `section_svg()` accepts native build123d shapes, while the CLI accepts STEP.
- `cad_dimension_drawing.py`: builds an exact build123d section, measures outer and inner wire spans and circular hole diameters, and renders an annotated SVG. `SectionDrawing`, `span_dimension()`, `Leader` and `render_section_drawing()` are reusable from model-specific scripts. Dimension values come from the CAD geometry, not the sampled SVG outline.
- `cad_sections.py`: makes three-axis raster/vector section panels directly from a mesh when STEP is unavailable.
- `cad_render_assembly.py`: camera-based assembly projection using `build123d.project_to_viewport()` and `ExportSVG`. Its `render_shape()` entry point accepts a native build123d compound directly; the CLI reads a STEP manifest. It can rasterize its own SVG to PNG using CairoSVG. Manifest paths are relative to the manifest file.
- `cad_render_shaded.py`: color shaded orthographic PNGs from native build123d assembly components. It tessellates the B-reps and uses a CPU depth buffer, so the camera views can regenerate without a GPU or window server. Its `render_assembly()` entry point accepts an assembly with named components and preserves separate part colors.
- `cad_geometry.py`: small build123d construction helpers for rounded and rectangular prisms, cylinders, cones, XZ extrusions, and radial profiles. Dimensions are in millimetres; Z extents are absolute.
- `cad_view_helpers.py`: writes assembly PNGs, exact section SVGs, and annotated drawing SVGs beside their defining scripts. Pass native assemblies, shapes, and `SectionDrawing` values; keep each model's part selection and colours in that model.
- `cad_assembly.py`: named, placed `Component` solids and an `Assembly` container with `compound()` and `get()` helpers. Components stay separate rather than being fused.

For Python imports, add this directory to `sys.path` or your project environment. A model can use `from cad_geometry import rounded_prism` and `from cad_view_helpers import section_view`. A shaded assembly provides `.components`; each component provides `.shape` and `.part_name` or `.name`. Pass `palette={"part-name": "#rrggbb"}` to `assembly_view()` for project colours. Components may alternatively supply a `color` attribute. Unspecified colours use a neutral blue.

Use `uv sync` at the repository root to create the shared `.venv` from `pyproject.toml` and `uv.lock`. `uv run regen --list` discovers build123d projects with a `regenerate.toml` manifest, then `uv run regen <project>` rebuilds their outputs. The render manifest format for `cad_render_assembly.py` is an array of `{ "file": "part.step", "translation": [0,0,0], "rotation_z": 0 }` entries. Use STEP files to retain exact geometry in the build123d projection.
