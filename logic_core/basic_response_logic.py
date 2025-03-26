#!/usr/bin/env python
# coding: utf-8
"""
# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================

模組名稱：Basic_Response_Logic
用途：實現一套完整的 AI 邏輯流程系統，處理從自然語言輸入到量子態演化的推理過程
應用場景：智能客服、決策支援、語意理解、知識推理等情境
結構設計理念：
    1. 分層處理：從輸入解析→意圖對齊→量子態演化→自適應學習→因果推理→遞歸修正→全局整合
    2. 模組化設計：每個步驟皆有獨立模組，可替換或擴展
    3. 可觀測性：完整的日誌追蹤與錯誤處理機制
    4. 可擴展性：支持未來語境生成與人機融合推理

版本：1.0.0
作者：AI 開發團隊
更新日期：2025-03-12
"""

# =======================================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# =======================================================

import logging
import math
import json
import os
import sys
import time
import numpy as np
import datetime
from typing import Any, Dict, List, Tuple, Union, Optional
from dataclasses import dataclass, field

# 設定 Logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("basic_response_logic.log")
    ]
)
logger = logging.getLogger(__name__)

# 全域常數
EPS = 1e-8  # 數值穩定性常數
K = 10      # 意圖類別數量
N_STATE = 10  # 量子態向量維度
DEFAULT_TIMEOUT = 30  # 秒
GLOBAL_DIMENSIONS = ["知識深度", "時間推理", "情境理解"]  # 全域維度列表

# =======================================================
# Segment 3: 配置管理區塊 (Configuration)
# =======================================================

@dataclass
class ModelConfig:
    """模型配置數據類，包含所有可調參數"""
    learning_rate: float = 0.01
    max_iterations: int = 100
    convergence_threshold: float = 0.001
    use_quantum_simulation: bool = True
    causal_weight: float = 0.5

class Config:
    """
    配置管理類別，負責管理系統運行所需的所有設定。
    
    功能:
    - 載入/保存配置
    - 更新運行時參數
    - 提供默認參數
    - 維護系統狀態
    """
    def __init__(self, timestamp: str = None, model_config: ModelConfig = None, 
                 log_level: str = "INFO", debug_mode: bool = False):
        """
        初始化配置管理器
        
        參數:
            timestamp (str, optional): 時間戳記，預設為當前UTC時間
            model_config (ModelConfig, optional): 模型參數配置
            log_level (str, optional): 日誌級別，可選 DEBUG/INFO/WARNING/ERROR/CRITICAL
            debug_mode (bool, optional): 是否啟用調試模式
        """
        self.timestamp = timestamp or datetime.datetime.utcnow().isoformat()
        self.model_config = model_config or ModelConfig()
        self.log_level = log_level
        self.debug_mode = debug_mode
        self._init_logging()
        
        # 系統路徑配置
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(self.base_path, "data")
        self.output_path = os.path.join(self.base_path, "output")
        
        # 確保必要目錄存在
        self._ensure_directories()
        logger.info(f"配置初始化完成，時間戳: {self.timestamp}")
    
    def _init_logging(self) -> None:
        """設置日誌級別"""
        numeric_level = getattr(logging, self.log_level.upper(), None)
        if isinstance(numeric_level, int):
            logger.setLevel(numeric_level)
    
    def _ensure_directories(self) -> None:
        """確保所需目錄存在"""
        for path in [self.data_path, self.output_path]:
            if not os.path.exists(path):
                os.makedirs(path)
                logger.debug(f"已創建目錄: {path}")
    
    def update_config(self, **kwargs) -> None:
        """
        更新配置參數
        
        參數:
            **kwargs: 鍵值對格式的配置參數
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logger.debug(f"更新配置: {key} = {value}")
            elif hasattr(self.model_config, key):
                setattr(self.model_config, key, value)
                logger.debug(f"更新模型配置: {key} = {value}")
            else:
                logger.warning(f"無法識別的配置參數: {key}")
    
    def load_config(self, config_file: str = None) -> Dict[str, Any]:
        """
        從檔案載入配置或返回當前配置
        
        參數:
            config_file (str, optional): 配置檔案路徑
            
        返回:
            Dict[str, Any]: 配置字典
        """
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.update_config(**loaded_config)
                    logger.info(f"已從 {config_file} 載入配置")
                    return loaded_config
            except Exception as e:
                logger.error(f"載入配置檔案時發生錯誤: {e}")
        
        # 返回當前配置
        return {
            "timestamp": self.timestamp,
            "global_dimensions": GLOBAL_DIMENSIONS,
            "log_level": self.log_level,
            "debug_mode": self.debug_mode,
            "model_config": self.model_config.__dict__
        }
    
    def save_config(self, config_file: str) -> bool:
        """
        保存當前配置到檔案
        
        參數:
            config_file (str): 配置檔案路徑
            
        返回:
            bool: 成功保存返回 True，否則返回 False
        """
        try:
            # 創建配置字典
            config_dict = self.load_config()
            
            # 寫入檔案
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
            
            logger.info(f"配置已保存至 {config_file}")
            return True
        except Exception as e:
            logger.error(f"保存配置時發生錯誤: {e}")
            return False

# =======================================================
# Segment 4: 資料結構 / 解析區塊 (Data Structures)
# =======================================================

class InputValidationError(Exception):
    """輸入驗證錯誤類"""
    pass

class ProcessingError(Exception):
    """處理過程錯誤類"""
    pass

@dataclass
class InputContext:
    """輸入上下文數據類"""
    text: str
    timestamp: str
    semantic_vector: np.ndarray = None
    intent: int = -1
    entropy: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DimensionState:
    """維度狀態數據類"""
    name: str
    state: np.ndarray
    entropy: float = 0.0
    weight: float = 0.0
    confidence: float = 0.0

@dataclass
class InferenceResult:
    """推理結果數據類"""
    input_text: str
    intent: int
    dimensions: Dict[str, DimensionState]
    final_score: float
    suggestions: Dict[str, Any]
    timestamp: str
    processing_time: float
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式"""
        result = {
            "input_text": self.input_text,
            "intent": self.intent,
            "dimensions": {},
            "final_score": self.final_score,
            "suggestions": self.suggestions,
            "timestamp": self.timestamp,
            "processing_time": self.processing_time
        }
        
        # 處理維度狀態轉換
        for dim_name, dim_state in self.dimensions.items():
            result["dimensions"][dim_name] = {
                "entropy": dim_state.entropy,
                "weight": dim_state.weight,
                "confidence": dim_state.confidence
            }
        
        return result

