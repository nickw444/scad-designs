// UniFi G5 PTZ low-profile two-part soffit mount
// Camera shoulder/body seating face is z=0.
//
// Export with:
//   openscad -D 'part="carrier"' -o ..._carrier.stl this_file.scad
//   openscad -D 'part="flange"'  -o ..._ceiling_flange.stl this_file.scad

$fn = 240;
part = "assembly"; // carrier, flange, assembly, section, diagnostics

// Established camera interface
outer_d = 60.40;
guide_d = 52.40;
radial_projection = 2.50;
contact_tip_d = guide_d-2*radial_projection;
contact_arc_length = 20.50;

// The proven camera-fin pattern remains at its existing rotation. The true
// front datum is the camera security-screw hole: the previous marker sat
// 3.0 mm to its right at the carrier OD when viewed from the camera side.
camera_contact_rear_angle = 0;
front_datum_offset_mm = -3.00;
front_datum_correction =
    front_datum_offset_mm/(outer_d/2)*180/PI; // -5.691 degrees
front_datum_angle = 180+front_datum_correction;
rear_datum_angle = front_datum_angle-180;
grommet_flat_angle = front_datum_angle;
grommet_profile_rotation = grommet_flat_angle-90;

fit_clearance = 0.20;
ordinary_camera_height = 5.10;
locking_camera_height = 8.30;
locking_detent_height = 7.60;
ordinary_top = ordinary_camera_height-fit_clearance; // 4.90 mm
locking_top = 7.50;

// Confirmed clockwise camera detent
detent_projection = locking_camera_height-locking_detent_height; // 0.70 mm
detent_depth = detent_projection;
detent_relief_floor = locking_top-detent_depth;                  // 6.80 mm
detent_width = 2.60;
detent_end_inset = 3.00;
detent_r = 25.20;

// Carrier body and top-loaded grommet seat. Override carrier_extension at
// export time to create a longer shaft while preserving both end interfaces.
carrier_extension = 0;
grommet_top_clearance = 0.50;
camera_cavity_h = 8.70;

// Direct cross-checks from each carrier contact face to the upper gasket
// corner. Both independently place that corner at z=14.90 in the locked
// carrier: 4.90+10.00 and 7.50+7.40.
ordinary_contact_to_gasket_top = 10.00;
locking_contact_to_gasket_top = 7.40;
camera_gasket_corner_z =
    (
        ordinary_top+ordinary_contact_to_gasket_top
        +locking_top+locking_contact_to_gasket_top
    )/2; // 14.90

grommet_measured_d = 32.00;
grommet_measured_flat_chord = 15.80;
grommet_measured_flat_r =
    sqrt(
        pow(grommet_measured_d/2, 2)
        -pow(grommet_measured_flat_chord/2, 2)
    ); // 13.92 mm from circle centre to flat
grommet_measured_flat_h =
    grommet_measured_d/2+grommet_measured_flat_r; // 29.92 mm
grommet_measured_h = 16.00;
grommet_xy_clearance = 0.50;     // 0.25 mm per side/profile clearance

grommet_pocket_d = grommet_measured_d+grommet_xy_clearance; // 32.50
grommet_pocket_flat_h =
    grommet_measured_flat_h+grommet_xy_clearance;            // 30.42
grommet_pocket_flat_y = grommet_pocket_flat_h-grommet_pocket_d/2;
// The factory shelf is only a chordal cap on the flat/front side; there is no
// perimeter ledge around the circular portion. The 3.0 mm hole is centred
// at the camera-confirmed r=11.6 position. The inner shelf chord remains at
// r=8.6; the cleared 32.5 mm pocket puts the pocket flat at r=14.17.
camera_screw_angle = grommet_flat_angle;
camera_screw_d = 3.00;
camera_screw_access_d = 6.50;
// Retain the factory-derived shelf and proven camera screw position even
// though the remeasured grommet channel is smaller.
grommet_shelf_edge_r =
    8.60;
