/*
 * Flush wall mount for a tablet-mounted sliding cleat.
 *
 * Reconstructed from the three legacy STL exports in /tablet-mount.  The
 * default dimensions intentionally preserve the legacy coordinate system and
 * mating geometry.  In particular, the housing pocket has 0.25 mm clearance
 * normal to each 45 degree cleat face (0.25 * sqrt(2) in X).
 */

/* [Part] */
part = "round_housing"; // [round_housing,flat_housing,australian_round_housing,australian_flat_housing,australian_vertical_round_housing,australian_vertical_flat_housing,european_uk_round_housing,european_uk_flat_housing,us_vertical_round_housing,us_vertical_flat_housing,cleat,vertical_cleat,assembly,vertical_assembly,us_vertical_assembly]

/* [Legacy-compatible cleat] */
cleat_width = 100;
cleat_height = 70;
cleat_depth = 5;
cleat_side_inset = 5;

vertical_cleat_width = 70;
vertical_cleat_height = 100;

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
legacy_screw_centres = [[30, 30], [70, 30]];
legacy_screw_shaft_diameter = 5;
legacy_screw_countersink_diameter = 10;
legacy_screw_straight_height = 2.5;
legacy_screw_countersink_height = 2.5;

// Australian electrical-box fixing pattern. The nominal M3.5 dome-head screw
// envelope is 7.35 mm diameter by 1.93 mm high. Diametral and depth clearance
// keep the head below the cleat pocket despite ordinary FDM variation.
australian_screw_spacing = 84;
australian_screw_y = housing_bottom + housing_height / 2;
australian_screw_nominal_diameter = 3.5;
australian_screw_diametral_clearance = 0.5;
australian_head_nominal_diameter = 7.35;
australian_head_diametral_clearance = 0.5;
australian_head_nominal_depth = 1.93;
australian_head_bore_depth = 3;

// BS 4662 uses 60.3 mm centres. Continental European device boxes commonly
// use 60.0 mm centres with smaller M3 screws; the 4.00 mm bore used here has
// ample clearance for their 0.15 mm-per-side offset from this shared pattern.
european_uk_screw_spacing = 60.3;

// US NEMA box-mount pattern. The standard 3.281 inch pitch converts to
// 83.3374 mm; 83.34 mm is used here. US device-box screws are #6-32 UNC.
// The slightly larger through bore accommodates normal FDM variation and the
// oval-head pocket is deliberately flat so the head cannot enter the cleat.
us_screw_spacing = 83.34;
us_screw_nominal_diameter = 3.5052; // #6 major diameter, 0.1380 in
us_screw_diametral_clearance = 0.5;
us_head_nominal_diameter = 6.65; // #6 oval head, 0.262 in maximum
us_head_diametral_clearance = 0.5;
us_head_bore_depth = 3.5;

vertical_housing_width = vertical_cleat_width + 10;
vertical_housing_height = vertical_cleat_height + 10;

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

module vertical_cleat() {
    profile = [
        [0, 0],
        [vertical_cleat_width, 0],
        [vertical_cleat_width - cleat_side_inset, cleat_depth],
        [cleat_side_inset, cleat_depth]
    ];

    extrude_xz(profile, 0, vertical_cleat_height);
}

module housing_blank() {
    translate([housing_left, housing_bottom, housing_back_z])
        rounded_rectangle_prism(
            [housing_width, housing_height],
            housing_corner_radius,
            housing_depth
        );
}

