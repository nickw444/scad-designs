// Focused shared cradle geometry for our NBN NTD and UCG Ultra rack mounts.
rack_width = 254.0;
// Height of the rack in U units, can be a fraction for partial U (e.g. 1.5 for 1U plus half of the next U)
rack_height = 1.0; // [0.5:0.5:5]


// Cross-section of the cradle behind the front retaining panel.
component_profile = "asymmetric_rounded_rectangle"; // [asymmetric_rounded_rectangle: UCG profile, d_shape: NBN profile]
// Lower and upper radii for an asymmetric rounded-rectangle component profile.
component_bottom_corner_radius = 0; // [0:0.1:50]
component_top_corner_radius = 0; // [0:0.1:50]
// Scale only the component cavity, leaving the measured outer cradle dimensions unchanged.
component_fit_scale = 1.0; // [1:0.001:1.03]
// Grow the cradle exterior with the fitted cavity so case_thickness remains the true wall thickness.
preserve_component_wall_thickness = false; // [true: Preserve wall thickness, false: Preserve nominal exterior]

// Position of the component cradle within the usable space between the rack ears.
component_alignment = "right"; // [left: Align left, center: Centre, right: Align right]
// Remove the cradle roof behind the front plate for drop-in access and cooling.
open_top = true;
// Open a large framed aperture in the lower wall behind the front plate.
open_bottom = true;

// ========================================
/* [Keystones] */
keystone_layout = "left_block"; // [left_block: Left of device, right_block: Right of device]
keystone_columns = 3; // [1:1:4]
keystone_rows = 2; // [1:1:2]
keystone_gap = 3; // [2:0.5:8]
// Optional independent vertical gap between rows; zero follows keystone_gap.
// Negative values overlap holder walls to form a compact shared-wall bank.
keystone_row_gap = 0; // [-2.5:0.1:8]
// Overlap adjacent holders so they share one wall; useful for compact single-row banks.
keystone_shared_walls = false; // [true: Share holder walls, false: Separate holders]
// Recess sequential port numbers into the upper border of each grid holder.
port_labels = false; // [true: Number grid ports, false: No labels]
port_label_size = 4.0;
port_label_depth = 0.6;
// Export the mount and matching label solids separately for multi-material slicing.
output_part = "assembled"; // [assembled: Complete preview, panel: Mount only, labels: Labels only]

// Adds hexagon air cutouts to reduce material and improve cooling.
air_holes = true; // [true:Show air holes, false:Hide air holes]

// ========================================
/* [Advanced] */
// Used when rack_height is a fraction, cuts a half oval for screws, otherwise will cover up the hole
half_height_holes = true; // [true:Show partial holes at edges, false:Hide partial holes]
// Thickness of the shell that wraps around the part.
case_thickness = 6; // Thickness of case walls
// Thickness of the front panel (the flat face plate).
front_plate_thickness = 3.0;
// Optional inset lip retained through the front portion of the faceplate.
front_retaining_lip = 0;
front_retaining_lip_depth = 0;
front_retaining_lip_corner_radius = 0;
// Flare the component entry outward by this amount per side.
front_entry_chamfer = 0;
// Front-to-back depth of the flared entry.
front_entry_chamfer_depth = 1;
// Width retained at each side of an open cradle roof.
open_top_side_retainer = 0;
// Width of the bridge between the faceplate and an open cradle roof.
open_top_front_retainer = 0;
// Additional longitudinal top rail retained along the component's right edge.
open_top_right_retainer = 0; // [0:0.5:20]
// Width of the rear bridge joining the side walls around an open cradle roof.
open_top_rear_retainer = 10; // [2:0.5:20]
// Radius of the large roof/floor ventilation aperture corners.
open_cutout_corner_radius = 0;
// Solid border retained around a rectangular bottom aperture.
bottom_cutout_border = 10; // [5:1:20]
// Optional independent side borders for asymmetric floor apertures; zero follows bottom_cutout_border.
bottom_cutout_left_border = 0;
bottom_cutout_right_border = 0;
// Optional front and rear borders for the bottom aperture; zero follows bottom_cutout_border.
bottom_cutout_front_border = 0;
bottom_cutout_rear_border = 0;
// Height that the two longitudinal stiffening ribs protrude below the cradle.
bottom_rib_height = 6; // [2:1:12]
// Thickness of each longitudinal bottom stiffening rib.
bottom_rib_thickness = 3; // [2:0.5:6]
// Depth each rib overlaps into the cradle shell to create a structural union.
bottom_rib_embed_depth = 0;
// Put bottom ribs beneath the aperture edge or entirely beneath its retained side borders.
bottom_rib_position = "centered"; // [centered: Centre on aperture edge, outside: Keep outside aperture]
// Select which vertical side receives the ribs; low is the underside of the component profile.
bottom_rib_side = "high"; // [high: High-Y side, low: Low-Y side]
// Optional distance from the cradle centreline to each rib centre; zero uses bottom_rib_position.
bottom_rib_center_offset = 0;
// Optional independent centreline offsets for asymmetric cradles; zero follows bottom_rib_center_offset.
bottom_rib_left_center_offset = 0;
bottom_rib_right_center_offset = 0;
// Extend longitudinal ribs through the entire cradle depth instead of stopping before the rear bridge.
bottom_rib_full_depth = false; // [true: Full cradle depth, false: Stop at aperture end]
// Rack-slot selection and dimensions. Zero dimensions use the rack defaults.
rack_hole_pattern = "standard"; // [standard: Three holes per U, outer: Top and bottom holes per U]
rack_slot_length = 0;
rack_slot_height = 0;
// Default gap between part and print walls
tolerance = 0.42;

