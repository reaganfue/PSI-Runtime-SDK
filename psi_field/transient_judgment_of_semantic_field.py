#!/usr/bin/env python
# coding: utf-8

# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================
"""
模組名稱：TransientJudgmentOfSemanticField
用途：實現語境場的動態解鎖、知識錨定與語義張力分析，支援人機協同推理
應用場景：語境解析、知識範圍管理、決策回饋、語義場演化

結構設計理念：
    - 從用戶對話解鎖知識，而非依賴向量庫查找
    - 通過上下文鏈 (C_t)、知識錨點 (K_a)、角色向量 (R) 構建高維語境場 (Ψ_t)
    - 語義場運算：Ψ_t = FΨ(C_t, K_a, R)
    - 語義場能量張力：I_t = α⋅E + β⋅U + γ⋅F
    - 支持最多20次對話來回，形成一個「語境穩定相位」(Context Stability Phase, CSP)
    - 知識解鎖機制 (SUS: Semantic Unlocking System)

系統核心組件：
    - PsiUnlockEngine: 語意解鎖知識模組
    - CSPController: 判定語境穩定期與語境記憶封閉點
    - EchoResolver: 語境回掃與語意解釋生成

核心運行邏輯：
    unlock → expand → collapse → refocus
    (解鎖 → 擴展 → 收縮 → 重聚焦)

整體架構：
    - NLP輸入解析 → 知識解鎖與場計算 → 語義張力分析 → 決策與詳細回饋
"""

# =======================================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# =======================================================
import logging
import numpy as np
import math
from typing import Any, Dict, List, Optional, Tuple, Union, Set
from collections import deque, defaultdict, Counter
import json
import time
import re
import uuid
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict

# Logging 設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("semantic_field.log", mode='a')
    ]
)
logger = logging.getLogger(__name__)

# 全域常數
MAX_DIALOGUE_HISTORY = 20  # 最大對話次數
EPS = 1e-8  # 數值穩定性常數
DEFAULT_TIMEOUT = 30  # 默認超時值 (秒)
FIELD_DIMENSION = 64  # 語義場向量維度
KNOWLEDGE_DIMENSION = 32  # 知識向量維度
ROLE_DIMENSION = 16  # 角色向量維度
CONTEXT_DIMENSION = 32  # 上下文向量維度
SAFETY_THRESHOLD = 0.85  # 安全閾值

# =======================================================
# Segment 3: 配置管理區塊 (Configuration)
# =======================================================
@dataclass
class FieldConfig:
    """
    語義場配置類：
    - 管理日誌級別、系統模式、報告路徑等參數
    - 提供配置更新與載入功能
    """
    # 基本配置
    log_level: int = logging.INFO
    mode: str = "production"  # "production" | "debug" | "research"
    report_path: str = "./reports"
    
    # 語義場參數
    field_dimension: int = FIELD_DIMENSION
    enable_context_backtracking: bool = True
    max_dialogue_history: int = MAX_DIALOGUE_HISTORY
    stability_threshold: float = 0.75
    
    # 語義張力配置
    emotion_weight: float = 0.3  # α
    uncertainty_weight: float = 0.3  # β
    intention_weight: float = 0.4  # γ
    
    # 進階特性
    enable_philosophical_analysis: bool = True
    enable_decision_habits_tracking: bool = True
    enable_detailed_logging: bool = True
    
    # 安全機制
    safety_threshold: float = SAFETY_THRESHOLD
    exit_conditions: List[str] = field(default_factory=lambda: ["toxicity", "harmful_intent"])
    
    def update_config(self, **kwargs) -> None:
        """
        更新配置參數並記錄日誌
        
        Args:
            **kwargs: 鍵值對，表示要更新的配置項及其新值
            
        Returns:
            None
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                old_value = getattr(self, key)
                setattr(self, key, value)
                logger.info(f"Config updated: {key} = {value} (was {old_value})")
            else:
                logger.warning(f"Unknown config parameter: {key}")
    
    def load_config(self, config_path: str = None) -> Dict[str, Any]:
        """
        從文件加載配置或返回當前配置字典
        
        Args:
            config_path: 可選，配置文件路徑
            
        Returns:
            Dict[str, Any]: 配置字典
        """
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    self.update_config(**config_data)
                    logger.info(f"Config loaded from {config_path}")
            except Exception as e:
                logger.error(f"Failed to load config from {config_path}: {e}")
        
        return asdict(self)
    
    def save_config(self, config_path: str) -> bool:
        """
        保存當前配置到文件
        
        Args:
            config_path: 配置文件保存路徑
            
        Returns:
            bool: 是否成功保存
        """
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self), f, indent=4, ensure_ascii=False)
            logger.info(f"Config saved to {config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config to {config_path}: {e}")
            return False

# =======================================================
# Segment 4: 資料結構 / 解析區塊 (Data Structures)
# =======================================================
@dataclass
class SemanticInput:
    """
    語意輸入資料結構：封裝用戶輸入的原始資料
    - 將原始文本轉換為結構化資料
    - 提供基本的元數據（時間戳等）
    """
    text: str
    timestamp: float = field(default_factory=time.time)
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式"""
        return asdict(self)


