# Architecture

**varstore** manages configuration variables across sources, scopes, and layers:

- **Sources** — named origins with numeric priority (`level`, lower = higher priority)
- **Scopes** — lists of sources (and nested scopes) to resolve against
- **Layers** — key/value payloads attached to a registered source
- **StoreManager** — raw storage (`get_value` / `get_values`; templates not expanded)
- **RenderableStoreManager** — same raw API, plus `get_renderer(scope).render_var(...)` / `render_values(...)`

Default template engine is shell expandvars (`$VAR` / `${VAR}`); alternate `py_stringtemplate` is available. The expand engine is vendored under `varstore.expand` (see `NOTICE` / `LICENSE.expandvars`).
