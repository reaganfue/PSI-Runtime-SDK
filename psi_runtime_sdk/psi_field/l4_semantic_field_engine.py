#!/usr/bin/env python
# coding: utf-8

"""
L4 PSI Field Engine - Meta-Cognitive Semantic Field Analysis

This module implements L4 (Level 4) meta-cognitive optimization for semantic field 
analysis and management. It provides advanced field stability, knowledge unlocking,
and cross-engine synchronization capabilities.

L4 Optimization Features:
- Meta-cognitive field stability optimization
- Adaptive knowledge unlocking mechanisms
- Cross-engine semantic synchronization
- Dynamic field evolution with stability preservation
- Advanced Context Stability Phase (CSP) control
"""

from __future__ import annotations
import json
import logging
import time
import uuid
from collections import deque
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
import numpy as np

# Setup logging
logger = logging.getLogger(__name__)


@dataclass
class L4PsiFieldConfig:
    """L4 PSI Field Configuration - Advanced Meta-Cognitive Parameters."""
    
    # Core field parameters
    field_dimension: int = 128
    knowledge_dimension: int = 64
    role_dimension: int = 32
    context_dimension: int = 64
    max_dialogue_history: int = 30
    
    # L4 meta-cognitive parameters
    l4_optimization_enabled: bool = True
    meta_stability_weight: float = 0.8
    adaptive_unlocking_enabled: bool = True
    cross_engine_sync: bool = True
    dynamic_field_evolution: bool = True
    
    # Advanced CSP parameters
    stability_threshold: float = 0.8
    meta_stability_threshold: float = 0.85
    field_coherence_weight: float = 0.7
    knowledge_retention_factor: float = 0.9
    adaptive_threshold_adjustment: bool = True
    
    # Knowledge management
    knowledge_similarity_threshold: float = 0.7
    knowledge_decay_rate: float = 0.03
    knowledge_activation_boost: float = 0.6
    max_knowledge_anchors: int = 50
    
    # Field evolution parameters
    field_evolution_rate: float = 0.05
    tension_sensitivity: float = 0.5
    phase_transition_smoothing: float = 0.3
    
    # Debugging and monitoring
    log_level: str = "INFO"
    debug_field_states: bool = False
    save_field_evolution: bool = True
    output_dir: str = "./output/l4_psi_field"


@dataclass
class L4KnowledgeAnchor:
    """L4 Enhanced Knowledge Anchor with meta-cognitive properties."""
    
    key: str
    vector: np.ndarray
    unlocked_at: float
    activation_level: float = 1.0
    related_keys: Set[str] = field(default_factory=set)
    
    # L4 meta-cognitive properties
    meta_relevance: float = 0.5
    stability_contribution: float = 0.5
    cross_engine_links: Dict[str, float] = field(default_factory=dict)
    evolution_history: List[float] = field(default_factory=list)
    
    def l4_decay(self, rate: float, stability_factor: float = 1.0):
        """L4 enhanced decay with stability consideration."""
        # Standard decay
        self.activation_level *= (1.0 - rate)
        
        # L4 stability-based preservation
        preservation_factor = stability_factor * self.stability_contribution
        self.activation_level = max(self.activation_level, preservation_factor * 0.1)
        
        # Update evolution history
        self.evolution_history.append(self.activation_level)
        if len(self.evolution_history) > 10:
            self.evolution_history.pop(0)
    
    def l4_activate(self, boost: float, meta_context: Optional[Dict] = None):
        """L4 enhanced activation with meta-cognitive boost."""
        base_activation = min(1.0, self.activation_level + boost)
        
        # L4 meta-cognitive enhancement
        if meta_context:
            relevance_boost = meta_context.get('relevance_score', 0.0) * 0.2
            stability_boost = meta_context.get('field_stability', 0.0) * 0.1
            base_activation += relevance_boost + stability_boost
        
        self.activation_level = min(1.0, base_activation)
        self.meta_relevance = min(1.0, self.meta_relevance + boost * 0.5)
        
        # Update evolution history
        self.evolution_history.append(self.activation_level)
        if len(self.evolution_history) > 10:
            self.evolution_history.pop(0)


