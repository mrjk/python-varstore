"""varstore — hierarchical variable store with shell-style template rendering.

Public API for consumers (including future Paasify integration)::

    from varstore import StoreManager, RenderableStoreManager, Source
    from varstore import UndefinedVarError
    from varstore.expand import expand, expandvars, ExpandParser
"""

from .core_engine import (
    InvalidTemplateVarNameError,
    StoreTemplateError,
    TemplateEngineError,
    TemplateKeyError,
    TemplateRenderingCircularValueError,
    TemplateRenderingError,
    TemplateValueError,
)
from .store_base import (
    AlreadyExistingSourceError,
    InvalidVarNameError,
    Layer,
    ReferenceToMissingSourceError,
    Scope,
    Source,
    StoreManager,
    UndefinedVarError,
    VarStoreAppError,
    VarStoreError,
    VarStoreUserError,
)
from .store_template import RenderableStoreManager, Renderer, RenderingSettings

__version__ = "0.1.0"

__all__ = [
    "AlreadyExistingSourceError",
    "InvalidTemplateVarNameError",
    "InvalidVarNameError",
    "Layer",
    "ReferenceToMissingSourceError",
    "RenderableStoreManager",
    "Renderer",
    "RenderingSettings",
    "Scope",
    "Source",
    "StoreManager",
    "StoreTemplateError",
    "TemplateEngineError",
    "TemplateKeyError",
    "TemplateRenderingCircularValueError",
    "TemplateRenderingError",
    "TemplateValueError",
    "UndefinedVarError",
    "VarStoreAppError",
    "VarStoreError",
    "VarStoreUserError",
    "__version__",
]