module vertical_housing_blank() {
    translate([housing_left, housing_bottom, housing_back_z])
        rounded_rectangle_prism(
            [vertical_housing_width, vertical_housing_height],
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

function pocket_transition_profile(amount, pocket_width = cleat_width) = [
    [-diagonal_clearance, pocket_floor_z],
    [pocket_width + diagonal_clearance, pocket_floor_z],
    [pocket_width + diagonal_clearance, 0],
    [pocket_width - (1 - amount) * housing_front_z
        + diagonal_clearance, housing_front_z],
    [(1 - amount) * housing_front_z
        - diagonal_clearance, housing_front_z],
    [-diagonal_clearance, 0]
];

module ruled_pocket_transition(
    y_start,
    y_end,
    pocket_width = cleat_width
) {
    transition_steps = 256;
    transition_skin = 0.00005;

    for (step = [0 : transition_steps - 1])
        hull() {
            extrude_xz(
                pocket_transition_profile(
                    step / transition_steps,
                    pocket_width
                ),
                y_start + (y_end - y_start) * step / transition_steps
                    - transition_skin,
                y_start + (y_end - y_start) * step / transition_steps
                    + transition_skin
            );
            extrude_xz(
                pocket_transition_profile(
                    (step + 1) / transition_steps,
                    pocket_width
                ),
                y_start + (y_end - y_start) * (step + 1)
                    / transition_steps - transition_skin,
                y_start + (y_end - y_start) * (step + 1)
                    / transition_steps + transition_skin
            );
        }
}

module vertical_dovetail_pocket() {
    captured_end_y = vertical_cleat_height - 10;
    transition_end_y = captured_end_y + 5;
    profile = [
        [-diagonal_clearance, pocket_floor_z],
        [vertical_cleat_width + diagonal_clearance, pocket_floor_z],
        [vertical_cleat_width + diagonal_clearance, 0],
        [vertical_cleat_width - housing_front_z + diagonal_clearance,
         housing_front_z],
        [housing_front_z - diagonal_clearance, housing_front_z],
        [-diagonal_clearance, 0]
    ];

    extrude_xz(profile, 0, captured_end_y);
    ruled_pocket_transition(
        captured_end_y,
        transition_end_y,
        vertical_cleat_width
    );
    extrude_xz(
        pocket_transition_profile(1, vertical_cleat_width),
        transition_end_y,
        vertical_housing_height
    );
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
            d = legacy_screw_shaft_diameter,
            h = legacy_screw_straight_height + epsilon,
            $fn = 48
        );
        translate([0, 0, legacy_screw_straight_height])
            cylinder(
                d1 = legacy_screw_shaft_diameter,
                d2 = legacy_screw_countersink_diameter,
                h = legacy_screw_countersink_height + epsilon,
                $fn = 48
            );
    }
}

module australian_counterbored_screw_void(position) {
    shaft_diameter = australian_screw_nominal_diameter
        + australian_screw_diametral_clearance;
    head_diameter = australian_head_nominal_diameter
        + australian_head_diametral_clearance;
    head_depth = australian_head_bore_depth;
    back_plate_depth = pocket_floor_z - housing_back_z;

    // The shaft passes through the complete back plate. A flat-bottomed bore
    // opens from the pocket side to house the dome head without imposing a
    // countersink angle or allowing the head to interfere with the cleat.
    translate([position[0], position[1], housing_back_z - epsilon])
        cylinder(
            d = shaft_diameter,
            h = back_plate_depth + 2 * epsilon,
            $fn = 48
        );

    translate([
        position[0],
        position[1],
        pocket_floor_z - head_depth
    ])
        cylinder(
            d = head_diameter,
            h = head_depth + epsilon,
            $fn = 48
        );
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

module mounting_screw_voids(mounting_pattern) {
    if (mounting_pattern == "australian_horizontal") {
        for (x = [
            cleat_width / 2 - australian_screw_spacing / 2,
            cleat_width / 2 + australian_screw_spacing / 2
        ])
            australian_counterbored_screw_void([x, australian_screw_y]);
    } else if (mounting_pattern == "european_uk_horizontal") {
        for (x = [
            cleat_width / 2 - european_uk_screw_spacing / 2,
            cleat_width / 2 + european_uk_screw_spacing / 2
        ])
            australian_counterbored_screw_void([x, australian_screw_y]);
    } else {
        for (position = legacy_screw_centres)
            countersunk_screw_void(position);
    }
}

module us_counterbored_screw_void(position) {
    shaft_diameter = us_screw_nominal_diameter
        + us_screw_diametral_clearance;
    head_diameter = us_head_nominal_diameter
        + us_head_diametral_clearance;
    back_plate_depth = pocket_floor_z - housing_back_z;

