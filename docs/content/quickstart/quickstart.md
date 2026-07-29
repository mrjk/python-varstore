# Quickstart

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

`get_value` returns the **raw** stored value. Use a `Renderer` to expand templates.

```python
from varstore import RenderableStoreManager

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
```

Default engine is **expandvars** (shell-style). Alternate: `engine="py_stringtemplate"`.

## String-only expand

```python
from varstore.expand import expand, expandvars, ExpandParser

expandvars("$HOME/bin")
expand("${FOO:-default}", environ={"FOO": "bar"})
```