@dataclass
class KnowledgeAnchor:
    """
    知識錨點：表示已解鎖的知識節點
    - 記錄知識的解鎖時間和相關上下文
    - 提供知識激活程度和關聯度計算
    """
    key: str
    context: str
    unlocked_at: float
    activation_level: float = 1.0
    related_keys: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    vector: Optional[np.ndarray] = None
    
    def decay(self, rate: float = 0.05) -> None:
        """知識活躍度衰減函數"""
        self.activation_level *= (1.0 - rate)
        
    def activate(self, boost: float = 0.5) -> None:
        """提升知識活躍度"""
        self.activation_level = min(1.0, self.activation_level + boost)
        
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式"""
        result = asdict(self)
        if self.vector is not None:
            result['vector'] = self.vector.tolist()
        return result


@dataclass
class ContextFieldState:
    """
    語境場狀態：代表當前的語義場 Ψ_t
    - 包含場張量、語義張力、穩定度等屬性
    - 提供場態演化和穩定性計算
    """
    tensor: np.ndarray
    semantic_tension: float
    stability: float
    timestamp: float = field(default_factory=time.time)
    dialogue_count: int = 0
    knowledge_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式"""
        result = asdict(self)
        result['tensor'] = self.tensor.tolist()
        return result


class DataParser:
    """
    資料解析器：
    - 驗證與結構化用戶輸入
    - 詞彙分析與語意向量化
    - 知識點提取
    """
    @staticmethod
    def parse(raw_input: str) -> SemanticInput:
        """
        解析用戶輸入並返回結構化資料
        
        Args:
            raw_input: 用戶輸入的原始文本
            
        Returns:
            SemanticInput: 結構化的語意輸入物件
            
        Raises:
            ValueError: 輸入為空時拋出
        """
        if not raw_input or not raw_input.strip():
            logger.error("Empty input provided.")
            raise ValueError("Input cannot be empty")
        
        # 基本清理與驗證
        text = raw_input.strip()
        
        # 創建 SemanticInput 物件
        return SemanticInput(
            text=text,
            metadata={
                "length": len(text),
                "word_count": len(text.split()),
                "has_question": "?" in text
            }
        )
    
    @staticmethod
    def extract_knowledge_keys(text: str) -> List[str]:
        """
        從文本中提取知識關鍵字
        
        Args:
            text: 輸入文本
            
        Returns:
            List[str]: 提取的知識關鍵字列表
        """
        # 簡單實現，實際應使用 NLP 技術提取關鍵詞
        # 例如使用 NLTK, spaCy 等工具
        words = re.findall(r'\b\w+\b', text.lower())
        # 過濾掉停用詞（示例）
        stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were'}
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # 選取最重要的幾個關鍵詞
        # 實際應用中可使用 TF-IDF, TextRank 等算法
        if not filtered_words:
            return [words[0]] if words else ["default_key"]
        
        # 計算詞頻
        counter = Counter(filtered_words)
        # 返回最頻繁的三個詞
        return [word for word, _ in counter.most_common(3)]
    
    @staticmethod
    def vectorize_text(text: str, dimension: int = FIELD_DIMENSION) -> np.ndarray:
        """
        將文本向量化成數值數組
        
        Args:
            text: 輸入文本
            dimension: 向量維度
            
        Returns:
            np.ndarray: 文本的向量表示
        """
        # 簡單實現，實際應使用詞嵌入或語言模型
        # 此處使用簡單的填充，模擬向量化過程
        hash_val = hash(text)
        rng = np.random.RandomState(hash_val)
        vector = rng.randn(dimension)
        # 歸一化
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector


