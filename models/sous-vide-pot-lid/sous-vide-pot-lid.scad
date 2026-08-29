/*
Parametric Sous Vide Pot Lid

The entered pot diameter is the inside diameter of the downward lip. The lip
therefore wraps around the outside of the pot, and the finished lid diameter is:

    pot_diameter + (2 * lip_thickness)

The sous vide opening is a U-shaped slot: a round end joined to a straight
channel that opens through the edge of the lid.
*/

/* [Pot and Lid] */

// Outside diameter of the pot where the lip fits (mm).
pot_diameter = 241; // [100:1:500]

// Radial thickness of the downward lip (mm).
lip_thickness = 2; // [1:0.1:10]

// Distance the lip extends below the lid (mm).
lip_height = 5; // [1:0.5:30]

// Thickness of the flat lid plate (mm).
lid_thickness = 3.5; // [1:0.1:15]

/* [Sous Vide Opening] */

// Diameter (and channel width) of the sous vide cutout (mm).
sous_vide_diameter = 62; // [20:0.5:150]

// Distance from the finished lid edge to the center of the round cutout (mm).
sous_vide_edge_offset = 42; // [1:0.5:150]

/* [Print Quality] */

// Number of facets used for circles. Higher values render more smoothly.
circle_facets = 180; // [48:12:360]

/* [Hidden] */

$fn = circle_facets;
epsilon = 0.02;

pot_radius = pot_diameter / 2;
outer_radius = pot_radius + lip_thickness;
cutout_radius = sous_vide_diameter / 2;
cutout_center_y = -outer_radius + sous_vide_edge_offset;
total_height = lip_height + lid_thickness;

assert(pot_diameter > 0, "Pot diameter must be greater than zero.");
assert(lip_thickness > 0, "Lip thickness must be greater than zero.");
assert(lip_height > 0, "Lip height must be greater than zero.");
assert(lid_thickness > 0, "Lid thickness must be greater than zero.");
assert(sous_vide_diameter > 0, "Sous vide diameter must be greater than zero.");
assert(sous_vide_edge_offset > 0,
       "Sous vide edge offset must be greater than zero.");
assert(sous_vide_edge_offset + cutout_radius < (2 * outer_radius),
       "Sous vide opening extends beyond the opposite side of the lid.");

module lid_and_lip() {
    union() {
        // Flat cover sits directly on the build plate for printing.
        cylinder(h = lid_thickness, r = outer_radius);

        // The finished lid's downward skirt is printed facing upward. Its
        // inner face matches the entered pot diameter.
        translate([0, 0, lid_thickness - epsilon])
        difference() {
            cylinder(h = lip_height, r = outer_radius);
            translate([0, 0, -epsilon])
                cylinder(h = lip_height + (2 * epsilon), r = pot_radius);
        }
    }
}

module sous_vide_cutout() {
    // Circular closed end of the U-shaped opening.
    translate([0, cutout_center_y, -epsilon])
        cylinder(h = total_height + (2 * epsilon), r = cutout_radius);

    // Same-width channel from the circle center through the near edge.
    translate([
        -cutout_radius,
        -outer_radius - epsilon,
        -epsilon
    ])
        cube([
            sous_vide_diameter,
            cutout_center_y + outer_radius + epsilon,
            total_height + (2 * epsilon)
        ]);
}

difference() {
    lid_and_lip();
    sous_vide_cutout();
}
