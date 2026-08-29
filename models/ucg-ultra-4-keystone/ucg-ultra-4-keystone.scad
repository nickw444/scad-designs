// Ubiquiti Cloud Gateway Ultra + four-keystone 10-inch rack mount.
// Dimensions are millimetres. OpenSCAD Customizer parameters are grouped below.

include <../../lib/rack/device_mount.scad>

/* [Output] */
output_part = "assembled"; // [assembled: Complete mount, panel: Mount only, labels: Labels only]

/* [Measured device] */
component_width = 142.2;
component_depth = 123.351;
component_height = 30.4;
component_fit_scale = 1.005;

/* [Rack] */
rack_width = 254;
rack_height = 1;
rack_hole_pattern = "outer";
rack_slot_length = 12;
rack_slot_height = 6.5;
half_height_holes = true;

/* [Cradle] */
component_alignment = "right";
component_profile = "asymmetric_rounded_rectangle";
component_bottom_corner_radius = 7.1;
component_top_corner_radius = 1;
preserve_component_wall_thickness = true;
case_thickness = 1.5;
tolerance = 0;
front_plate_thickness = 4;
front_entry_chamfer = 1;
front_entry_chamfer_depth = 1;
open_top = true;
open_top_side_retainer = 14.7355;
open_top_front_retainer = 12.116;
open_top_right_retainer = 0;
open_top_rear_retainer = 13.155;
open_bottom = true;
open_cutout_corner_radius = 10.083;
bottom_cutout_border = 14.7355;
bottom_cutout_front_border = 12.116;
bottom_cutout_rear_border = 13.155;
bottom_rib_height = 6;
bottom_rib_thickness = 3;
bottom_rib_embed_depth = 1.5;
bottom_rib_position = "centered";
bottom_rib_side = "low";
bottom_rib_center_offset = 65.713;
bottom_rib_full_depth = true;
air_holes = false;

/* [Keystones] */
keystone_layout = "left_block";
keystone_columns = 4;
keystone_rows = 1;
keystone_gap = 3;
keystone_shared_walls = true;
port_labels = false;

if ($preview) {
    rotate([-90, 0, 0])
        translate([0, -height/2, -component_depth/2])
            rack_device_mount(component_width, component_height, component_depth);
} else {
    rack_device_mount(component_width, component_height, component_depth);
}
