"""
PSI Runtime SDK - Enterprise Quantum-Inspired Reasoning Framework - L4 Enhanced

A cutting-edge framework with L4 (Level 4) meta-cognitive optimization that combines 
quantum-inspired reasoning and semantic field analysis technology for advanced 
human-computer collaborative reasoning with meta-cognitive capabilities.

L4 Features:
- Meta-cognitive reasoning optimization
- Cross-engine synchronization
- Adaptive confidence calibration
- Dynamic semantic field stability
- Quantum coherence optimization
"""

__version__ = "0.1.0-L4"
__author__ = "Reagan Fu"
__email__ = "reagan.fue@gmail.com"

# Import L4 enhanced components for easy access
from .logic_core import BasicResponseLogic
from .psi_field import L4SemanticFieldEngine as SemanticFieldEngine
from .quantum_engine import L4QuantumAnalyzer as QuantumAnalyzer

# Create L4 integrated analyzer
from .l4_integrated_analyzer import L4IntegratedAnalyzer

__all__ = [
    "BasicResponseLogic",
    "SemanticFieldEngine", 
    "QuantumAnalyzer",
    "L4IntegratedAnalyzer",
    "__version__",
]