# =======================================================
# Segment 5: 核心邏輯引擎 (Core Logic Engines)
# =======================================================
class PsiUnlockEngine:
    """
    語意解鎖引擎 (Ψ Unlock Engine)：
    - 負責解鎖知識模組
    - 根據語意內容確定知識解鎖範圍
    - 管理知識活躍度與相關性
    """
    def __init__(self, config: FieldConfig):
        self.config = config
        self.knowledge_base: Dict[str, KnowledgeAnchor] = {}
        self.locked_keys: Set[str] = set()  # 追蹤已知但仍然鎖定的知識點
        logger.info("PsiUnlockEngine initialized")
    
    def unlock_knowledge(self, semantic_input: SemanticInput) -> List[str]:
        """
        根據用戶輸入解鎖知識
        
        Args:
            semantic_input: 結構化的語意輸入
            
        Returns:
            List[str]: 新解鎖的知識關鍵字列表
        """
        # 提取潛在的知識關鍵字
        potential_keys = DataParser.extract_knowledge_keys(semantic_input.text)
        unlocked_keys = []
        
        for key in potential_keys:
            # 檢查是否已經解鎖
            if key in self.knowledge_base:
                # 刷新知識活躍度
                self.knowledge_base[key].activate()
                logger.debug(f"Knowledge refreshed: {key}")
                continue
                
            # 新知識點解鎖
            vector = DataParser.vectorize_text(key, KNOWLEDGE_DIMENSION)
            knowledge = KnowledgeAnchor(
                key=key,
                context=semantic_input.text,
                unlocked_at=semantic_input.timestamp,
                vector=vector
            )
            self.knowledge_base[key] = knowledge
            unlocked_keys.append(key)
            logger.info(f"Knowledge unlocked: {key}")
            
            # 從鎖定列表中移除（如果存在）
            if key in self.locked_keys:
                self.locked_keys.remove(key)
        
        # 更新知識間關聯性
        self._update_knowledge_relations(unlocked_keys)
        
        return unlocked_keys
    
    def _update_knowledge_relations(self, new_keys: List[str]) -> None:
        """
        更新新解鎖知識與現有知識的關聯性
        
        Args:
            new_keys: 新解鎖的知識關鍵字列表
            
        Returns:
            None
        """
        if not new_keys or len(self.knowledge_base) <= 1:
            return
            
        # 為新解鎖的知識建立關聯
        for new_key in new_keys:
            new_vector = self.knowledge_base[new_key].vector
            if new_vector is None:
                continue
                
            # 計算與其他知識的相似度
            for existing_key, existing_knowledge in self.knowledge_base.items():
                if existing_key == new_key or existing_knowledge.vector is None:
                    continue
                    
                # 使用餘弦相似度
                similarity = np.dot(new_vector, existing_knowledge.vector)
                if similarity > 0.6:  # 相似度閾值
                    # 互相添加為相關知識
                    self.knowledge_base[new_key].related_keys.add(existing_key)
                    existing_knowledge.related_keys.add(new_key)
                    logger.debug(f"Relation established: {new_key} <-> {existing_key}")
    
    def decay_all_knowledge(self, rate: float = 0.05) -> None:
        """
        對所有已解鎖知識進行活躍度衰減
        
        Args:
            rate: 衰減率
            
        Returns:
            None
        """
        for knowledge in self.knowledge_base.values():
            knowledge.decay(rate)
            # 如果活躍度太低，則標記為鎖定狀態
            if knowledge.activation_level < 0.1:
                self.locked_keys.add(knowledge.key)
                logger.debug(f"Knowledge locked due to low activation: {knowledge.key}")
    
    def get_knowledge_vector(self) -> np.ndarray:
        """
        獲取當前知識錨點的綜合向量表示
        
        Returns:
            np.ndarray: 知識向量
        """
        if not self.knowledge_base:
            return np.zeros(KNOWLEDGE_DIMENSION)
            
        # 加權合併所有活躍知識的向量
        vectors = []
        weights = []
        
        for knowledge in self.knowledge_base.values():
            if knowledge.vector is not None and knowledge.activation_level > 0.1:
                vectors.append(knowledge.vector)
                weights.append(knowledge.activation_level)
                
        if not vectors:
            return np.zeros(KNOWLEDGE_DIMENSION)
            
        # 歸一化權重
        weights = np.array(weights) / sum(weights)
        # 加權平均
        result = np.average(np.array(vectors), axis=0, weights=weights)
        # 再次歸一化
        norm = np.linalg.norm(result)
        if norm > 0:
            result /= norm
        return result
    
    def reset(self) -> None:
        """
        重置知識解鎖引擎
        
        Returns:
            None
        """
        self.knowledge_base.clear()
        self.locked_keys.clear()
        logger.info("PsiUnlockEngine reset")


