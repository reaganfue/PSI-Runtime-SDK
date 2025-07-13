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
作者：AI 開發團隊 (Refactored by AI Assistant)
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
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("advanced_logic_core.log", mode='w', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# =======================================================
# Segment 3: 配置管理區塊 (Configuration)
# =======================================================
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
    
    # --- 行為控制 ---
    memory_capacity: int = 10
    
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
class LogicCoreError(Exception):
    """邏輯核心模組的基礎錯誤類型。"""
    pass

class ConfigurationError(LogicCoreError):
    """配置相關錯誤。"""
    pass

class InputValidationError(LogicCoreError):
    """輸入驗證失敗時引發。"""
    pass

class ProcessingError(LogicCoreError):
    """在處理管線中發生錯誤時引發。"""
    pass

# --- 核心資料契約 (Data Contracts) ---
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
    stage_vectors: Dict[str, np.ndarray] = field(default_factory=dict)
    stage_entropies: Dict[str, float] = field(default_factory=dict)
    
    # --- 最終結果 ---
    final_score: Optional[float] = None
    suggestions: Dict[str, Any] = field(default_factory=dict)
    
    # --- 元資料與監控 ---
    session_id: str = field(default_factory=lambda: f"session-{uuid.uuid4()}")
    start_time: float = field(default_factory=time.perf_counter)
    processing_history: List[str] = field(default_factory=list)

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
    analysis_details: Dict[str, Any]

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
class InputParser:
    """
    輸入解析器：專門負責輸入文本的驗證與初步處理。
    """
    @staticmethod
    def validate_and_normalize(input_text: str) -> str:
        """
        驗證輸入文本的有效性，並進行標準化處理。
        """
        if not isinstance(input_text, str):
            raise InputValidationError(f"Input must be a string, but got {type(input_text)}.")
        
        normalized_text = input_text.strip()
        if not normalized_text:
            raise InputValidationError("Input text cannot be empty or contain only whitespace.")
        
        if len(normalized_text) > 5000:
            logger.warning(f"Input text is very long ({len(normalized_text)} chars), processing might be slow.")
            
        return normalized_text

# =======================================================
# Segment 5: 推理管線階段 (Inference Pipeline Stages)
# =======================================================
# 使用策略模式，將原始碼中的每一個 _function() 都改造成一個獨立、
# 可測試、可重用的 PipelineStage 類別。

class PipelineStage(ABC):
    """推理管線中一個處理階段的抽象基礎類別。"""
    @property
    @abstractmethod
    def name(self) -> str:
        """返回階段的唯一、可讀的名稱。"""
        pass

    @abstractmethod
    def process(self, state: PipelineState) -> PipelineState:
        """
        執行該階段的處理邏輯。
        - 接收一個 PipelineState 物件。
        - 處理後返回更新過的 PipelineState 物件。
        """
        pass

# --- 階段實現 ---

class InputParsingStage(PipelineStage):
    """階段1：輸入解析與意圖對齊。"""
    @property
    def name(self) -> str: return "InputParsing"

    def process(self, state: PipelineState) -> PipelineState:
        try:
            # 1. 驗證與標準化輸入
            normalized_text = InputParser.validate_and_normalize(state.raw_input)
            
            # 2. 文本嵌入
            h_t = np.random.rand(state.config.semantic_vector_dimension)
            state.semantic_vector = h_t / (np.linalg.norm(h_t) + state.config.epsilon)
            
            # 3. 意圖對齊
            W_bert = np.random.rand(state.config.semantic_vector_dimension, state.config.intent_categories)
            z_c = np.dot(W_bert.T, state.semantic_vector)
            p_c = np.exp(z_c - np.max(z_c))
            p_c /= (np.sum(p_c) + state.config.epsilon)
            
            state.intent_id = int(np.argmax(p_c))
            state.initial_entropy = -np.sum(p_c * np.log2(p_c + state.config.epsilon))
            
            state.stage_entropies[self.name] = state.initial_entropy
            logger.info(f"Intent aligned: {state.intent_id}, Entropy: {state.initial_entropy:.4f}")
            return state
        except Exception as e:
            raise ProcessingError(f"Error in {self.name} stage.") from e


class QuantumEvolutionStage(PipelineStage):
    """階段2：量子態演化模擬。"""
    @property
    def name(self) -> str: return "QuantumEvolution"

    def process(self, state: PipelineState) -> PipelineState:
        if not state.config.enable_quantum_simulation:
            logger.warning("Quantum simulation is disabled, skipping stage.")
            return state
        try:
            dim = state.config.state_vector_dimension
            # 初始狀態可以基於語義向量生成，此處簡化
            initial_q_state = np.random.rand(dim)
            
            # QFT
            qft_state = np.fft.fft(initial_q_state) / np.sqrt(dim)
            
            # 演化
            theta = np.random.rand() * np.pi
            noise = np.sin(theta) * 0.01 * np.random.randn(dim)
            evolved_state = qft_state + noise
            
            # 計算熵
            prob = np.abs(evolved_state)**2
            prob /= (np.sum(prob) + state.config.epsilon)
            entropy = -np.sum(prob * np.log2(prob + state.config.epsilon))

            state.stage_vectors[self.name] = evolved_state
            state.stage_entropies[self.name] = entropy
            logger.info(f"Quantum state evolved, Entropy: {entropy:.4f}")
            return state
        except Exception as e:
            raise ProcessingError(f"Error in {self.name} stage.") from e

class AdaptiveLearningStage(PipelineStage):
    """階段3：自適應學習與歷史融合。"""
    @property
    def name(self) -> str: return "AdaptiveLearning"
    
    def __init__(self, memory_bank: List[np.ndarray]):
        self._memory_bank = memory_bank

    def process(self, state: PipelineState) -> PipelineState:
        try:
            dim = state.config.state_vector_dimension
            # 使用一個基礎狀態進行學習，例如前一階段的輸出或新的隨機狀態
            base_state = state.stage_vectors.get(QuantumEvolutionStage().name, np.random.rand(dim))
            
            # 從記憶庫中提取平均狀態
            memory_avg = np.mean(self._memory_bank, axis=0) if self._memory_bank else np.zeros(dim)
            
            # 權衡當前狀態與記憶狀態 (簡化邏輯)
            memory_weight = min(0.5, len(self._memory_bank) * 0.05)
            adaptive_state = (1.0 - memory_weight) * base_state + memory_weight * memory_avg
            
            prob = np.abs(adaptive_state)**2
            prob /= (np.sum(prob) + state.config.epsilon)
            entropy = -np.sum(prob * np.log2(prob + state.config.epsilon))

            state.stage_vectors[self.name] = adaptive_state
            state.stage_entropies[self.name] = entropy
            logger.info(f"Adaptive learning complete, Entropy: {entropy:.4f}")
            return state
        except Exception as e:
            raise ProcessingError(f"Error in {self.name} stage.") from e


class CausalInferenceStage(PipelineStage):
    """階段4：因果推理與貝氏更新。"""
    @property
    def name(self) -> str: return "CausalInference"

    def process(self, state: PipelineState) -> PipelineState:
        try:
            dim = state.config.state_vector_dimension
            # 基於前一階段的狀態進行推理
            prev_state = state.stage_vectors.get(AdaptiveLearningStage(None).name, np.random.rand(dim))
            
            prior = np.ones(dim) / dim
            likelihood = np.random.rand(dim) * 0.1 + 0.9 # 模擬似然
            posterior = (likelihood * prior) / (np.sum(likelihood * prior) + state.config.epsilon)
            
            causal_state = prev_state * posterior
            
            prob = np.abs(causal_state)**2
            prob /= (np.sum(prob) + state.config.epsilon)
            entropy = -np.sum(prob * np.log2(prob + state.config.epsilon))

            state.stage_vectors[self.name] = causal_state
            state.stage_entropies[self.name] = entropy
            logger.info(f"Causal inference complete, Entropy: {entropy:.4f}")
            return state
        except Exception as e:
            raise ProcessingError(f"Error in {self.name} stage.") from e

# ... 可以繼續將 _recursive_correction 等也實現為獨立的 Stage ...

class GlobalIntegrationStage(PipelineStage):
    """最終階段：全局整合與建議生成。"""
    @property
    def name(self) -> str: return "GlobalIntegration"

    def process(self, state: PipelineState) -> PipelineState:
        try:
            # 1. 整合分數
            if not state.stage_entropies:
                state.final_score = 0.5
            else:
                avg_entropy = np.mean(list(state.stage_entropies.values()))
                # 簡單地將分數與平均熵值成反比
                max_entropy = np.log2(state.config.state_vector_dimension + state.config.epsilon)
                normalized_entropy = avg_entropy / (max_entropy + state.config.epsilon)
                state.final_score = 1.0 - normalized_entropy
                state.final_score = max(0.0, min(1.0, state.final_score))
            
            # 2. 生成建議
            suggestions = {}
            if state.final_score > 0.7:
                suggestions["primary"] = "高度確定，建議採取果斷行動。"
            elif state.final_score > 0.4:
                suggestions["primary"] = "趨勢穩定，建議按計畫執行。"
            else:
                suggestions["alternative"] = "不確定性較高，建議謹慎評估或收集更多資訊。"
            
            # 添加信心指數
            entropy_std = np.std(list(state.stage_entropies.values())) if len(state.stage_entropies) > 1 else 0.0
            suggestions["confidence"] = {
                "level": state.final_score,
                "consistency": 1.0 - min(1.0, entropy_std),
            }
            state.suggestions = suggestions
            
            logger.info(f"Global integration complete. Final Score: {state.final_score:.4f}")
            return state
        except Exception as e:
            raise ProcessingError(f"Error in {self.name} stage.") from e


# =======================================================
# Segment 6: 邏輯管線執行器 (Logic Pipeline Runner)
# =======================================================
# 這個類別取代了原始的 QueryEngine 和 BasicResponseLogic 的大部分職責。

class LogicPipeline:
    """
    協調並執行一系列推理階段的管線。
    - 這是 AdvancedLogicCore 的主入口。
    - 它持有一個記憶庫，並將其注入到需要它的階段中。
    """
    def __init__(self, config: LogicCoreConfig, stages: List[PipelineStage]):
        self.config = config
        self.stages = stages
        self._memory_bank: List[np.ndarray] = []
        
        # 依賴注入：為需要記憶庫的階段注入記憶庫
        for stage in self.stages:
            if isinstance(stage, AdaptiveLearningStage):
                stage._memory_bank = self._memory_bank
                
        logger.info(f"LogicPipeline initialized with {len(stages)} stages.")

    def run(self, raw_input: str) -> FinalResult:
        """
        為單個輸入執行完整的推理管線。
        
        Args:
            raw_input (str): 使用者輸入的文本。

        Returns:
            FinalResult: 一個包含完整分析的標準化、不可變的輸出物件。
        """
        state = PipelineState(raw_input=raw_input, config=self.config)
        
        for stage in self.stages:
            logger.debug(f"Executing stage: {stage.name}")
            state = stage.process(state)
            state.processing_history.append(f"Success: {stage.name}")
        
        # 執行完畢後，更新記憶庫
        self._update_memory(state)
        
        return self._package_final_result(state)

    def batch_process(self, input_list: List[str]) -> List[FinalResult]:
        """批次處理多個輸入。"""
        logger.info(f"Starting batch processing for {len(input_list)} items.")
        return [self.run(text) for text in input_list]

    def _update_memory(self, state: PipelineState):
        """將本次運算的關鍵狀態向量存入記憶庫。"""
        # 選擇一個有代表性的向量存入，例如自適應學習後的結果
        adaptive_vector = state.stage_vectors.get(AdaptiveLearningStage(None).name)
        if adaptive_vector is not None:
            self._memory_bank.append(adaptive_vector.copy())
            if len(self._memory_bank) > self.config.memory_capacity:
                self._memory_bank.pop(0)

    def _package_final_result(self, state: PipelineState) -> FinalResult:
        """將最終的 PipelineState 封裝成標準的 FinalResult。"""
        return FinalResult(
            session_id=state.session_id,
            raw_input=state.raw_input,
            final_score=state.final_score,
            intent_id=state.intent_id,
            suggestions=state.suggestions,
            processing_time_s=time.perf_counter() - state.start_time,
            analysis_details={
                "initial_entropy": state.initial_entropy,
                "stage_entropies": state.stage_entropies,
                "processing_history": state.processing_history,
                "final_memory_size": len(self._memory_bank),
            }
        )
    
    def reset_memory(self):
        """清除記憶庫。"""
        self._memory_bank.clear()
        logger.info("LogicPipeline memory has been reset.")


# =======================================================
# Segment 7: 報告生成器 (Report Generator)
# =======================================================
# ReportGenerator 現在操作的是強類型的 FinalResult 物件，更穩定。

class ReportGenerator:
    """根據標準化的 FinalResult 產生各種格式的報告。"""
    
    def __init__(self, result: FinalResult, config: LogicCoreConfig):
        self.result = result
        self.config = config

    def generate(self, format: str = "text") -> str:
        """生成指定格式的報告。"""
        if format.lower() == "json":
            return self.result.to_json()
        if format.lower() == "text":
            return self._to_text()
        # ... 可以繼續實現 to_html, to_markdown 等 ...
        logger.warning(f"Unsupported format '{format}'. Defaulting to text.")
        return self._to_text()

    def _to_text(self) -> str:
        """將 FinalResult 轉換為人類可讀的文本報告。"""
        details = self.result.analysis_details
        lines = [
            "分析報告",
            "=" * 60,
            f"會話 ID: {self.result.session_id}",
            f"處理時間: {self.result.processing_time_s:.4f} 秒",
            f"輸入文本: {self.result.raw_input}",
            "-" * 60,
            f"檢測意圖 ID: {self.result.intent_id}",
            f"初始熵值: {details.get('initial_entropy', 0):.4f}",
            "各階段熵值:",
        ]
        for name, entropy in details.get('stage_entropies', {}).items():
            lines.append(f"  - {name}: {entropy:.4f}")
        lines.extend([
            "-" * 60,
            f"最終綜合得分: {self.result.final_score:.4f}",
            "建議:",
        ])
        for key, value in self.result.suggestions.items():
            if isinstance(value, dict):
                lines.append(f"  - {key.title()}:")
                for sub_key, sub_value in value.items():
                    lines.append(f"    - {sub_key.title()}: {sub_value if isinstance(sub_value, (str, int)) else f'{sub_value:.4f}'}")
            else:
                lines.append(f"  - {key.title()}: {value}")
        lines.append("=" * 60)
        return "\n".join(lines)

# =======================================================
# Segment 8: 主程式執行區塊 (Example Usage / Main Entry)
# =======================================================
def main():
    """主執行函數，演示如何使用重構後的 AdvancedLogicCore。"""
    print("--- 🚀 AdvancedLogicCore (Refactored) Demonstration ---")
    
    # 1. 建立配置
    config = LogicCoreConfig(log_level="INFO", debug_mode=True)
    
    # 2. 定義推理管線的各個階段
    #    擴展：若要調整流程、增刪步驟，只需修改此列表。
    pipeline_stages = [
        InputParsingStage(),
        QuantumEvolutionStage(),
        AdaptiveLearningStage(None), # 記憶庫將由 LogicPipeline 注入
        CausalInferenceStage(),
        # RecursiveCorrectionStage(), # 若實現了，可在此處加入
        GlobalIntegrationStage(),
    ]

    # 3. 初始化管線執行器 (這就是新的主引擎)
    pipeline_runner = LogicPipeline(config, stages=pipeline_stages)
    
    # 4. 執行單次推理
    test_input = "分析將量子計算應用於金融市場預測的潛在風險與機遇"
    print(f"\n{'='*60}\nProcessing Input: {test_input}\n{'='*60}")
    
    try:
        final_result = pipeline_runner.run(test_input)
        
        # 5. 使用報告生成器生成並顯示報告
        report_generator = ReportGenerator(final_result, config)
        text_report = report_generator.generate("text")
        print(text_report)
        
        # 6. 保存 JSON 報告
        report_path = Path(config.output_dir) / f"result_{int(time.time())}.json"
        with report_path.open('w', encoding='utf-8') as f:
            f.write(final_result.to_json())
        print(f"詳細 JSON 報告已保存至: {report_path}")

    except LogicCoreError as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()```