// ========================================
/* [Hidden] */
height = 44.45 * rack_height;


// The main module containing all internal variables
module rack_device_mount(switch_width, switch_height, switch_depth) {
    assert(rack_width == 254, "These mounts support a 10-inch rack only.");
    usable_width = 221.5;
    usable_left = (rack_width - usable_width) / 2;
    usable_right = usable_left + usable_width;
    fitted_component_width = switch_width * component_fit_scale + (2 * tolerance);
    fitted_component_height = switch_height * component_fit_scale + (2 * tolerance);
    chassis_component_width = preserve_component_wall_thickness ? fitted_component_width : switch_width;
    chassis_component_height = preserve_component_wall_thickness ? fitted_component_height : switch_height;
    chassis_width = min(chassis_component_width + (2 * case_thickness), usable_width);
    chassis_height = min(chassis_component_height + (2 * case_thickness), height);
    chassis_x = component_alignment == "left" ? usable_left :
                component_alignment == "center" ? usable_left + (usable_width - chassis_width) / 2 :
                usable_right - chassis_width;
    corner_radius = 4.0;
    rear_clearance_depth = 7;
    chassis_depth_main = switch_depth + rear_clearance_depth;

    $fn = 64;

    // Calculated dimensions
    cutout_w = fitted_component_width;
    cutout_h = fitted_component_height;
    cutout_x = chassis_x + (chassis_width - cutout_w) / 2;
    cutout_y = (height - cutout_h) / 2;

    // Keystone placement — jack X span (width) goes horizontal, jack Z span (height) goes vertical
    keystone_outer_width  = 19.9; // jack_width + wall = (front_hole_width + wall) + wall
    keystone_outer_height = 27.5; // jack_height + wall
    keystone_plate_overlap = 0.4; // Front plate retained behind the frame to create a printable union
    keystone_effective_column_gap = keystone_shared_walls ? -2.5 : keystone_gap;
    keystone_effective_row_gap = keystone_shared_walls ? -2.5 :
        (keystone_row_gap != 0 ? keystone_row_gap : keystone_gap);
    keystone_enabled = keystone_columns > 0 && keystone_rows > 0;
    keystone_grid_width = keystone_enabled ?
        keystone_columns * keystone_outer_width + (keystone_columns - 1) * keystone_effective_column_gap : 0;
    keystone_grid_height = keystone_enabled ?
        keystone_rows * keystone_outer_height + (keystone_rows - 1) * keystone_effective_row_gap : 0;
    keystone_grid_left = keystone_layout == "left_block" ?
        usable_left + (chassis_x - usable_left - keystone_grid_width) / 2 :
        chassis_x + chassis_width + (usable_right - chassis_x - chassis_width - keystone_grid_width) / 2;
    keystone_grid_bottom = (height - keystone_grid_height) / 2;
    keystone_grid_available_width = keystone_layout == "left_block" ?
        chassis_x - usable_left : usable_right - (chassis_x + chassis_width);