class CSPController:
    """
    語境穩定相位控制器 (Context Stability Phase Controller)：
    - 判定語境穩定期
    - 管理語境記憶封閉點
    - 監控語義場演化
    """
    def __init__(self, config: FieldConfig):
        self.config = config
        self.field_history: List[ContextFieldState] = []
        self.stability_scores: List[float] = []
        self.phase_transitions: List[Dict[str, Any]] = []
        self.current_phase = "initial"  # initial, expanding, stable, collapsing, refocusing
        logger.info("CSPController initialized")
    
    def update_field_state(self, field_state: ContextFieldState) -> str:
        """
        更新語境場狀態並判定相位
        
        Args:
            field_state: 當前語境場狀態
            
        Returns:
            str: 當前相位名稱
        """
        # 保存場狀態歷史
        self.field_history.append(field_state)
        
        # 計算穩定度
        if len(self.field_history) > 1:
            # 基於前後場狀態計算穩定度
            prev_tensor = self.field_history[-2].tensor
            curr_tensor = field_state.tensor
            stability = self._calculate_stability(prev_tensor, curr_tensor)
            self.stability_scores.append(stability)
        
        # 判定相位轉換
        self._determine_phase_transition()
        
        return self.current_phase
    
    def _calculate_stability(self, prev_tensor: np.ndarray, curr_tensor: np.ndarray) -> float:
        """
        計算語境場穩定度
        
        Args:
            prev_tensor: 先前的場張量
            curr_tensor: 當前的場張量
            
        Returns:
            float: 穩定度 (0-1)
        """
        # 使用餘弦相似度
        similarity = np.dot(prev_tensor, curr_tensor)
        # 轉換為穩定度分數 (0-1)
        stability = (similarity + 1) / 2
        return stability
    
    def _determine_phase_transition(self) -> None:
        """
        判定相位轉換
        
        Returns:
            None
        """
        # 初始階段
        if len(self.stability_scores) < 3:
            if self.current_phase == "initial" and self.field_history:
                self.current_phase = "expanding"
                self._record_phase_transition("expanding", "開始語意擴展")
            return
            
        # 計算最近幾次的平均穩定度
        recent_stability = np.mean(self.stability_scores[-3:])
        threshold = self.config.stability_threshold
        
        # 相位判定邏輯
        if self.current_phase == "expanding":
            if recent_stability > threshold:
                self.current_phase = "stable"
                self._record_phase_transition("stable", "達到語境穩定相位")
        elif self.current_phase == "stable":
            if recent_stability < threshold - 0.2:
                self.current_phase = "collapsing"
                self._record_phase_transition("collapsing", "語境開始坍縮")
        elif self.current_phase == "collapsing":
            if recent_stability > threshold - 0.1:
                self.current_phase = "refocusing"
                self._record_phase_transition("refocusing", "語境重新聚焦")
        elif self.current_phase == "refocusing":
            if recent_stability > threshold:
                self.current_phase = "stable"
                self._record_phase_transition("stable", "重新達到語境穩定")
    
    def _record_phase_transition(self, phase: str, description: str) -> None:
        """
        記錄相位轉換
        
        Args:
            phase: 新相位名稱
            description: 轉換描述
            
        Returns:
            None
        """
        transition = {
            "timestamp": time.time(),
            "from_phase": self.current_phase,
            "to_phase": phase,
            "description": description,
            "dialogue_count": len(self.field_history),
            "stability": self.stability_scores[-1] if self.stability_scores else 0.0
        }
        self.phase_transitions.append(transition)
        logger.info(f"Phase transition: {transition['from_phase']} -> {transition['to_phase']}: {description}")
    
    def is_stable(self) -> bool:
        """
        檢查當前是否處於穩定相位
        
        Returns:
            bool: 是否穩定
        """
        return self.current_phase == "stable"
    
    def get_stability_report(self) -> Dict[str, Any]:
        """
        獲取穩定性報告
        
        Returns:
            Dict[str, Any]: 穩定性報告
        """
        report = {
            "current_phase": self.current_phase,
            "phase_transitions": self.phase_transitions,
            "current_stability": self.stability_scores[-1] if self.stability_scores else 0.0,
            "field_history_count": len(self.field_history)
        }
        return report
    
    def reset(self) -> None:
        """
        重置控制器
        
        Returns:
            None
        """
        self.field_history.clear()
        self.stability_scores.clear()
        self.phase_transitions.clear()
        self.current_phase = "initial"
        logger.info("CSPController reset")


