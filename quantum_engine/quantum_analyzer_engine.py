#!/usr/bin/env python
# coding: utf-8

# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================
"""
模組名稱：AdvancedLogicCore

用途：
    實現一套完整的、企業級的 AI 邏輯流程系統。本模組將一個複雜的、
    多階段的推理過程進行了架構性重構，以管線化的方式處理從自然語言
    輸入到多維度狀態演化，最終生成結構化決策建議的完整流程。

應用場景：
    - 智慧客服系統中的深度意圖理解
    - 複雜決策支援分析
    - 多維度語意理解與知識推理
    - 需要可追溯、可解釋思考過程的高階 AI 應用

結構設計理念：
    1. **分層與管線化 (Layered & Pipelined)**: 將原始設計中的七個核心
       處理步驟（輸入解析→意圖對齊→量子態演化→自適應學習→因果推理→
       遞歸修正→全局整合）抽象為一系列獨立、可插拔的「管線階段」
       (Pipeline Stages)。
    2. **模組化與策略模式 (Modular & Strategy Pattern)**: 每個處理階段
       都是一個獨立的模組（策略），可以被輕易地替換、重排或擴展，而
       不影響管線的其他部分。
    3. **可觀測性與資料契約 (Observability & Data Contracts)**: 整個
       推理流程中的狀態由一個統一的、強類型的 `PipelineState` 物件承載，
       取代了易錯的字典。這使得資料的流動清晰可見，並提供了完整的日誌
       追蹤與錯誤處理機制。
    4. **可擴展性 (Extensibility)**: 架構本身為未來的擴展預留了清晰的
       介面，例如支持更複雜的「未來語境生成」或「人機融合推理」作為
       新的管線階段加入。

版本：2.0.0
作者：Reagan Fu 開發團隊 
更新日期：2025-07-14
"""

# =======================================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# =======================================================
# --- 標準庫 ---
from __future__ import annotations
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# --- 第三方庫 ---
import numpy as np

# --- 日誌設定 ---
# 在配置類中進行更細緻的初始化，此處為基礎設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("advanced_logic_core.log", mode='w', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# --- 全域常數 ---
# 這些常數將被遷移到配置類中，以實現更好的管理，此處保留作為參考
# EPS = 1e-8
# K = 10
# N_STATE = 10
# DEFAULT_TIMEOUT = 30
# GLOBAL_DIMENSIONS = ["知識深度", "時間推理", "情境理解"]

# =======================================================
# Segment 3: 配置管理區塊 (Configuration)
# =======================================================
# 將原始的 ModelConfig 和 Config 類別整合為一個統一、強類型的配置中心。