camera_screw_r = 11.60;

// Support-free camera-body/gasket preload interface. A 45-degree cavity wall
// bears gently on the measured outer upper corner of the rubber gasket. The
// horizontal structural plane remains clear of the camera top.
camera_gasket_outer_d = 45.50;
camera_housing_d = 40.00;
camera_housing_diametral_clearance = 0.20;
camera_flat_inner_d =
    camera_housing_d+camera_housing_diametral_clearance; // 40.20
camera_gasket_chamfer_preload = 0.10;
camera_gasket_flat_clearance = 0.50;
camera_gasket_chamfer_contact_z =
    camera_gasket_corner_z-camera_gasket_chamfer_preload; // 14.80
camera_structural_flat_z =
    camera_gasket_corner_z+camera_gasket_flat_clearance; // 15.40
camera_gasket_chamfer_inner_r =
    camera_gasket_outer_d/2
    -(camera_structural_flat_z-camera_gasket_chamfer_contact_z); // 22.15
camera_gasket_chamfer_lower_z =
    camera_gasket_chamfer_contact_z
    -(guide_d/2-camera_gasket_outer_d/2); // 11.35
camera_flange_top_thickness = 0.40;
camera_flange_top_z =
    camera_structural_flat_z+camera_flange_top_thickness; // 15.80

camera_screw_shelf_thickness = 2.00;
// Extensions raise the chordal cable-grommet stop without changing the
// validated 2 mm camera-facing screw shelf at z=15.40..17.40.
// The grommet projects directly upward inside a vertical D-shaped channel.
grommet_base_shelf_top =
    camera_structural_flat_z+camera_screw_shelf_thickness;      // 17.40
grommet_pocket_bottom =
    grommet_base_shelf_top+carrier_extension;
grommet_pocket_top = grommet_pocket_bottom+grommet_measured_h;  // 33.40
carrier_h = grommet_pocket_top+grommet_top_clearance;
// carrier_extension raises the gasket shelf and the ceiling interface
// together. Compact / +15 / +30 heights: 33.90 / 48.90 / 63.90 mm.

cable_opening_w = 22.00;
cable_opening_h = 16.00;
cable_opening_r = 3.00;

// Protected ownership markings.
signature_depth = 0.35;
signature_font = "Liberation Sans:style=Bold";
carrier_signature_size = 1.50;
carrier_signature_line_offset = 1.30;
flange_signature_size = 3.20;
flange_signature_line_offset = 1.90;
flange_signature_center_r = 22.00;
flange_signature_angle = 0;

// Carrier/flange bayonet
cup_outer_r = 20.30;
groove_outer_r = 28.20;
lip_h = 3.00;
lip_bottom = carrier_h-lip_h;
insertion_gap = 34;
flange_lug_angle = 26;
keyed_insertion_gap = 46;
keyed_flange_lug_angle = 38;
keyed_lug_index = 0;
bayonet_stop_angle = 5;
bayonet_wrong_way_stop_angle = 6;

// Ceiling flange
flange_h = 5.00;
flange_spigot_h = 7.00;
flange_spigot_inner_r = 24.65;
flange_spigot_outer_r = 26.00;
flange_lug_outer_r = 28.00;
flange_lug_root_inner_r = 23.40;
flange_lug_root_extra_angle = 4;
flange_lug_fragments = 72;
flange_mount_r = 20.00;
flange_mount_clearance_d = 4.40;
flange_mount_head_d = 9.00;
flange_mount_head_depth = 3.70;
bayonet_radial_clearance = 0.12;
bayonet_axial_clearance = 0.15;
bayonet_socket_bottom =
    carrier_h-flange_spigot_h-bayonet_axial_clearance; // 26.75 + extension
bayonet_lip_inner_r =
    flange_spigot_outer_r+bayonet_radial_clearance;    // 26.12
