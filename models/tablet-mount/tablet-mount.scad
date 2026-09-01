/*
 * Flush wall mount for a tablet-mounted sliding cleat.
 *
 * Reconstructed from the three legacy STL exports in /tablet-mount.  The
 * default dimensions intentionally preserve the legacy coordinate system and
 * mating geometry.  In particular, the housing pocket has 0.25 mm clearance
 * normal to each 45 degree cleat face (0.25 * sqrt(2) in X).
 */

/* [Part] */
part = "round_housing"; // [round_housing,flat_housing,cleat,assembly]

/* [Legacy-compatible cleat] */
cleat_width = 100;
cleat_height = 70;
cleat_depth = 5;
cleat_side_inset = 5;

/* [Housing] */
housing_width = 110;
housing_height = 80;
housing_depth = 9.25;
housing_corner_radius = 3;
housing_back_z = -5.25;
housing_left = -5;
housing_bottom = -5;

/* [Cleat pocket] */
pocket_face_clearance = 0.25;
pocket_floor_z = -0.25;
entry_notch_left = 15;
entry_notch_right = 85;
entry_notch_bottom = 50;
entry_notch_corner_radius = 3;

/* [Fasteners] */
screw_centres = [[30, 30], [70, 30]];
screw_shaft_diameter = 5;
screw_countersink_diameter = 10;
screw_straight_height = 2.5;
screw_countersink_height = 2.5;

/* [Cable routing] */
cable_reservoir_centre = [50, 15.597899];
cable_reservoir_diameter = 25;
cable_void_top_z = -1.25;
ir_channel_y = [2.71079, 5.71079];
power_channel_bottom_y = 13.5979;
round_channel_width = 4;
flat_channel_width = 12;

/* [Mesh quality] */
$fn = 96;

epsilon = 0.01;
diagonal_clearance = pocket_face_clearance * sqrt(2);
housing_front_z = housing_back_z + housing_depth;

module rounded_rectangle_prism(size, radius, height) {
    linear_extrude(height = height)
        hull()
            for (x = [radius, size[0] - radius],
                 y = [radius, size[1] - radius])
                translate([x, y])
                    circle(r = radius, $fn = 48);
}

// Extrude a polygon drawn in the global X/Z plane along global Y.
module extrude_xz(profile, y_min, y_max) {
    translate([0, y_max, 0])
        rotate([90, 0, 0])
            linear_extrude(height = y_max - y_min)
                polygon(profile);
}

module cleat() {
    profile = [
        [0, 0],
        [cleat_width, 0],
        [cleat_width - cleat_side_inset, cleat_depth],
        [cleat_side_inset, cleat_depth]
    ];

    extrude_xz(profile, 0, cleat_height);
}

module housing_blank() {
    translate([housing_left, housing_bottom, housing_back_z])
        rounded_rectangle_prism(
            [housing_width, housing_height],
            housing_corner_radius,
            housing_depth
        );
}

module dovetail_pocket() {
    // The vertical 0.25 mm step at the pocket floor and the +/-0.353553 mm
    // diagonal offsets are present in the legacy mesh and determine its fit.
    profile = [
        [-diagonal_clearance, pocket_floor_z],
        [cleat_width + diagonal_clearance, pocket_floor_z],
        [cleat_width + diagonal_clearance, 0],
        [cleat_width - housing_front_z + diagonal_clearance,
         housing_front_z],
        [housing_front_z - diagonal_clearance, housing_front_z],
        [-diagonal_clearance, 0]
    ];

    // The captured run ends at Y=60.  Over the next 5 mm its sloped side
    // faces open out to the full back width, after which the pocket remains
    // open so the cleat can enter from the top of the U-shaped housing.
    extrude_xz(profile, 0, 60);
    ruled_pocket_transition(60, 65);
    extrude_xz(pocket_transition_profile(1), 65, housing_height);
}

function pocket_transition_profile(amount) = [
    [-diagonal_clearance, pocket_floor_z],
    [cleat_width + diagonal_clearance, pocket_floor_z],
    [cleat_width + diagonal_clearance, 0],
    [cleat_width - (1 - amount) * housing_front_z
        + diagonal_clearance, housing_front_z],
    [(1 - amount) * housing_front_z
        - diagonal_clearance, housing_front_z],
    [-diagonal_clearance, 0]
];

module ruled_pocket_transition(y_start, y_end) {
    transition_steps = 256;
    transition_skin = 0.00005;

