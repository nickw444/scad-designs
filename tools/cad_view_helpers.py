"""Write rerunnable CAD views beside their defining Python scripts.

The caller supplies a native assembly, shape, or measured SectionDrawing.
Project-specific part registries, variant selection and colour palettes stay
in the model project.
"""
from __future__ import annotations

from pathlib import Path

from cad_dimension_drawing import render_section_drawing
from cad_render_shaded import render_assembly
from cad_sections_build123d import section_svg


def assembly_view(script, assembly, *, camera, title, look_at=(0, 0, 50),
                  palette=None, width=1600, height=1200):
    output = Path(script).with_suffix('.png')
    render_assembly(assembly, output, camera=camera, look_at=look_at,
                    title=title, palette=palette, width=width, height=height)
    print(output)
    return output


def section_view(script, shape, *, plane, level_mm):
    output = Path(script).with_suffix('.svg')
    if not section_svg(shape, plane, level_mm, output):
        raise ValueError(f'{script}: section does not intersect the supplied shape')
    print(output)
    return output


def dimensioned_view(script, drawing, *, title, dimensions, leaders=(), notes=()):
    output = Path(script).with_suffix('.svg')
    render_section_drawing(drawing, output, title=title, dimensions=dimensions,
                           leaders=leaders, notes=notes)
    print(output)
    return output
