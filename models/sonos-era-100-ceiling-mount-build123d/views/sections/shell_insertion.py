"""Regenerate this view beside its definition."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from views.common import section_view


def render():
    section_view(__file__, part='housing-shell', plane='xy', level_mm=20)


if __name__ == '__main__':
    render()
