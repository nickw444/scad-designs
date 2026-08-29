/*
 * Rectangular stitch guides
 *
 * OpenSCAD uses millimetres. All imperial dimensions below are converted
 * using the exact relationship 1 inch = 25.4 mm.
 */

// Set to "all", "bow", "tails", "knot", or "rectangle_3_5x3".
part = "all";

module labelled_cuboid(size, imperial_label, metric_label, font_size) {
    base_height = 5;
    deboss_depth = 0.8;
    cut_overlap = 0.05;
    width = size[0];
    depth = size[1];
    line_spacing = font_size * 1.25;
    landscape_angle = depth > width ? 90 : 0;

    difference() {
        cube([width, depth, base_height]);

        // Recess the centred label and align it with the longest edge.
        translate([
            width / 2,
            depth / 2,
            base_height - deboss_depth
        ])
            rotate([0, 0, landscape_angle]) {
                translate([0, line_spacing / 2, 0])
                    linear_extrude(height = deboss_depth + cut_overlap)
                        text(
                            imperial_label,
                            size = font_size,
                            halign = "center",
                            valign = "center"
                        );

                translate([0, -line_spacing / 2, 0])
                    linear_extrude(height = deboss_depth + cut_overlap)
                        text(
                            metric_label,
                            size = font_size,
                            halign = "center",
                            valign = "center"
                        );
            }
    }
}

module bow() {
    labelled_cuboid(
        [88.90, 177.80],
        str("3 1/2", chr(34), " x 7", chr(34)),
        "88.90 x 177.80 mm",
        7
    );
}

module tails() {
    labelled_cuboid(
        [88.90, 127.00],
        str("3 1/2", chr(34), " x 5", chr(34)),
        "88.90 x 127.00 mm",
        7
    );
}

module knot() {
    labelled_cuboid(
        [44.45, 63.50],
        str("1 3/4", chr(34), " x 2 1/2", chr(34)),
        "44.45 x 63.50 mm",
        3.6
    );
}

module rectangle_3_5x3() {
    labelled_cuboid(
        [88.90, 76.20],
        str("3 1/2", chr(34), " x 3", chr(34)),
        "88.90 x 76.20 mm",
        7
    );
}

module all_parts() {
    gap = 12;

    bow();
    translate([88.90 + gap, 0, 0]) tails();
    translate([88.90 + gap, 127.00 + gap, 0]) knot();
    translate([88.90 + gap + 88.90 + gap, 0, 0]) rectangle_3_5x3();
}

if (part == "bow") {
    bow();
} else if (part == "tails") {
    tails();
} else if (part == "knot") {
    knot();
} else if (part == "rectangle_3_5x3") {
    rectangle_3_5x3();
} else if (part == "all") {
    all_parts();
} else {
    assert(false, str("Unknown part: ", part));
}
