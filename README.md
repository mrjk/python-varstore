# varstore

Hierarchical variable store with optional recursive shell-style template rendering.

Formerly **varmgr**. The expand engine from the [mrjk/python-expandvars](https://github.com/mrjk/python-expandvars) fork is **included** as batteries (`varstore.expand`) — no separate expandvars install is required.


## Table of Contents

- [Goal](#goal)
- [Install](#install)
- [Core concepts](#core-concepts)
- [Quickstart](#quickstart)
- [Template rendering](#template-rendering)
- [String-only expand API](#string-only-expand-api)
- [Inspection](#inspection)
- [Migration from varmgr](#migration-from-varmgr)
- [Development](#development)
- [Running tests](#running-tests)
- [Release](#release)


## Goal

**varstore** manages configuration variables across sources, scopes, and layers:

- Sources with numeric priority (`level`, lower = higher priority)
- Scopes listing sources and nested scopes
- Layers of key/value data per source
- Raw lookup (`StoreManager`) vs rendered lookup (`RenderableStoreManager`)
- Default template engine = shell expandvars (`$VAR` / `${VAR}`); alternate `py_stringtemplate` available


## Install

Python 3.10+. Zero hard runtime dependencies beyond the stdlib.

```bash
pip install mrjk.varstore
```

Import as `varstore`:

```python
from varstore import StoreManager, RenderableStoreManager, Source
```

Editable / from source:

```bash
mise trust && mise install
uv sync --all-groups
```


## Core concepts

### Sources

Named origins with optional priority `level` (lower = higher priority):

```python
Source("app_cli", level=300, help="Application main CLI")
Source("app_defaults", level=999, help="Application defaults")
```

### Scopes

Scopes list sources (and other scopes) to resolve against:

```python
store.set_scopes({
    "scope_app": ["app_cli", "app_env", "app_defaults"],
    "scope_project": ["project_cli", "project_env", "project_defaults", "scope_app"],
})
```

### Layers

Key/value payloads attached to a registered source:

```python
store.set_layer("app_cli", {"app_name": "myapp", "debug": True})
```

### Resolution APIs

1. **`StoreManager`** — raw storage: `get_value` / `get_values` return stored values as-is (templates are **not** expanded).
2. **`RenderableStoreManager`** — same raw API, plus `get_renderer(scope).render_var(...)` / `render_values(...)` for expansion.


## Quickstart

```python
from varstore import StoreManager, Source

store = StoreManager()

store.add_sources([
    Source("app_cli", level=300, help="Application main CLI"),
    Source("app_env", level=300, help="Application environment variables"),
    Source("app_defaults", level=999, help="Application defaults"),
])

store.set_scopes({
    "scope_app": ["app_cli", "app_env", "app_defaults"],
})

store.set_layer("app_cli", {
    "app_name": "myapp",
    "debug": True,
})

app_name = store.get_value("app_name")  # "myapp"
```


## Template rendering

`get_value` always returns the **raw** stored value. Use a `Renderer` to expand templates.

```python
from varstore import RenderableStoreManager, Source

store = RenderableStoreManager()

# ... add_sources / set_scopes ...

store.set_layer("project_env", {
    "project_name": "myproject",
    "env": "prod",
    "stack_name": "${project_name}-${env}",
})

assert store.get_value("stack_name") == "${project_name}-${env}"

renderer = store.get_renderer(scope_name="scope_project")
assert renderer.render_var("stack_name") == "myproject-prod"

values = renderer.render_values()
```

Default engine is **expandvars** (shell-style). Alternate Python `string.Template`:

```python
renderer = store.get_renderer(scope_name="scope_project", engine="py_stringtemplate")
```

Circular references raise `TemplateRenderingCircularValueError`. Undefined vars raise `UndefinedVarError` (customizable via render settings).


## String-only expand API

For expansion without a store:

```python
from varstore.expand import expand, expandvars, ExpandParser

expandvars("$HOME/bin")
expand("${FOO:-default}", environ={"FOO": "bar"})
ExpandParser(environ={"PATH": "/usr/bin"}).expand("$PATH:/opt/bin")
```


## Inspection

```python
store.show_sources_help()
layers = store.inspect_var("log_level", scope="scope_project")
names = store.get_source_names(scope="scope_stack")
value, report = renderer.render_var("stack_name", debug=True)
```

### Variable process order

`get_var_names` returns a **deterministic** list: keys are sorted alphabetically
within each layer, and names are first-seen across layers in
`get_ordered_layers` priority order. The result is a concatenation of those
per-layer alpha slices. It is stable across processes (not affected by
`PYTHONHASHSEED`). Value / merge priority is unchanged. This is process /
enumeration order, not template dependency order.


## Migration from varmgr

| Before (varmgr) | After (varstore) |
|-----------------|------------------|
| `from lib.store import ...` | `from varstore import ...` |
| `VarMgrError` / `VarMgrAppError` / `VarMgrUserError` | `VarStoreError` / `VarStoreAppError` / `VarStoreUserError` |
| `pip install git+...python-expandvars@develop` | not needed — engine is vendored |

Behavior of sources, scopes, layers, priority, and expand syntax is unchanged.


## Development

```bash
mise trust && mise install
uv sync --all-groups
```

With mise activated, `task` and `uv` are on your `PATH`. After `uv sync`, project tools live in `.venv`.

```bash
task               # list root tasks
task test_core     # unit + coverage + lint (no docs)
task test          # full CI gate (core + docs)
task fix_lint      # auto-fix formatters
task docs          # serve docs (Zensical)
```

More targets: `cd ci && task`, `cd docs && task`.


## Running tests

```bash
task test_core
# or
uv run pytest
```


## Release

```bash
./scripts/release.sh patch   # bump, commit, tag
git push && git push --tags
```

Tag push `v*` triggers PyPI publish (configure Trusted Publishing / `pypi` environment). Docs: [Zensical](https://zensical.org/) under `docs/` (`task docs`).
