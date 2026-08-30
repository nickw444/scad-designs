/*
 * Tesla trunk hook with a user-supplied, side-loaded M6 nut.
 *
 * Reverse-engineered from obj_1_Body1.stl. The preserved lower hook body is
 * stored locally as source/tesla-hook-arms.stl so this model rebuilds without
 * the original upload. The original internal thread was
 * M6 x 1 (measured minor diameter 5.035 mm, major diameter 6.147 mm, pitch
 * 0.99985 mm). This version removes the printed thread and captures a metal
 * ISO 4032 M6 hex nut immediately beneath the top of a reinforced boss.
 *
 * Print in the source orientation on the original flat underside.
 */

/* [Nut and bolt fit] */
bolt_clearance_diameter = 7.2; // Loose M6 passage; metal nut carries the load
nut_across_flats = 10.0;      // ISO 4032 M6 nut
nut_thickness = 5.2;          // ISO 4032 maximum
nut_side_clearance = 0.35;    // Clearance on each of the six flats
nut_depth_clearance = 0.40;

/* [Short-bolt geometry] */
top_skin = 2.0;               // Thin clamping face for the short exposed bolt
reinforced_boss_diameter = 22;
boss_flare_diameter = 25;
boss_flare_top = 17;
nut_slot_extra_width = 0.00;  // Slot aligns with the pocket's opposing flats

/* [Preserved hook body] */
source_mesh = "source/tesla-hook-arms.stl";
source_height = 45.0;

/* [Mesh quality] */
$fn = 96;

epsilon = 0.05;
nut_pocket_af = nut_across_flats + 2 * nut_side_clearance;
nut_pocket_depth = nut_thickness + nut_depth_clearance;
nut_pocket_top = source_height - top_skin;
nut_pocket_bottom = nut_pocket_top - nut_pocket_depth;

module hex_prism_across_flats(across_flats, height) {
    // For a regular hexagon, across-flats = 2 * circumradius * cos(30 deg).
    cylinder(r = across_flats / (2 * cos(30)), h = height, $fn = 6);
}

module preserved_hook_body() {
    import(source_mesh, convexity = 10);
}

module reinforced_boss() {
    // The flare begins on the build plate, so every layer is supported. Its
    // gentle inward taper transfers load into the three-arm hub without an
    // unsupported lower flange. The straight boss leaves about 5 mm of
    // material around the nut corners.
    hull() {
        translate([0, 0, 0])
            cylinder(d = boss_flare_diameter, h = epsilon);
        translate([0, 0, boss_flare_top])
            cylinder(d = reinforced_boss_diameter, h = epsilon);
    }

    translate([0, 0, boss_flare_top])
        cylinder(d = reinforced_boss_diameter,
                 h = source_height - boss_flare_top);
}

module nut_and_bolt_void() {
    // Smooth clearance passage removes all remnants of the printed M6 thread.
    translate([0, 0, -epsilon])
        cylinder(d = bolt_clearance_diameter,
                 h = source_height + 2 * epsilon);

    // The nut sits directly below the top skin, minimising the bolt length
    // needed before its thread engages the metal nut.
    translate([0, 0, nut_pocket_bottom])
        hex_prism_across_flats(nut_pocket_af,
                               nut_pocket_depth);

    // Side-loading tunnel: slide the nut in flat, then the hex pocket stops
    // it rotating. The tunnel opens only one side of the boss for strength.
    translate([
        0,
        -(nut_pocket_af / 2 + nut_slot_extra_width),
        nut_pocket_bottom
    ])
        cube([
            reinforced_boss_diameter / 2 + epsilon,
            nut_pocket_af + 2 * nut_slot_extra_width,
            nut_pocket_depth
        ]);
}

difference() {
    union() {
        preserved_hook_body();
        reinforced_boss();
    }
    nut_and_bolt_void();
}
