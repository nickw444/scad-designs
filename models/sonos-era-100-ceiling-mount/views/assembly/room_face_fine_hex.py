"""Regenerate this view beside its definition."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from views.common import assembly_view


def render():
    assembly_view(__file__, camera=(300, -380, -260), title='Fine hex grille · room face', grille='fine-hex-grille')


if __name__ == '__main__':
    render()
