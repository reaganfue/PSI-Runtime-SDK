"""
PsiRuntimeSDK - 量子啟發式推理與語義場分析SDK

提供三個核心模組:
- logic_core: 基礎推理邏輯層
- psi_field: 語義場處理層 
- quantum_engine: 量子啟發式分析層
"""

from . import logic_core
from . import psi_field
from . import quantum_engine

# 方便直接導入的常用類
from .logic_core import BasicResponseLogic
from .psi_field import SemanticFieldEngine
from .quantum_engine import QuantumAnalyzer

__all__ = [
    'logic_core',
    'psi_field',
    'quantum_engine',
    'BasicResponseLogic',
    'SemanticFieldEngine',
    'QuantumAnalyzer'
]

__version__ = '0.1.0' 