// Negative model rotation produces the requested clockwise locking motion
// when the carrier is viewed from below in its installed orientation.
assembly_lock_angle = -35;

function lug_angle_for_index(i) =
    i == keyed_lug_index ? keyed_flange_lug_angle : flange_lug_angle;
function insertion_gap_for_index(i) =
    i == keyed_lug_index ? keyed_insertion_gap : insertion_gap;
function lock_stop_start_for_index(i) =
    i*120+assembly_lock_angle-lug_angle_for_index(i)/2
    -bayonet_stop_angle;
function wrong_way_stop_start_for_index(i) =
    i*120+insertion_gap_for_index(i)/2;

// installed_flange() reflects the flange about local X before rotating it
// through assembly_lock_angle. This local rotation therefore makes the short
// side/normal of the ceiling cable opening share the installed grommet-flat
// datum, with its long edge parallel to the D-flat chord.
flange_cable_opening_angle =
    assembly_lock_angle-grommet_flat_angle-90; // -229.309 degrees

// Positive rotation lock using the UniFi-provided self-tapping security screw.
// All fastener features are true circular radial bores.
lock_screw_angle = rear_datum_angle;
lock_screw_z = carrier_h-3.50; // 30.40 + extension
security_screw_major_d = 2.50;
security_screw_length = 8.40;
security_screw_head_measured_d = 5.70;
security_screw_head_measured_h = 0.70;
lock_screw_clearance_d = 3.00; // 0.50 mm total clearance on the major thread
lock_screw_head_d = 6.20;      // 0.50 mm total head clearance
lock_screw_head_depth = 1.00;  // 0.30 mm deeper than the measured head

screw_boss_inner_r = 20.50;
screw_boss_angle = 14;
self_tap_pilot_d = 2.00;
self_tap_pilot_depth = 4.80;
flange_screw_angle = assembly_lock_angle-lock_screw_angle;
flange_screw_z = carrier_h+flange_h-lock_screw_z; // 8.50 local z

// Matching 45-degree ramps make both halves printable without support under
// the bayonet capture surfaces.
bayonet_ramp_clearance = 0.20;
carrier_ramp_outer_z =
    lip_bottom-(groove_outer_r-bayonet_lip_inner_r); // 36.42
flange_lug_inner_r = flange_spigot_outer_r-0.20;
flange_lug_top_z = flange_h+flange_spigot_h;
flange_lug_bottom_inner_z =
    carrier_h+flange_h
    -(carrier_ramp_outer_z+groove_outer_r-flange_lug_inner_r)
    +bayonet_ramp_clearance;
flange_lug_bottom_outer_z =
    carrier_h+flange_h
    -(carrier_ramp_outer_z+groove_outer_r-flange_lug_outer_r)
    +bayonet_ramp_clearance;
flange_lug_root_z = flange_h;
flange_lug_root_h = flange_lug_top_z-flange_lug_root_z;

wall_r = guide_d/2;
tip_r = contact_tip_d/2;
contact_root_r = wall_r+0.20; // structural overlap into carrier wall
contact_mid_r = (wall_r+tip_r)/2;
contact_angle = contact_arc_length/contact_mid_r*180/PI;
detent_offset =
    (contact_arc_length/2-detent_end_inset)/detent_r*180/PI;

module annular_sector(r_inner, r_outer, h, angle, fragments=undef) {
    rotate_extrude(
        angle=angle,
        convexity=10,
        $fn=is_undef(fragments)
            ? max(24, ceil($fn*angle/360))
            : fragments
    )
        translate([r_inner, 0, 0])
            square([r_outer-r_inner, h]);
}

module rounded_rect_2d(w, h, r) {
    hull()
        for (x=[-w/2+r, w/2-r], y=[-h/2+r, h/2-r])
            translate([x, y])
                circle(r=r);
}

module d_profile_2d(d, flat_y) {
    intersection() {
        circle(d=d);
        translate([-d, -d])
            square([2*d, d+flat_y]);
    }
}