    if (keystone_enabled) {
        assert(keystone_grid_width <= keystone_grid_available_width,
            "Keystone grid does not fit beside the component; reduce columns/gap or change component alignment.");
        assert(keystone_grid_height <= height,
            "Keystone grid does not fit within the selected rack height; reduce rows/gap or increase rack height.");
    }

    // Helper modules
    module capsule_slot_2d(L, H) {
        hull() {
            translate([-L/2 + H/2, 0]) circle(r=H/2);
            translate([L/2 - H/2, 0]) circle(r=H/2);
        }
    }
    
    module rounded_rect_2d(w, h, r) {
        safe_radius = min(r, min(w, h) / 2);
        if (safe_radius > 0) {
            hull() {
                translate([safe_radius, safe_radius]) circle(r=safe_radius);
                translate([w-safe_radius, safe_radius]) circle(r=safe_radius);
                translate([w-safe_radius, h-safe_radius]) circle(r=safe_radius);
                translate([safe_radius, h-safe_radius]) circle(r=safe_radius);
            }
        } else {
            square([w, h]);
        }
    }

    module asymmetric_rounded_rect_2d(w, h, bottom_r, top_r) {
        safe_bottom_r = min(bottom_r, min(w, h) / 2);
        safe_top_r = min(top_r, min(w, h) / 2);
        if (safe_bottom_r > 0 || safe_top_r > 0) {
            hull() {
                translate([safe_bottom_r, safe_bottom_r]) circle(r=safe_bottom_r);
                translate([w-safe_bottom_r, safe_bottom_r]) circle(r=safe_bottom_r);
                translate([safe_top_r, h-safe_top_r]) circle(r=safe_top_r);
                translate([w-safe_top_r, h-safe_top_r]) circle(r=safe_top_r);
            }
        } else {
            square([w, h]);
        }
    }

    module d_shape_2d(w, h) {
        union() {
            translate([h/2, 0]) square([w - h/2, h]);
            translate([h/2, h/2]) circle(r=h/2);
        }
    }

    module component_profile_2d(w, h, asymmetric_radius_offset=0, asymmetric_radius_scale=1) {
        if (component_profile == "d_shape") {
            d_shape_2d(w, h);
        } else {
            asymmetric_rounded_rect_2d(
                w,
                h,
                component_bottom_corner_radius * asymmetric_radius_scale + asymmetric_radius_offset,
                component_top_corner_radius * asymmetric_radius_scale + asymmetric_radius_offset
            );
        }
    }

    module component_cutout_volume(x, y, w, h, z, depth) {
        translate([x, y, z]) {
            linear_extrude(height=depth)
                component_profile_2d(w, h, tolerance, component_fit_scale);
        }
    }

    module chassis_profile(width, height, depth) {
        linear_extrude(height=depth)
            component_profile_2d(
                width,
                height,
                case_thickness + (preserve_component_wall_thickness ? tolerance : 0),
                preserve_component_wall_thickness ? component_fit_scale : 1
            );
    }
    
    // Create the main body as a separate module
    module main_body() {
        union() {
            // Front panel
            linear_extrude(height = front_plate_thickness) {
                rounded_rect_2d(rack_width, height, corner_radius);
            }
            // Chassis body
            translate([chassis_x, (height - chassis_height) / 2, front_plate_thickness]) {
                chassis_profile(chassis_width, chassis_height, chassis_depth_main - front_plate_thickness);
            }
        }
    }
    
    module switch_cutout() {
        if (front_retaining_lip > 0 && front_retaining_lip_depth > 0) {
            lip_depth = min(front_retaining_lip_depth, chassis_depth_main);
            overlap = 0.01;

            translate([
                cutout_x + front_retaining_lip,
                (height - cutout_h) / 2 + front_retaining_lip,
                -tolerance
            ]) linear_extrude(height=lip_depth + tolerance + overlap) {
                if (front_retaining_lip_corner_radius > 0) {
                    rounded_rect_2d(
                        cutout_w - 2 * front_retaining_lip,
                        cutout_h - 2 * front_retaining_lip,
                        front_retaining_lip_corner_radius
                    );
                } else {
                    component_profile_2d(
                        cutout_w - 2 * front_retaining_lip,
                        cutout_h - 2 * front_retaining_lip,
                        tolerance,
                        component_fit_scale
                    );
                }
            }

            component_cutout_volume(
                cutout_x,
                (height - cutout_h) / 2,
                cutout_w,
                cutout_h,
                lip_depth,
                chassis_depth_main - lip_depth + tolerance
            );
        } else {
            component_cutout_volume(
                cutout_x,
                (height - cutout_h) / 2,
                cutout_w,
                cutout_h,
                -tolerance,
                chassis_depth_main + 2*tolerance
            );
        }
    }