class EchoResolver:
    """
    語境回掃解析器 (Echo Resolver)：
    - 回掃對話歷史
    - 生成適合語境的解釋
    - 解決知識不足問題
    """
    def __init__(self, config: FieldConfig):
        self.config = config
        self.dialogue_history = deque(maxlen=config.max_dialogue_history)
        logger.info("EchoResolver initialized")
    
    def add_dialogue(self, user_input: str, ai_response: str) -> None:
        """
        添加對話到歷史
        
        Args:
            user_input: 用戶輸入
            ai_response: AI 回應
            
        Returns:
            None
        """
        self.dialogue_history.append({
            "user": user_input,
            "ai": ai_response,
            "timestamp": time.time()
        })
    
    def backtrack_context(self, query: str) -> Optional[Dict[str, Any]]:
        """
        回掃對話歷史，尋找相關上下文
        
        Args:
            query: 查詢關鍵詞或短語
            
        Returns:
            Optional[Dict[str, Any]]: 找到的相關對話，未找到則返回 None
        """
        if not self.config.enable_context_backtracking:
            return None
            
        if not query or not self.dialogue_history:
            return None
            
        # 每個對話的相關性分數
        scores = []
        
        # 回掃每個歷史對話
        for idx, dialogue in enumerate(self.dialogue_history):
            score = 0
            # 檢查用戶輸入
            if query.lower() in dialogue["user"].lower():
                score += 2  # 用戶提到的權重更高
            # 檢查 AI 回應
            if query.lower() in dialogue["ai"].lower():
                score += 1
                
            # 計算時間衰減因子（越久遠權重越低）
            time_factor = 1.0 / (1.0 + 0.1 * (len(self.dialogue_history) - 1 - idx))
            score *= time_factor
            
            scores.append(score)
            
        # 如果沒有相關性，返回 None
        if max(scores) == 0:
            return None
            
        # 選擇最相關的對話
        best_idx = scores.index(max(scores))
        found_dialogue = self.dialogue_history[best_idx]
        
        result = {
            "dialogue": found_dialogue,
            "relevance_score": scores[best_idx],
            "position": best_idx,
            "distance": len(self.dialogue_history) - 1 - best_idx  # 與最新對話的距離
        }
        
        logger.info(f"Context found in history for '{query}' with score {scores[best_idx]}")
        return result
    
    def resolve_unknown_query(self, query: str) -> Dict[str, Any]:
        """
        解析未知查詢
        
        Args:
            query: 未知查詢
            
        Returns:
            Dict[str, Any]: 解析結果
        """
        # 回掃尋找相關上下文
        context = self.backtrack_context(query)
        
        if context:
            return {
                "status": "context_found",
                "context": context,
                "suggestion": f"根據之前的對話，我們曾討論過相關內容: '{context['dialogue']['user']}'",
                "needs_clarification": False
            }
        else:
            return {
                "status": "no_context",
                "suggestion": f"我不確定 '{query}' 的具體內容，請提供更多資訊",
                "needs_clarification": True
            }
    
    def get_dialogue_history(self) -> List[Dict[str, Any]]:
        """
        獲取對話歷史
        
        Returns:
            List[Dict[str, Any]]: 對話歷史列表
        """
        return list(self.dialogue_history)
    
    def reset(self) -> None:
        """
        重置解析器
        
        Returns:
            None
        """
        self.dialogue_history.clear()
        logger.info("EchoResolver reset")


