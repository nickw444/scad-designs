// Numbered ten-port, two-thirds-U keystone patch panel for a 10-inch rack.
// Export panel and labels separately for a multi-material print.

include <../../lib/rack/patch_panel.scad>

/* [Output] */
output_part = "assembled"; // [assembled: Complete preview, panel: Panel only, labels: Labels only]

/* [Rack and panel] */
rack_width = 254;
rack_height = 0.666667;
front_thickness = 3;
corner_radius = 4;
/* [Labels] */
port_label_size = 4;
port_label_font = "Liberation Sans:style=Bold";
port_label_depth = 0.6;

/* [Hidden] */
height = 44.45 * rack_height;

if ($preview) {
    rotate([-90, 0, 0])
        translate([0, -height/2, -front_thickness/2])
            ten_port_patch_panel(
                output_part, rack_width, rack_height, front_thickness,
                corner_radius, port_label_size, port_label_font, port_label_depth
            );
} else {
    ten_port_patch_panel(
        output_part, rack_width, rack_height, front_thickness,
        corner_radius, port_label_size, port_label_font, port_label_depth
    );
}
