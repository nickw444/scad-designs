# MakerWorld listing

## Title

Super minimal frameless tablet / iPad wall mount

Published at: https://makerworld.com/en/models/1693448-super-minimal-frameless-tablet-ipad-wall-mount#profileId-1795300

## Description

A super clean, frameless wall mount for a tablet that uses a sliding vertical cleat design to allow the tablet to be easily removed from the wall when needed. Simply slide the tablet upward and out to use it elsewhere.

The cleat attaches to the rear of any tablet with secure mounting tape. Don't cheap out on the tape: it is the only thing holding the tablet to the mount.

The design incorporates a channel for routing the cable from a central hole behind the mount. In my case, the cable passes behind the wall to a cupboard where it receives power. There is a secondary channel for an accessory, in my case routing an IR LED for controlling an air conditioner unit.

There are two cable-channel profiles: one for a round cable and another with a wider channel for a flat cable. When using a flat right-angle cable, you may wish to finish the minimal look by pairing the mount with my [Shell Cover For Right Angle USB C Wallmount Tablet](https://makerworld.com/en/models/1724420-shell-cover-for-right-angle-usb-c-wallmount-tablet#profileId-1830685).

The updated files add regional electrical-box versions as well as the original wall-fixing pattern. Choose the housing and matching cleat below before printing.

## Variants

| Variant | Power channel | Wall fixing pattern | Matching cleat |
| --- | --- | --- | --- |
| Basic / legacy | Round, 4 mm, or flat, 12 mm | Two countersunk holes on 40 mm centres | `tablet-mount-cleat.stl` (100 × 70 × 5 mm) |
| Australian, landscape | Round, 4 mm, or flat, 12 mm | Electrical-box pattern, 84 mm horizontal centres | `tablet-mount-cleat.stl` (100 × 70 × 5 mm) |
| Australian, portrait | Round, 4 mm, or flat, 12 mm | Electrical-box pattern, 84 mm vertical centres | `tablet-mount-vertical-cleat.stl` (70 × 100 × 5 mm) |
| European / UK | Round, 4 mm, or flat, 12 mm | Electrical-box pattern, 60.3 mm horizontal centres | `tablet-mount-cleat.stl` (100 × 70 × 5 mm) |

Every housing retains the separate 3 mm IR-emitter channel. The round and flat
options only change the power-cable channel.

### STL files

- `tablet-mount-round-housing.stl` and `tablet-mount-flat-housing.stl` — basic / legacy housings.
- `tablet-mount-australian-round-housing.stl` and `tablet-mount-australian-flat-housing.stl` — Australian landscape housings.
- `tablet-mount-australian-vertical-round-housing.stl` and `tablet-mount-australian-vertical-flat-housing.stl` — Australian portrait housings.
- `tablet-mount-european-uk-round-housing.stl` and `tablet-mount-european-uk-flat-housing.stl` — shared European / UK housings.
- `tablet-mount-cleat.stl` — horizontal tablet-side cleat for the basic, Australian landscape, and European / UK housings.
- `tablet-mount-vertical-cleat.stl` — portrait tablet-side cleat for the Australian vertical housings.

## Regional fixing dimensions

All dimensions below are in millimetres and refer to the housing face-plate coordinate system.

| Housing | Screw centres | Screw / head clearance |
| --- | --- | --- |
| Basic / legacy | X = 30 and 70, Y = 30; 40 mm horizontal spacing | 5 mm straight bore with a 10 mm countersink |
| Australian, landscape | X = 8 and 92, Y = 35; 84 mm horizontal spacing | 4.00 mm through bore; 7.85 mm flat-bottomed head bore × 3.00 mm deep |
| Australian, portrait | X = 35, Y = 8 and 92; 84 mm vertical spacing | 4.00 mm through bore; 7.85 mm flat-bottomed head bore × 3.00 mm deep |
| European / UK | X = 19.85 and 80.15, Y = 35; 60.3 mm horizontal spacing | 4.00 mm through bore; 7.85 mm flat-bottomed head bore × 3.00 mm deep |

The Australian landscape and portrait patterns are intended for M3.5 dome-head screws. The nominal 3.5 mm screw uses a 4.00 mm printed bore, and the nominal 7.35 mm head uses a 7.85 mm counterbore. The portrait plate is 80 × 110 mm and uses the dedicated 70 × 100 mm vertical cleat.

The European / UK pattern is centred on the same 110 × 80 mm housing as the basic mount. It matches the 60.3 mm centres commonly used by UK BS 4662 boxes. Continental European boxes commonly use 60.0 mm centres and M3 screws; the 4.00 mm bores provide the small positional tolerance needed for that 0.15 mm per-side difference. Check the box and screw size in your installation before printing.

The regional housings have a continuous rear face plate over the electrical box. The basic housing retains the original rear entry cut-down and original 40 mm fixing pattern.

## Installation and printing

1. Select the housing for your cable and wall-box/fixing pattern.
2. Print the housing and its matching cleat. The cleat is installed on the rear of the tablet with high-quality mounting tape.
3. Fix the housing to the wall or electrical box, route the power cable and, if required, the IR lead through their channels.
4. Slide the tablet downward onto the cleat. Lift the tablet upward and out whenever it needs to be removed.

The cleat is a 5 mm deep dovetail with a 0.25 mm face clearance. Print the parts in a dimensionally stable material appropriate for the installation and verify the fit before applying tape to the tablet.

## Metadata

- **Category:** Tablet Accessories
- **Tags:** `tablet mount`, `ipad mount`, `wall mount`, `frameless`, `tablet wall mount`, `sliding cleat`, `usb c`, `home assistant`

## Disclaimer

Verify the tablet, cable, electrical-box opening, screw centres, and screw-head clearance against your installation before drilling or printing a final part. The mounting tape and wall fixings must be selected for the tablet weight and the wall material.