# =======================================================
# Segment 6: 語義張力分析 (Semantic Tension Analysis)
# =======================================================
class SemanticTensionAnalyzer:
    """
    語義張力分析器：
    - 計算語義張力 I_t = α⋅E + β⋅U + γ⋅F
    - 分析使用者意圖強度、模糊性和情緒激發度
    - 提供語義張力分析報告
    """
    def __init__(self, config: FieldConfig):
        self.config = config
        self.last_tension = 0.0
        logger.info("SemanticTensionAnalyzer initialized")
    
    def analyze(self, text: str, context_field: Optional[np.ndarray] = None) -> Dict[str, float]:
        """
        分析語義張力
        
        Args:
            text: 輸入文本
            context_field: 可選的語境場狀態
            
        Returns:
            Dict[str, float]: 語義張力分析結果
        """
        # 計算各個分量
        E = self._calculate_emotion_intensity(text)  # 情緒激發度
        U = self._calculate_uncertainty(text)  # 模糊性
        F = self._calculate_intention_strength(text, context_field)  # 使用者意圖強度
        
        # 應用權重計算語義張力
        α = self.config.emotion_weight
        β = self.config.uncertainty_weight
        γ = self.config.intention_weight
        I_t = α * E + β * U + γ * F
        
        # 保存結果
        self.last_tension = I_t
        
        result = {
            "tension": I_t,
            "emotion_intensity": E,
            "uncertainty": U,
            "intention_strength": F
        }
        
        logger.debug(f"Semantic tension calculated: {result}")
        return result
    
    def _calculate_emotion_intensity(self, text: str) -> float:
        """
        計算情緒激發度
        
        Args:
            text: 輸入文本
            
        Returns:
            float: 情緒激發度 (0-1)
        """
        # 簡單的情緒詞檢測，實際應使用情感分析模型
        emotion_words = {
            "高": ["興奮", "激動", "憤怒", "狂喜", "痛苦", "恐懼", "震驚"],
            "中": ["高興", "開心", "難過", "擔心", "煩悶", "喜歡", "討厭"],
            "低": ["平靜", "滿意", "不確定", "或許", "可能", "也許"]
        }
        
        score = 0.5  # 默認中等
        
        for level, words in emotion_words.items():
            for word in words:
                if word in text:
                    if level == "高":
                        score = 0.9
                    elif level == "中":
                        score = 0.6
                    else:  # 低
                        score = 0.3
        
        # 標點符號也是情緒線索
        if "!" in text or "！" in text:
            score += 0.1
        if "?" in text or "？" in text:
            score += 0.05
        
        return min(1.0, score)
    
    def _calculate_uncertainty(self, text: str) -> float:
        """
        計算模糊性
        
        Args:
            text: 輸入文本
            
        Returns:
            float: 模糊性 (0-1)
        """
        # 模糊詞檢測
        uncertainty_words = ["可能", "也許", "或許", "不確定", "大概", "應該", "或者", "?", "？"]
        
        # 計算模糊詞出現的比例
        word_count = len(text.split())
        if word_count == 0:
            return 0.5
            
        uncertainty_count = sum(1 for word in uncertainty_words if word in text)
        
        # 基礎模糊度 + 模糊詞影響
        base = 0.3
        uncertainty = base + (0.7 * uncertainty_count / (word_count + 1))
        
        return min(1.0, uncertainty)
    
    def _calculate_intention_strength(self, text: str, context_field: Optional[np.ndarray] = None) -> float:
        """
        計算使用者意圖強度
        
        Args:
            text: 輸入文本
            context_field: 語境場狀態
            
        Returns:
            float: 意圖強度 (0-1)
        """
        # 指令性詞彙檢測
        command_words = ["必須", "一定", "請", "需要", "告訴", "解釋", "說明", "幫助", "幫我"]
        
        # 計算指令性詞彙出現的影響
        strength = 0.5  # 默認中等
        
        for word in command_words:
            if word in text:
                strength += 0.1
        
        # 如果有上下文場，計算與之前意圖的連貫性
        if context_field is not None:
            # 模擬計算連貫性（在實際應用中可能更複雜）
            coherence = 0.7  # 假設有一定連貫性
            strength = (strength + coherence) / 2
        
        # 句子長度也影響意圖強度
        if len(text) > 50:
            strength += 0.1  # 較長的句子可能有更強的意圖
        
        return min(1.0, strength)


