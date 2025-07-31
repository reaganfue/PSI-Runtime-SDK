"""
PSI Runtime SDK - Enterprise Quantum-Inspired Reasoning Framework

A cutting-edge framework that combines quantum-inspired reasoning and semantic 
field analysis technology for advanced human-computer collaborative reasoning.
"""

__version__ = "0.1.0"
__author__ = "Reagan Fu"
__email__ = "reagan.fue@gmail.com"

# Import main components for easy access
from .logic_core import BasicResponseLogic
from .psi_field import SemanticFieldEngine, PsiFieldModel
from .quantum_engine import QuantumAnalyzer

__all__ = [
    "BasicResponseLogic",
    "SemanticFieldEngine", 
    "PsiFieldModel",
    "QuantumAnalyzer",
    "__version__",
]