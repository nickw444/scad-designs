// Focused geometry for our numbered ten-port, two-thirds-U patch panel.

module patch_keystone_holder() {
    e = 0.01;
    wall = 2.5;
    front_hole_width = 14.9;
    front_hole_height = 16.3;
    front_hole_z_offset = 4.28;
    front_hole_lip = 0;
    jack_width = front_hole_width + wall;
    jack_height = 25;
    jack_depth = 9.7;
    front_large_catch_depth = 3;
    front_chamfer_angle = 50;
    back_hole_height = 24.4;
    back_hole_z_offset = 1.9;
    back_small_catch_length = 2;
    back_small_catch_depth = 1.4;
    back_large_catch_length = 2.6;
    back_large_catch_depth = 1.3;
    back_chamfer = 1.2;

    translate([0, 0, jack_height + wall])
    mirror([0, 0, 1]) {
        union() {
            difference() {
                cube([jack_width + wall, jack_depth, jack_height + wall]);
                translate([(jack_width + wall - front_hole_width)/2, 0, front_hole_z_offset])
                    cube([front_hole_width, jack_depth + wall, front_hole_height]);
                translate([(jack_width + wall - front_hole_width)/2, front_large_catch_depth, back_hole_z_offset])
                    cube([front_hole_width, jack_depth + wall - front_large_catch_depth, back_hole_height]);
                translate([wall + front_hole_width, 0, 0])
                    rotate([0, -90, 0])
                        linear_extrude(front_hole_width)
                            polygon([
                                [front_hole_z_offset + front_hole_height - e, front_hole_lip - e],
                                [front_hole_z_offset + front_hole_height + (front_large_catch_depth - front_hole_lip) * tan(front_chamfer_angle), front_large_catch_depth],
                                [front_hole_z_offset + front_hole_height - e, front_large_catch_depth]
                            ]);
                translate([jack_width + wall + e, 0, -e])
                    rotate([0, -90, 0])
                        linear_extrude(jack_width + wall + 2*e)
                            polygon([[-e, jack_depth + e], [back_chamfer, jack_depth + e], [-e, jack_depth - back_chamfer]]);
                translate([jack_width + wall + e, 0, -e])
                    rotate([0, -90, 0])
                        linear_extrude(jack_width + wall + 2*e)
                            polygon([[jack_height + wall + 2*e, jack_depth + e], [jack_height + wall + 2*e - back_chamfer, jack_depth + e], [jack_height + wall + 2*e, jack_depth - back_chamfer]]);
                translate([0, 0, -e])
                    linear_extrude(jack_height + wall + 2*e)
                        polygon([[-e, jack_depth + e], [back_chamfer, jack_depth + e], [-e, jack_depth - back_chamfer]]);
                translate([0, 0, -e])
                    linear_extrude(jack_height + wall + 2*e)
                        polygon([[jack_width + wall + e, jack_depth + e], [jack_width + wall + e - back_chamfer, jack_depth + e], [jack_width + wall + e, jack_depth - back_chamfer]]);
            }
            translate([wall + front_hole_width, 0, 0])
                rotate([0, -90, 0])
                    linear_extrude(front_hole_width)
                        polygon([
                            [back_hole_z_offset + back_hole_height - back_small_catch_length, jack_depth - back_small_catch_depth],
                            [back_hole_z_offset + back_hole_height, jack_depth - back_small_catch_depth],
                            [back_hole_z_offset + back_hole_height, jack_depth],
                            [back_hole_z_offset + back_hole_height - back_small_catch_length, jack_depth]
                        ]);
            translate([wall + front_hole_width, 0, 0])
                rotate([0, -90, 0])
                    linear_extrude(front_hole_width)
                        polygon([
                            [back_hole_z_offset, jack_depth - back_large_catch_depth],
                            [back_hole_z_offset + back_large_catch_length, jack_depth - back_large_catch_depth],
                            [back_hole_z_offset + back_large_catch_length, jack_depth],
                            [back_hole_z_offset, jack_depth]
                        ]);
        }
    }
}