# =======================================================
# Segment 7: 核心功能實現 – 主類別 (SemanticFieldEngine)
# =======================================================
@dataclass
class SemanticOutput:
    """
    語意輸出資料結構：封裝 AI 的回應與分析結果
    """
    response_text: str
    session_id: str
    timestamp: float = field(default_factory=time.time)
    current_phase: str = "initial"
    stability: float = 0.0
    tension: float = 0.0
    unlocked_keys: List[str] = field(default_factory=list)
    analysis_details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)


class SemanticFieldEngine:
    """
    語義場引擎：
    實現 Transient Judgment of Semantic Field 的核心邏輯：
    - 初始化與資源管理
    - 對話流程與知識解鎖
    - 語境場計算與張力分析
    - 決策與詳細回饋
    """
    def __init__(self, config: FieldConfig):
        self.config = config
        self.psi_engine = PsiUnlockEngine(config)
        self.csp_controller = CSPController(config)
        self.echo_resolver = EchoResolver(config)
        self.tension_analyzer = SemanticTensionAnalyzer(config)
        
        self.context_history = deque(maxlen=config.max_dialogue_history)
        self.context_field: Optional[ContextFieldState] = None
        self.role_vector = self._initialize_role_vector()
        
        self.session_start_time = time.time()
        self.session_id = str(uuid.uuid4())
        self._init_logger()
        
        logger.info(f"SemanticFieldEngine initialized with session ID: {self.session_id}")

    def _init_logger(self) -> None:
        """根據配置更新日誌級別"""
        logging.getLogger().setLevel(self.config.log_level)
        logger.info(f"Logger level set to {logging.getLevelName(self.config.log_level)}")
        
    def _initialize_role_vector(self) -> np.ndarray:
        """初始化角色向量 (R)，此處為模擬"""
        # 在實際應用中，這可能代表 AI 的身份（例如：專家、助手）
        rng = np.random.RandomState(hash("ai_assistant"))
        vector = rng.randn(ROLE_DIMENSION)
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else np.zeros(ROLE_DIMENSION)

    def _update_context_field(self, semantic_input: SemanticInput) -> None:
        """
        核心運算：更新語義場 Ψ_t = FΨ(C_t, K_a, R)
        """
        # 1. 獲取上下文向量 (C_t) - 根據對話歷史生成
        context_text = " ".join([d['user'] for d in self.echo_resolver.get_dialogue_history()])
        context_vector = DataParser.vectorize_text(context_text, CONTEXT_DIMENSION)
        
        # 2. 獲取知識錨點向量 (K_a)
        knowledge_vector = self.psi_engine.get_knowledge_vector()
        
        # 3. 獲取角色向量 (R)
        role_vector = self.role_vector
        
        # 4. 組合向量形成語義場張量 FΨ
        # 簡單實現：拼接所有向量並進行歸一化
        combined_vector = np.concatenate([context_vector, knowledge_vector, role_vector])
        norm = np.linalg.norm(combined_vector)
        field_tensor = combined_vector / norm if norm > 0 else np.zeros(self.config.field_dimension)
        
        # 5. 計算語義張力
        tension_analysis = self.tension_analyzer.analyze(semantic_input.text, self.context_field.tensor if self.context_field else None)
        
        # 6. 計算穩定度 (由 CSPController 內部完成)
        # 此處先創建場態，穩定度在控制器更新時計算
        new_field_state = ContextFieldState(
            tensor=field_tensor,
            semantic_tension=tension_analysis['tension'],
            stability=0.0, # 稍後更新
            dialogue_count=len(self.echo_resolver.get_dialogue_history()) + 1,
            knowledge_count=len(self.psi_engine.knowledge_base)
        )
        
        self.context_field = new_field_state

    def _generate_response(self, semantic_input: SemanticInput, unlocked_keys: List[str]) -> str:
        """根據分析結果生成 AI 回應"""
        phase = self.csp_controller.current_phase
        tension = self.context_field.semantic_tension
        
        response = f"收到您的訊息：'{semantic_input.text}'。\n"
        
        if unlocked_keys:
            response += f"這次對話解鎖了新的知識點：{', '.join(unlocked_keys)}。\n"
        
        response += f"目前對話處於「{phase}」階段，語義張力為 {tension:.2f}。\n"

        if tension > 0.8:
            response += "偵測到較強的意圖或情緒，我會優先處理您的請求。"
        elif phase == "stable":
            response += "我們似乎已達成共識，可以繼續深入探討。"
        elif phase == "collapsing":
            response += "感覺對話方向有些發散，我們是否需要重新聚焦？"
        else:
            response += "我正在理解您的意圖，請繼續。"
            
        return response

    def process_input(self, raw_text: str) -> SemanticOutput:
        """
        處理單次用戶輸入的核心流程
        """
        logger.info(f"Processing input: '{raw_text}'")
        
        # 1. 解析輸入
        semantic_input = DataParser.parse(raw_text)
        
        # 2. 解鎖知識
        unlocked_keys = self.psi_engine.unlock_knowledge(semantic_input)
        
        # 3. 更新語義場
        self._update_context_field(semantic_input)
        
        # 4. 更新語境穩定相位
        current_phase = self.csp_controller.update_field_state(self.context_field)
        
        # 5. 生成回應
        ai_response_text = self._generate_response(semantic_input, unlocked_keys)
        
        # 6. 記錄對話歷史
        self.echo_resolver.add_dialogue(raw_text, ai_response_text)
        
        # 7. 知識衰減
        self.psi_engine.decay_all_knowledge()
        
        # 8. 封裝輸出
        output = SemanticOutput(
            response_text=ai_response_text,
            session_id=self.session_id,
            current_phase=current_phase,
            stability=self.csp_controller.stability_scores[-1] if self.csp_controller.stability_scores else 0.0,
            tension=self.context_field.semantic_tension,
            unlocked_keys=unlocked_keys,
            analysis_details={
                "tension_analysis": self.tension_analyzer.analyze(raw_text),
                "stability_report": self.csp_controller.get_stability_report()
            }
        )
        
        logger.info(f"Generated response with phase: {current_phase}, tension: {output.tension:.2f}")
        return output

    def get_session_report(self) -> Dict[str, Any]:
        """獲取當前會話的完整報告"""
        return {
            "session_id": self.session_id,
            "session_duration": time.time() - self.session_start_time,
            "config": self.config.load_config(),
            "dialogue_history": self.echo_resolver.get_dialogue_history(),
            "knowledge_base": {k: v.to_dict() for k, v in self.psi_engine.knowledge_base.items()},
            "stability_report": self.csp_controller.get_stability_report()
        }

    def reset_session(self) -> None:
        """重置整個會話狀態"""
        self.psi_engine.reset()
        self.csp_controller.reset()
        self.echo_resolver.reset()
        self.context_field = None
        self.session_id = str(uuid.uuid4())
        self.session_start_time = time.time()
        logger.info(f"Session reset. New session ID: {self.session_id}")