@dataclass
class L4SemanticFieldContext:
    """L4 Enhanced Semantic Field Context with meta-cognitive capabilities."""
    
    # Core field components
    field_vector: np.ndarray
    role_vector: np.ndarray
    session_id: str = field(default_factory=lambda: f"l4-psi-{uuid.uuid4()}")
    
    # Knowledge management
    knowledge_anchors: Dict[str, L4KnowledgeAnchor] = field(default_factory=dict)
    
    # Field state indicators
    semantic_tension: float = 0.0
    stability: float = 0.0
    phase: str = "initial"
    
    # L4 meta-cognitive properties
    meta_stability: float = 0.0
    field_coherence: float = 0.5
    cross_engine_harmony: float = 0.5
    adaptive_threshold: float = 0.8
    
    # Evolution tracking
    stability_history: List[float] = field(default_factory=list)
    phase_transitions: List[Dict] = field(default_factory=list)
    field_evolution_history: List[np.ndarray] = field(default_factory=list)
    
    # L4 specific tracking
    meta_stability_history: List[float] = field(default_factory=list)
    coherence_timeline: List[float] = field(default_factory=list)
    l4_optimizations_applied: List[str] = field(default_factory=list)
    
    @classmethod
    def create_l4(cls, config: L4PsiFieldConfig) -> L4SemanticFieldContext:
        """Factory method for creating L4-optimized semantic field context."""
        # Initialize role vector with better distribution
        role_vec = np.random.normal(0, 0.5, config.role_dimension)
        role_vec /= (np.linalg.norm(role_vec) + 1e-8)
        
        # Initialize field vector with L4 enhancements
        field_vec = np.zeros(config.field_dimension)
        
        context = cls(
            field_vector=field_vec,
            role_vector=role_vec,
            adaptive_threshold=config.stability_threshold
        )
        
        # L4 initialization
        context.l4_optimizations_applied.append("l4_initialization")
        return context
    
    def update_l4_metrics(self, config: L4PsiFieldConfig):
        """Update L4 meta-cognitive metrics."""
        # Calculate meta-stability
        if len(self.stability_history) >= 3:
            recent_stability = self.stability_history[-3:]
            self.meta_stability = np.mean(recent_stability) * (1.0 - np.std(recent_stability))
        else:
            self.meta_stability = self.stability * 0.8
        
        # Calculate field coherence
        if len(self.knowledge_anchors) > 0:
            activations = [anchor.activation_level for anchor in self.knowledge_anchors.values()]
            coherence_variance = 1.0 - np.std(activations) if len(activations) > 1 else 1.0
            knowledge_density = min(1.0, len(self.knowledge_anchors) / config.max_knowledge_anchors)
            self.field_coherence = (coherence_variance + knowledge_density) / 2.0
        
        # Update adaptive threshold based on performance
        if config.adaptive_threshold_adjustment and len(self.stability_history) >= 5:
            recent_performance = np.mean(self.stability_history[-5:])
            if recent_performance > 0.9:
                self.adaptive_threshold = min(0.95, self.adaptive_threshold + 0.01)
            elif recent_performance < 0.6:
                self.adaptive_threshold = max(0.6, self.adaptive_threshold - 0.01)
        
        # Update timelines
        self.meta_stability_history.append(self.meta_stability)
        self.coherence_timeline.append(self.field_coherence)
        
        # Limit history size
        if len(self.meta_stability_history) > 20:
            self.meta_stability_history.pop(0)
        if len(self.coherence_timeline) > 20:
            self.coherence_timeline.pop(0)