module ten_port_patch_panel(
    output_part = "assembled",
    rack_width = 254,
    rack_height = 0.666667,
    front_thickness = 3,
    corner_radius = 4,
    port_label_size = 4,
    port_label_font = "Liberation Sans:style=Bold",
    port_label_depth = 0.6
) {
    $fn = 64;
    height = 44.45 * rack_height;
    tolerance = 0.42;
    port_count = 10;
    holder_width = 19.9;
    holder_height = 27.5;
    holder_depth = 9.7;
    rib_thickness = 2;
    rib_depth = 3;

    assert(rack_width == 254, "This design supports a 10-inch rack only.");
    assert(port_count * holder_width <= 221.5, "Keystone holders do not fit between the rack ears.");
    assert(holder_height <= height, "Keystone holders do not fit the selected panel height.");

    module capsule_slot_2d(length, slot_height) {
        hull() {
            translate([-length/2 + slot_height/2, 0]) circle(r=slot_height/2);
            translate([ length/2 - slot_height/2, 0]) circle(r=slot_height/2);
        }
    }

    module rounded_rect_2d(width, rect_height, radius) {
        hull() {
            translate([radius, radius]) circle(r=radius);
            translate([width - radius, radius]) circle(r=radius);
            translate([width - radius, rect_height - radius]) circle(r=radius);
            translate([radius, rect_height - radius]) circle(r=radius);
        }
    }

    module chamfered_rib(width) {
        difference() {
            cube([width, rib_thickness, rib_depth]);
            translate([-rib_depth, -tolerance, rib_depth])
                rotate([0, 45, 0])
                    cube([rib_depth * 1.5, rib_thickness + 2*tolerance, rib_depth * 1.5]);
            translate([width, -tolerance, 0])
                rotate([0, -45, 0])
                    cube([rib_depth * 1.5, rib_thickness + 2*tolerance, rib_depth * 1.5]);
        }
    }

    module structural_ribs() {
        usable_width = 221.5 * 0.9;
        rib_start_x = (rack_width - usable_width) / 2;
        for (u = [0:ceil(rack_height) - 1]) {
            for (hole_pos = [6.35, 22.225, 38.1]) {
                rib_y = height - (u * 44.45 + hole_pos);
                if (rib_y >= rib_thickness/2 && rib_y <= height - rib_thickness/2) {
                    translate([rib_start_x, rib_y - rib_thickness/2, front_thickness])
                        chamfered_rib(usable_width);
                }
            }
        }
    }

    module plate_body() {
        union() {
            linear_extrude(height=front_thickness)
                rounded_rect_2d(rack_width, height, corner_radius);
            structural_ribs();
        }
    }

    module rack_holes() {
        hole_spacing_x = 236.525;
        slot_length = 10;
        slot_height = 7;
        for (side_x = [(rack_width - hole_spacing_x)/2, (rack_width + hole_spacing_x)/2]) {
            for (u = [0:ceil(rack_height) - 1]) {
                for (hole_pos = [6.35, 22.225, 38.1]) {
                    hole_y = height - (u * 44.45 + hole_pos);
                    fully_inside = hole_y >= slot_height/2 && hole_y <= height - slot_height/2;
                    partially_inside = hole_y + slot_height/2 > 0 && hole_y - slot_height/2 < height;
                    if (fully_inside || (partially_inside && !fully_inside)) {
                        translate([side_x, hole_y, 0])
                            linear_extrude(height=front_thickness + tolerance)
                                capsule_slot_2d(slot_length, slot_height);
                    }
                }
            }
        }
    }

    module holder_cutouts() {
        for (port = [0:port_count - 1]) {
            translate([
                rack_width/2 - port_count*holder_width/2 + port*holder_width,
                height/2 - holder_height/2,
                -tolerance
            ]) cube([holder_width, holder_height, holder_depth + 2*tolerance]);
        }
    }

    module holders() {
        for (port = [0:port_count - 1]) {
            translate([
                rack_width/2 - port_count*holder_width/2 + port*holder_width,
                height/2 + holder_height/2,
                0
            ]) rotate([90, 0, 0]) patch_keystone_holder();
        }
    }

    module panel_without_labels() translate([-rack_width/2, -height/2, 0]) {
        union() {
            difference() {
                plate_body();
                rack_holes();
                holder_cutouts();
            }
            holders();
        }
    }

    module labels(extra_depth=0) {
        label_y = -holder_height/2 + 24.04;
        for (port = [0:port_count - 1]) {
            translate([
                -port_count*holder_width/2 + port*holder_width + holder_width/2,
                label_y,
                -extra_depth
            ]) linear_extrude(height=port_label_depth + 2*extra_depth)
                mirror([1, 0, 0])
                    text(str(port_count - port), size=port_label_size,
                        font=port_label_font, halign="center", valign="center");
        }
    }

    module panel() {
        difference() {
            panel_without_labels();
            labels(tolerance);
        }
    }

    if (output_part == "labels") {
        labels();
    } else if (output_part == "panel") {
        panel();
    } else {
        panel();
        labels();
    }
}
