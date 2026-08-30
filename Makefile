OPENSCAD ?= $(shell command -v openscad 2>/dev/null || find /Applications -maxdepth 4 -type f -path '*/OpenSCAD*.app/Contents/MacOS/OpenSCAD' -print -quit 2>/dev/null)
PREVIEW_SIZE ?= 800,600
PREVIEW_FLAGS := --imgsize=$(PREVIEW_SIZE) --autocenter --viewall --projection=o --colorscheme="Tomorrow Night"
RACK_DIR := models/10-inch-rack
RACK_SHARED := $(RACK_DIR)/device-mount.scad
UCG_DIR := $(RACK_DIR)/ucg-ultra-4-keystone
UCG := $(UCG_DIR)/ucg-ultra-4-keystone.scad
NBN_DIR := $(RACK_DIR)/nbn-ntd
NBN_NO_KEYSTONE := $(NBN_DIR)/nbn-ntd-no-keystone.scad
NBN_1_KEYSTONE := $(NBN_DIR)/nbn-ntd-1-keystone.scad
NBN_4_KEYSTONE := $(NBN_DIR)/nbn-ntd-4-keystone.scad
NBN_6_KEYSTONE := $(NBN_DIR)/nbn-ntd-6-keystone.scad
PATCH_DIR := $(RACK_DIR)/10-port-two-thirds-u-patch-panel
PATCH := $(PATCH_DIR)/10-port-two-thirds-u-patch-panel.scad
PATCH_LIB := $(PATCH_DIR)/patch-panel.scad
SOUS_VIDE_DIR := models/sous-vide-pot-lid
SOUS_VIDE := $(SOUS_VIDE_DIR)/sous-vide-pot-lid.scad
STITCH_LIB := models/stitch-guides/stitch-guides.scad
STITCH_DIR := models/stitch-guides
UNIFI_DIR := models/unifi-g5-ptz-soffit-mount
UNIFI := $(UNIFI_DIR)/unifi-g5-ptz-soffit-mount.scad
TESLA_HOOK_DIR := models/tesla-hook
TESLA_HOOK := $(TESLA_HOOK_DIR)/tesla-hook.scad
TESLA_HOOK_SOURCE := $(TESLA_HOOK_DIR)/source/tesla-hook-arms.stl

BUILD_DIRS := \
	$(UCG_DIR)/build \
	$(NBN_DIR)/build \
	$(PATCH_DIR)/build \
	$(SOUS_VIDE_DIR)/build \
	$(STITCH_DIR)/build \
	$(UNIFI_DIR)/build \
	$(TESLA_HOOK_DIR)/build

OUTPUTS := \
	$(UCG_DIR)/build/ucg-ultra-4-keystone.stl \
	$(NBN_DIR)/build/nbn-ntd-6-keystone.stl \
	$(NBN_DIR)/build/nbn-ntd-no-keystone.stl \
	$(NBN_DIR)/build/nbn-ntd-1-keystone.stl \
	$(NBN_DIR)/build/nbn-ntd-4-keystone.stl \
	$(PATCH_DIR)/build/10-port-two-thirds-u-panel.stl \
	$(PATCH_DIR)/build/10-port-two-thirds-u-labels.stl \
	$(SOUS_VIDE_DIR)/build/sous-vide-pot-lid.stl \
	$(STITCH_DIR)/build/stitch-guide-bow.stl \
	$(STITCH_DIR)/build/stitch-guide-tails.stl \
	$(STITCH_DIR)/build/stitch-guide-knot.stl \
	$(STITCH_DIR)/build/stitch-guide-rectangle-3.5x3.stl \
	$(UNIFI_DIR)/build/unifi-g5-ptz-carrier.stl \
	$(UNIFI_DIR)/build/unifi-g5-ptz-carrier-plus15mm.stl \
	$(UNIFI_DIR)/build/unifi-g5-ptz-carrier-plus30mm.stl \
	$(UNIFI_DIR)/build/unifi-g5-ptz-ceiling-flange.stl \
	$(TESLA_HOOK_DIR)/build/tesla-hook-m6-nut.stl

PREVIEWS := \
	$(UCG_DIR)/preview.png \
	$(NBN_DIR)/preview-no-keystone.png \
	$(NBN_DIR)/preview-1-keystone.png \
	$(NBN_DIR)/preview-4-keystone.png \
	$(NBN_DIR)/preview-6-keystone.png \
	$(PATCH_DIR)/preview.png \
	$(SOUS_VIDE_DIR)/preview.png \
	$(STITCH_DIR)/preview-bow.png \
	$(STITCH_DIR)/preview-tails.png \
	$(STITCH_DIR)/preview-knot.png \
	$(STITCH_DIR)/preview-rectangle-3.5x3.png \
	$(UNIFI_DIR)/preview.png \
	$(TESLA_HOOK_DIR)/preview.png

.PHONY: all render preview clean check-openscad

all: render preview

render: check-openscad $(OUTPUTS)

preview: check-openscad $(PREVIEWS)

check-openscad:
	@test -n "$(OPENSCAD)" || (echo "OpenSCAD was not found; set OPENSCAD=/path/to/OpenSCAD" >&2; exit 1)

