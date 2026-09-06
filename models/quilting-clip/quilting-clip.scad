/*
  Quilting clip / quilt-basting ring

  Print flat, as supplied: it needs no supports or bridges. PETG is the
  preferred material because the part must spring open repeatedly; use a
  generous wall count (4+ perimeters) and 100% infill.
*/

// [Overall size]
outer_diameter = 70;       // [50:0.5:100] Outside diameter (mm)
ring_wall = 3;             // [2.4:0.2:6] Width of the flexible spring band (mm)
clip_height = 10;          // [3:0.2:15] Height when printed flat (mm)
opening = 12;              // [6:0.5:22] Clear gap between the rounded tips (mm)
edge_chamfer = 0.5;        // [0:0.1:1.2] 45-degree chamfer on base and top (mm)

// [Quality]
facet_count = 120;         // [48:8:180] Higher = smoother circular edge

assert(outer_diameter > 2 * ring_wall, "ring_wall is too large");
assert(opening < outer_diameter - 2 * ring_wall,
       "opening leaves no material in the ring");
assert(2 * edge_chamfer < ring_wall,
       "edge_chamfer is too large for ring_wall");

outer_radius = outer_diameter / 2;
inner_radius = outer_radius - ring_wall;
band_mid_radius = (outer_radius + inner_radius) / 2;
tip_radius = ring_wall / 2;
cap_overlap = 0.25;       // Overlap of each end cap into the band (mm)

// Nominal tip centres; caps move slightly into the band to form one solid.
tip_y = opening / 2 + tip_radius;
tip_angle = asin(tip_y / band_mid_radius);
tip_x = band_mid_radius * cos(tip_angle);
end_angle = tip_angle + atan(cap_overlap / band_mid_radius);
wedge_extent = outer_radius + opening + ring_wall + 2;

// A 45-degree chamfered solid disk, used for both the ring and the end caps.
module chamfered_disk(radius, height, chamfer) {
    union() {
        cylinder(h = chamfer, r1 = radius - chamfer, r2 = radius,
                 $fn = facet_count);
        translate([0, 0, chamfer])
            cylinder(h = height - 2 * chamfer, r = radius, $fn = facet_count);
        translate([0, 0, height - chamfer])
            cylinder(h = chamfer, r1 = radius, r2 = radius - chamfer,
                     $fn = facet_count);
    }
}

// Hole with the inverse taper, leaving matching 45-degree inner edge chamfers.
module chamfered_hole(radius, height, chamfer) {
    translate([0, 0, -0.01])
        cylinder(h = chamfer + 0.01, r1 = radius + chamfer, r2 = radius,
                 $fn = facet_count);
    translate([0, 0, chamfer])
        cylinder(h = height - 2 * chamfer, r = radius, $fn = facet_count);
    translate([0, 0, height - chamfer])
        cylinder(h = chamfer + 0.01, r1 = radius, r2 = radius + chamfer,
                 $fn = facet_count);
}

module quilting_clip() {
    /*
      The annulus is opened by an angular wedge. Round, chamfered caps are
      then added at the ends, making a smooth circular end profile rather than
      a flat-cut tip. The base and top receive a 0.5 mm, 45-degree chamfer.
    */
    union() {
        difference() {
            difference() {
                chamfered_disk(outer_radius, clip_height, edge_chamfer);
                chamfered_hole(inner_radius, clip_height, edge_chamfer);
            }

            // Remove the sector at +X between the centres of the end caps.
            translate([0, 0, -0.1])
                linear_extrude(height = clip_height + 0.2)
                    polygon(points = [
                        [0, 0],
                        [wedge_extent * cos(-end_angle),
                         wedge_extent * sin(-end_angle)],
                        [wedge_extent * cos( end_angle),
                         wedge_extent * sin( end_angle)]
                    ]);
        }

        // Circular ends overlap the band slightly, avoiding a tangent-only joint.
        translate([tip_x - sin(tip_angle) * cap_overlap,
                   tip_y + cos(tip_angle) * cap_overlap, 0])
            chamfered_disk(tip_radius, clip_height, edge_chamfer);
        translate([tip_x - sin(tip_angle) * cap_overlap,
                  -tip_y - cos(tip_angle) * cap_overlap, 0])
            chamfered_disk(tip_radius, clip_height, edge_chamfer);

    }
}

quilting_clip();
