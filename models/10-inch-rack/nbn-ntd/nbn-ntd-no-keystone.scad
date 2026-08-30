// Right-aligned NBN NTD mount without keystone ports.

include <../device-mount.scad>

/* [Output] */
output_part = "assembled"; // [assembled: Complete mount, panel: Mount only]

/* [Measured device] */
component_width = 135;
component_depth = 134;
component_height = 47;

/* [Rack] */
rack_width = 254;
rack_height = 59 / 44.45;
half_height_holes = true;

/* [Cradle] */
component_alignment = "right";
component_profile = "asymmetric_rounded_rectangle";
component_bottom_corner_radius = 7.5;
component_top_corner_radius = 7.5;
case_thickness = 3;
tolerance = 0.01;
front_plate_thickness = 4;
front_retaining_lip = 2;
front_retaining_lip_depth = 3;
front_retaining_lip_corner_radius = 13.5;
open_top = true;
open_top_side_retainer = 14.7355;
open_top_front_retainer = 12.116;
open_top_right_retainer = 0;
open_top_rear_retainer = 13.155;
open_bottom = true;
open_cutout_corner_radius = 10.083;
bottom_cutout_border = 10;
bottom_rib_height = 3;
bottom_rib_thickness = 3;
bottom_rib_side = "low";
air_holes = false;

/* [Keystones] */
keystone_columns = 0;
keystone_rows = 0;
port_labels = false;

if ($preview) {
    rotate([-90, 0, 0])
        translate([0, -height/2, -component_depth/2])
            rack_device_mount(component_width, component_height, component_depth);
} else {
    rack_device_mount(component_width, component_height, component_depth);
}