$(BUILD_DIRS):
	mkdir -p $@

$(UCG_DIR)/build/ucg-ultra-4-keystone.stl: $(UCG) $(RACK_SHARED) | $(UCG_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(NBN_DIR)/build/nbn-ntd-6-keystone.stl: $(NBN_6_KEYSTONE) $(RACK_SHARED) | $(NBN_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(NBN_DIR)/build/nbn-ntd-no-keystone.stl: $(NBN_NO_KEYSTONE) $(RACK_SHARED) | $(NBN_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(NBN_DIR)/build/nbn-ntd-1-keystone.stl: $(NBN_1_KEYSTONE) $(RACK_SHARED) | $(NBN_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(NBN_DIR)/build/nbn-ntd-4-keystone.stl: $(NBN_4_KEYSTONE) $(RACK_SHARED) | $(NBN_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(PATCH_DIR)/build/10-port-two-thirds-u-panel.stl: $(PATCH) $(PATCH_LIB) | $(PATCH_DIR)/build
	"$(OPENSCAD)" -D 'output_part="panel"' -o $@ $<

$(PATCH_DIR)/build/10-port-two-thirds-u-labels.stl: $(PATCH) $(PATCH_LIB) | $(PATCH_DIR)/build
	"$(OPENSCAD)" -D 'output_part="labels"' -o $@ $<

$(SOUS_VIDE_DIR)/build/sous-vide-pot-lid.stl: $(SOUS_VIDE) | $(SOUS_VIDE_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(STITCH_DIR)/build/stitch-guide-bow.stl: $(STITCH_DIR)/bow.scad $(STITCH_LIB) | $(STITCH_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(STITCH_DIR)/build/stitch-guide-tails.stl: $(STITCH_DIR)/tails.scad $(STITCH_LIB) | $(STITCH_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(STITCH_DIR)/build/stitch-guide-knot.stl: $(STITCH_DIR)/knot.scad $(STITCH_LIB) | $(STITCH_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(STITCH_DIR)/build/stitch-guide-rectangle-3.5x3.stl: $(STITCH_DIR)/rectangle-3.5x3.scad $(STITCH_LIB) | $(STITCH_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(UNIFI_DIR)/build/unifi-g5-ptz-carrier.stl: $(UNIFI) | $(UNIFI_DIR)/build
	"$(OPENSCAD)" -D 'part="carrier"' -o $@ $<

$(UNIFI_DIR)/build/unifi-g5-ptz-carrier-plus15mm.stl: $(UNIFI) | $(UNIFI_DIR)/build
	"$(OPENSCAD)" -D 'carrier_extension=15' -D 'part="carrier"' -o $@ $<

$(UNIFI_DIR)/build/unifi-g5-ptz-carrier-plus30mm.stl: $(UNIFI) | $(UNIFI_DIR)/build
	"$(OPENSCAD)" -D 'carrier_extension=30' -D 'part="carrier"' -o $@ $<

$(UNIFI_DIR)/build/unifi-g5-ptz-ceiling-flange.stl: $(UNIFI) | $(UNIFI_DIR)/build
	"$(OPENSCAD)" -D 'part="flange"' -o $@ $<

$(TESLA_HOOK_DIR)/build/tesla-hook-m6-nut.stl: $(TESLA_HOOK) $(TESLA_HOOK_SOURCE) | $(TESLA_HOOK_DIR)/build
	"$(OPENSCAD)" -o $@ $<

$(UCG_DIR)/preview.png: $(UCG) $(RACK_SHARED)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(NBN_DIR)/preview-6-keystone.png: $(NBN_6_KEYSTONE) $(RACK_SHARED)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(NBN_DIR)/preview-no-keystone.png: $(NBN_NO_KEYSTONE) $(RACK_SHARED)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(NBN_DIR)/preview-1-keystone.png: $(NBN_1_KEYSTONE) $(RACK_SHARED)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(NBN_DIR)/preview-4-keystone.png: $(NBN_4_KEYSTONE) $(RACK_SHARED)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(PATCH_DIR)/preview.png: $(PATCH) $(PATCH_LIB)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(SOUS_VIDE_DIR)/preview.png: $(SOUS_VIDE)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(STITCH_DIR)/preview-bow.png: $(STITCH_DIR)/bow.scad $(STITCH_LIB)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(STITCH_DIR)/preview-tails.png: $(STITCH_DIR)/tails.scad $(STITCH_LIB)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(STITCH_DIR)/preview-knot.png: $(STITCH_DIR)/knot.scad $(STITCH_LIB)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(STITCH_DIR)/preview-rectangle-3.5x3.png: $(STITCH_DIR)/rectangle-3.5x3.scad $(STITCH_LIB)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(UNIFI_DIR)/preview.png: $(UNIFI)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

$(TESLA_HOOK_DIR)/preview.png: $(TESLA_HOOK) $(TESLA_HOOK_SOURCE)
	"$(OPENSCAD)" $(PREVIEW_FLAGS) -o $@ $<

clean:
	rm -f $(OUTPUTS) $(PREVIEWS)