    module front_entry_chamfer_cutout() {
        if (front_entry_chamfer > 0 && front_entry_chamfer_depth > 0) {
            chamfer_depth = min(front_entry_chamfer_depth, chassis_depth_main);
            hull() {
                translate([
                    cutout_x - front_entry_chamfer,
                    (height - cutout_h) / 2 - front_entry_chamfer,
                    -tolerance
                ]) linear_extrude(height=0.01)
                    component_profile_2d(
                        cutout_w + 2*front_entry_chamfer,
                        cutout_h + 2*front_entry_chamfer,
                        tolerance + front_entry_chamfer,
                        component_fit_scale
                    );
                translate([
                    cutout_x,
                    (height - cutout_h) / 2,
                    chamfer_depth
                ]) linear_extrude(height=0.01)
                    component_profile_2d(
                        cutout_w,
                        cutout_h,
                        tolerance,
                        component_fit_scale
                    );
            }
        }
    }

    module xz_aperture_cutout(x, z, width, depth, radius, y_low, y_high) {
        translate([x, y_high, z])
            rotate([90, 0, 0])
                linear_extrude(height=max(0.01, y_high-y_low))
                    rounded_rect_2d(width, depth, radius);
    }

    // Open the roof only behind the front panel, retaining the front bezel and both side walls.
    module open_top_cutout() {
        if (open_top) {
            cutout_bottom = (height - cutout_h) / 2;
            top_opening_x = cutout_x + open_top_side_retainer - tolerance;
            top_opening_width = cutout_w - 2 * open_top_side_retainer - open_top_right_retainer + 2*tolerance;
            // The supplied NBN STL uses -Y as the installed top. Keep the smaller
            // front cutout as the retainer, then open that side toward the rear while
            // leaving a solid bridge between the side walls at the back of the cradle.
            // Overlap the back of the face plate slightly so the roof subtraction
            // cannot leave a coplanar zero-area seam at the face/body transition.
            top_opening_z = front_plate_thickness + open_top_front_retainer - tolerance;
            top_opening_depth = chassis_depth_main - top_opening_z - open_top_rear_retainer;
            xz_aperture_cutout(
                top_opening_x,
                top_opening_z,
                max(0.01, top_opening_width),
                max(0.01, top_opening_depth),
                open_cutout_corner_radius,
                -height,
                cutout_bottom + tolerance
            );
        }
    }

    module open_bottom_cutout() {
        if (open_bottom) {
            effective_left_border = bottom_cutout_left_border > 0 ? bottom_cutout_left_border : bottom_cutout_border;
            effective_right_border = bottom_cutout_right_border > 0 ? bottom_cutout_right_border : bottom_cutout_border;
            effective_front_border = bottom_cutout_front_border > 0 ? bottom_cutout_front_border : bottom_cutout_border;
            effective_rear_border = bottom_cutout_rear_border > 0 ? bottom_cutout_rear_border : bottom_cutout_border;
            cutout_top = (height - cutout_h) / 2 + cutout_h;
            bottom_surface_left = component_profile == "d_shape" ? cutout_x + cutout_h/2 : cutout_x;
            aperture_x = bottom_surface_left + effective_left_border;
            aperture_width = cutout_x + cutout_w - effective_right_border - aperture_x;
            aperture_z = front_plate_thickness + effective_front_border;
            aperture_depth = chassis_depth_main - aperture_z - effective_rear_border;
            xz_aperture_cutout(
                aperture_x,
                aperture_z,
                max(0.01, aperture_width),
                max(0.01, aperture_depth),
                open_cutout_corner_radius,
                cutout_top - tolerance,
                2*height
            );
        }
    }