@dataclass
class L4PsiFieldResult:
    """L4 PSI Field Analysis Result."""
    
    session_id: str
    query: str
    field_stability: float
    meta_stability: float
    field_coherence: float
    knowledge_unlocked: int
    phase: str
    
    # L4 specific results
    cross_engine_harmony: float
    adaptive_performance: float
    semantic_tension: float
    
    # Evolution data
    stability_timeline: List[float] = field(default_factory=list)
    coherence_timeline: List[float] = field(default_factory=list)
    phase_transitions: List[Dict] = field(default_factory=list)
    
    # Metadata
    processing_time: float = 0.0
    status: str = "success"
    l4_optimizations_applied: List[str] = field(default_factory=list)


class L4FieldStabilityOptimizer:
    """L4 Field Stability Optimization Engine."""
    
    def __init__(self, config: L4PsiFieldConfig):
        self.config = config
        self.stability_memory: List[float] = []
        
    def optimize_stability(self, context: L4SemanticFieldContext, query_context: Dict) -> L4SemanticFieldContext:
        """Apply L4 stability optimization to semantic field."""
        if not self.config.l4_optimization_enabled:
            return context
        
        original_stability = context.stability
        
        # L4 multi-factor stability calculation
        base_stability = self._calculate_base_stability(context)
        coherence_boost = self._calculate_coherence_boost(context)
        meta_cognitive_factor = self._calculate_meta_cognitive_factor(context)
        adaptive_adjustment = self._calculate_adaptive_adjustment(context)
        
        # L4 stability formula
        optimized_stability = (
            base_stability * (1 + coherence_boost) * 
            meta_cognitive_factor * adaptive_adjustment
        )
        optimized_stability = min(1.0, max(0.0, optimized_stability))
        
        context.stability = optimized_stability
        context.stability_history.append(optimized_stability)
        
        # Update meta-stability
        context.update_l4_metrics(self.config)
        
        # Track for learning
        self.stability_memory.append(optimized_stability)
        if len(self.stability_memory) > 30:
            self.stability_memory.pop(0)
        
        if not "stability_optimization" in context.l4_optimizations_applied:
            context.l4_optimizations_applied.append("stability_optimization")
        
        logger.info(f"L4 Stability optimized: {original_stability:.4f} → {optimized_stability:.4f}")
        return context
    
    def _calculate_base_stability(self, context: L4SemanticFieldContext) -> float:
        """Calculate base stability from field properties."""
        # Knowledge anchor consistency
        if len(context.knowledge_anchors) > 0:
            activations = [anchor.activation_level for anchor in context.knowledge_anchors.values()]
            anchor_stability = 1.0 - np.std(activations) if len(activations) > 1 else 1.0
        else:
            anchor_stability = 0.5
        
        # Field vector stability
        field_magnitude = np.linalg.norm(context.field_vector)
        field_stability = min(1.0, field_magnitude / 10.0)  # Normalize
        
        return (anchor_stability + field_stability) / 2.0
    
    def _calculate_coherence_boost(self, context: L4SemanticFieldContext) -> float:
        """Calculate coherence-based stability boost."""
        coherence_factor = context.field_coherence * self.config.field_coherence_weight
        return min(0.3, coherence_factor * 0.4)  # Max 30% boost
    
    def _calculate_meta_cognitive_factor(self, context: L4SemanticFieldContext) -> float:
        """Calculate meta-cognitive enhancement factor."""
        if len(context.meta_stability_history) < 2:
            return 1.0
        
        # Stability trend analysis
        recent_meta = context.meta_stability_history[-3:]
        trend = np.polyfit(range(len(recent_meta)), recent_meta, 1)[0] if len(recent_meta) > 1 else 0.0
        
        # Positive trend gives boost, negative trend reduces
        trend_factor = 1.0 + (trend * 0.2)
        return max(0.8, min(1.2, trend_factor))
    
    def _calculate_adaptive_adjustment(self, context: L4SemanticFieldContext) -> float:
        """Calculate adaptive threshold adjustment factor."""
        if not self.config.adaptive_threshold_adjustment:
            return 1.0
        
        # Adjustment based on current performance vs adaptive threshold
        current_performance = context.stability
        threshold_diff = current_performance - context.adaptive_threshold
        
        # If performing above threshold, slight boost; if below, slight reduction
        adjustment = 1.0 + (threshold_diff * 0.1)
        return max(0.9, min(1.1, adjustment))


