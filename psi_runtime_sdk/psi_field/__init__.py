"""
PSI Field 模組 - 語義場處理層 - L4 Enhanced

提供L4級別的語境場動態解鎖、知識錨定與語義張力分析。
包含元認知優化、適應性知識解鎖和跨引擎同步功能。
"""

# L4 Enhanced Semantic Field Engine
from .l4_semantic_field_engine import (
    L4SemanticFieldEngine,
    L4PsiFieldConfig,
    L4KnowledgeAnchor,
    L4SemanticFieldContext,
    L4PsiFieldResult,
    create_l4_semantic_field_engine
)

# Legacy compatibility
from .transient_judgment_of_semantic_field import (
    SemanticFieldEngine,
    FieldConfig,
    DataParser,
    SemanticInput,
    KnowledgeAnchor,
    PsiFieldModel,
    SemanticFieldContext
)

# Prefer L4 implementations
SemanticFieldEngine = L4SemanticFieldEngine
FieldConfig = L4PsiFieldConfig

__all__ = [
    # L4 Enhanced exports
    'L4SemanticFieldEngine',
    'L4PsiFieldConfig',
    'L4KnowledgeAnchor', 
    'L4SemanticFieldContext',
    'L4PsiFieldResult',
    'create_l4_semantic_field_engine',
    
    # Legacy compatibility exports
    'SemanticFieldEngine',
    'FieldConfig', 
    'DataParser',
    'SemanticInput',
    'KnowledgeAnchor',
    'PsiFieldModel',
    'SemanticFieldContext'
]