module aligned_grommet_profile_2d(d, flat_y) {
    // Native D profile has its flat at +Y; rotate it onto the front datum.
    rotate([0, 0, grommet_profile_rotation])
        d_profile_2d(d, flat_y);
}

module ownership_signature_2d(size, line_offset) {
    union() {
        translate([0, -line_offset])
            text(
                "© 2026",
                size=size,
                font=signature_font,
                halign="center",
                valign="center"
            );
        translate([0, line_offset])
            text(
                "Nick Whyte",
                size=size,
                font=signature_font,
                halign="center",
                valign="center"
            );
    }
}

module carrier_signature_cut() {
    // Deboss the concealed flat annular floor of the upper bayonet socket.
    // Local X follows the tangent and local Y spans the floor radially, keeping
    // the marking completely outside the cable-grommet pocket.
    signature_r = (cup_outer_r+bayonet_lip_inner_r)/2;
    rotate([0, 0, grommet_flat_angle-90])
        translate([
            0,
            signature_r,
            bayonet_socket_bottom-signature_depth
        ])
            linear_extrude(height=signature_depth+0.02)
                ownership_signature_2d(
                    carrier_signature_size,
                    carrier_signature_line_offset
                );
}

module flange_signature_cut() {
    // Concealed ceiling-facing identification, positioned tangentially in the
    // clear +X sector between the central cable opening and flange edge.
    // Mirroring local X makes it read correctly when viewed from the exterior
    // ceiling side (-Z), rather than from inside the part (+Z).
    rotate([0, 0, flange_signature_angle])
        translate([flange_signature_center_r, 0, -0.02])
            rotate([0, 0, 90])
                mirror([1, 0, 0])
                    linear_extrude(height=signature_depth+0.04)
                        ownership_signature_2d(
                            flange_signature_size,
                            flange_signature_line_offset
                        );
}

module grommet_below_shelf_opening_2d() {
    // Match the grommet pocket around the complete circular edge, retaining
    // material only between the front flat and the factory shelf chord.
    intersection() {
        aligned_grommet_profile_2d(
            grommet_pocket_d,
            grommet_pocket_flat_y
        );
        rotate([0, 0, grommet_flat_angle])
            translate([-2*grommet_pocket_d, -grommet_pocket_d])
                square([
                    2*grommet_pocket_d+grommet_shelf_edge_r,
                    2*grommet_pocket_d
                ]);
    }
}

module radial_circular_bore(angle, radius, z, diameter, length) {
    rotate([0, 0, angle])
        translate([radius, 0, z])
            rotate([0, 90, 0])
                cylinder(d=diameter, h=length);
}

module solid_contact(center_angle, top_height) {
    rotate([0, 0, center_angle-contact_angle/2])
        annular_sector(tip_r, contact_root_r, top_height, contact_angle);
}

// Radially extruded rectangular cutter producing a positive-sided groove.
module clockwise_detent_cut() {
    centre = camera_contact_rear_angle-detent_offset;
    radial_margin = 0.10;
    cutter_overrun = 0.20;

    rotate([0, 0, centre])
        translate([tip_r-radial_margin, 0, 0])
            rotate([0, 90, 0])
                linear_extrude(
                    height=contact_root_r-tip_r+2*radial_margin,
                    convexity=4
                )
                    polygon(points=[
                        [-(locking_top+cutter_overrun), -detent_width/2],
                        [-detent_relief_floor, -detent_width/2],
                        [-detent_relief_floor, detent_width/2],
                        [-(locking_top+cutter_overrun), detent_width/2]
                    ]);
}

module camera_contacts() {
    solid_contact(camera_contact_rear_angle+120, ordinary_top);
    solid_contact(camera_contact_rear_angle+240, ordinary_top);

    difference() {
        solid_contact(camera_contact_rear_angle, locking_top);
        clockwise_detent_cut();
    }
}