class DataParser:
    """
    資料解析器：負責輸入文本的處理、解析和向量化
    
    主要功能:
    - 驗證輸入格式
    - 將文本轉換為語義向量
    - 計算意圖對齊與信息熵
    - 初始化上下文結構
    """
    
    @staticmethod
    def validate_input(input_text: str) -> bool:
        """
        驗證輸入文本是否有效
        
        參數:
            input_text (str): 輸入文本
            
        返回:
            bool: 是否有效
            
        異常:
            InputValidationError: 當輸入無效時
        """
        if not isinstance(input_text, str):
            raise InputValidationError("輸入必須是字符串類型")
        
        if not input_text.strip():
            raise InputValidationError("輸入不能為空")
        
        if len(input_text) > 1000:
            logger.warning("輸入文本過長，可能影響處理效率")
        
        return True

    @staticmethod
    def parse_input(input_text: str) -> np.ndarray:
        """
        解析輸入並生成語義向量
        
        參數:
            input_text (str): 輸入文本
            
        返回:
            np.ndarray: 語義向量表示
        """
        try:
            DataParser.validate_input(input_text)
            logger.info(f"解析輸入文本 (長度: {len(input_text)}) 並生成語義向量")
            
            # 模擬 BERT 或其他嵌入模型的輸出，生成 768 維向量
            # 實際實現可以接入真實的語言模型
            h_t = np.random.rand(768)
            h_t = h_t / np.linalg.norm(h_t)  # 標準化
            
            return h_t
        except Exception as e:
            logger.error(f"解析輸入時發生錯誤: {e}")
            raise ProcessingError(f"無法解析輸入: {str(e)}")

    @staticmethod
    def align_intent(h_t: np.ndarray) -> Tuple[int, float]:
        """
        進行意圖對齊並計算信息熵
        
        參數:
            h_t (np.ndarray): 語義向量
            
        返回:
            Tuple[int, float]: (意圖索引, 信息熵)
        """
        logger.info("計算意圖得分與熵值")
        try:
            # 模擬意圖分類器，定義權重矩陣 W_bert (768 x K)
            W_bert = np.random.rand(768, K)
            
            # 計算意圖得分：z_c = W_bert^T * h_t
            z_c = np.dot(W_bert.T, h_t)
            
            # 計算 softmax
            z_c_max = np.max(z_c)
            exp_z = np.exp(z_c - z_c_max)
            p_c = exp_z / (np.sum(exp_z) + EPS)
            
            # 選擇意圖：argmax
            intent = int(np.argmax(p_c))
            
            # 計算熵值 H(p_c)
            H_p_c = -np.sum(p_c * np.log2(p_c + EPS))
            
            logger.debug(f"意圖: {intent}, 熵值: {H_p_c:.4f}")
            return intent, H_p_c
        except Exception as e:
            logger.error(f"意圖對齊時發生錯誤: {e}")
            # 出錯時返回默認值
            return 0, 1.0

    @staticmethod
    def create_context(input_text: str, timestamp: str, semantic_vector: np.ndarray, 
                       intent: int, entropy: float) -> InputContext:
        """
        創建輸入上下文
        
        參數:
            input_text (str): 輸入文本
            timestamp (str): 時間戳
            semantic_vector (np.ndarray): 語義向量
            intent (int): 意圖索引
            entropy (float): 意圖熵
            
        返回:
            InputContext: 輸入上下文對象
        """
        return InputContext(
            text=input_text,
            timestamp=timestamp,
            semantic_vector=semantic_vector,
            intent=intent,
            entropy=entropy,
            metadata={
                "length": len(input_text),
                "processed_time": datetime.datetime.utcnow().isoformat()
            }
        )