    module bottom_longitudinal_ribs() {
        if (open_bottom && bottom_rib_height > 0 && bottom_rib_thickness > 0) {
            effective_left_border = bottom_cutout_left_border > 0 ? bottom_cutout_left_border : bottom_cutout_border;
            effective_right_border = bottom_cutout_right_border > 0 ? bottom_cutout_right_border : bottom_cutout_border;
            effective_front_border = bottom_cutout_front_border > 0 ? bottom_cutout_front_border : bottom_cutout_border;
            effective_rear_border = bottom_cutout_rear_border > 0 ? bottom_cutout_rear_border : bottom_cutout_border;
            chassis_y = (height - chassis_height) / 2;
            outer_low_y = chassis_y;
            outer_high_y = chassis_y + chassis_height;
            available_rib_height = bottom_rib_side == "low" ? outer_low_y : height - outer_high_y;
            effective_rib_height = min(bottom_rib_height, available_rib_height);
            bottom_surface_left = component_profile == "d_shape" ? cutout_x + cutout_h/2 : cutout_x;
            aperture_x = bottom_surface_left + effective_left_border;
            aperture_width = cutout_x + cutout_w - effective_right_border - aperture_x;
            aperture_z = front_plate_thickness + effective_front_border;
            aperture_depth = chassis_depth_main - aperture_z - effective_rear_border;
            rib_z = front_plate_thickness;
            rib_depth = bottom_rib_full_depth ? chassis_depth_main - rib_z : aperture_z + aperture_depth - rib_z;
            chassis_center_x = chassis_x + chassis_width/2;
            effective_left_rib_offset = bottom_rib_left_center_offset > 0 ? bottom_rib_left_center_offset : bottom_rib_center_offset;
            effective_right_rib_offset = bottom_rib_right_center_offset > 0 ? bottom_rib_right_center_offset : bottom_rib_center_offset;
            positioned_ribs = effective_left_rib_offset > 0 && effective_right_rib_offset > 0 ?
                [chassis_center_x - effective_left_rib_offset - bottom_rib_thickness/2,
                 chassis_center_x + effective_right_rib_offset - bottom_rib_thickness/2] :
                (bottom_rib_position == "outside" ?
                    [aperture_x - bottom_rib_thickness, aperture_x + aperture_width] :
                    [aperture_x - bottom_rib_thickness/2, aperture_x + aperture_width - bottom_rib_thickness/2]);
            effective_rib_embed_depth = min(bottom_rib_embed_depth, case_thickness);
            rib_y = bottom_rib_side == "low" ?
                outer_low_y - effective_rib_height :
                outer_high_y - effective_rib_embed_depth - tolerance;

            if (effective_rib_height > 0) {
                for (rib_x = positioned_ribs) {
                    translate([
                        rib_x,
                        rib_y,
                        rib_z
                    ]) cube([
                        bottom_rib_thickness,
                        effective_rib_height + effective_rib_embed_depth + tolerance,
                        rib_depth
                    ]);
                }
            }
        }
    }

    // Create all rack holes
    module all_rack_holes() {
        // Rack standard: 3 holes per U, with specific positioning
        // Each U is 44.45mm, holes are at specific positions within each U
        hole_spacing_x = 236.525;
        hole_left_x = (rack_width - hole_spacing_x) / 2;
        hole_right_x = (rack_width + hole_spacing_x) / 2;

        default_slot_len = 10.0;
        default_slot_height = 7.0;
        slot_len = rack_slot_length > 0 ? rack_slot_length : default_slot_len;
        slot_height = rack_slot_height > 0 ? rack_slot_height : default_slot_height;

        // Standard rack hole positions within each 1U (44.45mm) unit:
        // First hole: 6.35mm from top of U
        // Second hole: 22.225mm from top of U (middle)
        // Third hole: 38.1mm from top of U (6.35mm from bottom)
        u_hole_positions = [6.35, 22.225, 38.1]; // positions within each U
        
        // Calculate how many full and partial U units we need to consider
        max_u = ceil(rack_height); // Include partial U units
        
        for (side_x = [hole_left_x, hole_right_x]) {
            for (u = [0:max_u-1]) {
                for (hole_index = [0:len(u_hole_positions)-1]) {
                    hole_pos = u_hole_positions[hole_index];
                    // Calculate hole position from top of entire rack
                    hole_y = height - (u * 44.45 + hole_pos);
                    // Always show holes that are at least partially within the rack height
                    // Always show holes fully inside the rack
                    fully_inside = (hole_y >= slot_height/2 && hole_y <= height - slot_height/2);
                    // Show partial holes at edge only if half_height_holes is true
                    partially_inside = (hole_y + slot_height/2 > 0 && hole_y - slot_height/2 < height);
                    pattern_allows_hole = rack_hole_pattern == "standard" || hole_index != 1;
                    show_hole = pattern_allows_hole &&
                        (fully_inside || (half_height_holes && partially_inside && !fully_inside));
                    if (show_hole) {
                        translate([side_x, hole_y, 0]) {
                            linear_extrude(height = chassis_depth_main) {
                                capsule_slot_2d(slot_len, slot_height);
                            }
                        }
                    }
                }
            }
        }
    }

