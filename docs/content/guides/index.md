# Guides

## Migration from varmgr

| Before (varmgr) | After (varstore) |
| --- | --- |
| `from lib.store import ...` | `from varstore import ...` |
| `VarMgrError` / `VarMgrAppError` / `VarMgrUserError` | `VarStoreError` / `VarStoreAppError` / `VarStoreUserError` |
| `pip install git+...python-expandvars@develop` | not needed — engine is vendored |

Behavior of sources, scopes, layers, priority, and expand syntax is unchanged.
