"""Regenerate the immutable, measured-as-printed retainer baseline drawing."""
from math import sqrt
from pathlib import Path

# Frozen at the first printed prototype, before changing the retainer geometry.
HALF_CONTACT = 40.0
OLD_RADIUS = 70.0
OLD_CENTRE_Z = 7.2
OLD_SEAT_Z = 6.0
OLD_WIDTH = 14.0
MEASURED_END_GAP = 3.0
INFERRED_RADIUS = (HALF_CONTACT**2 + (OLD_RADIUS-sqrt(OLD_RADIUS**2-HALF_CONTACT**2)+MEASURED_END_GAP)**2) / (2*(OLD_RADIUS-sqrt(OLD_RADIUS**2-HALF_CONTACT**2)+MEASURED_END_GAP))


def render():
    scale = 5.0
    ox, oy = 470.0, 220.0
    def point(x, z):
        return f'{ox+x*scale:.2f},{oy-z*scale:.2f}'
    def curve(radius, centre):
        return ' '.join(('M' if x == -40 else 'L') + point(x, centre+radius-sqrt(radius*radius-x*x))
                        for x in range(-40,41))
    retainer_reverse = ' '.join('L'+point(x, OLD_CENTRE_Z+OLD_RADIUS-sqrt(OLD_RADIUS**2-x*x))
                                for x in range(40,-41,-1))
    inferred = curve(INFERRED_RADIUS, OLD_CENTRE_Z)
    gap_z = OLD_CENTRE_Z + OLD_RADIUS-sqrt(OLD_RADIUS**2-HALF_CONTACT**2)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="940" height="470" viewBox="0 0 940 470">
<rect width="940" height="470" fill="#f8fafc"/>
<text x="48" y="45" font-size="25" font-family="sans-serif" fill="#172554">Retainer · before first fit revision</text>
<text x="48" y="75" font-size="15" font-family="sans-serif" fill="#475569">X–Z section at Y = 82 mm; dimensions in mm</text>
<path d="M{point(-71.5,0)} L{point(71.5,0)} L{point(71.5,6)} L{point(40,6)} {retainer_reverse} L{point(-40,6)} L{point(-71.5,6)} Z" fill="#93c5fd" fill-opacity=".65" stroke="#2563eb" stroke-width="2"/>
<path d="{inferred}" fill="none" stroke="#e11d48" stroke-width="2.5" stroke-dasharray="8 5"/>
<path d="M{point(-40,0)} L{point(-40,28)} M{point(40,0)} L{point(40,28)} M{point(0,0)} L{point(0,27)}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 4"/>
<path d="M{point(-40,-3)} L{point(40,-3)}" stroke="#334155" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
<text x="435" y="255" font-size="15" font-family="sans-serif" fill="#334155">80 contact span</text>
<path d="M{point(40,gap_z)} L{point(40,gap_z+MEASURED_END_GAP)}" stroke="#e11d48" stroke-width="2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
<text x="680" y="126" font-size="15" font-family="sans-serif" fill="#be123c">≈3 end gap, reported on print</text>
<text x="48" y="315" font-size="16" font-family="sans-serif" fill="#2563eb">Blue: original R70 contact; 7.2 centre height; 6.0 base</text>
<text x="48" y="342" font-size="16" font-family="sans-serif" fill="#be123c">Dashed red: inferred loaded speaker front, R{INFERRED_RADIUS:.1f} from ≈3 end gap</text>
<text x="48" y="382" font-size="15" font-family="sans-serif" fill="#475569">This is an inference from the owner's printed fit, not a direct radius measurement.</text>
<text x="48" y="407" font-size="15" font-family="sans-serif" fill="#475569">Existing bar is {OLD_WIDTH:.0f} wide in Y; there is no rear stiffening rib.</text>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto-start-reverse"><path d="M8 0 L0 4 L8 8" fill="none" stroke="#334155"/></marker></defs>
</svg>'''
    Path(__file__).with_suffix('.svg').write_text(svg)


if __name__ == '__main__':
    render()