    // The shaft passes through the complete back plate. A flat-bottomed bore
    // houses the #6-32 oval head below the cleat pocket.
    translate([position[0], position[1], housing_back_z - epsilon])
        cylinder(
            d = shaft_diameter,
            h = back_plate_depth + 2 * epsilon,
            $fn = 48
        );

    translate([
        position[0],
        position[1],
        pocket_floor_z - us_head_bore_depth
    ])
        cylinder(
            d = head_diameter,
            h = us_head_bore_depth + epsilon,
            $fn = 48
        );
}

module vertical_australian_mounting_screw_voids() {
    plate_centre_x = housing_left + vertical_housing_width / 2;
    plate_centre_y = housing_bottom + vertical_housing_height / 2;

    for (y = [
        plate_centre_y - australian_screw_spacing / 2,
        plate_centre_y + australian_screw_spacing / 2
    ])
        australian_counterbored_screw_void([plate_centre_x, y]);
}

module vertical_us_mounting_screw_voids() {
    plate_centre_x = housing_left + vertical_housing_width / 2;
    plate_centre_y = housing_bottom + vertical_housing_height / 2;

    for (y = [
        plate_centre_y - us_screw_spacing / 2,
        plate_centre_y + us_screw_spacing / 2
    ])
        us_counterbored_screw_void([plate_centre_x, y]);
}

module housing(
    channel_width,
    mounting_pattern = "legacy",
    full_back_plate = false
) {
    difference() {
        housing_blank();
        dovetail_pocket();
        if (!full_back_plate)
            entry_notch();
        cable_void(channel_width);
        mounting_screw_voids(mounting_pattern);
    }
}

module vertical_australian_housing(channel_width) {
    vertical_box_housing(channel_width, "australian");
}

module vertical_us_housing(channel_width) {
    vertical_box_housing(channel_width, "us");
}

module vertical_box_housing(channel_width, mounting_pattern) {
    plate_centre = [
        housing_left + vertical_housing_width / 2,
        housing_bottom + vertical_housing_height / 2
    ];
    cable_translation = [
        plate_centre[0] - cable_reservoir_centre[0],
        plate_centre[1] - cable_reservoir_centre[1],
        0
    ];

    difference() {
        vertical_housing_blank();
        vertical_dovetail_pocket();
        translate(cable_translation)
            cable_void(channel_width);
        if (mounting_pattern == "us")
            vertical_us_mounting_screw_voids();
        else
            vertical_australian_mounting_screw_voids();
    }
}

module selected_part() {
    if (part == "cleat") {
        cleat();
    } else if (part == "vertical_cleat") {
        vertical_cleat();
    } else if (part == "australian_vertical_round_housing") {
        vertical_australian_housing(round_channel_width);
    } else if (part == "australian_vertical_flat_housing") {
        vertical_australian_housing(flat_channel_width);
    } else if (part == "us_vertical_round_housing") {
        vertical_us_housing(round_channel_width);
    } else if (part == "us_vertical_flat_housing") {
        vertical_us_housing(flat_channel_width);
    } else if (part == "australian_round_housing") {
        housing(round_channel_width, "australian_horizontal", true);
    } else if (part == "australian_flat_housing") {
        housing(flat_channel_width, "australian_horizontal", true);
    } else if (part == "european_uk_round_housing") {
        housing(round_channel_width, "european_uk_horizontal", true);
    } else if (part == "european_uk_flat_housing") {
        housing(flat_channel_width, "european_uk_horizontal", true);
    } else if (part == "flat_housing") {
        housing(flat_channel_width);
    } else if (part == "assembly") {
        housing(round_channel_width);
        color("black", 0.65)
            translate([0, 0, pocket_floor_z + pocket_face_clearance])
                cleat();
    } else if (part == "vertical_assembly") {
        vertical_australian_housing(round_channel_width);
        color("black", 0.65)
            translate([0, 0, pocket_floor_z + pocket_face_clearance])
                vertical_cleat();
    } else if (part == "us_vertical_assembly") {
        vertical_us_housing(round_channel_width);
        color("black", 0.65)
            translate([0, 0, pocket_floor_z + pocket_face_clearance])
                vertical_cleat();
    } else {
        housing(round_channel_width);
    }
}

selected_part();