class L4KnowledgeUnlocker:
    """L4 Enhanced Knowledge Unlocking Engine."""
    
    def __init__(self, config: L4PsiFieldConfig):
        self.config = config
        self.unlocking_history: List[str] = []
        
    def l4_unlock_knowledge(self, text: str, context: L4SemanticFieldContext) -> L4SemanticFieldContext:
        """Perform L4 enhanced knowledge unlocking."""
        if not self.config.adaptive_unlocking_enabled:
            return self._basic_unlock(text, context)
        
        # L4 intelligent tokenization
        knowledge_candidates = self._extract_l4_knowledge_candidates(text, context)
        
        # L4 relevance scoring and filtering
        relevant_knowledge = self._score_and_filter_knowledge(knowledge_candidates, context)
        
        # L4 unlocking with meta-cognitive consideration
        for key, relevance_score in relevant_knowledge.items():
            self._l4_unlock_single_knowledge(key, relevance_score, context)
        
        # L4 knowledge consolidation
        self._consolidate_knowledge_anchors(context)
        
        if not "l4_knowledge_unlocking" in context.l4_optimizations_applied:
            context.l4_optimizations_applied.append("l4_knowledge_unlocking")
        
        logger.info(f"L4 Knowledge unlocking completed: {len(relevant_knowledge)} keys processed")
        return context
    
    def _extract_l4_knowledge_candidates(self, text: str, context: L4SemanticFieldContext) -> Dict[str, float]:
        """Extract knowledge candidates with L4 intelligence."""
        words = text.lower().split()
        candidates = {}
        
        # Basic filtering
        for word in words:
            if len(word) > 3 and word.isalpha():
                # L4 relevance scoring based on context
                relevance = self._calculate_word_relevance(word, context)
                if relevance > 0.3:  # Threshold for consideration
                    candidates[word] = relevance
        
        # L4 phrase extraction
        for i in range(len(words) - 1):
            phrase = f"{words[i]}_{words[i+1]}"
            if len(phrase) > 7:
                relevance = self._calculate_phrase_relevance(phrase, context)
                if relevance > 0.4:
                    candidates[phrase] = relevance
        
        return candidates
    
    def _score_and_filter_knowledge(self, candidates: Dict[str, float], context: L4SemanticFieldContext) -> Dict[str, float]:
        """Score and filter knowledge candidates using L4 meta-cognitive analysis."""
        scored_knowledge = {}
        
        for key, base_relevance in candidates.items():
            # L4 multi-factor scoring
            context_fit = self._calculate_context_fit(key, context)
            novelty_score = self._calculate_novelty_score(key, context)
            field_harmony = self._calculate_field_harmony(key, context)
            
            # L4 composite score
            composite_score = (
                base_relevance * 0.4 +
                context_fit * 0.3 +
                novelty_score * 0.2 +
                field_harmony * 0.1
            )
            
            # Filter by L4 threshold
            if composite_score > self.config.knowledge_similarity_threshold:
                scored_knowledge[key] = composite_score
        
        # L4 ranking and capacity management
        if len(scored_knowledge) + len(context.knowledge_anchors) > self.config.max_knowledge_anchors:
            # Keep only top-scoring candidates
            n_to_keep = self.config.max_knowledge_anchors - len(context.knowledge_anchors)
            sorted_items = sorted(scored_knowledge.items(), key=lambda x: x[1], reverse=True)
            scored_knowledge = dict(sorted_items[:n_to_keep])
        
        return scored_knowledge
    
    def _l4_unlock_single_knowledge(self, key: str, relevance_score: float, context: L4SemanticFieldContext):
        """Unlock single knowledge item with L4 enhancements."""
        if key in context.knowledge_anchors:
            # L4 enhanced reactivation
            meta_context = {
                'relevance_score': relevance_score,
                'field_stability': context.stability,
                'field_coherence': context.field_coherence
            }
            context.knowledge_anchors[key].l4_activate(
                self.config.knowledge_activation_boost, 
                meta_context
            )
        else:
            # Create new L4 knowledge anchor
            vector = np.random.normal(0, 0.5, self.config.knowledge_dimension)
            vector /= (np.linalg.norm(vector) + 1e-8)
            
            anchor = L4KnowledgeAnchor(
                key=key,
                vector=vector,
                unlocked_at=time.time(),
                activation_level=min(1.0, relevance_score),
                meta_relevance=relevance_score,
                stability_contribution=min(0.8, relevance_score * 1.2)
            )
            
            context.knowledge_anchors[key] = anchor
            self.unlocking_history.append(key)
            
            if len(self.unlocking_history) > 100:
                self.unlocking_history.pop(0)
    
    def _consolidate_knowledge_anchors(self, context: L4SemanticFieldContext):
        """L4 knowledge anchor consolidation and cleanup."""
        # Remove low-activation anchors if at capacity
        if len(context.knowledge_anchors) >= self.config.max_knowledge_anchors:
            items = list(context.knowledge_anchors.items())
            items.sort(key=lambda x: x[1].activation_level, reverse=True)
            
            # Keep top performers
            keep_count = int(self.config.max_knowledge_anchors * 0.9)
            context.knowledge_anchors = dict(items[:keep_count])
        
        # Apply L4 decay to all anchors
        field_stability = context.stability
        for anchor in context.knowledge_anchors.values():
            anchor.l4_decay(self.config.knowledge_decay_rate, field_stability)
    
    def _calculate_word_relevance(self, word: str, context: L4SemanticFieldContext) -> float:
        """Calculate word relevance with L4 context awareness."""
        # Base relevance (length-based)
        base_relevance = min(1.0, len(word) / 10.0)
        
        # Context boost if related to existing knowledge
        context_boost = 0.0
        for anchor in context.knowledge_anchors.values():
            if word in anchor.key or anchor.key in word:
                context_boost = max(context_boost, anchor.activation_level * 0.3)
        
        return min(1.0, base_relevance + context_boost)
    
    def _calculate_phrase_relevance(self, phrase: str, context: L4SemanticFieldContext) -> float:
        """Calculate phrase relevance with L4 semantic analysis."""
        words = phrase.split('_')
        word_relevances = [self._calculate_word_relevance(word, context) for word in words]
        return np.mean(word_relevances) * 1.2  # Bonus for phrases
    
    def _calculate_context_fit(self, key: str, context: L4SemanticFieldContext) -> float:
        """Calculate how well the key fits current context."""
        # Fit based on current phase and stability
        phase_bonus = 0.1 if context.phase in ["unlocking", "expanding"] else 0.0
        stability_factor = context.stability * 0.5
        return min(1.0, 0.5 + phase_bonus + stability_factor)
    
    def _calculate_novelty_score(self, key: str, context: L4SemanticFieldContext) -> float:
        """Calculate novelty score - higher for new concepts."""
        if key in context.knowledge_anchors:
            return 0.2  # Low novelty for existing
        
        # Higher novelty for completely new concepts
        similarity_scores = []
        for existing_key in context.knowledge_anchors.keys():
            similarity = len(set(key) & set(existing_key)) / max(len(key), len(existing_key))
            similarity_scores.append(similarity)
        
        if not similarity_scores:
            return 1.0  # Maximum novelty if no existing knowledge
        
        max_similarity = max(similarity_scores)
        return 1.0 - max_similarity
    
    def _calculate_field_harmony(self, key: str, context: L4SemanticFieldContext) -> float:
        """Calculate harmony with current field state."""
        return context.field_coherence * 0.8 + 0.2  # Base harmony
    
    def _basic_unlock(self, text: str, context: L4SemanticFieldContext) -> L4SemanticFieldContext:
        """Basic knowledge unlocking for fallback."""
        words = [word for word in text.split() if len(word) > 3]
        for word in words[:5]:  # Limit to avoid overload
            if word not in context.knowledge_anchors:
                vector = np.random.normal(0, 0.5, self.config.knowledge_dimension)
                vector /= (np.linalg.norm(vector) + 1e-8)
                
                anchor = L4KnowledgeAnchor(
                    key=word,
                    vector=vector,
                    unlocked_at=time.time()
                )
                context.knowledge_anchors[word] = anchor
        
        return context


