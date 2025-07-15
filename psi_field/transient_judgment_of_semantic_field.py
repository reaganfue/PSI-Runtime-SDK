#!/usr/bin/env python
# coding: utf-8

# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================
"""
模組名稱：PsiFieldRuntime

用途：
    實現 PSI SDK 的核心運行時，專門負責「語義場 (Semantic Field)」的
    動態管理與演化。本模組是 "Transient Judgment of Semantic Field"
    理論的工程化實現。

應用場景：
    - 需要深度上下文理解與追蹤的長對話系統。
    - 動態知識探索與管理。
    - 人機協同推理與決策支援。
    - 需要監控與引導對話狀態（穩定、發散、聚焦）的應用。

結構設計理念：
    - **狀態為核 (State as Core)**: 以一個統一的、可變的 `SemanticFieldContext`
      物件作為語義場的唯一載體。這個物件承載了對話歷史、知識錨點、場向量
      等所有動態資訊。
    - **服務化組件 (Componentized Services)**: 將原有的各個引擎
      (PsiUnlockEngine, CSPController, etc.) 改造為無狀態的「服務」類別。
      這些服務被注入到主運行時中，並對傳入的 `SemanticFieldContext` 進行操作。
    - **動態循環 (Dynamic Loop)**: 主運行時的核心 `process` 方法實現了
      `unlock → expand → collapse → refocus` 的概念性循環。它會根據
      語義場的當前相位 (phase) 和狀態，動態地選擇執行哪些服務和邏輯。
    - **職責分離 (SoC)**:
        - `PsiFieldRuntime`: 負責流程控制和協調。
        - `Services (Unlocker, Controller, etc.)`: 負責單一的原子操作。
        - `SemanticFieldContext`: 負責承載所有狀態。

核心公式（概念性，由各服務協同實現）：
    - Ψ_t = FΨ(C_t, K_a, R)
    - I_t = α⋅E + β⋅U + γ⋅F

作者：Reagan Fu 開發
"""

# =======================================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# =======================================================
# --- 標準庫 ---
from __future__ import annotations
import json
import logging
import re
import time
import uuid
from collections import Counter, deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# --- 第三方庫 ---
import numpy as np

# --- 日誌設定 ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("psi_field_runtime.log", mode='w', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# --- 全域常數 ---
# 這些常數將被遷移到配置類中，以實現更好的管理
# MAX_DIALOGUE_HISTORY = 20
# EPS = 1e-8
# FIELD_DIMENSION = 64
# ...

# =======================================================
# Segment 3: 配置管理區塊 (Configuration)
# =======================================================
@dataclass
class PsiFieldConfig:
    """
    語義場運行時的統一配置中心。
    """
    # --- 基本配置 ---
    log_level: str = "INFO"
    mode: str = "production"  # "production" | "debug" | "research"
    output_dir: str = "./output/psi_field"

    # --- 語義場參數 ---
    field_dimension: int = 64
    knowledge_dimension: int = 32
    role_dimension: int = 16
    context_dimension: int = 32
    max_dialogue_history: int = 20
    
    # --- CSP 控制參數 ---
    stability_threshold: float = 0.75
    stability_window_size: int = 3 # 用於計算移動平均穩定度的窗口大小
    
    # --- 語義張力配置 (α, β, γ) ---
    tension_weights: Dict[str, float] = field(default_factory=lambda: {
        "emotion": 0.3,
        "uncertainty": 0.3,
        "intention": 0.4,
    })
    
    # --- 知識解鎖與衰減 ---
    knowledge_similarity_threshold: float = 0.6
    knowledge_decay_rate: float = 0.05
    knowledge_activation_boost: float = 0.5
    
    # --- 功能開關 ---
    enable_context_backtracking: bool = True
    enable_detailed_logging: bool = True
    
    # --- 數值穩定性 ---
    epsilon: float = 1e-8

    def __post_init__(self):
        """配置實例化後執行。"""
        level = getattr(logging, self.log_level.upper(), logging.INFO)
        logging.getLogger().setLevel(level)
        Path(self.output_dir).mkdir(exist_ok=True, parents=True)
        logger.info("PsiFieldConfig initialized.")

# =======================================================
# Segment 4: 資料結構與核心狀態 (Data Structures & Core State)
# =======================================================
# --- 自訂錯誤 ---
class PsiFieldError(Exception):
    """PSI Field Runtime 的基礎錯誤。"""
    pass

# --- 核心資料模型 ---
@dataclass
class KnowledgeAnchor:
    """知識錨點：表示已解鎖的知識節點。"""
    key: str
    vector: np.ndarray
    unlocked_at: float
    activation_level: float = 1.0
    related_keys: Set[str] = field(default_factory=set)

    def decay(self, rate: float):
        self.activation_level *= (1.0 - rate)

    def activate(self, boost: float):
        self.activation_level = min(1.0, self.activation_level + boost)

@dataclass
class DialogueTurn:
    """代表一個對話回合。"""
    speaker: str # 'user' or 'engine'
    text: str
    timestamp: float = field(default_factory=time.time)

@dataclass
class SemanticFieldContext:
    """
    【核心狀態物件】語義場的統一狀態載體。
    這是一個可變的物件，由主運行時創建和管理，並在各個服務間傳遞。
    """
    # --- 身份與歷史 ---
    session_id: str = field(default_factory=lambda: f"psi-session-{uuid.uuid4()}")
    dialogue_history: deque[DialogueTurn] = field(default_factory=deque) # 使用 deque 自動管理長度
    
    # --- 語義場核心要素 (Ψ_t = FΨ(C_t, K_a, R)) ---
    field_vector: np.ndarray # (Ψ_t) 主場向量
    knowledge_anchors: Dict[str, KnowledgeAnchor] = field(default_factory=dict) # (K_a) 知識錨點庫
    role_vector: np.ndarray # (R) 角色向量
    
    # --- 動態指標 ---
    semantic_tension: float = 0.0 # (I_t) 語義張力
    stability: float = 0.0 # CSP 穩定性
    phase: str = "initial"  # initial, unlocking, expanding, stable, collapsing, refocusing
    
    # --- 內部追蹤 ---
    stability_history: List[float] = field(default_factory=list)
    phase_transitions: List[Dict] = field(default_factory=list)

    @classmethod
    def create(cls, config: PsiFieldConfig) -> SemanticFieldContext:
        """工廠方法：創建一個全新的、初始化的語義場上下文。"""
        # 初始化角色向量 (R)
        rng = np.random.default_rng(hash("ai_assistant"))
        role_vec = rng.random(config.role_dimension)
        role_vec /= (np.linalg.norm(role_vec) + config.epsilon)

        return cls(
            dialogue_history=deque(maxlen=config.max_dialogue_history),
            field_vector=np.zeros(config.field_dimension),
            role_vector=role_vec
        )

@dataclass(frozen=True)
class RuntimeOutput:
    """
    單次 process 呼叫的標準化、不可變輸出。
    """
    session_id: str
    response_text: str
    current_phase: str
    current_stability: float
    current_tension: float
    unlocked_keys: List[str]