    for (step = [0 : transition_steps - 1])
        hull() {
            extrude_xz(
                pocket_transition_profile(step / transition_steps),
                y_start + (y_end - y_start) * step / transition_steps
                    - transition_skin,
                y_start + (y_end - y_start) * step / transition_steps
                    + transition_skin
            );
            extrude_xz(
                pocket_transition_profile((step + 1) / transition_steps),
                y_start + (y_end - y_start) * (step + 1)
                    / transition_steps - transition_skin,
                y_start + (y_end - y_start) * (step + 1)
                    / transition_steps + transition_skin
            );
        }
}

module entry_notch() {
    notch_left = entry_notch_left - diagonal_clearance;
    notch_right = entry_notch_right + diagonal_clearance;
    bottom_corner_y = entry_notch_bottom + entry_notch_corner_radius;
    housing_top_y = housing_bottom + housing_height;
    top_corner_y = housing_top_y - housing_corner_radius;
    top_left = notch_left - entry_notch_corner_radius;
    top_right = notch_right + entry_notch_corner_radius;
    arc_steps = 12;
    notch_profile = concat(
        [[notch_left + entry_notch_corner_radius, entry_notch_bottom]],
        [for (a = [-90 : 90 / arc_steps : 0])
            [notch_right - entry_notch_corner_radius
                + entry_notch_corner_radius * cos(a),
             bottom_corner_y + entry_notch_corner_radius * sin(a)]],
        [[notch_right, top_corner_y]],
        [for (a = [180 : -90 / arc_steps : 90])
            [top_right + entry_notch_corner_radius * cos(a),
             top_corner_y + entry_notch_corner_radius * sin(a)]],
        [[top_left, housing_top_y]],
        [for (a = [90 : -90 / arc_steps : 0])
            [top_left + entry_notch_corner_radius * cos(a),
             top_corner_y + entry_notch_corner_radius * sin(a)]],
        [[notch_left, bottom_corner_y]],
        [for (a = [180 : 90 / arc_steps : 270])
            [notch_left + entry_notch_corner_radius
                + entry_notch_corner_radius * cos(a),
             bottom_corner_y + entry_notch_corner_radius * sin(a)]]
    );

    translate([0, 0, housing_back_z - epsilon])
        linear_extrude(height = housing_depth + 2 * epsilon)
            polygon(notch_profile);
}

module countersunk_screw_void(position) {
    translate([position[0], position[1], housing_back_z - epsilon]) {
        cylinder(
            d = screw_shaft_diameter,
            h = screw_straight_height + epsilon,
            $fn = 48
        );
        translate([0, 0, screw_straight_height])
            cylinder(
                d1 = screw_shaft_diameter,
                d2 = screw_countersink_diameter,
                h = screw_countersink_height + epsilon,
                $fn = 48
            );
    }
}

module cable_void(channel_width) {
    void_height = cable_void_top_z - (housing_back_z - epsilon);
    ir_bridge = [
        [57.446827, 5.558239],
        [60.512051, ir_channel_y[0]],
        [housing_left + housing_width + epsilon, ir_channel_y[0]],
        [housing_left + housing_width + epsilon, ir_channel_y[1]],
        [61.690475, ir_channel_y[1]],
        [59.628357, 7.626402]
    ];

    translate([0, 0, housing_back_z - epsilon])
        linear_extrude(height = void_height)
            union() {
                translate(cable_reservoir_centre)
                    circle(d = cable_reservoir_diameter, $fn = 96);

                // Shared narrow path for the IR emitter lead.
                polygon(ir_bridge);

                // Power lead: 4 mm for a round cable, 12 mm for a flat plug.
                translate([
                    cable_reservoir_centre[0],
                    power_channel_bottom_y
                ])
                    square([housing_width, channel_width]);
            }
}

module housing(channel_width) {
    difference() {
        housing_blank();
        dovetail_pocket();
        entry_notch();
        cable_void(channel_width);
        for (position = screw_centres)
            countersunk_screw_void(position);
    }
}

module selected_part() {
    if (part == "cleat") {
        cleat();
    } else if (part == "flat_housing") {
        housing(flat_channel_width);
    } else if (part == "assembly") {
        housing(round_channel_width);
        color("black", 0.65)
            translate([0, 0, pocket_floor_z + pocket_face_clearance])
                cleat();
    } else {
        housing(round_channel_width);
    }
}

selected_part();
