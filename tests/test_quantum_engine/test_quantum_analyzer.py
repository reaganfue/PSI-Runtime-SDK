"""
========================================
Segment 1: 模組說明 (Module Docstring)
========================================
QuantumAnalyzer 單元測試模組

本模組用於驗證 QuantumAnalyzer 的各項功能，包括：
    - 輸入解析功能
    - 純量子分析模式與基礎邏輯模式下的推理結果
    - 綜合分析與結果整合
    - 初始化狀態檢查

版本: 1.0.0
作者: 測試團隊
許可證: Proprietary
"""

import pytest
import numpy as np
import logging

# ========================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# ========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 修改導入路徑以匹配實際目錄結構
from quantum_engine import QuantumAnalyzer, Config, DataParser

# ========================================
# Segment 3: 測試案例與測試環境設置 (Test Cases & Environment Setup)
# ========================================
class TestQuantumAnalyzer:
    @pytest.fixture
    def qa_engine(self):
        """
        創建測試用的 QuantumAnalyzer 引擎實例。

        返回:
            QuantumAnalyzer: 量子分析引擎實例，配置為 WARNING 級別輸出。
        """
        config = Config(log_level=30)  # 設置為 WARNING 級別，減少測試輸出
        engine = QuantumAnalyzer(config)
        logger.info("QuantumAnalyzer 引擎初始化完成")
        return engine

    def test_init(self, qa_engine):
        """
        測試 QuantumAnalyzer 初始化狀態。

        驗證:
            - 引擎實例不為 None
            - 配置存在
            - 擁有 BasicResponseLogic 實例 (brl)
        """
        assert qa_engine is not None, "QuantumAnalyzer 實例不應為 None"
        assert qa_engine.config is not None, "配置對象不應為 None"
        assert hasattr(qa_engine, "brl"), "QuantumAnalyzer 應包含 BasicResponseLogic 實例"
        logger.info("初始化測試通過")

    def test_parse_input(self, qa_engine):
        """
        測試輸入解析功能。

        流程:
            1. 傳入測試文本。
            2. 驗證返回結果為字典，並包含原始文本。

        驗證:
            - 返回值為 dict 並包含鍵 "text"
            - 鍵值與輸入文本一致
        """
        text = "測試量子分析功能"
        parsed = qa_engine.parse_input(text)
        logger.info("解析結果: %s", parsed)
        
        assert isinstance(parsed, dict), "解析結果必須為字典"
        assert "text" in parsed, "解析結果中必須包含 'text' 鍵"
        assert parsed["text"] == text, "解析結果的 'text' 鍵值應與輸入文本一致"

    def test_run_inference_quantum(self, qa_engine):
        """
        測試純量子分析模式。

        流程:
            1. 傳入測試文本。
            2. 設置 use_basic_logic 為 False 執行純量子模式。

        驗證:
            - 返回結果為 float 類型
            - 結果值在 0 到 1.0 之間
        """
        input_text = "分析未來技術發展趨勢"
        result = qa_engine.run_inference(input_text, use_basic_logic=False)
        logger.info("純量子模式推理結果: %s", result)
        
        assert isinstance(result, float), "純量子模式結果必須為 float 類型"
        assert 0 <= result <= 1.0, "結果超出 0 到 1.0 的範圍"

    def test_run_inference_basic(self, qa_engine):
        """
        測試基礎邏輯分析模式。

        流程:
            1. 傳入測試文本。
            2. 設置 use_basic_logic 為 True 執行基礎邏輯模式。

        驗證:
            - 返回結果為 dict 並包含 'final_result' 鍵
            - 'final_result' 為 float 且在 0 到 1.0 之間
        """
        input_text = "分析未來技術發展趨勢"
        result = qa_engine.run_inference(input_text, use_basic_logic=True)
        logger.info("基礎邏輯模式推理結果: %s", result)
        
        assert isinstance(result, dict), "基礎邏輯模式結果必須為字典"
        assert "final_result" in result, "結果中必須包含 'final_result' 鍵"
        assert isinstance(result["final_result"], float), "'final_result' 必須為 float 類型"
        assert 0 <= result["final_result"] <= 1.0, "'final_result' 超出有效範圍"

    def test_comprehensive_analysis(self, qa_engine):
        """
        測試綜合分析功能。

        流程:
            1. 傳入測試文本進行綜合分析。

        驗證:
            - 返回結果為 dict
            - 包含 'integrated_score', 'quantum_result' 與 'basic_result' 鍵
            - 'integrated_score' 為 float 且在 0 到 1.0 之間
        """
        input_text = "分析未來技術發展趨勢"
        result = qa_engine.comprehensive_analysis(input_text)
        logger.info("綜合分析結果: %s", result)
        
        assert isinstance(result, dict), "綜合分析結果必須為字典"
        assert "integrated_score" in result, "結果中必須包含 'integrated_score' 鍵"
        assert "quantum_result" in result, "結果中必須包含 'quantum_result' 鍵"
        assert "basic_result" in result, "結果中必須包含 'basic_result' 鍵"
        assert isinstance(result["integrated_score"], float), "'integrated_score' 必須為 float 類型"
        assert 0 <= result["integrated_score"] <= 1.0, "'integrated_score' 超出有效範圍"

    def test_integrate_results(self, qa_engine):
        """
        測試結果整合功能。

        流程:
            1. 定義純量子分析結果與基礎邏輯分析結果。
            2. 呼叫 integrate_results 方法進行整合。

        驗證:
            - 返回結果為 dict 並包含 'integrated_score' 和 'suggestions' 鍵
            - 'integrated_score' 為兩種結果加權平均的數值
            - 建議中包含 'quantum_insight' 鍵
        """
        quantum_result = 0.75
        basic_result = {"final_result": 0.65, "context": {"timestamp": "2025-01-01"}}
        
        integrated = qa_engine.integrate_results(quantum_result, basic_result)
        logger.info("結果整合結果: %s", integrated)
        
        expected_score = 0.75 * 0.5 + 0.65 * 0.5
        assert isinstance(integrated, dict), "整合結果必須為字典"
        assert "integrated_score" in integrated, "整合結果中必須包含 'integrated_score' 鍵"
        assert integrated["integrated_score"] == expected_score, "整合結果的 'integrated_score' 計算錯誤"
        assert "suggestions" in integrated, "整合結果中必須包含 'suggestions' 鍵"
        assert "quantum_insight" in integrated["suggestions"], "建議中必須包含 'quantum_insight' 鍵"
