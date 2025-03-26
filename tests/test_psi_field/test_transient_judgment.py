"""
SemanticFieldEngine 單元測試
"""
import pytest
import numpy as np
from psi_runtime_sdk.psi_field import (
    SemanticFieldEngine, 
    FieldConfig, 
    DataParser, 
    SemanticInput, 
    KnowledgeAnchor
)

class TestSemanticFieldEngine:
    @pytest.fixture
    def field_engine(self):
        """創建測試用的語義場引擎"""
        config = FieldConfig(enable_detailed_logging=False)  # 測試時禁用詳細日誌
        return SemanticFieldEngine(config)
    
    @pytest.fixture
    def sample_input(self):
        """創建測試用的語義輸入"""
        return DataParser.parse("人工智能與量子計算的結合")
    
    def test_init(self, field_engine):
        """測試初始化"""
        assert field_engine is not None
        assert field_engine.config is not None
        assert field_engine.psi_engine is not None
        assert field_engine.csp_controller is not None
        assert field_engine.echo_resolver is not None
    
    def test_data_parser(self):
        """測試數據解析器"""
        text = "測試語義解析功能"
        semantic_input = DataParser.parse(text)
        
        assert isinstance(semantic_input, SemanticInput)
        assert semantic_input.text == text
        assert hasattr(semantic_input, "timestamp")
        assert hasattr(semantic_input, "session_id")
    
    def test_extract_knowledge_keys(self):
        """測試知識關鍵字提取"""
        text = "人工智能和機器學習技術的發展趨勢"
        keys = DataParser.extract_knowledge_keys(text)
        
        assert isinstance(keys, list)
        assert len(keys) > 0
        # 檢查是否提取了合理的關鍵詞（這裡我們只能大概檢查）
        common_words = ["人工智能", "機器學習", "技術", "發展", "趨勢"]
        assert any(key in common_words for key in keys)
    
    def test_unlock_knowledge(self, field_engine, sample_input):
        """測試知識解鎖功能"""
        # 執行知識解鎖
        unlocked_keys = field_engine.psi_engine.unlock_knowledge(sample_input)
        
        # 檢查基本結果
        assert isinstance(unlocked_keys, list)
        assert len(unlocked_keys) > 0
        
        # 檢查知識庫更新
        for key in unlocked_keys:
            assert key in field_engine.psi_engine.knowledge_base
            knowledge = field_engine.psi_engine.knowledge_base[key]
            assert isinstance(knowledge, KnowledgeAnchor)
            assert knowledge.activation_level > 0
            
    def test_knowledge_decay(self, field_engine, sample_input):
        """測試知識活躍度衰減功能"""
        # 先解鎖一些知識
        unlocked_keys = field_engine.psi_engine.unlock_knowledge(sample_input)
        
        # 記錄原始活躍度
        original_levels = {key: field_engine.psi_engine.knowledge_base[key].activation_level 
                         for key in unlocked_keys}
        
        # 執行衰減
        field_engine.psi_engine.decay_all_knowledge(rate=0.2)
        
        # 檢查衰減後的活躍度
        for key in unlocked_keys:
            new_level = field_engine.psi_engine.knowledge_base[key].activation_level
            assert new_level < original_levels[key]
            assert new_level == original_levels[key] * 0.8  # 衰減率為0.2 
