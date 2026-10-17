"""Regenerate the revised retainer/speaker XZ contact comparison."""
from math import sqrt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from speaker import SPEAKER_FRONT_RADIUS, SPEAKER_FRONT_Z
from parts import retainers
from parts import housing


def render():
    half = retainers.RETAINER_CONTACT_HALF_WIDTH
    radius = SPEAKER_FRONT_RADIUS
    centre = housing.RETAINER_CENTRE_HEIGHT
    scale, ox, oy = 5.0, 470.0, 220.0
    def point(x,z):
        return f'{ox+x*scale:.2f},{oy-z*scale:.2f}'
    def height(x,cz):
        return cz+radius-sqrt(radius*radius-x*x)
    retainer = ' '.join('L'+point(x,height(x,centre)) for x in range(int(half),-int(half)-1,-1))
    speaker = ' '.join(('M' if x == -int(half) else 'L')+point(x,height(x,SPEAKER_FRONT_Z))
                       for x in range(-int(half),int(half)+1))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="940" height="470" viewBox="0 0 940 470">
<rect width="940" height="470" fill="#f8fafc"/>
<text x="48" y="45" font-size="25" font-family="sans-serif" fill="#172554">Retainer · revised contact profile</text>
<text x="48" y="75" font-size="15" font-family="sans-serif" fill="#475569">X–Z section at Y = -82 mm; dimensions in mm</text>
<path d="M{point(-71.5,0)} L{point(71.5,0)} L{point(71.5,6)} L{point(61.5,7.2)} L{point(half,height(half,centre)-0.2)} {retainer} L{point(-half,height(half,centre)-0.2)} L{point(-61.5,7.2)} L{point(-71.5,6)} Z" fill="#93c5fd" fill-opacity=".65" stroke="#2563eb" stroke-width="2"/>
<path d="{speaker}" fill="none" stroke="#e11d48" stroke-width="2.5" stroke-dasharray="8 5"/>
<path d="M{point(-half,0)} L{point(-half,28)} M{point(half,0)} L{point(half,28)} M{point(0,0)} L{point(0,27)}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 4"/>
<path d="M{point(-half,-3)} L{point(half,-3)}" stroke="#334155" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
<text x="435" y="255" font-size="15" font-family="sans-serif" fill="#334155">80 contact span</text>
<path d="M{point(half,height(half,centre))} L{point(half,height(half,SPEAKER_FRONT_Z))}" stroke="#e11d48" stroke-width="2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
<text x="680" y="126" font-size="15" font-family="sans-serif" fill="#be123c">0.8 nominal gap along arc</text>
<text x="48" y="315" font-size="16" font-family="sans-serif" fill="#2563eb">Blue: revised R{radius:.1f} contact; {centre:.1f} centre height; 6.0 base</text>
<text x="48" y="342" font-size="16" font-family="sans-serif" fill="#be123c">Dashed red: revised R{radius:.1f} speaker dummy, 0.8 mm above retainer</text>
<text x="48" y="382" font-size="15" font-family="sans-serif" fill="#475569">The R{radius:.1f} dummy is a circular proxy for the measured ≈3 mm former end gap.</text>
<text x="48" y="407" font-size="15" font-family="sans-serif" fill="#475569">End shoulders fill the unused height to the fixing areas; see retainer_after_shoulder.svg.</text>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto-start-reverse"><path d="M8 0 L0 4 L8 8" fill="none" stroke="#334155"/></marker></defs>
</svg>'''
    Path(__file__).with_suffix('.svg').write_text(svg)


if __name__=='__main__':
    render()