module transition_cavity() {
    // Vertical fin clearance followed by an exact 45-degree printable cavity
    // wall. The line passes 0.1 mm into the measured Ø45.5 gasket corner and
    // terminates at the horizontal plane 0.5 mm above the camera top.
    union() {
        translate([0, 0, camera_cavity_h-0.02])
            cylinder(
                d=guide_d,
                h=camera_gasket_chamfer_lower_z-camera_cavity_h+0.04
            );
        translate([0, 0, camera_gasket_chamfer_lower_z-0.01])
            cylinder(
                r1=guide_d/2,
                r2=camera_gasket_chamfer_inner_r,
                h=camera_structural_flat_z
                    -camera_gasket_chamfer_lower_z+0.02
            );
    }
}

module bayonet_lug_track_void() {
    rotate_extrude(convexity=10)
        polygon(points=[
            [bayonet_lip_inner_r, bayonet_socket_bottom],
            [groove_outer_r, bayonet_socket_bottom],
            [groove_outer_r, carrier_ramp_outer_z],
            [bayonet_lip_inner_r, lip_bottom]
        ]);
}

module carrier() {
    union() {
        difference() {
            cylinder(d=outer_d, h=carrier_h);

            // Camera neck cavity and printable transition.
            translate([0, 0, -0.10])
                cylinder(d=guide_d, h=camera_cavity_h+0.10);
            transition_cavity();

            // Central clearance beneath the horizontal structural plane. The
            // 45-degree transition cavity—not this plane—preloads the gasket.
            translate([0, 0, camera_gasket_corner_z-0.02])
                cylinder(
                    d=camera_flat_inner_d,
                    h=camera_structural_flat_z
                        -camera_gasket_corner_z+0.02
                );

            // Above the camera-facing structural flat, retain only the
            // factory flat-side chordal shelf; the circular side remains open.
            translate([0, 0, camera_structural_flat_z-0.02])
                linear_extrude(
                    height=carrier_h-camera_structural_flat_z+0.22
                )
                    grommet_below_shelf_opening_2d();

            // The complete D profile starts at the top of the 2 mm chordal
            // screw shelf. Its boundary is vertical: no continued chamfer.
            translate([0, 0, grommet_pocket_bottom])
                linear_extrude(
                    height=carrier_h-grommet_pocket_bottom+0.20
                )
                    aligned_grommet_profile_2d(
                        grommet_pocket_d,
                        grommet_pocket_flat_y
                    );

            // Centred 3.0 mm axial clearance hole through the shelf and into
            // the camera's factory threaded retention point.
            rotate([0, 0, camera_screw_angle])
                translate([camera_screw_r, 0, -0.10])
                    cylinder(d=camera_screw_d, h=carrier_h+0.20);

            // Extended carriers raise the gasket shelf but retain the factory
            // screw at the original 2 mm shelf. This 6.5 mm access well lets
            // the factory screw head and driver reach that unchanged seat.
            if (carrier_extension > 0)
                rotate([0, 0, camera_screw_angle])
                    translate([
                        camera_screw_r,
                        0,
                        grommet_base_shelf_top
                    ])
                        cylinder(
                            d=camera_screw_access_d,
                            h=carrier_extension+0.20
                        );

            carrier_signature_cut();

            // Shallow blind clearance socket for the complete annular flange
            // spigot. It terminates near the ceiling end rather than forming
            // a water path down the carrier.
            translate([0, 0, bayonet_socket_bottom])
                difference() {
                    cylinder(
                        r=bayonet_lip_inner_r,
                        h=carrier_h-bayonet_socket_bottom+0.20
                    );
                    translate([0, 0, -0.10])
                        cylinder(
                            r=cup_outer_r,
                            h=carrier_h-bayonet_socket_bottom+0.40
                        );
                }

            // Outer lug track with a 45-degree ceiling. This leaves a matching
            // self-supporting ramp beneath the retaining lip.
            bayonet_lug_track_void();

            // Concentric annular-sector entry slots: curved inner/outer faces
            // and straight end faces radiating from the part centre.
            for (i=[0:2])
                rotate([
                    0,
                    0,
                    i*120-insertion_gap_for_index(i)/2
                ])
                    translate([0, 0, carrier_ramp_outer_z-0.10])
                        annular_sector(
                            bayonet_lip_inner_r-0.10,
                            groove_outer_r+0.10,
                            carrier_h-carrier_ramp_outer_z+0.30,
                            insertion_gap_for_index(i),
                            flange_lug_fragments
                        );

            // True circular 3.0 mm radial clearance for the 2.5 mm security
            // screw thread.
            radial_circular_bore(
                lock_screw_angle,
                flange_spigot_outer_r-0.20,
                lock_screw_z,
                lock_screw_clearance_d,
                outer_d/2-flange_spigot_outer_r+0.40
            );

            // Circular flat-bottom counterbore for the measured 5.7 x 0.7 mm
            // head: 6.2 mm diameter and 1.0 mm radial depth lets it sit flush.
            radial_circular_bore(
                lock_screw_angle,
                outer_d/2-lock_screw_head_depth,
                lock_screw_z,
                lock_screw_head_d,
                lock_screw_head_depth+0.20
            );
        }

