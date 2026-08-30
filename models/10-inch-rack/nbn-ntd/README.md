# NBN NTD 10-inch rack mounts

Four variants of the same 1⅓U NBN NTD cradle are kept together for publishing
as one model with selectable print profiles.

| Variant | Layout | Production files |
| --- | --- | --- |
| No keystones | NTD right | `nbn-ntd-no-keystone.stl` |
| 1 keystone | Single port left, NTD right | `nbn-ntd-1-keystone.stl` |
| 4 keystones | Compact 2×2 bank left, NTD right | `nbn-ntd-4-keystone.stl` |
| 6 keystones | Compact 3×2 bank left, NTD right | `nbn-ntd-6-keystone.stl` |

All current production STLs are in the shared `build/` directory. Keystone
frames are intentionally unnumbered and each variant is a single printable mesh.
The NTD opening restores the original rounded profile on both sides, including
a 2 mm inset lip through the first 3 mm of the 4 mm faceplate.
The two-row variants overlap adjacent row frames by one 2.5 mm wall thickness,
removing the previous gap and balancing the faceplate margin above and below.

The existing 3MF files are preserved slicer projects containing earlier variant
geometry or alignment. Use the current STLs above as the canonical geometry.