class L4SemanticFieldEngine:
    """L4 Meta-Cognitive Semantic Field Engine - Enterprise Grade."""
    
    def __init__(self, config: Optional[L4PsiFieldConfig] = None):
        """Initialize L4 Semantic Field Engine."""
        self.config = config or L4PsiFieldConfig()
        self.stability_optimizer = L4FieldStabilityOptimizer(self.config)
        self.knowledge_unlocker = L4KnowledgeUnlocker(self.config)
        self.active_contexts: Dict[str, L4SemanticFieldContext] = {}
        
        # Setup logging
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logger.setLevel(log_level)
        
        logger.info("L4 Semantic Field Engine initialized with meta-cognitive optimization")
    
    def analyze(self, query: str, session_id: Optional[str] = None, context_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform L4 semantic field analysis."""
        start_time = time.perf_counter()
        context_data = context_data or {}
        
        try:
            # Get or create context
            if session_id and session_id in self.active_contexts:
                context = self.active_contexts[session_id]
            else:
                context = L4SemanticFieldContext.create_l4(self.config)
                if session_id:
                    self.active_contexts[session_id] = context
            
            # L4 knowledge unlocking
            context = self.knowledge_unlocker.l4_unlock_knowledge(query, context)
            
            # L4 stability optimization
            context = self.stability_optimizer.optimize_stability(context, context_data)
            
            # L4 phase management
            context = self._manage_l4_phase_transitions(context, query)
            
            # Calculate L4 metrics
            l4_metrics = self._calculate_l4_field_metrics(context)
            
            # Generate result
            result = L4PsiFieldResult(
                session_id=context.session_id,
                query=query,
                field_stability=context.stability,
                meta_stability=context.meta_stability,
                field_coherence=context.field_coherence,
                knowledge_unlocked=len(context.knowledge_anchors),
                phase=context.phase,
                cross_engine_harmony=context.cross_engine_harmony,
                adaptive_performance=l4_metrics['adaptive_performance'],
                semantic_tension=context.semantic_tension,
                stability_timeline=context.stability_history.copy(),
                coherence_timeline=context.coherence_timeline.copy(),
                phase_transitions=context.phase_transitions.copy(),
                processing_time=time.perf_counter() - start_time,
                l4_optimizations_applied=context.l4_optimizations_applied.copy()
            )
            
            return self._result_to_enterprise_format(result)
            
        except Exception as e:
            logger.error(f"L4 Semantic field analysis failed: {e}")
            return {
                "field_stability": 0.0,
                "meta_stability": 0.0,
                "field_coherence": 0.0,
                "knowledge_unlocked": 0,
                "phase": "error",
                "status": "error",
                "error": str(e),
                "l4_optimizations_applied": []
            }
    
    def _manage_l4_phase_transitions(self, context: L4SemanticFieldContext, query: str) -> L4SemanticFieldContext:
        """Manage L4 enhanced phase transitions."""
        old_phase = context.phase
        
        # L4 adaptive phase transition logic
        if context.phase == "initial":
            if len(context.knowledge_anchors) > 0:
                context.phase = "unlocking"
        elif context.phase == "unlocking":
            if context.stability > self.config.stability_threshold:
                context.phase = "stable"
            elif len(context.knowledge_anchors) > 5:
                context.phase = "expanding"
        elif context.phase == "expanding":
            if context.stability > self.config.meta_stability_threshold:
                context.phase = "stable"
        elif context.phase == "stable":
            if context.stability < self.config.stability_threshold * 0.8:
                context.phase = "refocusing"
        elif context.phase == "refocusing":
            if context.stability > self.config.stability_threshold:
                context.phase = "stable"
        
        # Record phase transition
        if old_phase != context.phase:
            transition = {
                "from": old_phase,
                "to": context.phase,
                "timestamp": time.time(),
                "stability": context.stability,
                "trigger": "l4_adaptive_transition"
            }
            context.phase_transitions.append(transition)
            
            if not "phase_transition_management" in context.l4_optimizations_applied:
                context.l4_optimizations_applied.append("phase_transition_management")
            
            logger.info(f"L4 Phase transition: {old_phase} → {context.phase}")
        
        return context
    
    def _calculate_l4_field_metrics(self, context: L4SemanticFieldContext) -> Dict[str, float]:
        """Calculate L4 field-specific metrics."""
        # Adaptive performance based on historical data
        if len(context.stability_history) >= 3:
            recent_performance = np.mean(context.stability_history[-3:])
            performance_trend = np.polyfit(range(len(context.stability_history)), context.stability_history, 1)[0]
            adaptive_performance = recent_performance + (performance_trend * 0.5)
        else:
            adaptive_performance = context.stability
        
        adaptive_performance = max(0.0, min(1.0, adaptive_performance))
        
        # Cross-engine harmony (enhanced calculation)
        knowledge_factor = min(1.0, len(context.knowledge_anchors) / 20.0)
        stability_factor = context.stability
        coherence_factor = context.field_coherence
        
        context.cross_engine_harmony = (
            knowledge_factor * 0.3 +
            stability_factor * 0.4 +
            coherence_factor * 0.3
        )
        
        return {
            'adaptive_performance': adaptive_performance
        }
    
    def _result_to_enterprise_format(self, result: L4PsiFieldResult) -> Dict[str, Any]:
        """Convert L4 result to enterprise-compatible format."""
        return {
            "field_stability": result.field_stability,
            "meta_stability": result.meta_stability,
            "field_coherence": result.field_coherence,
            "knowledge_unlocked": result.knowledge_unlocked,
            "phase": result.phase,
            "cross_engine_harmony": result.cross_engine_harmony,
            "adaptive_performance": result.adaptive_performance,
            "semantic_tension": result.semantic_tension,
            "stability_timeline": result.stability_timeline,
            "coherence_timeline": result.coherence_timeline,
            "phase_transitions": result.phase_transitions,
            "processing_time": result.processing_time,
            "l4_optimizations_applied": result.l4_optimizations_applied,
            "status": result.status,
            "analysis_type": "l4_semantic_field"
        }
    
    def get_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get context information for a session."""
        if session_id in self.active_contexts:
            context = self.active_contexts[session_id]
            return {
                "session_id": context.session_id,
                "phase": context.phase,
                "stability": context.stability,
                "meta_stability": context.meta_stability,
                "field_coherence": context.field_coherence,
                "knowledge_count": len(context.knowledge_anchors),
                "l4_optimizations": context.l4_optimizations_applied
            }
        return None
    
    def get_l4_status(self) -> Dict[str, Any]:
        """Get L4 semantic field engine status."""
        return {
            "status": "ready",
            "l4_optimization_enabled": self.config.l4_optimization_enabled,
            "field_dimension": self.config.field_dimension,
            "active_contexts": len(self.active_contexts),
            "adaptive_unlocking_enabled": self.config.adaptive_unlocking_enabled,
            "cross_engine_sync": self.config.cross_engine_sync,
            "l4_features": [
                "meta_cognitive_stability",
                "adaptive_knowledge_unlocking",
                "field_coherence_optimization",
                "phase_transition_management",
                "cross_engine_synchronization"
            ]
        }


# Backward compatibility aliases
SemanticFieldEngine = L4SemanticFieldEngine
FieldConfig = L4PsiFieldConfig


def create_l4_semantic_field_engine(config: Optional[Dict] = None) -> L4SemanticFieldEngine:
    """Factory function to create L4 Semantic Field Engine."""
    if config:
        field_config = L4PsiFieldConfig(**config)
    else:
        field_config = L4PsiFieldConfig()
    
    return L4SemanticFieldEngine(field_config)