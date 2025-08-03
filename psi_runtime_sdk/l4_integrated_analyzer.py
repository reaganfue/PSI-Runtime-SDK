#!/usr/bin/env python
# coding: utf-8

"""
L4 Integrated Analyzer - Meta-Cognitive Cross-Engine Integration

This module implements the L4 (Level 4) integrated analyzer that combines all three
core engines (Logic Core, Quantum Engine, PSI Field Engine) with meta-cognitive
optimization and cross-engine synchronization capabilities.

L4 Integration Features:
- Meta-cognitive cross-engine reasoning
- Adaptive confidence calibration across engines
- Dynamic engine weight optimization
- Holistic semantic-quantum coherence
- Advanced error handling and recovery
- Real-time performance optimization
"""

from __future__ import annotations
import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from .logic_core import BasicResponseLogic, Config as LogicCoreConfig
from .quantum_engine import L4QuantumAnalyzer, L4QuantumConfig  
from .psi_field import L4SemanticFieldEngine, L4PsiFieldConfig

# Setup logging
logger = logging.getLogger(__name__)


@dataclass
class L4IntegratedConfig:
    """L4 Integrated Analyzer Configuration."""
    
    # Engine configurations
    logic_config: Optional[LogicCoreConfig] = None
    quantum_config: Optional[L4QuantumConfig] = None
    field_config: Optional[L4PsiFieldConfig] = None
    
    # L4 integration parameters
    l4_integration_enabled: bool = True
    cross_engine_synchronization: bool = True
    adaptive_engine_weighting: bool = True
    meta_cognitive_optimization: bool = True
    
    # Engine weights (adaptive if enabled)
    logic_weight: float = 0.4
    quantum_weight: float = 0.3
    field_weight: float = 0.3
    
    # L4 meta-cognitive thresholds
    confidence_threshold: float = 0.8
    coherence_threshold: float = 0.75
    stability_threshold: float = 0.8
    integration_threshold: float = 0.85
    
    # Performance optimization
    parallel_processing: bool = False  # Future feature
    caching_enabled: bool = True
    error_recovery_enabled: bool = True
    
    # Debugging and monitoring
    log_level: str = "INFO"
    debug_integration: bool = False
    save_integration_history: bool = True


