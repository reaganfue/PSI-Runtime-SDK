"""
# ===========================
# Segment 1: 模組說明 (Module Docstring)
# ===========================

企業級AI系統核心模組 (Enterprise AI System Core)

本模組實現企業級AI系統架構中語義場引擎的單元測試，確保主要功能、知識解鎖與活躍度衰減邏輯完整且正確。
採用單一責任原則與標準化設計，符合企業級設計規範與 SDK/API 一致性要求。

版本: 1.0.0
作者: Reagan Fu 團隊
許可證: Proprietary

主要功能與測試目標:
1. 驗證語義場引擎初始化與配置
2. 測試數據解析器功能與輸入驗證
3. 驗證知識關鍵字提取、解鎖及活躍度衰減邏輯

參考規範: :contentReference[oaicite:0]{index=0}&#8203;:contentReference[oaicite:1]{index=1}
"""

# ===========================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# ===========================
# 基礎套件用途:
# - logging: 實現結構化日誌，追蹤操作與錯誤
# - pytest: 單元測試框架
# - numpy: 高效數學運算支持
# - 型別安全支持
#
# 外部依賴:
# - psi_field 模組：包含 SemanticFieldEngine、FieldConfig、DataParser、SemanticInput 與 KnowledgeAnchor

import logging
import pytest
import numpy as np
from psi_field import (
    SemanticFieldEngine, 
    FieldConfig, 
    DataParser, 
    SemanticInput, 
    KnowledgeAnchor
)

# 設置全域日誌系統，符合企業級日誌配置要求
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ===========================
# Segment 14: 主程式進入點 (Main Application Entry)
# ===========================
# 此模組作為單元測試模組的主進入點，透過 pytest 執行測試案例，
# 並展示從初始化、數據解析、知識提取到活躍度衰減的全流程測試。

def main():
    pytest.main()

# ===========================
# Segment 5: 單元測試案例 (Unit Test Cases)
# ===========================
# 測試涵蓋:
# 1. 語義場引擎初始化與依賴元件驗證
# 2. DataParser 的解析與關鍵詞提取功能
# 3. 知識解鎖及知識活躍度衰減功能的正確性

class TestSemanticFieldEngine:
    @pytest.fixture
    def field_engine(self):
        """
        創建測試用的語義場引擎

        配置:
        - 禁用詳細日誌以簡化測試輸出
        """
        config = FieldConfig(enable_detailed_logging=False)  # 測試時禁用詳細日誌
        return SemanticFieldEngine(config)
    
    @pytest.fixture
    def sample_input(self):
        """
        創建測試用的語義輸入

        使用 DataParser 將輸入文本轉換為 SemanticInput 對象，
        以驗證輸入解析及內部結構生成正確性。
        """
        return DataParser.parse("人工智能與量子計算的結合")
    
    def test_init(self, field_engine):
        """
        測試初始化:
        驗證 SemanticFieldEngine 實例及其依賴元件是否正確初始化。
        """
        assert field_engine is not None
        assert field_engine.config is not None
        assert field_engine.psi_engine is not None
        assert field_engine.csp_controller is not None
        assert field_engine.echo_resolver is not None
    
    def test_data_parser(self):
        """
        測試數據解析器:
        驗證 DataParser.parse 方法能正確解析輸入文本，並生成具備必要屬性的 SemanticInput 對象。
        """
        text = "測試語義解析功能"
        semantic_input = DataParser.parse(text)
        
        assert isinstance(semantic_input, SemanticInput)
        assert semantic_input.text == text
        # 檢查是否包含時間戳與 session_id 屬性
        assert hasattr(semantic_input, "timestamp")
        assert hasattr(semantic_input, "session_id")
    
    def test_extract_knowledge_keys(self):
        """
        測試知識關鍵字提取:
        驗證 DataParser.extract_knowledge_keys 方法能從文本中提取合理的關鍵詞列表，
        並包含預期關鍵詞之一。
        """
        text = "人工智能和機器學習技術的發展趨勢"
        keys = DataParser.extract_knowledge_keys(text)
        
        assert isinstance(keys, list)
        assert len(keys) > 0
        common_words = ["人工智能", "機器學習", "技術", "發展", "趨勢"]
        assert any(key in common_words for key in keys)
    
    def test_unlock_knowledge(self, field_engine, sample_input):
        """
        測試知識解鎖功能:
        驗證 unlock_knowledge 方法能夠正確解鎖知識，更新知識庫，並確保每個知識錨點的活躍度大於零。
        """
        # 執行知識解鎖
        unlocked_keys = field_engine.psi_engine.unlock_knowledge(sample_input)
        
        # 驗證返回值為非空列表
        assert isinstance(unlocked_keys, list)
        assert len(unlocked_keys) > 0
        
        # 檢查知識庫更新
        for key in unlocked_keys:
            assert key in field_engine.psi_engine.knowledge_base
            knowledge = field_engine.psi_engine.knowledge_base[key]
            assert isinstance(knowledge, KnowledgeAnchor)
            assert knowledge.activation_level > 0
            
    def test_knowledge_decay(self, field_engine, sample_input):
        """
        測試知識活躍度衰減功能:
        驗證在應用指定衰減率後，知識錨點的活躍度是否按照預期減少。
        """
        # 解鎖部分知識
        unlocked_keys = field_engine.psi_engine.unlock_knowledge(sample_input)
        
        # 記錄原始活躍度
        original_levels = {
            key: field_engine.psi_engine.knowledge_base[key].activation_level 
            for key in unlocked_keys
        }
        
        # 執行衰減，衰減率為 0.2，預期新活躍度為原始的 0.8 倍
        field_engine.psi_engine.decay_all_knowledge(rate=0.2)
        
        for key in unlocked_keys:
            new_level = field_engine.psi_engine.knowledge_base[key].activation_level
            assert new_level < original_levels[key]
            # 考慮浮點數精度誤差
            assert abs(new_level - original_levels[key] * 0.8) < 1e-6

if __name__ == "__main__":
    main()
