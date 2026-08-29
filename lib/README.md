# Reusable OpenSCAD code

Libraries should contain modules, functions, and shared geometry—not project-specific measured dimensions. Group them by domain (`rack`, `fasteners`, `enclosures`, and so on) once a second real consumer exists; avoid a single catch-all utilities file.

Prefer `use` for self-contained modules. Use `include` only when a module intentionally consumes parameters owned by its model entry point, as the two focused cradle designs currently do. Libraries must not render automatically; each model entry point owns the preview orientation and calls one public module.
