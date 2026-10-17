"""Regenerate all or selected annotated dimensional drawings."""
from __future__ import annotations
import argparse
import importlib

DRAWINGS = ('shell_insertion', 'shell_centre_xz', 'flange_fixings',
            'flange_head_clearance', 'cable_passage', 'retainer_before',
            'retainer_after_contact', 'retainer_after_shoulder')


def render(names):
    for name in names:
        importlib.import_module(f'views.drawings.{name}').render()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('drawings', nargs='*', choices=DRAWINGS)
    args = parser.parse_args()
    render(args.drawings or DRAWINGS)
