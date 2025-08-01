"""
Quantum Engine 模組 - 量子啟發式分析層 - L4 Enhanced

提供L4級別的量子啟發式推理與人機語意融合邏輯。
包含元認知優化、量子相干性優化和跨引擎同步功能。
"""

# L4 Enhanced Quantum Analyzer
from .l4_quantum_analyzer import (
    L4QuantumAnalyzer,
    L4QuantumConfig,
    QuantumState,
    L4QuantumResult,
    create_l4_quantum_analyzer
)

# Legacy compatibility
from .quantum_analyzer_engine import (
    QuantumAnalyzer,
    Config,
    DataParser,
    QueryEngine,
    ReportGenerator
)

# Prefer L4 implementations
QuantumAnalyzer = L4QuantumAnalyzer
Config = L4QuantumConfig

__all__ = [
    # L4 Enhanced exports
    'L4QuantumAnalyzer',
    'L4QuantumConfig', 
    'QuantumState',
    'L4QuantumResult',
    'create_l4_quantum_analyzer',
    
    # Legacy compatibility exports
    'QuantumAnalyzer',
    'Config',
    'DataParser',
    'QueryEngine',
    'ReportGenerator'
]