@dataclass
class L4IntegratedResult:
    """L4 Integrated Analysis Result combining all engines."""
    
    session_id: str
    query: str
    
    # Integrated scores
    confidence: float
    integrated_score: float
    l4_meta_score: float
    
    # Engine-specific results
    logic_result: Dict[str, Any]
    quantum_result: Dict[str, Any] 
    field_result: Dict[str, Any]
    
    # L4 integration metrics
    cross_engine_harmony: float
    coherence_score: float
    stability_index: float
    adaptation_score: float
    
    # Engine weights used
    engine_weights: Dict[str, float] = field(default_factory=dict)
    
    # Meta-cognitive insights
    reasoning_path: List[str] = field(default_factory=list)
    confidence_calibration: Dict[str, float] = field(default_factory=dict)
    optimization_applied: List[str] = field(default_factory=list)
    
    # Performance metrics
    processing_time: float = 0.0
    engine_timings: Dict[str, float] = field(default_factory=dict)
    
    # Status
    status: str = "success"
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class L4CrossEngineOptimizer:
    """L4 Cross-Engine Optimization and Synchronization."""
    
    def __init__(self, config: L4IntegratedConfig):
        self.config = config
        self.performance_history: List[Dict] = []
        self.optimal_weights: Dict[str, float] = {
            "logic": config.logic_weight,
            "quantum": config.quantum_weight,
            "field": config.field_weight
        }
        
    def optimize_engine_weights(self, results: Dict[str, Dict], query_complexity: float) -> Dict[str, float]:
        """Optimize engine weights based on performance and query characteristics."""
        if not self.config.adaptive_engine_weighting:
            return self.optimal_weights.copy()
        
        # Base weights
        weights = self.optimal_weights.copy()
        
        # Adjust based on engine performance
        logic_confidence = results.get('logic', {}).get('confidence', 0.5)
        quantum_confidence = results.get('quantum', {}).get('confidence', 0.5)
        field_stability = results.get('field', {}).get('field_stability', 0.5)
        
        # Performance-based adjustment
        performance_scores = {
            "logic": logic_confidence,
            "quantum": quantum_confidence,
            "field": field_stability
        }
        
        # Query complexity adjustment
        if query_complexity > 0.8:  # Complex queries favor quantum and field
            weights["quantum"] *= 1.2
            weights["field"] *= 1.1
            weights["logic"] *= 0.9
        elif query_complexity < 0.3:  # Simple queries favor logic
            weights["logic"] *= 1.2
            weights["quantum"] *= 0.9
            weights["field"] *= 0.9
        
        # Performance boost for well-performing engines
        total_performance = sum(performance_scores.values())
        if total_performance > 0:
            for engine, score in performance_scores.items():
                if score > 0.8:  # High performance
                    weights[engine] *= (1 + score * 0.1)
                elif score < 0.4:  # Low performance
                    weights[engine] *= (1 - (1 - score) * 0.1)
        
        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v / total_weight for k, v in weights.items()}
        
        # Update optimal weights for learning
        self._update_optimal_weights(weights, performance_scores)
        
        return weights
    
    def calculate_cross_engine_harmony(self, results: Dict[str, Dict]) -> float:
        """Calculate harmony/consistency across engines."""
        confidences = []
        
        # Extract confidence-like scores from each engine
        if 'logic' in results:
            confidences.append(results['logic'].get('confidence', 0.5))
        if 'quantum' in results:
            confidences.append(results['quantum'].get('confidence', 0.5))
        if 'field' in results:
            confidences.append(results['field'].get('field_stability', 0.5))
        
        if len(confidences) < 2:
            return 0.5
        
        # Harmony based on consistency (low variance = high harmony)
        mean_confidence = np.mean(confidences)
        variance = np.var(confidences)
        harmony = mean_confidence * (1.0 - variance)
        
        return max(0.0, min(1.0, harmony))
    
    def synchronize_engines(self, results: Dict[str, Dict]) -> Dict[str, Dict]:
        """Apply cross-engine synchronization optimizations."""
        if not self.config.cross_engine_synchronization:
            return results
        
        # Extract shared context for synchronization
        shared_context = self._extract_shared_context(results)
        
        # Apply synchronization to each engine result
        synchronized_results = {}
        
        for engine_name, result in results.items():
            sync_result = result.copy()
            
            # Apply cross-engine confidence boost
            cross_boost = self._calculate_cross_engine_boost(result, shared_context)
            if 'confidence' in sync_result:
                sync_result['confidence'] = min(1.0, sync_result['confidence'] + cross_boost)
            
            # Add cross-engine context
            sync_result['cross_engine_context'] = shared_context
            sync_result['synchronization_applied'] = True
            
            synchronized_results[engine_name] = sync_result
        
        return synchronized_results
    
    def _extract_shared_context(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """Extract shared context across engines for synchronization."""
        shared = {}
        
        # Aggregate confidence scores
        confidences = []
        for result in results.values():
            if 'confidence' in result:
                confidences.append(result['confidence'])
        
        if confidences:
            shared['avg_confidence'] = np.mean(confidences)
            shared['confidence_consistency'] = 1.0 - np.std(confidences)
        
        # Aggregate processing times
        processing_times = []
        for result in results.values():
            if 'processing_time' in result:
                processing_times.append(result['processing_time'])
        
        if processing_times:
            shared['avg_processing_time'] = np.mean(processing_times)
        
        # Add optimization indicators
        optimizations = set()
        for result in results.values():
            if 'l4_optimizations_applied' in result:
                optimizations.update(result['l4_optimizations_applied'])
        
        shared['applied_optimizations'] = list(optimizations)
        
        return shared
    
    def _calculate_cross_engine_boost(self, result: Dict, shared_context: Dict) -> float:
        """Calculate confidence boost from cross-engine agreement."""
        confidence_consistency = shared_context.get('confidence_consistency', 0.5)
        avg_confidence = shared_context.get('avg_confidence', 0.5)
        
        # Boost based on consistency and overall performance
        base_boost = confidence_consistency * 0.1  # Max 10% boost
        performance_boost = (avg_confidence - 0.5) * 0.05  # Additional boost for high avg
        
        return max(0.0, min(0.15, base_boost + performance_boost))  # Max 15% total boost
    
    def _update_optimal_weights(self, current_weights: Dict[str, float], performance_scores: Dict[str, float]):
        """Update optimal weights based on performance feedback."""
        learning_rate = 0.05  # Conservative learning
        
        total_performance = sum(performance_scores.values())
        if total_performance > 0:
            for engine in self.optimal_weights:
                if engine in performance_scores and engine in current_weights:
                    performance_ratio = performance_scores[engine] / total_performance
                    weight_adjustment = (performance_ratio - 1/3) * learning_rate  # 1/3 = equal weight
                    self.optimal_weights[engine] += weight_adjustment
        
        # Normalize optimal weights
        total_optimal = sum(self.optimal_weights.values())
        if total_optimal > 0:
            self.optimal_weights = {k: v / total_optimal for k, v in self.optimal_weights.items()}


class L4MetaCognitiveProcessor:
    """L4 Meta-Cognitive Processing and Calibration."""
    
    def __init__(self, config: L4IntegratedConfig):
        self.config = config
        self.calibration_history: List[Dict] = []
        
    def apply_meta_cognitive_optimization(self, results: Dict[str, Dict], query: str) -> Dict[str, Any]:
        """Apply L4 meta-cognitive optimization to integrated results."""
        if not self.config.meta_cognitive_optimization:
            return self._basic_integration(results)
        
        # Calculate query complexity for context
        query_complexity = self._analyze_query_complexity(query)
        
        # Apply meta-cognitive confidence calibration
        calibrated_results = self._calibrate_confidence_scores(results, query_complexity)
        
        # Generate meta-cognitive insights
        meta_insights = self._generate_meta_insights(calibrated_results, query)
        
        # Calculate L4 meta-score
        l4_meta_score = self._calculate_l4_meta_score(calibrated_results, meta_insights)
        
        return {
            "calibrated_results": calibrated_results,
            "meta_insights": meta_insights,
            "l4_meta_score": l4_meta_score,
            "query_complexity": query_complexity
        }
    
    def _analyze_query_complexity(self, query: str) -> float:
        """Analyze query complexity for meta-cognitive processing."""
        # Basic complexity metrics
        word_count = len(query.split())
        unique_words = len(set(query.lower().split()))
        avg_word_length = np.mean([len(word) for word in query.split()])
        
        # Complexity indicators
        question_marks = query.count('?')
        complex_words = sum(1 for word in query.split() if len(word) > 8)
        
        # Normalize complexity score
        complexity = (
            min(1.0, word_count / 50.0) * 0.3 +  # Length factor
            min(1.0, unique_words / word_count) * 0.3 +  # Vocabulary diversity
            min(1.0, avg_word_length / 10.0) * 0.2 +  # Word complexity
            min(1.0, (question_marks + complex_words) / 5.0) * 0.2  # Structure complexity
        )
        
        return max(0.0, min(1.0, complexity))
    
    def _calibrate_confidence_scores(self, results: Dict[str, Dict], query_complexity: float) -> Dict[str, Dict]:
        """Apply meta-cognitive confidence calibration."""
        calibrated = {}
        
        for engine_name, result in results.items():
            calibrated_result = result.copy()
            
            if 'confidence' in result:
                original_confidence = result['confidence']
                
                # Apply complexity-based calibration
                complexity_factor = 1.0 - (query_complexity * 0.2)  # Reduce confidence for complex queries
                
                # Apply historical calibration if available
                historical_factor = self._get_historical_calibration_factor(engine_name)
                
                # Combine calibration factors
                calibrated_confidence = original_confidence * complexity_factor * historical_factor
                calibrated_confidence = max(0.0, min(1.0, calibrated_confidence))
                
                calibrated_result['confidence'] = calibrated_confidence
                calibrated_result['confidence_calibration'] = {
                    'original': original_confidence,
                    'complexity_factor': complexity_factor,
                    'historical_factor': historical_factor,
                    'calibrated': calibrated_confidence
                }
            
            calibrated[engine_name] = calibrated_result
        
        return calibrated
    
    def _generate_meta_insights(self, results: Dict[str, Dict], query: str) -> Dict[str, Any]:
        """Generate meta-cognitive insights from integrated analysis."""
        insights = {}
        
        # Engine agreement analysis
        confidences = [r.get('confidence', 0.5) for r in results.values()]
        insights['engine_agreement'] = 1.0 - np.std(confidences) if len(confidences) > 1 else 1.0
        
        # Processing efficiency analysis
        times = [r.get('processing_time', 0.1) for r in results.values()]
        insights['processing_efficiency'] = 1.0 / (1.0 + np.mean(times))
        
        # Optimization effectiveness
        all_optimizations = set()
        for result in results.values():
            if 'l4_optimizations_applied' in result:
                all_optimizations.update(result['l4_optimizations_applied'])
        
        insights['optimization_coverage'] = len(all_optimizations) / 10.0  # Normalize by expected max
        insights['optimizations_applied'] = list(all_optimizations)
        
        # Reasoning depth analysis
        reasoning_depths = []
        for result in results.values():
            if 'reasoning_path' in result:
                reasoning_depths.append(len(result['reasoning_path']))
            elif 'evolution_path' in result:
                reasoning_depths.append(len(result['evolution_path']))
        
        if reasoning_depths:
            insights['avg_reasoning_depth'] = np.mean(reasoning_depths)
            insights['reasoning_consistency'] = 1.0 - np.std(reasoning_depths) / max(reasoning_depths)
        
        return insights
    
    def _calculate_l4_meta_score(self, results: Dict[str, Dict], meta_insights: Dict[str, Any]) -> float:
        """Calculate L4 meta-cognitive score."""
        # Base score from average confidence
        confidences = [r.get('confidence', 0.5) for r in results.values()]
        base_score = np.mean(confidences) if confidences else 0.5
        
        # Meta-cognitive enhancements
        agreement_boost = meta_insights.get('engine_agreement', 0.5) * 0.2
        efficiency_boost = meta_insights.get('processing_efficiency', 0.5) * 0.1
        optimization_boost = meta_insights.get('optimization_coverage', 0.5) * 0.15
        reasoning_boost = meta_insights.get('reasoning_consistency', 0.5) * 0.1
        
        # L4 meta-score formula
        l4_score = base_score + agreement_boost + efficiency_boost + optimization_boost + reasoning_boost
        
        return max(0.0, min(1.0, l4_score))
    
    def _get_historical_calibration_factor(self, engine_name: str) -> float:
        """Get historical calibration factor for engine."""
        if not self.calibration_history:
            return 1.0
        
        # Find recent calibrations for this engine
        recent_calibrations = []
        for record in self.calibration_history[-10:]:  # Last 10 records
            if engine_name in record:
                recent_calibrations.append(record[engine_name])
        
        if not recent_calibrations:
            return 1.0
        
        # Calculate adjustment based on historical accuracy
        avg_accuracy = np.mean(recent_calibrations)
        if avg_accuracy > 0.8:
            return 1.05  # Slight boost for consistently high performance
        elif avg_accuracy < 0.6:
            return 0.95  # Slight reduction for consistently low performance
        else:
            return 1.0
    
    def _basic_integration(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """Basic integration fallback when meta-cognitive optimization is disabled."""
        confidences = [r.get('confidence', 0.5) for r in results.values()]
        return {
            "calibrated_results": results,
            "meta_insights": {"basic_integration": True},
            "l4_meta_score": np.mean(confidences) if confidences else 0.5,
            "query_complexity": 0.5
        }


class L4IntegratedAnalyzer:
    """L4 Meta-Cognitive Integrated Analyzer - Enterprise Grade."""
    
    def __init__(self, config: Optional[L4IntegratedConfig] = None):
        """Initialize L4 Integrated Analyzer."""
        self.config = config or L4IntegratedConfig()
        
        # Initialize engines with their configs
        logic_config = self.config.logic_config or LogicCoreConfig()
        quantum_config = self.config.quantum_config or L4QuantumConfig()
        field_config = self.config.field_config or L4PsiFieldConfig()
        
        self.logic_engine = BasicResponseLogic(logic_config)
        self.quantum_engine = L4QuantumAnalyzer(quantum_config)
        self.field_engine = L4SemanticFieldEngine(field_config)
        
        # Initialize L4 optimizers
        self.cross_engine_optimizer = L4CrossEngineOptimizer(self.config)
        self.meta_cognitive_processor = L4MetaCognitiveProcessor(self.config)
        
        # Analysis history for learning
        self.analysis_history: List[L4IntegratedResult] = []
        
        # Setup logging
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logger.setLevel(log_level)
        
        logger.info("L4 Integrated Analyzer initialized with meta-cognitive optimization")
    
    def analyze(self, query: str, context: Optional[Dict] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Perform L4 integrated analysis across all engines."""
        start_time = time.perf_counter()
        session_id = session_id or f"l4-integrated-{uuid.uuid4()}"
        context = context or {}
        
        try:
            # Run analysis on all engines
            engine_results, engine_timings = self._run_engine_analysis(query, context, session_id)
            
            # Apply cross-engine optimization
            if self.config.cross_engine_synchronization:
                engine_results = self.cross_engine_optimizer.synchronize_engines(engine_results)
            
            # Apply meta-cognitive processing
            meta_result = self.meta_cognitive_processor.apply_meta_cognitive_optimization(engine_results, query)
            
            # Calculate optimal engine weights
            optimal_weights = self.cross_engine_optimizer.optimize_engine_weights(
                meta_result['calibrated_results'], 
                meta_result['query_complexity']
            )
            
            # Calculate integrated scores
            integrated_scores = self._calculate_integrated_scores(
                meta_result['calibrated_results'], 
                optimal_weights
            )
            
            # Generate L4 reasoning path
            reasoning_path = self._generate_integrated_reasoning_path(engine_results, meta_result)
            
            # Create integrated result
            result = L4IntegratedResult(
                session_id=session_id,
                query=query,
                confidence=integrated_scores['confidence'],
                integrated_score=integrated_scores['integrated_score'],
                l4_meta_score=meta_result['l4_meta_score'],
                logic_result=engine_results.get('logic', {}),
                quantum_result=engine_results.get('quantum', {}),
                field_result=engine_results.get('field', {}),
                cross_engine_harmony=self.cross_engine_optimizer.calculate_cross_engine_harmony(engine_results),
                coherence_score=integrated_scores.get('coherence_score', 0.5),
                stability_index=integrated_scores.get('stability_index', 0.5),
                adaptation_score=integrated_scores.get('adaptation_score', 0.5),
                engine_weights=optimal_weights,
                reasoning_path=reasoning_path,
                confidence_calibration=self._extract_confidence_calibration(meta_result['calibrated_results']),
                optimization_applied=meta_result['meta_insights'].get('optimizations_applied', []),
                processing_time=time.perf_counter() - start_time,
                engine_timings=engine_timings
            )
            
            # Store in history
            self.analysis_history.append(result)
            if len(self.analysis_history) > 50:  # Limit history size
                self.analysis_history.pop(0)
            
            return self._result_to_enterprise_format(result)
            
        except Exception as e:
            logger.error(f"L4 Integrated analysis failed: {e}")
            return {
                "confidence": 0.0,
                "integrated_score": 0.0,
                "l4_meta_score": 0.0,
                "cross_engine_harmony": 0.0,
                "status": "error",
                "error": str(e),
                "processing_time": time.perf_counter() - start_time
            }
    
    def _run_engine_analysis(self, query: str, context: Dict, session_id: str) -> Tuple[Dict[str, Dict], Dict[str, float]]:
        """Run analysis on all engines and collect results."""
        engine_results = {}
        engine_timings = {}
        
        # Logic Engine Analysis
        try:
            logic_start = time.perf_counter()
            logic_result = self.logic_engine.run(query, context)
            logic_time = time.perf_counter() - logic_start
            
            engine_results['logic'] = logic_result
            engine_timings['logic'] = logic_time
        except Exception as e:
            logger.warning(f"Logic engine failed: {e}")
            engine_results['logic'] = {"confidence": 0.0, "status": "error", "error": str(e)}
            engine_timings['logic'] = 0.0
        
        # Quantum Engine Analysis
        try:
            quantum_start = time.perf_counter()
            quantum_result = self.quantum_engine.comprehensive_analysis(query, context)
            quantum_time = time.perf_counter() - quantum_start
            
            engine_results['quantum'] = quantum_result
            engine_timings['quantum'] = quantum_time
        except Exception as e:
            logger.warning(f"Quantum engine failed: {e}")
            engine_results['quantum'] = {"confidence": 0.0, "status": "error", "error": str(e)}
            engine_timings['quantum'] = 0.0
        
        # PSI Field Engine Analysis
        try:
            field_start = time.perf_counter()
            field_result = self.field_engine.analyze(query, session_id, context)
            field_time = time.perf_counter() - field_start
            
            engine_results['field'] = field_result
            engine_timings['field'] = field_time
        except Exception as e:
            logger.warning(f"PSI Field engine failed: {e}")
            engine_results['field'] = {"field_stability": 0.0, "status": "error", "error": str(e)}
            engine_timings['field'] = 0.0
        
        return engine_results, engine_timings
    
    def _calculate_integrated_scores(self, calibrated_results: Dict[str, Dict], weights: Dict[str, float]) -> Dict[str, float]:
        """Calculate integrated scores using weighted combination."""
        # Extract key metrics from each engine
        logic_confidence = calibrated_results.get('logic', {}).get('confidence', 0.0)
        quantum_confidence = calibrated_results.get('quantum', {}).get('confidence', 0.0)
        field_stability = calibrated_results.get('field', {}).get('field_stability', 0.0)
        
        # Calculate weighted integrated score
        integrated_score = (
            logic_confidence * weights.get('logic', 0.33) +
            quantum_confidence * weights.get('quantum', 0.33) +
            field_stability * weights.get('field', 0.34)
        )
        
        # Calculate overall confidence (similar but with different weighting)
        confidence = (
            logic_confidence * 0.4 +
            quantum_confidence * 0.3 +
            field_stability * 0.3
        )
        
        # Calculate coherence score
        coherence_scores = []
        if 'quantum' in calibrated_results:
            coherence_scores.append(calibrated_results['quantum'].get('quantum_coherence', 0.5))
        if 'field' in calibrated_results:
            coherence_scores.append(calibrated_results['field'].get('field_coherence', 0.5))
        
        coherence_score = np.mean(coherence_scores) if coherence_scores else 0.5
        
        # Calculate stability index
        stability_scores = []
        if 'field' in calibrated_results:
            stability_scores.append(calibrated_results['field'].get('field_stability', 0.5))
        if 'logic' in calibrated_results:
            stability_scores.append(calibrated_results['logic'].get('confidence', 0.5))
        
        stability_index = np.mean(stability_scores) if stability_scores else 0.5
        
        # Calculate adaptation score
        adaptation_scores = []
        if 'quantum' in calibrated_results:
            adaptation_scores.append(calibrated_results['quantum'].get('adaptation_score', 0.5))
        if 'field' in calibrated_results:
            adaptation_scores.append(calibrated_results['field'].get('adaptive_performance', 0.5))
        
        adaptation_score = np.mean(adaptation_scores) if adaptation_scores else 0.5
        
        return {
            'confidence': confidence,
            'integrated_score': integrated_score,
            'coherence_score': coherence_score,
            'stability_index': stability_index,
            'adaptation_score': adaptation_score
        }
    
    def _generate_integrated_reasoning_path(self, engine_results: Dict[str, Dict], meta_result: Dict[str, Any]) -> List[str]:
        """Generate integrated reasoning path from all engines."""
        path = ["L4-Integrated: Multi-engine analysis initiated"]
        
        # Add engine-specific paths
        for engine_name, result in engine_results.items():
            if 'reasoning_path' in result:
                path.extend([f"L4-{engine_name.title()}: {step}" for step in result['reasoning_path'][-3:]])
            elif 'evolution_path' in result:
                path.extend([f"L4-{engine_name.title()}: {step}" for step in result['evolution_path'][-2:]])
        
        # Add meta-cognitive insights
        meta_insights = meta_result.get('meta_insights', {})
        if 'engine_agreement' in meta_insights:
            agreement = meta_insights['engine_agreement']
            path.append(f"L4-Meta: Engine agreement {agreement:.3f}")
        
        if 'optimization_coverage' in meta_insights:
            coverage = meta_insights['optimization_coverage']
            path.append(f"L4-Meta: Optimization coverage {coverage:.3f}")
        
        # Add final integration step
        path.append(f"L4-Integration: Meta-cognitive synthesis complete")
        
        return path
    
    def _extract_confidence_calibration(self, calibrated_results: Dict[str, Dict]) -> Dict[str, float]:
        """Extract confidence calibration information."""
        calibration = {}
        
        for engine_name, result in calibrated_results.items():
            if 'confidence_calibration' in result:
                cal_info = result['confidence_calibration']
                calibration[f"{engine_name}_original"] = cal_info.get('original', 0.0)
                calibration[f"{engine_name}_calibrated"] = cal_info.get('calibrated', 0.0)
                calibration[f"{engine_name}_adjustment"] = cal_info.get('calibrated', 0.0) - cal_info.get('original', 0.0)
        
        return calibration
    
    def _result_to_enterprise_format(self, result: L4IntegratedResult) -> Dict[str, Any]:
        """Convert L4 integrated result to enterprise-compatible format."""
        return {
            "session_id": result.session_id,
            "query": result.query,
            "confidence": result.confidence,
            "integrated_score": result.integrated_score,
            "l4_meta_score": result.l4_meta_score,
            "cross_engine_harmony": result.cross_engine_harmony,
            "coherence_score": result.coherence_score,
            "stability_index": result.stability_index,
            "adaptation_score": result.adaptation_score,
            "engine_weights": result.engine_weights,
            "reasoning_path": result.reasoning_path,
            "confidence_calibration": result.confidence_calibration,
            "optimization_applied": result.optimization_applied,
            "processing_time": result.processing_time,
            "engine_timings": result.engine_timings,
            "engine_results": {
                "logic": result.logic_result,
                "quantum": result.quantum_result,
                "field": result.field_result
            },
            "status": result.status,
            "warnings": result.warnings,
            "errors": result.errors,
            "analysis_type": "l4_integrated",
            "l4_version": "advanced"
        }
    
    def get_l4_status(self) -> Dict[str, Any]:
        """Get L4 integrated analyzer status."""
        return {
            "status": "ready",
            "l4_integration_enabled": self.config.l4_integration_enabled,
            "engines": {
                "logic": self.logic_engine.get_status(),
                "quantum": self.quantum_engine.get_l4_status(),
                "field": self.field_engine.get_l4_status()
            },
            "integration_features": [
                "cross_engine_synchronization",
                "adaptive_engine_weighting", 
                "meta_cognitive_optimization",
                "confidence_calibration",
                "integrated_reasoning_paths"
            ],
            "analysis_history_size": len(self.analysis_history),
            "optimal_weights": self.cross_engine_optimizer.optimal_weights
        }


def create_l4_integrated_analyzer(config: Optional[Dict] = None) -> L4IntegratedAnalyzer:
    """Factory function to create L4 Integrated Analyzer."""
    if config:
        integrated_config = L4IntegratedConfig(**config)
    else:
        integrated_config = L4IntegratedConfig()
    
    return L4IntegratedAnalyzer(integrated_config)