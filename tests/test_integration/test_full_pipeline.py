"""
========================================
Segment 1: 模組說明 (Module Docstring)
========================================
PSI Runtime SDK 整合測試模組

本模組用於驗證 PSI Runtime SDK 各引擎（包括基礎邏輯、語義場及量子分析）的整合運作。
測試範圍包括：
    - 基礎邏輯至量子分析流程
    - 語義場至量子分析流程
    - 完整流水線整合測試

版本: 1.0.0
作者: 測試團隊
許可證: Proprietary
"""

import pytest
import logging
from logic_core import BasicResponseLogic, Config as BRLConfig
from psi_field import SemanticFieldEngine, FieldConfig, DataParser as PsiDataParser
from quantum_engine import QuantumAnalyzer, Config as QAConfig

# ========================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# ========================================
# 設置日誌配置與全域常數
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

"""
========================================
Segment 3: 測試案例與測試環境設置 (Test Cases & Environment Setup)
========================================
以下定義整合測試所需的 pytest 測試案例與引擎初始化 fixture。
"""

class TestIntegration:
    @pytest.fixture
    def all_engines(self):
        """
        初始化所有引擎。

        返回:
            dict: 包含基礎邏輯引擎、語義場引擎及量子分析引擎與其配置的字典。
        """
        # 初始化各引擎配置
        brl_config = BRLConfig(debug_mode=False)
        field_config = FieldConfig(enable_detailed_logging=False)
        qa_config = QAConfig(log_level=30)
        
        logger.info("初始化所有引擎")
        return {
            "brl": BasicResponseLogic(),
            "field": SemanticFieldEngine(field_config),
            "qa": QuantumAnalyzer(qa_config),
            "brl_config": brl_config,
            "field_config": field_config,
            "qa_config": qa_config
        }
    
    def test_basic_to_quantum_flow(self, all_engines):
        """
        測試從基礎邏輯到量子分析的流程。

        流程:
            1. 使用 BRL 進行初步分析。
            2. 將輸入傳遞給量子分析器。
            3. 驗證各階段的輸出結果與連貫性。

        參數:
            all_engines (dict): 包含所有引擎與配置的字典。
        """
        # 1. 使用 BRL 進行初步分析
        input_text = "分析人工智能對未來五年的影響"
        brl_result = all_engines["brl"].run(input_text, all_engines["brl_config"])
        logger.info("BRL 分析結果: %s", brl_result)
        
        # 驗證 BRL 結果
        assert isinstance(brl_result, dict), "BRL 結果必須為字典"
        assert "final_result" in brl_result, "BRL 結果缺少 'final_result' 關鍵字"
        
        # 2. 將結果傳遞給量子分析器
        qa_result = all_engines["qa"].run_inference(input_text, use_basic_logic=False)
        logger.info("量子分析結果: %s", qa_result)
        
        # 驗證量子分析結果
        assert isinstance(qa_result, float), "量子分析結果必須為浮點數"
        
        # 3. 測試流程的連貫性
        assert 0 <= brl_result["final_result"] <= 1.0, "BRL 結果超出有效範圍"
        assert 0 <= qa_result <= 1.0, "量子分析結果超出有效範圍"
    
    def test_field_to_quantum_flow(self, all_engines):
        """
        測試從語義場到量子分析的流程。

        流程:
            1. 使用語義場引擎解鎖知識。
            2. 驗證解鎖結果。
            3. 傳遞輸入給量子分析器並驗證結果。

        參數:
            all_engines (dict): 包含所有引擎與配置的字典。
        """
        # 1. 使用語義場引擎解鎖知識
        input_text = "量子計算和神經網絡的融合應用"
        semantic_input = PsiDataParser.parse(input_text)
        unlocked_keys = all_engines["field"].psi_engine.unlock_knowledge(semantic_input)
        logger.info("解鎖知識結果: %s", unlocked_keys)
        
        # 驗證解鎖結果
        assert isinstance(unlocked_keys, list), "解鎖結果必須為列表"
        assert len(unlocked_keys) > 0, "解鎖知識結果應至少包含一個知識點"
        
        # 2. 將結果傳遞給量子分析器
        qa_result = all_engines["qa"].run_inference(input_text, use_basic_logic=False)
        logger.info("量子分析結果: %s", qa_result)
        
        # 驗證量子分析結果
        assert isinstance(qa_result, float), "量子分析結果必須為浮點數"
    
    def test_full_pipeline(self, all_engines):
        """
        測試完整的分析流水線。

        流程:
            1. 語義場處理：解析輸入並解鎖知識。
            2. 量子分析：進行綜合量子分析。
            3. 基礎邏輯分析：執行傳統邏輯處理。
            4. 整合結果：計算綜合信心分數並生成最終結果。

        參數:
            all_engines (dict): 包含所有引擎與配置的字典。
        """
        input_text = "分析量子計算對密碼學的影響"
        
        # 1. 語義場處理
        semantic_input = PsiDataParser.parse(input_text)
        unlocked_keys = all_engines["field"].psi_engine.unlock_knowledge(semantic_input)
        logger.info("語義場解鎖結果: %s", unlocked_keys)
        
        # 2. 量子分析
        qa_result = all_engines["qa"].comprehensive_analysis(input_text)
        logger.info("量子綜合分析結果: %s", qa_result)
        
        # 3. 基礎邏輯分析
        brl_result = all_engines["brl"].run(input_text, all_engines["brl_config"])
        logger.info("基礎邏輯分析結果: %s", brl_result)
        
        # 4. 整合結果
        integrated_result = {
            "query": input_text,
            "unlocked_knowledge": unlocked_keys,
            "quantum_analysis": qa_result,
            "logical_analysis": brl_result,
            "confidence": (
                qa_result.get("integrated_score", 0.5) +
                brl_result.get("final_result", 0.5)
            ) / 2
        }
        logger.info("整合結果: %s", integrated_result)
        
        # 驗證整合結果
        assert isinstance(integrated_result, dict), "整合結果必須為字典"
        assert "confidence" in integrated_result, "整合結果缺少 'confidence'"
        assert 0 <= integrated_result["confidence"] <= 1.0, "信心分數超出有效範圍"
        assert "unlocked_knowledge" in integrated_result, "整合結果缺少 'unlocked_knowledge'"
        assert "quantum_analysis" in integrated_result, "整合結果缺少 'quantum_analysis'"
        assert "logical_analysis" in integrated_result, "整合結果缺少 'logical_analysis'"
