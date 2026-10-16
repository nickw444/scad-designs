"""Exact B-rep comparison of two STEP solids using build123d/OCCT booleans.

Symmetric-difference volume is a stronger check than mesh samples. Boolean
operations on dense lattices can be expensive, so use cad_compare.py first.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from build123d import import_step


def compare(reference:Path,candidate:Path):
    a=import_step(str(reference));b=import_step(str(candidate))
    missing=(a-b).volume
    extra=(b-a).volume
    return {'reference':str(reference),'candidate':str(candidate),
            'reference_volume_mm3':a.volume,'candidate_volume_mm3':b.volume,
            'missing_volume_mm3':missing,'extra_volume_mm3':extra,
            'symmetric_difference_mm3':missing+extra,
            'reference_valid':a.is_valid,'candidate_valid':b.is_valid}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('reference',type=Path);p.add_argument('candidate',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args();result=json.dumps(compare(a.reference,a.candidate),indent=2)
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(result+'\n')
    print(result)

if __name__=='__main__':main()
