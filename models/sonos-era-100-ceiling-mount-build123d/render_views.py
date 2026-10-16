"""Regenerate the individually defined colour assembly views."""
from __future__ import annotations
import argparse
import importlib

VIEWS = ('rear_assembly', 'room_face', 'exploded_assembly',
         'room_face_fine_hex', 'rear_with_gasket')

def render(names):
    for name in names:
        importlib.import_module(f'views.assembly.{name}').render()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('views', nargs='*', choices=VIEWS)
    args = parser.parse_args()
    render(args.views or VIEWS)