# =======================================================
# Segment 5: 查詢引擎 (Query Engine)
# =======================================================

class QueryEngine:
    """
    查詢引擎：負責協調整個推理流程的執行
    
    主要功能:
    - 整合各個處理模塊
    - 提供統一的 API 接口
    - 控制推理流程與資源
    - 處理執行異常
    """
    
    def __init__(self, config: Config):
        """
        初始化查詢引擎
        
        參數:
            config (Config): 系統配置
        """
        self.config = config
        self.logic_engine = BasicResponseLogic()
        logger.info("查詢引擎初始化完成")
    
    def run_inference_pipeline(self, input_text: str) -> Dict[str, Any]:
        """
        執行完整推理流程
        
        參數:
            input_text (str): 輸入文本
            
        返回:
            Dict[str, Any]: 推理結果
        """
        start_time = time.time()
        logger.info(f"啟動推理流程，輸入: '{input_text[:50]}...' (如果較長)")
        
        try:
            # 執行核心推理流程
            result = self.logic_engine.run(input_text, self.config)
            
            # 記錄執行時間
            processing_time = time.time() - start_time
            logger.info(f"推理完成，耗時: {processing_time:.4f}秒")
            
            # 添加處理時間到結果
            if isinstance(result, dict):
                result["processing_time"] = processing_time
            
            return result
        except InputValidationError as e:
            logger.error(f"輸入驗證失敗: {e}")
            return {"error": "輸入驗證失敗", "message": str(e), "status": "error"}
        except ProcessingError as e:
            logger.error(f"處理過程失敗: {e}")
            return {"error": "處理過程失敗", "message": str(e), "status": "error"}
        except Exception as e:
            logger.error(f"推理過程中發生未預期錯誤: {e}", exc_info=True)
            return {"error": "系統錯誤", "message": str(e), "status": "error"}
    
    def quick_query(self, input_text: str) -> str:
        """
        快速查詢模式 - 使用預設配置執行簡化流程
        
        參數:
            input_text (str): 輸入文本
            
        返回:
            str: 簡化的結果描述
        """
        try:
            result = self.run_inference_pipeline(input_text)
            if "error" in result:
                return f"查詢失敗: {result['message']}"
            
            if "final_result" in result:
                return f"查詢結果: {result['final_result']:.4f}, 一致性: {result['consistency']}"
            
            return f"查詢完成，但結果格式不完整"
        except Exception as e:
            logger.error(f"快速查詢失敗: {e}")
            return f"查詢異常: {str(e)}"
    
    def batch_process(self, input_list: List[str]) -> List[Dict[str, Any]]:
        """
        批次處理多個輸入
        
        參數:
            input_list (List[str]): 輸入文本列表
            
        返回:
            List[Dict[str, Any]]: 結果列表
        """
        logger.info(f"開始批次處理 {len(input_list)} 個查詢")
        results = []
        
        for idx, input_text in enumerate(input_list):
            logger.info(f"處理第 {idx+1}/{len(input_list)} 個查詢")
            result = self.run_inference_pipeline(input_text)
            results.append(result)
        
        logger.info(f"批次處理完成，共 {len(results)} 個結果")
        return results

# =======================================================
# Segment 6: 報告生成器 (Report Generator)
# =======================================================

