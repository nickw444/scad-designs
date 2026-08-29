OPENSCAD ?= $(shell command -v openscad 2>/dev/null || find /Applications -maxdepth 4 -type f -path '*/OpenSCAD*.app/Contents/MacOS/OpenSCAD' -print -quit 2>/dev/null)
PYTHON ?= python3
BUILD := build

UCG := models/ucg-ultra-4-keystone/ucg-ultra-4-keystone.scad
NBN := models/nbn-ntd-6-keystone/nbn-ntd-6-keystone.scad
PATCH := models/10-port-two-thirds-u-patch-panel/10-port-two-thirds-u-patch-panel.scad

OUTPUTS := \
	$(BUILD)/ucg-ultra-4-keystone.stl \
	$(BUILD)/nbn-ntd-6-keystone-panel.stl \
	$(BUILD)/nbn-ntd-6-keystone-labels.stl \
	$(BUILD)/10-port-two-thirds-u-panel.stl \
	$(BUILD)/10-port-two-thirds-u-labels.stl

.PHONY: all render validate clean check-openscad

all: validate

render: check-openscad $(OUTPUTS)

validate: render
	$(PYTHON) tools/stl_compare.py tests/reference/ucg-ultra-4-keystone.stl $(BUILD)/ucg-ultra-4-keystone.stl
	$(PYTHON) tools/stl_compare.py tests/reference/nbn-ntd-6-keystone-panel.stl $(BUILD)/nbn-ntd-6-keystone-panel.stl
	$(PYTHON) tools/stl_compare.py tests/reference/nbn-ntd-6-keystone-labels.stl $(BUILD)/nbn-ntd-6-keystone-labels.stl
	$(PYTHON) tools/stl_compare.py tests/reference/10-port-two-thirds-u-panel.stl $(BUILD)/10-port-two-thirds-u-panel.stl
	$(PYTHON) tools/stl_compare.py tests/reference/10-port-two-thirds-u-labels.stl $(BUILD)/10-port-two-thirds-u-labels.stl

check-openscad:
	@test -n "$(OPENSCAD)" || (echo "OpenSCAD was not found; set OPENSCAD=/path/to/OpenSCAD" >&2; exit 1)

$(BUILD):
	mkdir -p $@

$(BUILD)/ucg-ultra-4-keystone.stl: $(UCG) lib/rack/device_mount.scad | $(BUILD)
	"$(OPENSCAD)" -o $@ $<

$(BUILD)/nbn-ntd-6-keystone-panel.stl: $(NBN) lib/rack/device_mount.scad | $(BUILD)
	"$(OPENSCAD)" -D 'output_part="panel"' -o $@ $<

$(BUILD)/nbn-ntd-6-keystone-labels.stl: $(NBN) lib/rack/device_mount.scad | $(BUILD)
	"$(OPENSCAD)" -D 'output_part="labels"' -o $@ $<

$(BUILD)/10-port-two-thirds-u-panel.stl: $(PATCH) lib/rack/patch_panel.scad | $(BUILD)
	"$(OPENSCAD)" -D 'output_part="panel"' -o $@ $<

$(BUILD)/10-port-two-thirds-u-labels.stl: $(PATCH) lib/rack/patch_panel.scad | $(BUILD)
	"$(OPENSCAD)" -D 'output_part="labels"' -o $@ $<

clean:
	rm -f $(OUTPUTS)