        camera_contacts();

        // Positive rotational stops at exactly the clockwise 35-degree
        // screw-alignment position. Each lug's trailing radial face meets a
        // stop derived from that lug's actual angular width.
        for (i=[0:2])
            intersection() {
                bayonet_lug_track_void();
                rotate([0, 0, lock_stop_start_for_index(i)])
                    translate([0, 0, bayonet_socket_bottom-0.10])
                        annular_sector(
                            bayonet_lip_inner_r-0.10,
                            groove_outer_r+0.10,
                            carrier_h-bayonet_socket_bottom+0.20,
                            bayonet_stop_angle
                        );
            }

        // Shoulders immediately beside the entry slots reject rotation in the
        // wrong direction. Only the clockwise assembly_lock_angle path reaches
        // the security-screw/pilot alignment.
        for (i=[0:2])
            intersection() {
                bayonet_lug_track_void();
                rotate([0, 0, wrong_way_stop_start_for_index(i)])
                    translate([0, 0, bayonet_socket_bottom-0.10])
                        annular_sector(
                            bayonet_lip_inner_r-0.10,
                            groove_outer_r+0.10,
                            carrier_h-bayonet_socket_bottom+0.20,
                            bayonet_wrong_way_stop_angle
                        );
            }
    }
}

module flange_screw_boss() {
    rotate([0, 0, flange_screw_angle-screw_boss_angle/2])
        translate([0, 0, flange_h])
            annular_sector(
                screw_boss_inner_r,
                flange_spigot_outer_r,
                flange_spigot_h,
                screw_boss_angle
            );
}

module flange_lug_root_reinforcements() {
    for (i=[0:2])
        let(
            c=i*120,
            root_angle=lug_angle_for_index(i)+flange_lug_root_extra_angle
        )
        rotate([0, 0, c-root_angle/2])
            translate([0, 0, flange_lug_root_z])
                annular_sector(
                    flange_lug_root_inner_r,
                    flange_spigot_outer_r,
                    flange_lug_root_h,
                    root_angle,
                    flange_lug_fragments
                );
}

module flange_lugs() {
    for (i=[0:2])
        let(c=i*120, lug_angle=lug_angle_for_index(i))
        rotate([0, 0, c-lug_angle/2])
            rotate_extrude(
                angle=lug_angle,
                convexity=10,
                $fn=flange_lug_fragments
            )
                polygon(points=[
                    [flange_lug_inner_r, flange_lug_bottom_inner_z],
                    [flange_lug_outer_r, flange_lug_bottom_outer_z],
                    [flange_lug_outer_r, flange_lug_top_z],
                    [flange_lug_inner_r, flange_lug_top_z]
                ]);
}