# =======================================================
# Segment 8: 執行範例 (Example Usage)
# =======================================================
if __name__ == '__main__':
    # 1. 初始化配置和引擎
    config = FieldConfig(mode="debug", log_level=logging.INFO)
    engine = SemanticFieldEngine(config)
    
    print(f"初始化語義場引擎，會話 ID: {engine.session_id}\n")
    
    # 2. 模擬對話流程
    dialogue = [
        "你好，我想了解一下關於『深度學習』的基本概念。",
        "那麼，『神經網路』和『深度學習』之間有什麼區別和聯繫？",
        "解釋得很好！可否深入說明一下『卷積神經網路』的應用場景？",
        "我明白了。非常感謝你的詳細解釋！",
        "等一下，我突然想到一個問題，你覺得哲學和AI有關聯嗎？",
        "這個觀點很有趣，特別是『計算機倫理』這個概念，必須深入研究！"
    ]
    
    for i, user_input in enumerate(dialogue):
        print(f"--- 對話回合 {i+1} ---\n使用者輸入: {user_input}")
        
        # 3. 處理輸入並獲取輸出
        output = engine.process_input(user_input)
        
        # 4. 打印簡化回應
        print(f"\nAI 回應:\n{output.response_text}")
        print("-" * 20 + "\n")
        time.sleep(1) # 模擬思考時間

    # 5. 結束時打印會話總結報告
    print("\n\n===================================")
    print("對話結束，生成會話總結報告：")
    print("===================================")
    report = engine.get_session_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))