@dataclass
class LogicCoreConfig:
    """
    邏輯核心的統一配置中心。
    - 集中管理所有可調參數，取代了原有的 Config 和 ModelConfig。
    - 支援從檔案載入、保存和動態更新。
    """
    # --- 系統行為配置 ---
    log_level: str = "INFO"
    debug_mode: bool = False
    output_dir: str = "./output"

    # --- 演算法超參數 (原 ModelConfig) ---
    learning_rate: float = 0.01
    max_iterations: int = 100
    convergence_threshold: float = 0.001
    enable_quantum_simulation: bool = True
    causal_weight: float = 0.5
    
    # --- 維度和意圖配置 ---
    intent_categories: int = 10
    state_vector_dimension: int = 10
    semantic_vector_dimension: int = 768 # 模擬 BERT 的維度
    global_dimensions: List[str] = field(default_factory=lambda: ["知識深度", "時間推理", "情境理解"])
    
    # --- 數值穩定性 ---
    epsilon: float = 1e-8

    def __post_init__(self):
        """配置實例化後執行的初始化邏輯。"""
        # 1. 設置日誌級別
        numeric_level = getattr(logging, self.log_level.upper(), logging.INFO)
        if isinstance(numeric_level, int):
            logging.getLogger().setLevel(numeric_level)
            logger.info(f"Logger level set to '{self.log_level.upper()}'.")
        
        # 2. 確保輸出目錄存在
        Path(self.output_dir).mkdir(exist_ok=True, parents=True)
        logger.debug(f"Output directory ensured at: '{self.output_dir}'.")
    
    def update(self, **kwargs) -> None:
        """動態、安全地更新配置參數。"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logger.debug(f"Configuration updated: {key} = {value}")
            else:
                logger.warning(f"Attempted to update unknown config parameter: '{key}'.")

    @classmethod
    def from_file(cls, path: str | Path) -> LogicCoreConfig:
        """從 JSON 檔案安全地載入配置，並返回一個新的配置實例。"""
        config_path = Path(path)
        if not config_path.is_file():
            raise ConfigurationError(f"Config file not found at: {config_path}")
        try:
            with config_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(**data)
        except (json.JSONDecodeError, TypeError) as e:
            raise ConfigurationError(f"Failed to load or parse config from '{config_path}': {e}")

    def save_to_file(self, path: str | Path) -> None:
        """將當前配置儲存到 JSON 檔案。"""
        config_path = Path(path)
        try:
            with config_path.open('w', encoding='utf-8') as f:
                json.dump(asdict(self), f, indent=4, ensure_ascii=False)
            logger.info(f"Configuration successfully saved to '{config_path}'.")
        except Exception as e:
            raise ConfigurationError(f"Failed to save config to '{config_path}': {e}")

# =======================================================
# Segment 4: 資料結構 / 解析區塊 (Data Structures)
# =======================================================
# --- 自訂錯誤類型 ---
# 將原始的錯誤類別繼承自一個統一的基礎錯誤，便於上層統一捕獲。

class LogicCoreError(Exception):
    """邏輯核心模組的基礎錯誤類型。"""
    pass

class InputValidationError(LogicCoreError):
    """輸入驗證失敗時引發。"""
    pass

class ProcessingError(LogicCoreError):
    """在處理管線中發生錯誤時引發。"""
    pass

# --- 核心資料契約 (Data Contracts) ---
# 使用強類型的 dataclass 取代原始的、分散的資料結構。

@dataclass
class PipelineState:
    """
    在推理管線中流動的統一狀態物件。
    - 這個物件是可變的，它會被每個管線階段逐步地豐富和修改。
    - 它取代了原始設計中分散的 `InputContext`, `DimensionState` 和
      在各個方法間傳遞的大型字典。
    """
    # --- 初始輸入與配置 ---
    raw_input: str
    config: LogicCoreConfig
    
    # --- 輸入解析階段產出 ---
    semantic_vector: Optional[np.ndarray] = None
    intent_id: Optional[int] = None
    initial_entropy: Optional[float] = None
    
    # --- 各階段的狀態與熵值 ---
    # 這個字典將儲存每個階段（如量子演化、因果推理等）的核心輸出狀態向量
    stage_vectors: Dict[str, np.ndarray] = field(default_factory=dict)
    # 這個字典將儲存每個階段計算出的熵值，便於追蹤和整合
    stage_entropies: Dict[str, float] = field(default_factory=dict)
    
    # --- 最終結果 ---
    final_score: Optional[float] = None
    suggestions: Dict[str, Any] = field(default_factory=dict)
    
    # --- 元資料與監控 ---
    session_id: str = field(default_factory=lambda: f"session-{uuid.uuid4()}")
    start_time: float = field(default_factory=time.perf_counter)
    processing_history: List[str] = field(default_factory=list) # 記錄每個階段的執行狀態

@dataclass(frozen=True)
class FinalResult:
    """
    標準化的、不可變的最終輸出物件。
    - 這是整個邏輯核心提供給外部呼叫者的最終產物。
    - 它融合了原始 `InferenceResult` 的概念，但結構更清晰。
    """
    session_id: str
    raw_input: str
    final_score: float
    intent_id: int
    suggestions: Dict[str, Any]
    processing_time_s: float
    analysis_details: Dict[str, Any] # 用於儲存詳細的中間過程，如各階段的熵值

    def to_json(self, indent: int = 2) -> str:
        """將結果序列化為 JSON 字串，並處理 NumPy 等特殊類型。"""
        def json_encoder(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, (np.float32, np.float64)):
                return float(obj)
            return str(obj)
        
        return json.dumps(asdict(self), indent=indent, ensure_ascii=False, default=json_encoder)

# --- 資料解析器 ---
# DataParser 的職責被重新定義，更專注於純粹的「解析」與「驗證」。
# 意圖對齊等更複雜的邏輯將被移到管線的第一個階段中。
class InputParser:
    """
    輸入解析器：專門負責輸入文本的驗證與初步處理。
    """
    @staticmethod
    def validate_and_normalize(input_text: str) -> str:
        """
        驗證輸入文本的有效性，並進行標準化處理。
        
        Args:
            input_text (str): 使用者輸入的原始文本。

        Returns:
            str: 經過清理和驗證後的文本。

        Raises:
            InputValidationError: 當輸入無效時（例如，非字串、空字串）。
        """
        if not isinstance(input_text, str):
            raise InputValidationError(f"Input must be a string, but got {type(input_text)}.")
        
        normalized_text = input_text.strip()
        if not normalized_text:
            raise InputValidationError("Input text cannot be empty or contain only whitespace.")
        
        if len(normalized_text) > 5000: # 可配置的長度限制
            logger.warning(f"Input text is very long ({len(normalized_text)} chars), processing might be slow.")
            
        return normalized_text

# =======================================================
# Segment 5: 核心資料結構 (Core Data Structures)
# =======================================================
# 引入了代表核心狀態的 SemanticFieldContext

@dataclass
class KnowledgeAnchor:
    """代表一個被解鎖的知識錨點。"""
    key: str
    activation_level: float = 1.0
    # ... 可擴展更多屬性，如來源、向量表示等 ...

@dataclass
class SemanticFieldContext:
    """
    【核心】代表一個持續演化的語義場。
    這是一個可變的物件，承載了整個對話的狀態。
    """
    session_id: str
    field_vector: np.ndarray  # 主語義場向量
    stability: float = 0.0  # 當前場的穩定性
    phase: str = "unlocking"  # 當前所處階段: unlocking, expanding, collapsing, refocusing, stable
    dialogue_history: List[str] = field(default_factory=list)
    knowledge_anchors: Dict[str, KnowledgeAnchor] = field(default_factory=dict)
    
@dataclass(frozen=True)
class EngineOutput:
    """單次 process 呼叫的標準化、不可變輸出。"""
    session_id: str
    response_text: str
    current_phase: str
    current_stability: float
    analysis_payload: Optional[Dict] = None # 用於存放擴展分析的結果

# =======================================================
# Segment 6: 內部服務與分析工具 (Internal Services & Tools)
# =======================================================
# 將原有的功能拆分為更小的服務或工具

class KnowledgeUnlocker:
    """服務1：負責知識解鎖。"""
    @staticmethod
    def unlock(text: str, context: SemanticFieldContext) -> SemanticFieldContext:
        # 模擬從文本中提取關鍵字作為知識點
        new_keys = [word for word in text.split() if len(word) > 3]
        for key in new_keys:
            if key not in context.knowledge_anchors:
                context.knowledge_anchors[key] = KnowledgeAnchor(key=key)
                logger.info(f"Knowledge unlocked: '{key}'")
            else:
                # 重新激活已存在的知識點
                context.knowledge_anchors[key].activation_level = 1.0
        return context

class CSPController:
    """服務2：負責計算穩定性與控制相位轉換。"""
    @staticmethod
    def update(new_vector: np.ndarray, context: SemanticFieldContext, config: PsiRuntimeConfig) -> SemanticFieldContext:
        if np.all(context.field_vector == 0): # 首次運行
            context.stability = 0.5
        else:
            # 計算與前一狀態的餘弦相似度作為穩定性
            similarity = np.dot(new_vector, context.field_vector) / (np.linalg.norm(new_vector) * np.linalg.norm(context.field_vector) + EPSILON)
            context.stability = (similarity + 1) / 2 # 歸一化到 [0, 1]
        
        # 根據穩定性更新相位 (簡化邏輯)
        if context.stability > config.stability_threshold:
            context.phase = "stable"
        elif context.stability > context.stability * 0.9: # 穩定性在增加
            context.phase = "expanding"
        else: # 穩定性在下降
            context.phase = "collapsing"
            
        logger.info(f"CSP updated. Stability: {context.stability:.4f}, Phase: {context.phase}")
        return context

class QuantumAnalysisTool:
    """分析工具：提供量子啟發式分析能力 (原 QuantumSimulationPipeline)。"""
    def __init__(self, config: PsiRuntimeConfig):
        self.config = config

    def run(self, text: str) -> Dict:
        # 此處嵌入原 QuantumSimulationPipeline 的邏輯
        # ... 省略詳細實現，返回一個字典結果 ...
        logger.info("QuantumAnalysisTool executed.")
        return {"quantum_score": np.random.rand(), "comment": "Quantum analysis complete."}


# =======================================================
# Segment 7: PSI 運行時主引擎 (PSI Runtime Engine)
# =======================================================
class PsiRuntimeException:
    """
    PSI 運行時主引擎。
    - 管理 SemanticFieldContext 的生命週期。
    - 實現 `unlock -> expand -> collapse -> refocus` 的處理循環。
    """
    def __init__(self, config: PsiRuntimeConfig):
        self.config = config
        
        # --- 依賴注入內部服務和工具 ---
        self.knowledge_unlocker = KnowledgeUnlocker()
        self.csp_controller = CSPController()
        # 工具是可選的，可以在需要時才初始化和調用
        self.quantum_tool = QuantumAnalysisTool(config) if config else None
        
        logger.setLevel(getattr(logging, config.log_level.upper()))
        logger.info("PsiRuntimeException initialized.")

    def create_new_context(self) -> SemanticFieldContext:
        """創建一個全新的、空的語義場上下文。"""
        session_id = f"psi-session-{uuid.uuid4()}"
        return SemanticFieldContext(
            session_id=session_id,
            field_vector=np.zeros(self.config.field_dimension)
        )

    def process(self, text: str, context: SemanticFieldContext) -> Tuple[EngineOutput, SemanticFieldContext]:
        """
        【核心方法】處理單次輸入，並演化語義場。

        Args:
            text (str): 最新的使用者輸入。
            context (SemanticFieldContext): 當前的語義場狀態。

        Returns:
            Tuple[EngineOutput, SemanticFieldContext]: (本次處理的輸出, 更新後的語義場狀態)
        """
        logger.info(f"Processing text for session {context.session_id} in phase '{context.phase}'")
        context.dialogue_history.append(text)

        # 1. 解鎖 (Unlock)
        context = self.knowledge_unlocker.unlock(text, context)
        
        # --- 根據當前相位執行不同邏輯 ---
        analysis_payload = None
        
        # 2. 擴展 (Expand)
        # 在擴展階段，我們可以調用昂貴的分析工具來獲取更深層的洞見
        if context.phase == "expanding":
            logger.info("Phase is 'expanding', running advanced analysis tools.")
            if self.quantum_tool:
                analysis_payload = self.quantum_tool.run(text)
        
        # 3. 坍縮 (Collapse) & 4. 重聚焦 (Refocus)
        # 此處可以加入更複雜的邏輯，例如修剪不活躍的知識錨點或重新計算場向量
        
        # --- 更新語義場向量與穩定性 ---
        # 簡化模擬：將新文本向量和知識向量加權平均到舊的場向量中
        text_vector = self._embed_text(text)
        # 這裡可以加入更複雜的知識向量融合邏輯
        knowledge_vector = self._embed_text(" ".join(context.knowledge_anchors.keys()))

        # 簡單的加權更新
        new_field_vector = (
            context.field_vector * 0.7 +
            text_vector * 0.2 +
            knowledge_vector * 0.1
        )
        new_field_vector /= (np.linalg.norm(new_field_vector) + EPSILON)

        # 更新穩定性與相位
        context = self.csp_controller.update(new_field_vector, context)
        context.field_vector = new_field_vector # 更新場向量

        # --- 生成本次回應 ---
        response_text = self._generate_response(context)
        
        output = EngineOutput(
            session_id=context.session_id,
            response_text=response_text,
            current_phase=context.phase,
            current_stability=context.stability,
            analysis_payload=analysis_payload
        )
        
        return output, context
    
    def _embed_text(self, text: str) -> np.ndarray:
        """模擬文本嵌入。"""
        seed = hash(text)
        rng = np.random.default_rng(seed)
        vector = rng.random(self.config.field_dimension)
        return vector / (np.linalg.norm(vector) + EPSILON)

    def _generate_response(self, context: SemanticFieldContext) -> str:
        """根據當前語義場狀態生成回應。"""
        response = f"Phase: {context.phase}, Stability: {context.stability:.2f}. "
        if context.phase == "stable":
            response += "Context is stable. Ready for deep reasoning."
        elif context.phase == "expanding":
            response += "Context is expanding with new knowledge."
        elif context.phase == "collapsing":
            response += "Context seems to be collapsing. Suggest refocusing."
        else:
            response += f"Unlocked {len(context.knowledge_anchors)} knowledge anchors."
        return response

# =======================================================
# Segment 8/9/10: API, CLI 和主執行範例
# =======================================================
# ... API 和 CLI 的部分可以保持，但需要調整以適應新的引擎交互模式 ...
# ... (例如，API 需要管理 session 狀態，將 context 物件存儲在記憶體或快取中) ...

def run_runtime_demonstration():
    """演示 PSI Runtime 的動態、多輪對話處理能力。"""
    print("--- 🚀 PSI Runtime Engine Demonstration ---")
    
    # 1. 初始化配置和運行時引擎
    config = PsiRuntimeConfig(log_level="INFO")
    engine = PsiRuntimeException(config)

    # 2. 創建一個新的對話會話 (語義場)
    context = engine.create_new_context()
    print(f"New session started: {context.session_id}\n")

    # 3. 模擬多輪對話
    dialogue = [
        "我想了解一下關於『語義場理論』的基本概念。",
        "這個理論聽起來很有趣，特別是『知識解鎖』這個機制。",
        "那麼當上下文持續擴展時，穩定性是如何計算的？",
        "我明白了。當穩定性下降時，系統會如何應對？",
        "好的，感謝你的解釋。我們現在似乎對這個主題達成了共識。"
    ]

    for i, user_input in enumerate(dialogue):
        print(f"--- Turn {i+1} ---")
        print(f"User: {user_input}")
        
        # 4. 調用 process 方法，傳入當前的 context
        output, updated_context = engine.process(user_input, context)
        
        # 5. 更新 context 以便下一輪使用
        context = updated_context
        
        # 6. 打印本次的輸出
        print(f"Engine: {output.response_text}")
        if output.analysis_payload:
            print(f"  -> Analysis Payload: {output.analysis_payload}")
        print("-" * 15 + "\n")
        time.sleep(1)

    print("--- 🏁 Demonstration Finished ---")


if __name__ == "__main__":
    run_runtime_demonstration()
    
    # 若要啟動 CLI，請使用: python your_script_name.py analyze --text "some text"
    # cli()
    
    # 若要啟動 API 伺服器，請使用: uvicorn your_script_name:app --reload
    # if uvicorn:
    #     uvicorn.run(app, host="0.0.0.0", port=8000)
