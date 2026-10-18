"""Regenerate this view beside its definition."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from views.common import assembly_view


def render():
    assembly_view(__file__, camera=(350, -450, 280), title='Exploded assembly', explode=45)


if __name__ == '__main__':
    render()
