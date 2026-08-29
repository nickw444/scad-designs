# UniFi G5 PTZ soffit mount

[View this model on MakerWorld](https://makerworld.com/en/models/3095613-unifi-g5-ptz-soffit-ceiling-mount#profileId-3488652).

Parametric two-part OpenSCAD mount for installing a UniFi G5 PTZ beneath a
soffit.

The camera carrier attaches to the camera and houses its cable grommet. A
separate ceiling flange screws to the soffit; the carrier inserts into it and
locks with a short three-lug bayonet twist.

## Current camera fit

The camera-body seating face is `z=0`.

| Feature | Camera measurement | Modeled contact top | Clearance |
|---|---:|---:|---:|
| Ordinary fin faces | 5.10 mm | 4.90 mm | 0.20 mm |
| Tall fin face | 8.30 mm | 7.50 mm | 0.80 mm |
| Tall-fin detent tip | 7.60 mm | 7.50 mm approach plateau | 0.10 mm |
| Tall-fin detent depth | 0.70 mm | 6.80 mm relief floor | — |

Only the physically confirmed clockwise locking detent is modeled. Its carrier
relief is now a positive-sided 2.6 mm rectangular groove rather than a V. The
camera detent’s own taper provides the climbing action. This revision keeps
the ordinary contacts loose and uses the camera’s rubber base gasket for final
axial preload rather than tight fin contact.

Direct measurements from the fin mating faces to the camera's upper gasket
corner cross-check the locked height: `4.9 + 10.0 mm` from an ordinary contact
and `7.5 + 7.4 mm` from the locking contact both place that corner at
`z=14.9 mm` in the carrier.

## Alignment datum

Viewed from the camera side, the camera security-screw hole defines the true
front datum. The previous front marker sat 3.0 mm to its right at the 60.4 mm
carrier diameter, so the body datum is corrected by `-5.691°` relative to the
proven camera-fin pattern.

The grommet flat, axial camera-retention screw, UniFi-logo/front marker, and
exterior UniFi security screw all derive from this corrected axis. The
ceiling-interface screw is exactly opposite at the rear. The camera contact
pattern itself stays at its physically tested rotation.

## Top-loaded grommet seat

The remeasured grommet body is a 32.0 mm circle truncated by the approximately
15.8 mm flat chord and is 16.0 mm high. Holding that chord measurement gives
29.92 mm from the flat to the opposite round edge.

The carrier uses:

- 32.5 × 30.42 mm truncated-circle pocket
- 0.5 mm total profile clearance (0.25 mm per side)
- a flat-side chordal shelf matching the factory bracket

The grommet is inserted from the ceiling side and stops positively on the
2.0 mm-thick chordal shelf at `z=17.4`. Its camera-facing underside remains at
`z=15.4`, 0.5 mm above the locked camera's measured upper surface. The shelf
is only a cap on the flat/front side—not a surrounding
perimeter ledge. Everywhere else, the opening below follows the grommet’s
circular perimeter. The 16.0 mm grommet projects upward to `z=33.4`; the
matching D-shaped guide continues vertically to the ceiling side for
insertion. The corrected height allows the compact carrier to be 33.9 mm tall
while retaining 0.5 mm of channel above the gasket and the complete validated
7.15 mm ceiling-bayonet stack.

The `carrier_extension` source parameter raises the gasket shelf and complete
ceiling-bayonet stack together. The top of the gasket is always 16.0 mm above
the shelf face and remains 0.5 mm below the carrier top, avoiding a deep open
shaft above the gasket. The supplied production variants use 0, 15, and 30 mm
extensions, giving overall carrier heights of 33.9, 48.9, and 63.9 mm
respectively.

On the extended carriers, the raised chordal shelf forms a pedestal above the
original 2.0 mm camera-screw shelf. A 6.5 mm diameter access well passes down
through that pedestal so the original factory screw head and driver can still
reach the unchanged 3.0 mm clearance hole at the camera.

The lower camera cavity uses a support-free 45-degree wall against the measured
45.5 mm outer upper corner of the camera gasket. It begins at the 52.4 mm guide
diameter at `z=11.35` and reaches a 44.3 mm diameter at the horizontal plane at
`z=15.4`. At the measured corner plane (`z=14.9`) it provides 0.1 mm nominal
edge preload. The horizontal plane itself remains 0.5 mm above the camera and
is clearance rather than a pressure land.

The flat/front shelf includes a 3.0 mm axial clearance hole for the screw into
the camera's factory threaded retention point. The confirmed hole centre
remains at an 11.6 mm radius and the inner shelf chord remains at 8.6 mm. With
the cleared grommet pocket, the pocket flat is at approximately 14.17 mm,
giving 1.5 mm of material at the inner hole edge and approximately 1.07 mm at
the outer edge. The final screw thread and length must be confirmed against
the camera before installation.

The camera's outer radial rubber gasket is handled separately from the central
cable grommet. The 45-degree wall bears on the compliant outer corner rather
than a support-printed horizontal underside. The central cable-grommet shelf
and camera security screw remain in the separate flat plate above.

## Ownership markings

Both printed parts are debossed with `© 2026` and `Nick Whyte`. The carrier
marking is on the concealed flat annular floor of its upper bayonet socket,
outside the cable-grommet pocket. The ceiling-flange marking is on its
concealed ceiling-facing flat, mirrored to read correctly from that exterior
side and positioned clear of the cable and fixing holes.

## Reinforced and positively locked ceiling bayonet

The ceiling joint uses three concentric annular-sector load-bearing lugs. Each
lug and carrier entry slot has curved inner and outer faces centred on the
part axis, with straight end faces that radiate from the centre:

- 1.88 mm radial engagement under the carrier lips
- two 26-degree lugs in 34-degree entry slots
- one keyed 38-degree lug in its unique 46-degree entry slot
- matching 45-degree lug and retaining-lip ramps
- approximately 1.9 mm minimum lug thickness at the outer capture edge
- approximately 3.9 mm lug thickness at the reinforced root
- 3.0 mm retaining-lip thickness
- inward reinforcement pads behind all three lug roots
- exactly 35 degrees of clockwise nominal locking rotation, viewed from below
- radial stop faces that land at the security-screw/pilot alignment
- anti-reverse shoulders that permit rotation only toward the locked position

The longer keyed lug cannot pass through either ordinary entry slot, so the
flange and carrier can only be brought together in the orientation that leads
to the security-screw pilot after the clockwise locking turn.

At the locked position, the supplied UniFi self-tapping security screw aligns
with a reinforced inward boss on the ceiling-flange spigot. Its measured major
thread diameter is 2.5 mm and its length is 8.4 mm. The flange has a circular
2.0 mm diameter × 4.8 mm deep blind pilot, leaving 0.7 mm of solid material at
the inner end of the strengthened boss.

The carrier has a 3.0 mm clearance bore for the thread. Its measured 5.7 mm
diameter × 0.7 mm thick head sits in a circular 6.2 mm diameter × 1.0 mm deep
flat-bottom counterbore, providing 0.25 mm radial and 0.3 mm depth tolerance so
the head can sit flush. Insert the carrier, rotate it fully to the locked
position, and only then form the thread with the screw. The three bayonet lugs
carry the axial load; the screw prevents the joint from counter-rotating
toward the insertion gaps.

The three ceiling mounting-hole centres remain on their original 40.0 mm
pitch circle. Their Ø4.4 mm through holes now have Ø9.0 × 3.7 mm flat-bottom
head recesses, deepened by 1.2 mm and widened by 0.6 mm from the earlier
revision so the countersunk mounting-screw heads sit below the flange face.

The ceiling cable cutout is pre-rotated in the flange so that, after the
35-degree locking twist, its short-side normal shares the carrier grommet-flat
datum and its long edge is parallel to the grommet's D-flat chord.

## Support-free print features

Print the carrier camera-side down and the flange ceiling-face down. The
bayonet retaining lips and flange lugs use matching 45-degree ramps, so neither
part begins with an unsupported horizontal ledge. The radial screw clearance,
flat-bottom head counterbore, and self-tapping pilot are deliberately true
circular bores.

The camera-gasket contact is itself a 45-degree self-supporting wall, so its
fit no longer depends on the underside quality of a supported flat land. The
horizontal structural plate and chordal screw shelf still require generated
tree support, but their camera-facing plane has 0.5 mm axial clearance and is
not intended to touch the camera.

## Water-path isolation

The ceiling-flange bayonet uses a shallow 7.15 mm blind socket at the top of
the compact carrier. A solid floor at `z=26.75` separates the socket from the
camera cavity below. The full annular flange spigot occupies the inner portion
of this socket, while only its three locking lugs enter the wider outer track.

There is no continuous outer cavity from the ceiling flange to the camera
interface. The cable passage and camera-retention bore are both inside the
central region covered by the flange and grommet. The retention bore is
occupied by its screw in service; use an appropriate sealing washer or sealant
if testing shows water can track along that fastener.

## Printable files

- `build/unifi-g5-ptz-carrier.stl`
- `build/unifi-g5-ptz-carrier-plus15mm.stl`
- `build/unifi-g5-ptz-carrier-plus30mm.stl`
- `build/unifi-g5-ptz-ceiling-flange.stl`

The canonical source is `models/unifi-g5-ptz-soffit-mount/unifi-g5-ptz-soffit-mount.scad`.

## Generate the parts

```sh
make render
```

Set `part` to `"assembly"` or `"section"` in OpenSCAD to inspect the installed
arrangement and grommet shelf.

The complete compact carrier and ceiling flange have been physically printed
and their camera interface, gasket pressure, datum alignment, clockwise keyed
bayonet, locked-angle hard stop, ceiling-cutout alignment, and security-screw
alignment confirmed.