    // Side-wall airflow used by the NBN mount. The open roof and floor do not
    // need the original generator's additional top/bottom honeycomb branch.
    module air_holes() {
        hole_d = 16;
        spacing_x = 15;
        spacing_z = 17;
        margin = 3;
        side_margin = chassis_x;
        cutout_center_z = front_plate_thickness + switch_depth / 2;
        available_height = chassis_height - (2 * margin);
        available_side_depth = switch_depth - (2 * margin);
        y_cols = floor(available_height / spacing_x);
        z_rows_side = floor(available_side_depth / spacing_z);
        actual_grid_height = (y_cols - 1) * spacing_x;
        actual_grid_depth_side = (z_rows_side - 1) * spacing_z;
        cutout_center_y = height / 2;
        y_start = cutout_center_y - actual_grid_height / 2;
        z_start_side = cutout_center_z - actual_grid_depth_side / 2;

        if (y_cols > 0 && z_rows_side > 0) {
            for (i = [0:y_cols-1]) {
                for (j = [0:z_rows_side-1]) {
                    z_offset = (i % 2 == 1) ? spacing_z/2 : 0;
                    y_pos = y_start + i * spacing_x;
                    z_pos = z_start_side + j * spacing_z + z_offset;
                    if (y_pos + hole_d/2 <= cutout_center_y + chassis_height/2 - margin &&
                        y_pos - hole_d/2 >= cutout_center_y - chassis_height/2 + margin &&
                        z_pos + hole_d/2 <= cutout_center_z + switch_depth/2 - margin &&
                        z_pos - hole_d/2 >= cutout_center_z - switch_depth/2 + margin) {
                        translate([side_margin - 1, y_pos, z_pos]) {
                            rotate([0, 90, 0]) {
                                rotate([0, 0, 90]) {
                                    cylinder(h = chassis_width + 2, d = hole_d, $fn = 6);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    module rack_keystone_holder() {
        e=0.01; // epsilon for coplanar face fixes, fixes bug where some faces leave a thin sliver of material
        wall=2.5;
        front_hole_width=14.9;
        front_hole_height=16.3;
        front_hole_z_offset=4.28;
        front_hole_lip=0;

        jack_width=front_hole_width+wall;
        jack_height=25;
        jack_depth=9.7;
        front_large_catch_depth=3;
        front_chamfer_angle=50; // degrees from horizontal (depth axis)

        back_hole_height=24.4;
        back_hole_z_offset=1.9;

        back_small_catch_length=2;
        back_small_catch_depth=1.4;

        back_large_catch_length=2.6;
        back_large_catch_depth=1.3;
        
        back_chamfer=1.2;

        // Flip entire part because I accidentially desinged it upside down
        translate([0, 0, jack_height + wall])
        mirror([0, 0, 1]) {
            union(){
                // Back edge chamfer via intersection with hull (4 separate cuts → 1 operation)
                intersection() {
                    difference(){
                        cube([jack_width+wall,jack_depth,jack_height+wall]);
                        // Front hole
                        translate([(jack_width+wall-front_hole_width)/2,0,front_hole_z_offset])
                            cube([front_hole_width,jack_depth+wall,front_hole_height]);
                        // Back hole
                        translate([(jack_width+wall-front_hole_width)/2,front_large_catch_depth,back_hole_z_offset])
                            cube([front_hole_width,jack_depth+wall-front_large_catch_depth,back_hole_height]);
                        // Chamfer on front face of small catch
                        translate([wall + front_hole_width, 0, 0])
                            rotate([0, -90, 0])
                                linear_extrude(front_hole_width)
                                    polygon([
                                        [front_hole_z_offset + front_hole_height - e, front_hole_lip - e],
                                        [front_hole_z_offset + front_hole_height + (front_large_catch_depth - front_hole_lip) * tan(front_chamfer_angle), front_large_catch_depth],
                                        [front_hole_z_offset + front_hole_height - e, front_large_catch_depth]
                                    ]);
                    } // end difference
                    // Chamfer all 4 back edges in one hull operation
                    hull() {
                        cube([jack_width+wall, jack_depth-back_chamfer, jack_height+wall]);
                        translate([back_chamfer, 0, back_chamfer])
                            cube([jack_width+wall-2*back_chamfer, jack_depth, jack_height+wall-2*back_chamfer]);
                    }
                } // end intersection

                // Small back catch
                translate([
                    (jack_width + wall - front_hole_width)/2 - e,
                    jack_depth - back_small_catch_depth,
                    back_hole_z_offset + back_hole_height - back_small_catch_length - e
                ]) cube([
                    front_hole_width + 2*e,
                    back_small_catch_depth + e,
                    back_small_catch_length + 2*e
                ]);

                // Large back catch
                translate([
                    (jack_width + wall - front_hole_width)/2 - e,
                    jack_depth - back_large_catch_depth,
                    back_hole_z_offset - e
                ]) cube([
                    front_hole_width + 2*e,
                    back_large_catch_depth + e,
                    back_large_catch_length + 2*e
                ]);

            } // end union
        } // end mirror
    } // end module keystone



    module keystone_grid_cutouts() {
        if (keystone_enabled) {
            for (row = [0:keystone_rows-1]) {
                for (column = [0:keystone_columns-1]) {
                    translate([
                        keystone_grid_left + column * (keystone_outer_width + keystone_effective_column_gap) + keystone_plate_overlap,
                        keystone_grid_bottom + row * (keystone_outer_height + keystone_effective_row_gap) + keystone_plate_overlap,
                        -tolerance
                    ]) cube([
                        keystone_outer_width - 2 * keystone_plate_overlap,
                        keystone_outer_height - 2 * keystone_plate_overlap,
                        front_plate_thickness + 2 * tolerance
                    ]);
                }
            }
        }
    }

    module keystone_grid() {
        if (keystone_enabled) {
            for (row = [0:keystone_rows-1]) {
                for (column = [0:keystone_columns-1]) {
                    translate([
                        keystone_grid_left + column * (keystone_outer_width + keystone_effective_column_gap),
                        keystone_grid_bottom + row * (keystone_outer_height + keystone_effective_row_gap) + keystone_outer_height,
                        0
                    ]) rotate([90,0,0]) rack_keystone_holder();
                }
            }
        }
    }

    // Recess labels into the clear upper border of each grid holder. The NBN
    // cradle's installed top is model -Y, so row zero is the visible top row.
    module keystone_grid_labels(extra_depth=0) {
        label_y_in_holder = 2.2;
        if (keystone_enabled && port_labels) {
            for (row = [0:keystone_rows-1]) {
                for (column = [0:keystone_columns-1]) {
                    port_number = row * keystone_columns + column + 1;
                    translate([
                        keystone_grid_left + column * (keystone_outer_width + keystone_effective_column_gap) + keystone_outer_width/2,
                        keystone_grid_bottom + row * (keystone_outer_height + keystone_effective_row_gap) + label_y_in_holder,
                        -extra_depth
                    ]) linear_extrude(height=port_label_depth + 2*extra_depth)
                        mirror([0, 1, 0])
                            text(str(port_number), size=port_label_size,
                                halign="center", valign="center");
                }
            }
        }
    }

    module unlabelled_assembly() {
        union() {
            difference() {
                main_body();
                union() {
                    switch_cutout();
                    front_entry_chamfer_cutout();
                    open_top_cutout();
                    open_bottom_cutout();
                    all_rack_holes();
                    if (air_holes) {
                        air_holes();
                    }
                    keystone_grid_cutouts();
                }
            }
            bottom_longitudinal_ribs();
            keystone_grid();
        }
    }

    module labelled_panel() {
        difference() {
            unlabelled_assembly();
            keystone_grid_labels(tolerance);
        }
    }

    // All output modes use the same origin so panel and label STLs can be imported
    // together as parts of one object without any manual alignment in the slicer.
    translate([-rack_width/2, -height/2, 0]) {
        if (output_part == "labels") {
            keystone_grid_labels();
        } else if (output_part == "panel") {
            labelled_panel();
        } else {
            labelled_panel();
            keystone_grid_labels();
        }
    }
}