module flange_self_tap_pilot() {
    // Circular blind pilot from the reinforced boss's outer face. The 2.0 mm
    // bore lets the supplied 2.5 mm thread form directly into the printed part
    // while retaining 0.7 mm of material at the boss's inner end.
    radial_circular_bore(
        flange_screw_angle,
        flange_spigot_outer_r-self_tap_pilot_depth,
        flange_screw_z,
        self_tap_pilot_d,
        self_tap_pilot_depth+0.20
    );
}

module ceiling_flange() {
    difference() {
        union() {
            difference() {
                cylinder(d=outer_d, h=flange_h);

                translate([0, 0, -0.10])
                    linear_extrude(height=flange_h+0.20)
                        rotate([0, 0, flange_cable_opening_angle])
                            rounded_rect_2d(
                                cable_opening_w,
                                cable_opening_h,
                                cable_opening_r
                            );

                // Three soffit screws on the unchanged 40 mm pitch circle.
                // The deeper, wider flat-bottom pockets accommodate the
                // countersunk screw heads without leaving them proud.
                for (a=[60, 180, 300]) {
                    translate([
                        flange_mount_r*cos(a),
                        flange_mount_r*sin(a),
                        -0.10
                    ])
                        cylinder(
                            d=flange_mount_clearance_d,
                            h=flange_h+0.20
                        );
                    translate([
                        flange_mount_r*cos(a),
                        flange_mount_r*sin(a),
                        flange_h-flange_mount_head_depth
                    ])
                        cylinder(
                            d=flange_mount_head_d,
                            h=flange_mount_head_depth+0.20
                        );
                }
            }

            translate([0, 0, flange_h])
                difference() {
                    cylinder(r=flange_spigot_outer_r, h=flange_spigot_h);
                    translate([0, 0, -0.10])
                        cylinder(
                            r=flange_spigot_inner_r,
                            h=flange_spigot_h+0.20
                        );
                }

            flange_screw_boss();
            flange_lug_root_reinforcements();
            flange_lugs();
        }

        flange_self_tap_pilot();
        flange_signature_cut();
    }
}

module grommet_reference() {
    difference() {
        linear_extrude(height=grommet_measured_h)
            aligned_grommet_profile_2d(
                grommet_measured_d,
                grommet_measured_flat_h-grommet_measured_d/2
            );
        translate([0, 0, -0.10])
            cylinder(d=7.00, h=grommet_measured_h+0.20);
    }
}

module installed_flange(rotation=assembly_lock_angle) {
    translate([0, 0, carrier_h+flange_h])
        rotate([0, 0, rotation])
            rotate([180, 0, 0])
                ceiling_flange();
}

module installed_assembly() {
    color("white")
        carrier();
    color("lightsteelblue")
        installed_flange();
    color("dimgray")
        translate([0, 0, grommet_pocket_bottom])
            grommet_reference();
}

if (part == "carrier")
    carrier();
else if (part == "flange")
    ceiling_flange();
else if (part == "grommet")
    grommet_reference();
else if (part == "carrier_signature_tool")
    carrier_signature_cut();
else if (part == "flange_signature_tool")
    flange_signature_cut();
else if (part == "section")
    intersection() {
        installed_assembly();
        translate([0, -outer_d, -1])
            cube([outer_d, 2*outer_d, carrier_h+flange_h+2]);
    }
else if (part == "interference")
    intersection() {
        carrier();
        installed_flange();
    }
else if (part == "insertion_interference")
    intersection() {
        carrier();
        installed_flange(rotation=0);
    }
else if (part == "grommet_interference")
    intersection() {
        carrier();
        translate([0, 0, grommet_pocket_bottom])
            grommet_reference();
    }
else
    installed_assembly();
