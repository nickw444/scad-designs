"""Regenerate the individually defined exact section views."""
from __future__ import annotations
import argparse
import importlib

SECTIONS = ('shell_insertion', 'shell_mid_depth', 'shell_roof',
            'shell_centre_xz', 'shell_centre_yz', 'flange_joint')

def render(names):
    for name in names:
        importlib.import_module(f'views.sections.{name}').render()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sections', nargs='*', choices=SECTIONS)
    args = parser.parse_args()
    render(args.sections or SECTIONS)