class ReportGenerator:
    """
    報告生成器：根據分析結果產生各種格式的報告
    
    主要功能:
    - 生成不同格式的報告 (JSON, HTML, Markdown)
    - 數據可視化
    - 結果摘要與統計
    - 報告存檔與輸出
    """
    
    def __init__(self, result: Dict[str, Any], config: Optional[Config] = None):
        """
        初始化報告生成器
        
        參數:
            result (Dict[str, Any]): 推理結果
            config (Config, optional): 系統配置
        """
        self.result = result
        self.config = config or Config()
        logger.info("報告生成器初始化完成")
    
    def generate_report(self, format: str = "json") -> Any:
        """
        生成指定格式的報告
        
        參數:
            format (str): 報告格式，支持 "json", "text", "html", "md"
            
        返回:
            Any: 生成的報告內容
        """
        logger.info(f"生成 {format} 格式報告")
        
        if "error" in self.result:
            logger.warning("結果包含錯誤，生成錯誤報告")
            return self._generate_error_report(format)
        
        try:
            if format.lower() == "json":
                return self._to_json()
            elif format.lower() == "text":
                return self._to_text()
            elif format.lower() == "html":
                return self._to_html()
            elif format.lower() == "md" or format.lower() == "markdown":
                return self._to_markdown()
            else:
                logger.warning(f"不支持的報告格式: {format}，使用默認的 JSON 格式")
                return self._to_json()
        except Exception as e:
            logger.error(f"生成報告時發生錯誤: {e}")
            return f"報告生成失敗: {str(e)}"
    
    def _generate_error_report(self, format: str) -> Any:
        """生成錯誤報告"""
        error_msg = self.result.get("message", "未知錯誤")
        error_type = self.result.get("error", "錯誤")
        
        if format.lower() == "json":
            return json.dumps(self.result, indent=4, ensure_ascii=False)
        else:
            return f"錯誤報告\n{'='*60}\n類型: {error_type}\n消息: {error_msg}\n{'='*60}"
    
    def _to_json(self) -> str:
        """轉換為 JSON 格式"""
        return json.dumps(self.result, indent=4, ensure_ascii=False)
    
    def _to_text(self) -> str:
        """轉換為純文本格式"""
        lines = [
            "分析報告",
            "="*60,
            f"輸入文本: {self.result.get('context', {}).get('input', '未提供')}",
            f"時間戳: {self.result.get('context', {}).get('timestamp', '未提供')}",
            f"意圖: {self.result.get('intent', '未知')}",
            f"熵值: {self.result.get('H_intent', 0):.4f}",
            "-"*60,
            "維度分析:",
        ]
        
        # 添加維度信息
        dimensions = self.result.get("context", {}).get("dimensions", {})
        for dim, data in dimensions.items():
            lines.append(f"  - {dim}: 熵值={data.get('entropy', 0):.4f}, 權重={data.get('weight', 0):.4f}")
        
        lines.extend([
            "-"*60,
            f"最終結果: {self.result.get('final_result', 0):.4f}",
            f"一致性: {self.result.get('consistency', '未知')}",
            "-"*60,
            "建議:",
        ])
        
        # 添加建議
        suggestions = self.result.get("suggestions", {})
        for sug_type, sug_data in suggestions.items():
            if isinstance(sug_data, list):
                lines.append(f"  {sug_type}:")
                for item in sug_data:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            lines.append(f"    - {k}: {v}")
                    else:
                        lines.append(f"    - {item}")
            else:
                lines.append(f"  {sug_type}: {sug_data}")
        
        lines.append("="*60)
        
        return "\n".join(lines)
    
    def _to_html(self) -> str:
        """轉換為 HTML 格式"""
        # 這裡提供一個簡單的 HTML 模板
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>分析報告</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
                .section {{ margin: 15px 0; }}
                .footer {{ margin-top: 30px; font-size: 0.8em; color: #666; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>語義分析報告</h1>
                <p>生成時間: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            
            <div class="section">
                <h2>基本信息</h2>
                <p><strong>輸入文本:</strong> {self.result.get('context', {}).get('input', '未提供')}</p>
                <p><strong>意圖:</strong> {self.result.get('intent', '未知')}</p>
                <p><strong>熵值:</strong> {self.result.get('H_intent', 0):.4f}</p>
            </div>
            
            <div class="section">
                <h2>最終結果</h2>
                <p><strong>結果值:</strong> {self.result.get('final_result', 0):.4f}</p>
                <p><strong>一致性:</strong> {self.result.get('consistency', '未知')}</p>
            </div>
            
            <div class="footer">
                <p>報告由 BasicResponseLogic 自動生成</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def _to_markdown(self) -> str:
        """轉換為 Markdown 格式"""
        md = [
            "# 語義分析報告",
            "",
            f"生成時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 基本信息",
            "",
            f"- **輸入文本:** {self.result.get('context', {}).get('input', '未提供')}",
            f"- **意圖:** {self.result.get('intent', '未知')}",
            f"- **熵值:** {self.result.get('H_intent', 0):.4f}",
            "",
            "## 維度分析",
            ""
        ]
        
        # 添加維度信息
        dimensions = self.result.get("context", {}).get("dimensions", {})
        for dim, data in dimensions.items():
            md.append(f"- **{dim}:** 熵值={data.get('entropy', 0):.4f}, 權重={data.get('weight', 0):.4f}")
        
        md.extend([
            "",
            "## 最終結果",
            "",
            f"- **結果值:** {self.result.get('final_result', 0):.4f}",
            f"- **一致性:** {self.result.get('consistency', '未知')}",
            "",
            "## 建議",
            ""
        ])
        
        # 添加建議
        suggestions = self.result.get("suggestions", {})
        for sug_type, sug_data in suggestions.items():
            md.append(f"### {sug_type}")
            md.append("")
            if isinstance(sug_data, list):
                for item in sug_data:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            md.append(f"- **{k}:** {v}")
                    else:
                        md.append(f"- {item}")
            else:
                md.append(f"- {sug_data}")
            md.append("")
        
        return "\n".join(md)
    
    def save_report(self, filename: str, format: str = "json") -> bool:
        """
        保存報告到文件
        
        參數:
            filename (str): 檔案名稱
            format (str, optional): 報告格式
            
        返回:
            bool: 成功為 True，失敗為 False
        """
        try:
            # 生成報告內容
            content = self.generate_report(format)
            
            # 確定檔案路徑
            if not os.path.isabs(filename):
                # 如果不是絕對路徑，使用配置的輸出路徑
                filename = os.path.join(self.config.output_path, filename)
            
            # 確保檔案有正確的擴展名
            if not filename.endswith(f".{format.lower()}"):
                filename = f"{filename}.{format.lower()}"
            
            # 寫入檔案
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"報告已保存至 {filename}")
            return True
        except Exception as e:
            logger.error(f"保存報告時發生錯誤: {e}")
            return False

# =======================================================
# Segment 7: 核心功能實現 – 主類別 (BasicResponseLogic)
# =======================================================

class BasicResponseLogic:
    """
    BasicResponseLogic 主類別，實現完整的邏輯推理流程
    
    主要功能流程:
      1. 輸入解析與意圖對齊
      2. 初始化上下文
      3. 量子態演化
      4. 自適應學習與歷史記憶
      5. 因果推理
      6. 遞歸修正
      7. 全局分析與最終整合
      8. 生成建議與監控指標
    """

    def __init__(self, memory_capacity: int = 10):
        """
        初始化 BasicResponseLogic
        
        參數:
            memory_capacity (int, optional): 記憶容量，默認為 10
        """
        self.memory_states = []  # 歷史記憶列表
        self.memory_capacity = memory_capacity
        self.iteration_counter = 0
        logger.info(f"初始化 BasicResponseLogic，記憶容量={memory_capacity}")
    
    def _parse_and_embed(self, input_text: str) -> Tuple[np.ndarray, int, float]:
        """
        解析輸入並生成語義向量與意圖
        
        參數:
            input_text (str): 輸入文本
            
        返回:
            Tuple[np.ndarray, int, float]: (語義向量, 意圖索引, 熵值)
        """
        logger.info("執行輸入解析與向量化")
        
        try:
            # 解析輸入文本
            h_t = DataParser.parse_input(input_text)
            
            # 意圖對齊
            intent, H_p_c = DataParser.align_intent(h_t)
            
            return h_t, intent, H_p_c
        except Exception as e:
            logger.error(f"解析與嵌入過程失敗: {e}")
            raise ProcessingError(f"解析失敗: {str(e)}")
    
    def _simulate_quantum_attention(self, state_0: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        模擬量子態演化與注意力機制
        
        參數:
            state_0 (np.ndarray): 初始狀態向量
            
        返回:
            Tuple[np.ndarray, float]: (演化後狀態, 熵值)
        """
        logger.info("執行量子態演化與注意力模擬")
        
        try:
            # 標準化輸入狀態
            if np.sum(np.abs(state_0)) > EPS:
                state_0 = state_0 / np.sum(np.abs(state_0))
            
            # QFT: 使用 FFT 模擬量子傅里葉變換
            qft_state = np.fft.fft(state_0) / math.sqrt(N_STATE)
            
            # 模擬量子相位旋轉
            theta = np.random.rand() * math.pi
            f_theta = math.sin(theta) * 0.5
            
            # 量子噪聲模擬
            delta = f_theta * np.random.randn(N_STATE) * 0.01
            
            # 應用演化
            evolved_state = qft_state + delta
            
            # 標準化並計算熵
            evolved_prob = np.abs(evolved_state) / (np.sum(np.abs(evolved_state)) + EPS)
            H_evolved = -np.sum(evolved_prob * np.log2(evolved_prob + EPS))
            
            logger.debug(f"量子態演化完成，熵值={H_evolved:.4f}")
            return evolved_state, H_evolved
        except Exception as e:
            logger.error(f"量子態演化失敗: {e}")
            # 返回原始狀態和高熵值表示高不確定性
            return state_0, 1.0
    
    def _adaptive_learning(self, state_0: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        自適應學習與歷史融合
        
        參數:
            state_0 (np.ndarray): 初始狀態向量
            
        返回:
            Tuple[np.ndarray, float]: (適應性狀態, 熵值)
        """
        logger.info("執行自適應學習與歷史記憶融合")
        
        try:
            # 計算初始熵值
            state_prob = np.abs(state_0) / (np.sum(np.abs(state_0)) + EPS)
            H_state = -np.sum(state_prob * np.log2(state_prob + EPS))
            
            # 計算梯度 (近似)
            gradients = np.zeros_like(state_0)
            for i in range(1, len(state_0)-1):
                gradients[i] = (state_0[i+1] - state_0[i-1]) / 2
            
            # 梯度範數
            grad_norm = np.linalg.norm(gradients)
            
            # 生成模擬相關性矩陣
            R = np.eye(N_STATE) + 0.1 * np.random.rand(N_STATE, N_STATE)
            
            # 計算複雜度指標
            complexity = 0.4 * H_state + 0.3 * grad_norm + 0.3 * np.mean(np.abs(R))
            
            # 從記憶中提取平均狀態
            memory_avg = np.mean(self.memory_states, axis=0) if self.memory_states else np.zeros(N_STATE)
            
            # 權衡當前狀態與記憶狀態，複雜度越高權重越大
            memory_weight = min(0.5, complexity * 0.3)
            current_weight = 1.0 - memory_weight
            
            # 融合狀態
            new_state = current_weight * state_0 + memory_weight * memory_avg
            
            # 標準化並計算熵
            new_prob = np.abs(new_state) / (np.sum(np.abs(new_state)) + EPS)
            H_adaptive = -np.sum(new_prob * np.log2(new_prob + EPS))
            
            logger.debug(f"自適應學習完成，熵值={H_adaptive:.4f}，複雜度={complexity:.4f}")
            return new_state, H_adaptive
        except Exception as e:
            logger.error(f"自適應學習失敗: {e}")
            return state_0, H_state if 'H_state' in locals() else 1.0
    
    def _causal_inference(self, state: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        因果推理與貝氏更新
        
        參數:
            state (np.ndarray): 狀態向量
            
        返回:
            Tuple[np.ndarray, float]: (因果推理後狀態, 熵值)
        """
        logger.info("執行因果推理與貝氏更新")
        
        try:
            # 先驗分布 (均勻)
            prior = np.ones(N_STATE) / N_STATE
            
            # 似然函數 (模擬)
            likelihood = 0.1 * np.random.rand(N_STATE) + 0.9
            
            # 貝氏更新
            posterior = (likelihood * prior) / (np.sum(likelihood * prior) + EPS)
            
            # 應用到狀態
            causal_state = state * posterior
            
            # 標準化並計算熵
            causal_prob = np.abs(causal_state) / (np.sum(np.abs(causal_state)) + EPS)
            H_causal = -np.sum(causal_prob * np.log2(causal_prob + EPS))
            
            logger.debug(f"因果推理完成，熵值={H_causal:.4f}")
            return causal_state, H_causal
        except Exception as e:
            logger.error(f"因果推理失敗: {e}")
            return state, 1.0
    
    def _recursive_correction(self, state: np.ndarray, target_state: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        遞歸修正與目標對齊
        
        參數:
            state (np.ndarray): 當前狀態向量
            target_state (np.ndarray): 目標狀態向量
            
        返回:
            Tuple[np.ndarray, float]: (修正後狀態, 熵值)
        """
        logger.info("執行遞歸修正與目標對齊")
        
        try:
            # 生成相位角
            theta_corr = np.random.rand() * math.pi
            f_theta_corr = math.sin(theta_corr) * 0.5
            
            # 計算目標 (以目標狀態的平均作為參考點)
            target = np.mean(np.abs(target_state))
            
            # 計算誤差
            error = target - np.mean(np.abs(state))
            
            # 誤差修正幅度
            correction_amplitude = 0.3 * error + f_theta_corr * 0.01
            
            # 應用修正
            correction_vector = correction_amplitude * np.ones_like(state)
            corrected_state = state + correction_vector
            
            # 標準化並計算熵
            corrected_prob = np.abs(corrected_state) / (np.sum(np.abs(corrected_state)) + EPS)
            H_corrected = -np.sum(corrected_prob * np.log2(corrected_prob + EPS))
            
            logger.debug(f"遞歸修正完成，熵值={H_corrected:.4f}，誤差={error:.4f}")
            return corrected_state, H_corrected
        except Exception as e:
            logger.error(f"遞歸修正失敗: {e}")
            return state, 1.0
    
    def _global_integration(self, states: Dict[str, np.ndarray], entropies: Dict[str, float]) -> float:
        """
        全局整合與決策生成
        
        參數:
            states (Dict[str, np.ndarray]): 狀態字典
            entropies (Dict[str, float]): 熵值字典
            
        返回:
            float: 最終整合結果
        """
        logger.info("執行全局整合與決策生成")
        
        try:
            # 提取關鍵狀態
            evolved = states.get("evolved", np.zeros(N_STATE))
            adaptive = states.get("adaptive", np.zeros(N_STATE))
            causal = states.get("causal", np.zeros(N_STATE))
            corrected = states.get("corrected", np.zeros(N_STATE))
            
            # 經典平均
            classical_result = np.mean([
                np.mean(np.abs(evolved)), 
                np.mean(np.abs(adaptive)), 
                np.mean(np.abs(causal)), 
                np.mean(np.abs(corrected))
            ])
            
            # 量子權重計算 (模擬量子疊加效應)
            quantum_weights = np.array([
                np.sum(np.abs(evolved) ** 2),
                np.sum(np.abs(adaptive) ** 2),
                np.sum(np.abs(causal) ** 2),
                np.sum(np.abs(corrected) ** 2)
            ])
            quantum_weights = quantum_weights / (np.sum(quantum_weights) + EPS)
            
            # 量子加權和
            quantum_result = np.sum([
                quantum_weights[0] * np.mean(np.abs(evolved)),
                quantum_weights[1] * np.mean(np.abs(adaptive)),
                quantum_weights[2] * np.mean(np.abs(causal)),
                quantum_weights[3] * np.mean(np.abs(corrected))
            ])
            
            # 融合經典與量子結果
            fused = 0.5 * classical_result + 0.5 * quantum_result
            
            # 最終的量子相位調整
            theta_final = np.random.rand() * math.pi
            final_result = fused + 0.1 * math.sin(theta_final)
            
            # 檢查結果是否在合理範圍
            final_result = max(0.0, min(1.0, final_result))
            
            logger.debug(f"全局整合完成，最終結果={final_result:.4f}")
            return final_result
        except Exception as e:
            logger.error(f"全局整合失敗: {e}")
            return 0.5  # 返回中性結果
    
    def _generate_suggestions(self, context: Dict[str, Any], final_result: float, entropies: Dict[str, float]) -> Dict[str, Any]:
        """
        根據結果生成建議
        
        參數:
            context (Dict[str, Any]): 上下文信息
            final_result (float): 最終結果值
            entropies (Dict[str, float]): 熵值字典
            
        返回:
            Dict[str, Any]: 建議字典
        """
        logger.info("生成建議與行動計劃")
        
        suggestions = {"primary": [], "alternative": [], "future": {}}
        
        try:
            # 檢查各維度的熵值，低熵代表高確定性
            for dim, data in context["dimensions"].items():
                dim_state = data["state"]
                p_dim = np.abs(dim_state) / (np.sum(np.abs(dim_state)) + EPS)
                H_dim = -np.sum(p_dim * np.log2(p_dim + EPS))
                data["entropy"] = H_dim  # 添加到上下文中
                
                # 基於熵值分類建議
                if H_dim < 1.0:  # 高確定性
                    suggestions["primary"].append({dim: "強烈趨勢，建議積極行動"})
                elif H_dim < 1.5:  # 中等確定性
                    suggestions["primary"].append({dim: "明確趨勢，可以計劃行動"})
                elif H_dim < 2.0:  # 中等不確定性
                    suggestions["alternative"].append({dim: "趨勢不明確，建議謹慎觀察"})
                else:  # 高不確定性
                    suggestions["alternative"].append({dim: "高度不確定，建議暫緩決策"})
            
            # 未來趨勢預測
            if final_result > 0.7:
                suggestions["future"] = "強勁擴展勢頭，可積極投入資源"
            elif final_result > 0.5:
                suggestions["future"] = "穩健增長，持續優化現有策略"
            elif final_result > 0.3:
                suggestions["future"] = "趨勢平緩，維持現狀並尋找改進點"
            else:
                suggestions["future"] = "下行風險，建議保守策略與風險管理"
            
            # 檢查熵值一致性
            avg_entropy = np.mean(list(entropies.values()))
            entropy_std = np.std(list(entropies.values()))
            
            # 添加信心指數
            suggestions["confidence"] = {
                "level": 1.0 - min(1.0, avg_entropy / 3.0),  # 熵值越低，信心越高
                "consistency": 1.0 - min(1.0, entropy_std),  # 熵值標準差越低，一致性越高
                "avg_entropy": avg_entropy
            }
            
            logger.debug(f"建議生成完成，平均熵值={avg_entropy:.4f}，信心指數={suggestions['confidence']['level']:.4f}")
            return suggestions
        except Exception as e:
            logger.error(f"生成建議時發生錯誤: {e}")
            return {"primary": ["無法生成有效建議"], "error": str(e)}
    
    def _update_memory(self, state: np.ndarray) -> None:
        """
        更新系統記憶
        
        參數:
            state (np.ndarray): 狀態向量
        """
        self.memory_states.append(state.copy())
        
        # 保持記憶在容量範圍內
        if len(self.memory_states) > self.memory_capacity:
            self.memory_states.pop(0)
        
        logger.debug(f"更新系統記憶，當前記憶數量: {len(self.memory_states)}")
    
    def run(self, input_text: str, config: Config) -> Dict[str, Any]:
        """
        執行完整推理流程
        
        參數:
            input_text (str): 輸入文本
            config (Config): 系統配置
            
        返回:
            Dict[str, Any]: 推理結果字典
        """
        self.iteration_counter += 1
        logger.info(f"開始第 {self.iteration_counter} 次推理流程")
        
        result = {}
        entropies = {}
        states = {}
        
        try:
            # Step 1: 輸入解析與意圖對齊
            h_t, intent, H_p_c = self._parse_and_embed(input_text)
            result["intent"] = intent
            result["H_intent"] = H_p_c
            entropies["intent"] = H_p_c
            
            # Step 2: 初始化上下文
            context = {
                "input": input_text,
                "timestamp": config.timestamp,
                "dimensions": {
                    dim: {"state": np.random.rand(N_STATE), "entropy": 0.0, "weight": 1/3}
                    for dim in config.load_config()["global_dimensions"]
                },
                "intent": intent
            }
            result["context"] = context
            
            # Step 3: 量子態演化
            state_0 = np.random.rand(N_STATE)
            evolved_state, H_evolved = self._simulate_quantum_attention(state_0)
            result["evolved_state"] = evolved_state.tolist()
            result["H_evolved"] = H_evolved
            entropies["evolved"] = H_evolved
            states["evolved"] = evolved_state
            
            # Step 4: 自適應學習與歷史融合
            adaptive_state, H_adaptive = self._adaptive_learning(state_0)
            result["adaptive_state"] = adaptive_state.tolist()
            result["H_adaptive"] = H_adaptive
            entropies["adaptive"] = H_adaptive
            states["adaptive"] = adaptive_state
            
            # Step 5: 因果推理
            causal_state, H_causal = self._causal_inference(adaptive_state)
            result["causal_state"] = causal_state.tolist()
            result["H_causal"] = H_causal
            entropies["causal"] = H_causal
            states["causal"] = causal_state
            
            # Step 6: 遞歸修正
            corrected_state, H_corrected = self._recursive_correction(causal_state, evolved_state)
            result["corrected_state"] = corrected_state.tolist()
            result["H_corrected"] = H_corrected
            entropies["corrected"] = H_corrected
            states["corrected"] = corrected_state
            
            # Step 7: 全局分析與最終整合
            final_result = self._global_integration(states, entropies)
            result["final_result"] = final_result
            
            # 檢查各熵值的一致性
            entropy_values = list(entropies.values())
            consistency = "一致" if (max(entropy_values) - min(entropy_values)) < 0.5 else "差異"
            result["consistency"] = consistency
            
            # Step 8: 生成建議
            suggestions = self._generate_suggestions(context, final_result, entropies)
            result["suggestions"] = suggestions
            
            # Step 9: 監控指標
            avg_entropy = np.mean(entropy_values)
            result["monitor"] = {
                "avg_entropy": avg_entropy, 
                "consistency": consistency,
                "iteration": self.iteration_counter,
                "memory_size": len(self.memory_states)
            }
            
            # 更新系統記憶
            self._update_memory(state_0)
            
            logger.info(f"推理流程完成，最終結果: {final_result:.4f}，一致性: {consistency}")
            return result
        except Exception as e:
            logger.error(f"推理流程失敗: {e}", exc_info=True)
            return {
                "error": "推理流程錯誤",
                "message": str(e),
                "status": "error",
                "partial_result": result if result else None
            }
    
    def reset(self) -> None:
        """重置系統狀態"""
        self.memory_states = []
        self.iteration_counter = 0
        logger.info("系統狀態已重置")

# =======================================================
# Segment 8: 主程式執行區塊 (Example Usage / Main Entry)
# =======================================================

if __name__ == "__main__":
    # 建立配置
    config = Config(timestamp="2025-03-12T00:00:00", debug_mode=True)
    
    # 建立查詢引擎並執行推理流程
    engine = QueryEngine(config)
    
    # 定義測試輸入
    test_inputs = [
        "請分析未來市場趨勢並給出建議",
        "我需要了解最新的技術發展方向",
        "如何優化現有產品的用戶體驗"
    ]
    
    for input_text in test_inputs:
        print(f"\n{'='*60}\n處理輸入: {input_text}\n{'='*60}")
        
        # 執行推理
        inference_result = engine.run_inference_pipeline(input_text)
        
        # 生成報告
        report = ReportGenerator(inference_result).generate_report(format="text")
        
        # 顯示結果
        print(report)
        
        # 生成並保存 JSON 報告 (如果存在輸出目錄)
        if os.path.exists(config.output_path):
            filename = f"result_{int(time.time())}.json"
            ReportGenerator(inference_result, config).save_report(filename)
            print(f"報告已保存至 {os.path.join(config.output_path, filename)}")
        
        # 暫停一下，避免輸出太快
        time.sleep(1)
