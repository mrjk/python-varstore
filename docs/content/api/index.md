# API

Install: `pip install mrjk.varstore`. Import package: `varstore`.

```python
from varstore import (
    StoreManager,
    RenderableStoreManager,
    Source,
    UndefinedVarError,
    TemplateRenderingCircularValueError,
)
from varstore.expand import expand, expandvars, ExpandParser
```

| Symbol | Role |
| --- | --- |
| `StoreManager` | Hierarchical store: sources, scopes, layers, raw lookup |
| `RenderableStoreManager` | Store plus template rendering |
| `Source` | Named source with priority `level` |
| `Renderer` / `RenderingSettings` | Per-scope rendering |
| `varstore.expand` | Standalone shell-style expansion |

`get_var_names` order is deterministic (alphabetical within each layer,
first-seen across priority layers). Same inputs yield the same list across runs.

See the repository README for migration from **varmgr** and inspection helpers (`inspect_var`, `show_sources_help`).
