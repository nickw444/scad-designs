// NBN NTD + six numbered keystones, sized to pair with the 2/3U patch panel.
// Export panel and labels separately for a multi-material print.

include <../../lib/rack/device_mount.scad>

/* [Output] */
output_part = "assembled"; // [assembled: Complete preview, panel: Mount only, labels: Labels only]

/* [Measured device] */
component_width = 135;
component_depth = 134;
component_height = 47;

/* [Rack] */
rack_width = 254;
rack_height = 1.333333;
half_height_holes = true;

/* [Cradle] */
component_alignment = "left";
component_profile = "d_shape";
case_thickness = 3;
tolerance = 0.42;
front_plate_thickness = 3;
open_top = true;
open_top_side_retainer = 0;
open_top_right_retainer = 10;
open_top_rear_retainer = 10;
open_bottom = true;
bottom_cutout_border = 10;
bottom_rib_height = 3;
bottom_rib_thickness = 3;
air_holes = true;

/* [Keystones and labels] */
keystone_layout = "right_block";
keystone_columns = 3;
keystone_rows = 2;
keystone_gap = 3;
port_labels = true;
port_label_size = 4;
port_label_depth = 0.6;

if ($preview) {
    rotate([-90, 0, 0])
        translate([0, -height/2, -component_depth/2])
            rack_device_mount(component_width, component_height, component_depth);
} else {
    rack_device_mount(component_width, component_height, component_depth);
}
